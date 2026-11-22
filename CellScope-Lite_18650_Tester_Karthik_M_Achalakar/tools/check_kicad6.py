"""Structural check of converted files against real KiCad 6.0 files.

Usage: python tools/check_kicad6.py <ref_dir> <file> [<file> ...]

For each converted file, every (parent-keyword, child-keyword) pair and every
bare atom used as a flag is compared with the set seen in KiCad 6.0 reference
files of the same type (.kicad_pcb / .kicad_sch / .kicad_sym).  Anything that
never occurs in the references is listed for manual review against the
KiCad 6.0.11 parser source.
"""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sexpr import Sym, parse  # noqa: E402

CTX = {"symbol"}       # make lib symbol vs. placed symbol distinct


def pairs(t, parent="ROOT", acc=None, depth=0):
    acc = set() if acc is None else acc
    if not isinstance(t, list) or not t:
        return acc
    h = str(t[0]) if isinstance(t[0], Sym) else "<list>"
    me = h
    if h == "symbol":
        me = "symbol@" + parent
    for x in t[1:]:
        if isinstance(x, list) and x and isinstance(x[0], Sym):
            acc.add((me, str(x[0])))
            pairs(x, me, acc, depth + 1)
        elif isinstance(x, list):
            pairs(x, me, acc, depth + 1)
        elif isinstance(x, Sym) and not x.replace(".", "").replace("-", "").isdigit():
            acc.add((me, "atom:" + str(x)))
    return acc


def main():
    ref, files = sys.argv[1], sys.argv[2:]
    bad_total = 0
    for f in files:
        ext = os.path.splitext(f)[1]
        refs = glob.glob(os.path.join(ref, "*" + ext))
        if ext == ".kicad_sym":
            refs += glob.glob(os.path.join(ref, "*.kicad_sch"))
        rp = set()
        for r in refs:
            rp |= pairs(parse(open(r, encoding="utf-8").read()))
        if ext == ".kicad_sym":      # lib file symbols appear under lib_symbols in schematics
            rp |= {(("symbol@ROOT" if a == "symbol@lib_symbols" else a), b) for a, b in rp}
            rp |= {("kicad_symbol_lib", "symbol"), ("kicad_symbol_lib", "version"), ("kicad_symbol_lib", "generator"),
                   ("kicad_symbol_lib", "atom:kicad_symbol_editor")}
        mine = pairs(parse(open(f, encoding="utf-8").read()))
        bad = sorted(p for p in mine - rp if not p[1].startswith("atom:") or True)
        bad = [p for p in bad if p not in rp]
        print("%s: %d pairs, %d not seen in KiCad 6 references" % (f, len(mine), len(bad)))
        for p in bad:
            print("   ", p)
        bad_total += len(bad)
    return bad_total


if __name__ == "__main__":
    main()
