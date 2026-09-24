#!/usr/bin/env python3
"""Certificate that a list of affine classes of minimum unique-sum-free sets is complete
(Krug 2026, Prop. 15 pattern: uniqueness up to isomorphism as an UNSAT certificate).

Formula: gen_cnf(p, k) without the reflection breaker (0, 1 in A, |A| = k, no unique sum)
plus one blocking clause per normalized affine image of every listed class
(images containing {0, 1}; every set in a listed class has such an image, so a model of
the blocked formula would be a set outside every listed class). UNSAT => list complete.
Solver: cadical --lrat (binary), checker: cake_lpr. Emits one JSON line.
Usage: cert_classes.py p k list.txt out.jsonl [time_limit_s]
"""
import hashlib, json, os, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor, as_completed

# The repository root holds gen_cnf.py and cubes.py; nothing here depends on an absolute path.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gen_cnf

# Solver and checker are taken from the environment, falling back to the names on PATH.
CADICAL = os.environ.get("CADICAL", "cadical")
CAKE = os.environ.get("CAKE_LPR", "cake_lpr")


def preflight():
    """Fail before any solving if a tool is missing, rather than logging thousands of ERROR cubes."""
    import shutil
    missing = [n for n, p in (("cadical", CADICAL), ("cake_lpr", CAKE))
               if not (os.path.isfile(p) and os.access(p, os.X_OK)) and shutil.which(p) is None]
    if missing:
        sys.stderr.write(
            "missing tool(s): %s\n"
            "Set CADICAL and CAKE_LPR to the binaries, or put them on PATH.\n" % ", ".join(missing))
        sys.exit(2)


def reps(path):
    return [tuple(int(x) for x in l[2:].strip().strip("{}").split(",")) for l in open(path) if l.startswith("W ")]


def normalized_images(A, p):
    out = set()
    for a in range(1, p):
        for b in range(p):
            img = tuple(sorted((a * x + b) % p for x in A))
            if 0 in img and 1 in img:
                out.add(img)
    return out


def main():
    preflight()
    p, k, lst, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
    lim = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    classes = reps(lst)
    images = set()
    for A in classes:
        assert len(A) == k
        images |= normalized_images(A, p)
    nvars, clauses = gen_cnf.build(p, k, reflection_break=False)
    blocks = [[-(x + 1) for x in img] for img in sorted(images)]   # membership of i on var i+1
    with tempfile.TemporaryDirectory() as tmp:
        cnf = os.path.join(tmp, f"classes_p{p}k{k}.cnf")
        lrat = os.path.join(tmp, f"classes_p{p}k{k}.lrat")
        with open(cnf, "w") as f:
            f.write(f"p cnf {nvars} {len(clauses) + len(blocks)}\n")
            for c in clauses:
                f.write(" ".join(map(str, dict.fromkeys(c))) + " 0\n")
            for b in blocks:
                f.write(" ".join(map(str, b)) + " 0\n")
        sha = hashlib.sha256(open(cnf, "rb").read()).hexdigest()
        cmd = [CADICAL, "-q", "--lrat"] + (["-t", str(lim)] if lim else []) + [cnf, lrat]
        t0 = time.time()
        r = subprocess.run(cmd, capture_output=True, text=True)
        solve_s = round(time.time() - t0, 1)
        e = {"p": p, "k": k, "classes": len(classes), "blocking_clauses": len(blocks),
             "cnf_sha256": sha, "solve_s": solve_s, "rc": r.returncode}
        if r.returncode == 20:
            t1 = time.time()
            c = subprocess.run([CAKE, cnf, lrat], capture_output=True, text=True)
            ok = c.returncode == 0 and "s VERIFIED UNSAT" in (c.stdout + c.stderr)
            e.update({"status": "UNSAT", "cake_lpr": "VERIFIED" if ok else "FAILED",
                      "check_s": round(time.time() - t1, 1),
                      "lrat_sha256": hashlib.sha256(open(lrat, "rb").read()).hexdigest(),
                      "lrat_mb": round(os.path.getsize(lrat) / 1048576, 1),
                      "verdict": "LIST-COMPLETE-CERTIFIED" if ok else "CHECK-FAILED"})
        elif r.returncode == 10:
            lits = []
            for line in r.stdout.splitlines():
                if line.startswith("v "):
                    lits += [int(t) for t in line[2:].split() if t != "0"]
            e.update({"status": "SAT", "verdict": "LIST-INCOMPLETE",
                      "new_set": sorted(l - 1 for l in lits if 0 < l <= p)})
        else:
            e.update({"status": "TIMEOUT" if "UNKNOWN" in r.stdout else "ERROR", "verdict": "UNDECIDED"})
    with open(out, "a") as f:
        f.write(json.dumps(e) + "\n")
    print(json.dumps(e), flush=True)


if __name__ == "__main__":
    main()
