"""CellScope-Lite grid router v2 (A*, 8-direction / 45-degree, 2 signal layers + vias, plane fan-out).

Input : build/geom.json (from export_geom.py)
Output: build/routes.json  {tracks:[{net,layer,w,x1,y1,x2,y2}], vias:[{net,x,y,d,drill}], failed:[...]}

Stack-up: F.Cu signal, In1.Cu = GND plane, In2.Cu = +3V3 plane, B.Cu signal.
* GND / +3V3 SMD pads are fanned out to a via (plane connection).
* Every other net is grown as a tree: the first pad is the root and each further pad is routed
  to copper that is *already connected* to the tree (true connectivity, no accidental islands).
* Route ends are snapped exactly onto the copper they join (pad interior, track centre-line or via).
* Fine-pitch packages get straight escape stubs, so the A* grid never squeezes between pads.
* Routing clearance 0.25 mm, which is above every DRC clearance (0.2 mm Power, 0.15 mm Default).
"""
import heapq
import json
import random
import sys

import numpy as np
from matplotlib.path import Path
from scipy.ndimage import distance_transform_edt

G = 0.1                         # grid pitch, mm
CLR = 0.25                      # routing clearance (DRC: Power 0.20, Default 0.15)
MARGIN = 0.075                  # rasterisation safety margin
VIA_D, VIA_DRILL = 0.6, 0.3
PVIA_D, PVIA_DRILL = 0.8, 0.4   # vias on power-class tracks
HOLE2HOLE = 0.3                 # drill edge to drill edge (DRC min 0.25)
EDGE = 0.5                      # copper-to-board-edge keep-off
PLANE = {"GND", "+3V3"}
POWER_W = {"/VBAT": 0.8, "+5V": 0.8, "/VBUS_IN": 0.8, "/SENSE_HI": 0.8, "/BAT_N": 0.8, "/FET_D": 0.8}
SIG_W = 0.25
HEAVY = {("R16", "2"): 3, ("Q1", "6"): 2, ("Q1", "7"): 2, ("C1", "2"): 2, ("C11", "2"): 2,
         ("U1", "9"): 3, ("D1", "2"): 2, ("C3", "2"): 2}
SKIP_FANOUT = {("NT1", "1"), ("U6", "7")}   # NT1: Kelvin tie via R16 pad 2; U6.7: via its decoupling cap C12
EXPLICIT = [("GND", ("NT1", "1"), ("R16", "2"), 0.5),
            ("GND", ("U6", "7"), ("C12", "2"), 0.25)]   # INA226 GND pin straight to its decoupling-cap ground
ESCAPE = {"U6": 0.55, "Q1": 0.5, "J1": 0.6}   # fine-pitch parts: stub length beyond pad end (mm)
STUB_EXT = {}                   # per-pad stub length overrides
POWER_CLASS = {"/VBAT", "+5V", "/VBUS_IN", "/SENSE_HI", "/FET_D", "/BAT_N", "GND"}   # 0.2 mm DRC class
FINE_ZONE = 2.0                 # mm around fine-pitch pads where exact class clearances are used
FINE_MARGIN = 0.07

DIRS = [(1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0),
        (1, 1, 1.4142), (1, -1, 1.4142), (-1, 1, 1.4142), (-1, -1, 1.4142)]


def seg_dist(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / L2))
    qx, qy = x1 + t * dx, y1 + t * dy
    return ((px - qx) ** 2 + (py - qy) ** 2) ** 0.5, qx, qy


