# Checker tool chain

Nothing here is vendored. Build the two checkers from the pinned upstream
commits and put the binaries (or symlinks) at `tools/drat-trim/drat-trim` and
`tools/cake_lpr/cake_lpr`, or point `DRAT_TRIM` and `CAKE_LPR` at them.

| tool | upstream | pinned commit / version | license |
|---|---|---|---|
| kissat | https://github.com/arminbiere/kissat | 4.0.4 | MIT |
| drat-trim | https://github.com/marijnheule/drat-trim | 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 | MIT |
| cake_lpr | https://github.com/tanyongkiam/cake_lpr | a36874a8b750b43fe4b385b8ddbf5b033e46a3fa | CakeML (BSD-style) |

```
git clone https://github.com/marijnheule/drat-trim tools/drat-trim
git -C tools/drat-trim checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
make -C tools/drat-trim

git clone https://github.com/tanyongkiam/cake_lpr tools/cake_lpr
git -C tools/cake_lpr checkout a36874a8b750b43fe4b385b8ddbf5b033e46a3fa
make -C tools/cake_lpr            # on arm64 use the cake_lpr_arm8.S target
```

Two things that bit during setup: drat-trim prints `\r` at line ends on some
builds (the verifier strips it before matching `s VERIFIED`), and cake_lpr
rejects an LRAT whose clause numbering disagrees with the CNF it reads, which
happens when the CNF contains duplicate literals in a clause. `cubes.py`
deduplicates literals at serialization time for that reason.
