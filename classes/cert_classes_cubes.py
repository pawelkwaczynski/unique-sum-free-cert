#!/usr/bin/env python3
"""Class-completeness certificate by cube-and-conquer (for p where the whole formula is too hard).

Formula per cube: gen_cnf(p, k) without the reflection breaker, plus one blocking clause per
normalized affine image of every listed class, plus the position-cube units (c, d) = "3rd and
4th smallest elements of A", which partition the space for k >= 4 (same partition as the
production certificates; coverage argument identical). Every cube UNSAT (cadical --lrat,
cake_lpr) => no unique-sum-free set of size k outside the listed classes => list complete.
A cube that times out is split into children at any depth, up to max_depth, and the work
runs in rounds: compute the frontier, solve it, compute the frontier again, stop when empty.
Splitting only at the top level is not enough; at p = 59 the children of 109 top-level cubes
included 323 that timed out in turn, and those cubes cannot be closed without a deeper split.
Output: one JSON line per cube (append, resumable) + final summary line.
Usage: cert_classes_cubes.py p k list.txt out.jsonl [time_limit_s] [workers] [max_depth]
"""
import hashlib, json, os, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor, as_completed

# The repository root holds gen_cnf.py and cubes.py; nothing here depends on an absolute path.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gen_cnf
from cubes import tag_units, children_tags, serialize_cnf

# Solver and checker are taken from the environment, falling back to the names on PATH.
CADICAL = os.environ.get("CADICAL", "cadical")
CAKE = os.environ.get("CAKE_LPR", "cake_lpr")


def write_cnf(path, nvars, clauses, extra_units):
    """One writer for the DIMACS bytes, shared with cubes.cnf_sha256, so the hash in the
    ledger is the hash of the file the solver and cake_lpr actually read."""
    with open(path, "wb") as f:
        f.write(serialize_cnf(nvars, clauses, extra_units))


def preflight():
    """Fail before any solving if a tool is missing, rather than logging thousands of ERROR cubes.
    Called once the first round has work to do, so a finished ledger can be re-checked without them."""
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
    max_depth = int(sys.argv[7]) if len(sys.argv) > 7 else 6
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
    tops = [f"c{c}_d{d}" for c in range(2, p) for d in range(c + 1, p)]

    def frontier(tag, depth):
        """Cubes that must be solved before tag can be closed. A cube absent from the ledger
        counts as work to do, never as an excuse to descend into children that are absent too."""
        e = done.get(tag)
        if e is None:
            return [tag]
        st = e.get("status")
        if st == "SAT" or (st == "UNSAT" and e.get("proof_verified")):
            return []
        if st in ("TIMEOUT", "ERROR"):
            if depth >= max_depth:
                return []
            kids = children_tags(p, tag)
            if not kids:
                return []
            acc = []
            for kt in kids:
                acc.extend(frontier(kt, depth + 1))
            return acc
        return [tag]

    def closed(tag, depth):
        e = done.get(tag)
        if e is None:
            return False
        if e.get("status") == "UNSAT" and e.get("proof_verified"):
            return True
        if e.get("status") in ("TIMEOUT", "ERROR"):
            if depth >= max_depth:
                return False
            kids = children_tags(p, tag)
            return bool(kids) and all(closed(kt, depth + 1) for kt in kids)
        return False

    print(f"p={p} k={k} classes={len(classes)} blocking={len(blocks)} done={len(done)} max_depth={max_depth}", flush=True)
    rounds = 0
    with tempfile.TemporaryDirectory() as tmp:
        while True:
            rounds += 1
            todo, seen = [], set()
            for t in tops:
                for x in frontier(t, 2):
                    if x not in seen:
                        seen.add(x)
                        todo.append(x)
            if not todo:
                break
            by_depth = {}
            for t in todo:
                by_depth[t.count("_") + 1] = by_depth.get(t.count("_") + 1, 0) + 1
            print(f"round {rounds}: {len(todo)} cubes, by depth {sorted(by_depth.items())}", flush=True)
            if rounds == 1:
                preflight()   # only now, so re-checking a finished ledger needs no solver
            with open(out, "a") as fout, ThreadPoolExecutor(max_workers=workers) as ex:
                futs = [ex.submit(one_cube, base, blocks, p, k, t, tmp, lim) for t in todo]
                for fut in as_completed(futs):
                    e = fut.result()
                    fout.write(json.dumps(e) + "\n")
                    fout.flush()
                    done[e["cube"]] = e
            if any(done[t].get("status") == "SAT" for t in todo):
                print(f"round {rounds}: SAT, the list is not complete", flush=True)
                break
    # summary: complete iff every top-level cube is UNSAT-verified or fully covered by verified children
    sat = [e for e in done.values() if e.get("status") == "SAT"]
    n_closed = sum(1 for t in tops if closed(t, 2))
    verdict = "LIST-INCOMPLETE" if sat else ("LIST-COMPLETE-CERTIFIED" if n_closed == len(tops) else "UNDECIDED")
    summary = {"p": p, "k": k, "classes": len(classes), "blocking_clauses": len(blocks), "top_cubes": len(tops),
               "closed": n_closed, "open": len(tops) - n_closed, "max_depth": max_depth, "rounds": rounds,
               "sat_found": [e["new_set"] for e in sat], "verdict": verdict}
    with open(out, "a") as f:
        f.write(json.dumps(summary) + "\n")
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