class Board:
    def __init__(self, geom):
        o = geom["outline"]
        self.x0, self.y0 = o["x0"], o["y0"]
        self.nx = int(round((o["x1"] - o["x0"]) / G)) + 1
        self.ny = int(round((o["y1"] - o["y0"]) / G)) + 1
        self.pads = [dict(p) for p in geom["pads"]]
        for p in self.pads:
            if p["net"].startswith("unconnected-"):
                p["net"] = ""
        names = sorted({p["net"] for p in self.pads if p["net"]})
        self.nid = {n: i for i, n in enumerate(names)}
        self.names = names
        self.cu = [np.full((self.ny, self.nx), -1, np.int32) for _ in range(2)]
        self.holes = np.zeros((self.ny, self.nx), bool)        # via centre forbidden (hole-to-hole)
        self.smd = np.full((self.ny, self.nx), -1, np.int32)
        yy, xx = np.mgrid[0:self.ny, 0:self.nx]
        self.cx = self.x0 + xx * G
        self.cy = self.y0 + yy * G
        e = int(round(EDGE / G)) + 1
        edge = np.zeros((self.ny, self.nx), bool)
        edge[:, :e] = edge[:, -e:] = True
        edge[:e, :] = edge[-e:, :] = True
        r = 3.0
        for ccx, ccy, sx, sy in [(o["x0"] + r, o["y0"] + r, -1, -1), (o["x1"] - r, o["y0"] + r, 1, -1),
                                 (o["x0"] + r, o["y1"] - r, -1, 1), (o["x1"] - r, o["y1"] - r, 1, 1)]:
            corner = ((self.cx - ccx) * sx > 0) & ((self.cy - ccy) * sy > 0)
            edge |= corner & (np.hypot(self.cx - ccx, self.cy - ccy) > r - EDGE)
        self.edge = edge
        for p in self.pads:
            p["mask"] = self.raster_poly(p["poly"])
            if not p["mask"].any():
                i, j = self.cell(p["x"], p["y"])
                p["mask"][j, i] = True
            p["path"] = [Path(np.array(q)) for q in p["poly"]]
            owner = self.nid[p["net"]] if p["net"] else -2
            for li, L in enumerate("FB"):
                if L in p["layers"]:
                    self.cu[li][p["mask"]] = owner
            if p["drill"] > 0:
                self.holes |= np.hypot(self.cx - p["x"], self.cy - p["y"]) <= p["drill"] / 2 + HOLE2HOLE + VIA_DRILL / 2
            if not p["tht"] and p["net"]:
                self.smd[p["mask"]] = owner
            p["stub"] = None
        self.tracks, self.vias = [], []
        self.segs = {}    # net id -> list of (layer, x1, y1, x2, y2, hw)
        self.power_ids = np.array(sorted(self.nid[k] for k in POWER_CLASS if k in self.nid), np.int32)
        fine = np.zeros((self.ny, self.nx), bool)
        for p in self.pads:
            if p["ref"] in ESCAPE:
                fine |= p["mask"]
        self.fine = distance_transform_edt(~fine) * G < FINE_ZONE

    # ---------------- geometry helpers ----------------
    def cell(self, x, y):
        return int(round((x - self.x0) / G)), int(round((y - self.y0) / G))

    def xy(self, i, j):
        return round(self.x0 + i * G, 4), round(self.y0 + j * G, 4)

    def raster_poly(self, polys):
        m = np.zeros((self.ny, self.nx), bool)
        for poly in polys:
            pts = np.array(poly)
            i0, j0 = self.cell(*pts.min(0))
            i1, j1 = self.cell(*pts.max(0))
            i0, j0 = max(i0 - 1, 0), max(j0 - 1, 0)
            i1, j1 = min(i1 + 1, self.nx - 1), min(j1 + 1, self.ny - 1)
            sub = np.stack([self.cx[j0:j1 + 1, i0:i1 + 1].ravel(), self.cy[j0:j1 + 1, i0:i1 + 1].ravel()], 1)
            m[j0:j1 + 1, i0:i1 + 1] |= Path(pts).contains_points(sub).reshape(j1 - j0 + 1, i1 - i0 + 1)
        return m

    def stamp(self, n, l, x1, y1, x2, y2, hw, tree=None):
        i0, j0 = self.cell(min(x1, x2) - hw - 0.2, min(y1, y2) - hw - 0.2)
        i1, j1 = self.cell(max(x1, x2) + hw + 0.2, max(y1, y2) + hw + 0.2)
        i0, j0, i1, j1 = max(i0, 0), max(j0, 0), min(i1, self.nx - 1), min(j1, self.ny - 1)
        X = self.cx[j0:j1 + 1, i0:i1 + 1]
        Y = self.cy[j0:j1 + 1, i0:i1 + 1]
        dx, dy = x2 - x1, y2 - y1
        L2 = dx * dx + dy * dy
        t = np.clip(((X - x1) * dx + (Y - y1) * dy) / L2, 0, 1) if L2 > 0 else 0
        inside = np.hypot(X - (x1 + t * dx), Y - (y1 + t * dy)) <= hw + 1e-9
        sub = self.cu[l][j0:j1 + 1, i0:i1 + 1]
        sub[inside & (sub == -1)] = n
        if tree is not None:
            tree[l][j0:j1 + 1, i0:i1 + 1] |= inside

    def add_track(self, n, l, x1, y1, x2, y2, w, tree=None):
        if abs(x1 - x2) < 1e-6 and abs(y1 - y2) < 1e-6:
            return
        self.tracks.append(dict(net=self.names[n], layer="FB"[l], w=w, x1=round(x1, 4), y1=round(y1, 4),
                                x2=round(x2, 4), y2=round(y2, 4)))
        self.segs.setdefault(n, []).append((l, x1, y1, x2, y2, w / 2))
        self.stamp(n, l, x1, y1, x2, y2, w / 2, tree)

    def add_via(self, n, x, y, d, drill, tree=None):
        self.vias.append(dict(net=self.names[n], x=x, y=y, d=d, drill=drill))
        for l in range(2):
            self.stamp(n, l, x, y, x, y, d / 2, tree)
            self.segs.setdefault(n, []).append((l, x, y, x, y, d / 2))
        self.holes |= np.hypot(self.cx - x, self.cy - y) <= drill / 2 + HOLE2HOLE + VIA_DRILL / 2

    def snap(self, n, l, x, y, pads):
        """Point on existing copper of net n (layer l) that (x, y) should connect to, or None if already inside."""
        for p in pads:
            if "FB"[l] in p["layers"] and any(pp.contains_point((x, y)) for pp in p["path"]):
                return None
        best = None
        for (sl, x1, y1, x2, y2, hw) in self.segs.get(n, []):
            if sl != l:
                continue
            d, qx, qy = seg_dist(x, y, x1, y1, x2, y2)
            if d < 1e-4:
                return None
            if best is None or d < best[0]:
                best = (d, qx, qy)
        if best and best[0] <= 0.35:
            return best[1], best[2]
        # nearest pad centre as last resort
        for p in pads:
            if "FB"[l] in p["layers"] and np.hypot(p["x"] - x, p["y"] - y) < 1.5:
                return p["x"], p["y"]
        return None

    # ---------------- clearance maps ----------------
    def free_maps(self, n, w):
        """Free cells for a track of width w of net n.
        Outside fine-pitch zones: 0.25 mm to everything (+margin).
        Inside: exact DRC class clearance (0.2 mm to Power-class copper or when n is Power, else 0.15 mm) + 0.05 mm."""
        hw = w / 2
        n_power = n in set(self.power_ids.tolist())
        free, dmin = [], []
        for li in range(2):
            c = self.cu[li]
            isp = np.isin(c, self.power_ids)
            occ_p = isp & (c != n)
            occ_o = ((c != -1) & ~isp & (c != n)) | self.edge
            dp = distance_transform_edt(~occ_p) * G
            do = distance_transform_edt(~occ_o) * G
            out_ok = (dp >= CLR + hw + MARGIN) & (do >= CLR + hw + MARGIN)
            in_ok = (dp >= 0.2 + hw + FINE_MARGIN) & (do >= (0.2 if n_power else 0.15) + hw + FINE_MARGIN)
            free.append(np.where(self.fine, in_ok, out_ok))
            dmin.append(np.minimum(dp, do))
        via_ok = (dmin[0] >= CLR + VIA_D / 2 + MARGIN) & (dmin[1] >= CLR + VIA_D / 2 + MARGIN) & ~self.holes
        own_smd = self.smd == n
        if own_smd.any():
            via_ok &= distance_transform_edt(~own_smd) * G > VIA_D / 2 + 0.05
        return free, via_ok

    def anchors(self, p):
        """Cells where a route may start/finish on pad p: escape-stub end, else the pad centre."""
        if p["stub"]:
            x, y = p["stub"]
            i, j = self.cell(x, y)
            return [(0, j, i)]
        out = []
        for li, L in enumerate("FB"):
            if L in p["layers"]:
                i, j = self.cell(p["x"], p["y"])
                out.append((li, j, i))
        return out

    # ---------------- A* ----------------
    def astar(self, starts, goal, free, via_ok, max_nodes=1500000, via_goal=False):
        h = distance_transform_edt(~(goal if via_goal else (goal[0] | goal[1])))
        gbest, came, heap = {}, {}, []
        for (l, j, i) in starts:
            gbest[(l, j, i)] = 0.0
            heapq.heappush(heap, (h[j, i], 0.0, l, j, i, -1, None))
        viac = 12.0
        n = 0
        nx, ny = self.nx, self.ny
        while heap:
            f, gc, l, j, i, d0, par = heapq.heappop(heap)
            key = (l, j, i)
            if key in came:
                continue
            came[key] = par
            n += 1
            if n > max_nodes:
                return None
            if via_goal:
                if l == 0 and goal[j, i] and par is not None:
                    return self.backtrack(came, key)
            elif goal[l][j, i] and par is not None:
                return self.backtrack(came, key)
            for k, (di, dj, c) in enumerate(DIRS):
                i2, j2 = i + di, j + dj
                if i2 < 0 or j2 < 0 or i2 >= nx or j2 >= ny or not free[l][j2, i2]:
                    continue
                if di and dj and not (free[l][j, i2] and free[l][j2, i]):
                    continue
                g2 = gc + c + (0.5 if (d0 >= 0 and d0 != k) else 0.0)
                k2 = (l, j2, i2)
                if k2 in came or gbest.get(k2, 1e18) <= g2:
                    continue
                gbest[k2] = g2
                heapq.heappush(heap, (g2 + h[j2, i2], g2, l, j2, i2, k, key))
            if not via_goal and via_ok[j, i] and free[1 - l][j, i]:
                k2 = (1 - l, j, i)
                g2 = gc + viac
                if k2 not in came and gbest.get(k2, 1e18) > g2:
                    gbest[k2] = g2
                    heapq.heappush(heap, (g2 + h[j, i], g2, 1 - l, j, i, -1, key))
        return None

    @staticmethod
    def backtrack(came, key):
        path = []
        while key is not None:
            path.append(key)
            key = came[key]
        return path[::-1]

    # ---------------- commit ----------------
    def commit(self, n, path, w, pads, tree=None, end_via=False):
        """Turn an A* cell path into tracks + vias; snap both ends onto existing copper."""
        pts = []  # (layer, x, y) corners
        vias = []
        prev = path[0]
        pts.append((prev[0],) + self.xy(prev[2], prev[1]))
        pdir = None
        for cur in path[1:]:
            if cur[0] != prev[0]:
                x, y = self.xy(prev[2], prev[1])
                if (pts[-1][1], pts[-1][2]) != (x, y):
                    pts.append((prev[0], x, y))
                vias.append((x, y))
                pts.append((cur[0], x, y))
                pdir = None
            else:
                d = (cur[1] - prev[1], cur[2] - prev[2])
                if pdir is not None and d != pdir:
                    pts.append((prev[0],) + self.xy(prev[2], prev[1]))
                pdir = d
            prev = cur
        pts.append((prev[0],) + self.xy(prev[2], prev[1]))
        # snap start / end onto existing copper of this net
        s = self.snap(n, pts[0][0], pts[0][1], pts[0][2], pads)
        if s:
            pts.insert(0, (pts[0][0], s[0], s[1]))
        if not end_via:
            e = self.snap(n, pts[-1][0], pts[-1][1], pts[-1][2], pads)
            if e:
                pts.append((pts[-1][0], e[0], e[1]))
        big = w >= 0.6
        for a, b in zip(pts, pts[1:]):
            if a[0] == b[0]:
                self.add_track(n, a[0], a[1], a[2], b[1], b[2], w, tree)
        for (x, y) in vias:
            self.add_via(n, x, y, PVIA_D if big else VIA_D, PVIA_DRILL if big else VIA_DRILL, tree)
        return pts[-1]


