"""Compare eSchema-exported netlist with design/circuit.py (pin-by-pin)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "design"))
from sexpr import parse, find, find_all
import circuit

t = parse(open(sys.argv[1], encoding="utf-8").read())
got = {}
names = []
for n in find_all(find(t, "nets"), "net"):
    name = find(n, "name")[1]
    names.append(name)
    nodes = frozenset((find(x, "ref")[1], find(x, "pin")[1]) for x in find_all(n, "node"))
    if not name.startswith("unconnected-"):
        got[name.lstrip("/")] = nodes
want = {k: frozenset(v) for k, v in circuit.nets().items()}
bad = 0
for k, v in want.items():
    if got.get(k) != v:
        bad += 1
        print("MISMATCH", k, "want", sorted(v), "got", sorted(got.get(k, [])))
for k in got:
    if k not in want:
        bad += 1
        print("EXTRA NET", k, sorted(got[k]))
comps = {find(c, "ref")[1] for c in find_all(find(t, "components"), "comp")}
wantc = {p["ref"] for p in circuit.PARTS}
print("components:", len(comps), "expected:", len(wantc), "missing:", sorted(wantc - comps), "extra:", sorted(comps - wantc))
print("net names sample:", names[:6])
print("RESULT:", "PASS" if bad == 0 and comps == wantc else "FAIL (%d)" % bad)
