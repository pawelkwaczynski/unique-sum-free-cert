"""Replay a random sample of our p53 k=13 cubes on Watson's pinned encoder.
Both encoders put membership of i on variable i+1, so our unit clauses apply
literally. Expect UNSAT for every cube (all are certified UNSAT on ours)."""
import json, random, subprocess, sys, time
OTHER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usf_encode_pinned.py")
LEDGER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ledgers", "p53", "k13", "certified.jsonl")
N = int(sys.argv[1]); seed = int(sys.argv[2]); out = sys.argv[3]
last = {}
for l in open(LEDGER):
    if l.strip():
        r = json.loads(l); last[r["cube"]] = r
cubes = sorted(t for t, r in last.items() if r["status"] == "UNSAT" and r.get("proof_verified"))
random.Random(seed).shuffle(cubes)
base = subprocess.run([sys.executable, OTHER, "53", "13"], capture_output=True, text=True, check=True).stdout
hdr, body = base.split("\n", 1)
_, _, nv, nc = hdr.split()
rows = []; bad = 0
for t in cubes[:N]:
    units = last[t]["units"]
    cnf = f"p cnf {nv} {int(nc)+len(units)}\n" + body + "".join(f"{u} 0\n" for u in units)
    t0 = time.time()
    r = subprocess.run(["kissat", "-q", "--time=600"], input=cnf, capture_output=True, text=True)
    v = "UNSAT" if r.returncode == 20 else "SAT" if r.returncode == 10 else f"rc{r.returncode}"
    bad += v != "UNSAT"
    rows.append({"cube": t, "units": units, "watson_verdict": v, "seconds": round(time.time()-t0, 2), "ours_solve_s": last[t]["solve_s"]})
    print(f"{t:16s} {v:6s} {rows[-1]['seconds']:7.2f}s (ours {last[t]['solve_s']}s)", flush=True)
json.dump({"p": 53, "k": 13, "sample": N, "seed": seed, "mismatches": bad, "rows": rows}, open(out, "w"), indent=1)
print("MISMATCHES", bad)
