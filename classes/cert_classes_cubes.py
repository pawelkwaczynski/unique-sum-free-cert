#!/usr/bin/env python3
"""Class-completeness certificate by cube-and-conquer (for p where the whole formula is too hard).

Formula per cube: gen_cnf(p, k) without the reflection breaker, plus one blocking clause per
normalized affine image of every listed class, plus the position-cube units (c, d) = "3rd and
4th smallest elements of A", which partition the space for k >= 4 (same partition as the
production certificates; coverage argument identical). Every cube UNSAT (cadical --lrat,
cake_lpr) => no unique-sum-free set of size k outside the listed classes => list complete.
Cubes that time out are split into children (c, d, e) once; deeper splits are reported.
Output: one JSON line per cube (append, resumable) + final summary line.
Usage: cert_classes_cubes.py p k list.txt out.jsonl [time_limit_s] [workers]
"""
import hashlib, json, os, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, "/home/green27/green27_algo")
sys.path.insert(0, "/home/green27/green27_algo/drat")
import gen_cnf
from certify import parent_units, child_units, tag_units, write_cnf, children_tags

CADICAL = "/home/green27/green27/tools/cadical/build/cadical"
CAKE = "/home/green27/green27/tools/cake_lpr/cake_lpr"


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


def one_cube(base, blocks, p, k, tag, workdir, lim):
    nvars, clauses = base
    cnf = os.path.join(workdir, f"{tag}.cnf")
    lrat = os.path.join(workdir, f"{tag}.lrat")
    write_cnf(cnf, nvars, clauses + blocks, tag_units(p, tag))
    sha = hashlib.sha256(open(cnf, "rb").read()).hexdigest()
    t0 = time.time()
    r = subprocess.run([CADICAL, "-q", "--lrat", "-t", str(lim), cnf, lrat], capture_output=True, text=True)
    e = {"p": p, "k": k, "cube": tag, "cnf_sha256": sha, "solve_s": round(time.time() - t0, 1)}
    if r.returncode == 20:
        t1 = time.time()
        c = subprocess.run([CAKE, cnf, lrat], capture_output=True, text=True)
        ok = c.returncode == 0 and "s VERIFIED UNSAT" in (c.stdout + c.stderr)
        e.update({"status": "UNSAT", "cake_lpr": "VERIFIED" if ok else "FAILED", "check_s": round(time.time() - t1, 1),
                  "lrat_sha256": hashlib.sha256(open(lrat, "rb").read()).hexdigest(),
                  "lrat_mb": round(os.path.getsize(lrat) / 1048576, 1), "proof_verified": ok})
    elif r.returncode == 10:
        lits = []
        for line in r.stdout.splitlines():
            if line.startswith("v "):
                lits += [int(t) for t in line[2:].split() if t != "0"]
        e.update({"status": "SAT", "new_set": sorted(l - 1 for l in lits if 0 < l <= p)})
    else:
        e["status"] = "TIMEOUT" if "UNKNOWN" in r.stdout else "ERROR"
    for f_ in (cnf, lrat):
        if os.path.exists(f_):
            os.unlink(f_)
    return e


def main():
    p, k, lst, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
    lim = int(sys.argv[5]) if len(sys.argv) > 5 else 900
    workers = int(sys.argv[6]) if len(sys.argv) > 6 else 1
    classes = reps(lst)
    images = set()
    for A in classes:
        images |= normalized_images(A, p)
    blocks = [[-(x + 1) for x in img] for img in sorted(images)]
    base = gen_cnf.build(p, k, reflection_break=False)
    done = {}
    if os.path.exists(out):
        for l in open(out):
            try:
                e = json.loads(l)
                if e.get("cube"):
                    done[e["cube"]] = e
            except ValueError:
                pass
    todo = [f"c{c}_d{d}" for c in range(2, p) for d in range(c + 1, p)]
    # one level of split for known timeouts
    for tag, e in list(done.items()):
        if e.get("status") == "TIMEOUT" and tag.count("_") == 1:
            todo += children_tags(p, tag)
    todo = [t for t in todo if t not in done or done[t].get("status") not in ("UNSAT", "SAT")]
    todo = [t for t in todo if not (t.count("_") == 1 and done.get(t, {}).get("status") == "TIMEOUT")]
    print(f"p={p} k={k} classes={len(classes)} blocking={len(blocks)} cubes_todo={len(todo)} done={len(done)}", flush=True)
    with tempfile.TemporaryDirectory() as tmp, open(out, "a") as fout, ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(one_cube, base, blocks, p, k, t, tmp, lim) for t in todo]
        for fut in as_completed(futs):
            e = fut.result()
            fout.write(json.dumps(e) + "\n")
            fout.flush()
            done[e["cube"]] = e
    # summary: complete iff every top-level cube is UNSAT-verified or fully covered by verified children
    def closed(tag):
        e = done.get(tag)
        if e and e.get("status") == "UNSAT" and e.get("proof_verified"):
            return True
        kids = children_tags(p, tag)
        return bool(kids) and all(closed(kt) for kt in kids)
    tops = [f"c{c}_d{d}" for c in range(2, p) for d in range(c + 1, p)]
    sat = [e for e in done.values() if e.get("status") == "SAT"]
    n_closed = sum(closed(t) for t in tops)
    verdict = "LIST-INCOMPLETE" if sat else ("LIST-COMPLETE-CERTIFIED" if n_closed == len(tops) else "UNDECIDED")
    summary = {"p": p, "k": k, "classes": len(classes), "blocking_clauses": len(blocks), "top_cubes": len(tops),
               "closed": n_closed, "sat_found": [e["new_set"] for e in sat], "verdict": verdict}
    with open(out, "a") as f:
        f.write(json.dumps(summary) + "\n")
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