def min_dim(p):
    pts = np.array(p["poly"][0])
    return float(min(np.ptp(pts[:, 0]), np.ptp(pts[:, 1])))


def route_all(geom, seed=0, priority=()):
    b = Board(geom)
    failed = []
    by_net = {}
    for p in b.pads:
        if p["net"]:
            by_net.setdefault(p["net"], []).append(p)
    # 0) escape stubs (fine pitch): straight out along the pad's long axis, away from the package centre
    for ref, ext in ESCAPE.items():
        fps = [p for p in b.pads if p["ref"] == ref]
        sig = [p for p in fps if not p["tht"]]
        cxm, cym = np.mean([p["x"] for p in sig]), np.mean([p["y"] for p in sig])
        for p in sig:
            if not p["net"]:
                continue
            pts = np.array(p["poly"][0])
            lx, ly = np.ptp(pts[:, 0]), np.ptp(pts[:, 1])
            e = STUB_EXT.get((p["ref"], p["num"]), ext)
            if lx >= ly:
                x2, y2 = p["x"] + np.sign(p["x"] - cxm or 1) * (lx / 2 + e), p["y"]
            else:
                x2, y2 = p["x"], p["y"] + np.sign(p["y"] - cym or 1) * (ly / 2 + e)
            i, j = b.cell(x2, y2)
            x2, y2 = b.xy(i, j)
            # keep the stub on its own axis: snap only the free coordinate
            if lx >= ly:
                y2 = p["y"]
            else:
                x2 = p["x"]
            n = b.nid[p["net"]]
            w = 0.25 if min(lx, ly) < 0.55 else 0.4
            b.add_track(n, 0, p["x"], p["y"], x2, y2, w)
            p["stub"] = (x2, y2)

    def member(tree, p):
        for li, L in enumerate("FB"):
            if L in p["layers"]:
                tree[li] |= p["mask"]
        if p["stub"]:
            b.stamp(b.nid[p["net"]], 0, p["x"], p["y"], p["stub"][0], p["stub"][1], 0.125, tree)

    def run(n, net, src, tree, w, extra_goal_pads, via_goal=False, max_nodes=1500000):
        free, via_ok = b.free_maps(n, w)
        st = b.anchors(src)
        for (l, j, i) in st:
            free[l][j, i] = True
        cand = [(l, j, i) for li, L in enumerate("FB") if L in src["layers"]
                for (l, j, i) in [(li, jj, ii) for jj, ii in zip(*np.nonzero(src["mask"] & free[li]))]]
        starts = st + ([] if src["stub"] else cand)
        if via_goal:
            return b.astar(starts, via_ok, free, via_ok, max_nodes=max_nodes, via_goal=True), free
        goal = [tree[0] & free[0], tree[1] & free[1]]
        for q in extra_goal_pads:
            for (l, j, i) in b.anchors(q):
                goal[l][j, i] = True
                free[l][j, i] = True
        for li, L in enumerate("FB"):
            if L in src["layers"]:
                goal[li] &= ~src["mask"]
        return b.astar(starts, goal, free, via_ok, max_nodes=max_nodes), free

    # 1) explicit Kelvin tie
    for net, a, c, w in EXPLICIT:
        n = b.nid[net]
        pa = next(p for p in b.pads if (p["ref"], p["num"]) == a)
        pc = next(p for p in b.pads if (p["ref"], p["num"]) == c)
        tree = [np.zeros((b.ny, b.nx), bool), np.zeros((b.ny, b.nx), bool)]
        member(tree, pc)
        path, _ = run(n, net, pa, tree, w, [pc])
        if path:
            b.commit(n, path, w, [pa, pc])
        else:
            failed.append(("explicit", net, a[0], a[1]))

    # 2) trees for all routed nets
    rnd = random.Random(seed)
    nets = [k for k in by_net if k not in PLANE and len(by_net[k]) > 1]

    def span(k):
        xs = [p["x"] for p in by_net[k]]
        ys = [p["y"] for p in by_net[k]]
        return (max(xs) - min(xs)) + (max(ys) - min(ys))
    nets.sort(key=lambda k: (k not in priority, k not in POWER_W, span(k) * (1 + (rnd.random() - 0.5) * 0.6 * (seed > 0))))
    for net in nets:
        n = b.nid[net]
        ps = sorted(by_net[net], key=lambda p: (-min_dim(p), p["ref"]))
        tree = [np.zeros((b.ny, b.nx), bool), np.zeros((b.ny, b.nx), bool)]
        members = [ps[0]]
        member(tree, ps[0])
        rest = ps[1:]
        while rest:
            mx = np.array([[q["x"], q["y"]] for q in members])
            rest.sort(key=lambda p: np.min(np.hypot(mx[:, 0] - p["x"], mx[:, 1] - p["y"])))
            p = rest.pop(0)
            wmax = POWER_W.get(net, SIG_W)
            w = max(0.3, min(wmax, round(min_dim(p) * 0.9, 2))) if net in POWER_W else SIG_W
            if p["stub"]:
                w = min(w, 0.4 if min_dim(p) >= 0.55 else 0.25)
            ok = False
            for ww in sorted({w, min(w, 0.5), min(w, 0.3), SIG_W}, reverse=True):
                path, _ = run(n, net, p, tree, ww, members)
                if path:
                    b.commit(n, path, ww, by_net[net], tree)
                    ok = True
                    break
            if not ok:
                failed.append((net, p["ref"], p["num"]))
            member(tree, p)
            members.append(p)

    # 3) plane fan-out vias
    for net in sorted(PLANE):
        n = b.nid[net]
        for p in by_net.get(net, []):
            if p["tht"] or (p["ref"], p["num"]) in SKIP_FANOUT:
                continue
            for _ in range(HEAVY.get((p["ref"], p["num"]), 1)):
                w = 0.4 if min_dim(p) >= 0.45 else 0.25
                path, _ = run(n, net, p, None, w, [], via_goal=True, max_nodes=250000)
                if not path:
                    failed.append((net + "-fanout", p["ref"], p["num"]))
                    break
                end = b.commit(n, path, w, by_net[net], end_via=True)
                b.add_via(n, end[1], end[2], VIA_D, VIA_DRILL)
    # 4) drop escape stubs nothing connected to (avoids dangling-track warnings)
    stubs = {(round(p["x"], 4), round(p["y"], 4), round(p["stub"][0], 4), round(p["stub"][1], 4)) for p in b.pads if p["stub"]}
    keep = []
    for t in b.tracks:
        key = (t["x1"], t["y1"], t["x2"], t["y2"])
        if key in stubs:
            ex, ey = t["x2"], t["y2"]
            used = any(o is not t and o["net"] == t["net"] and o["layer"] == t["layer"] and
                       min(np.hypot(o["x1"] - ex, o["y1"] - ey), np.hypot(o["x2"] - ex, o["y2"] - ey)) < 0.15 for o in b.tracks) or                 any(v["net"] == t["net"] and np.hypot(v["x"] - ex, v["y"] - ey) < 0.15 for v in b.vias)
            if not used:
                continue
        keep.append(t)
    b.tracks = keep
    return b, failed


def main(gpath, out):
    geom = json.load(open(gpath))
    best, prio = None, ()
    for attempt in range(6):
        b, failed = route_all(geom, attempt, prio)
        print("attempt %d: tracks %d vias %d failed %d %s" % (attempt, len(b.tracks), len(b.vias), len(failed), failed[:6]), flush=True)
        if best is None or len(failed) < len(best[1]):
            best = (b, failed)
        if not failed:
            break
        prio = tuple(dict.fromkeys([f[0] for f in failed if not f[0].endswith("fanout") and f[0] != "explicit"] + list(prio)))
    b, failed = best
    json.dump(dict(tracks=b.tracks, vias=b.vias, failed=failed), open(out, "w"), indent=0)
    print("RESULT tracks=%d vias=%d failed=%d" % (len(b.tracks), len(b.vias), len(failed)))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
