#!/bin/bash
# Negative controls: the audit must FAIL on tampered inputs. Each case is a
# fresh copy of the p = 53, k = 5 ledger (small) with one corruption applied.
# Exit 0 only when every corruption is rejected.
set -u
cd "$(dirname "$0")/.."
L=ledgers/p53/k5/certified.jsonl; C=ledgers/p53/k5/cover.jsonl
T=$(mktemp -d); fails=0
expect_fail() { # name, command...
  name=$1; shift
  if "$@" >/dev/null 2>&1; then echo "NOT REJECTED: $name"; fails=$((fails+1)); else echo "rejected: $name"; fi
}
# 1. one ledger row deleted: coverage must be incomplete
sed '5d' $L > $T/missing.jsonl
expect_fail "deleted row" python3 audit_coverage.py 53 5 $T/missing.jsonl
# 2. one cnf_sha256 mutated: row must be unbound from the formula
python3 - $L $T/badhash.jsonl <<'PY'
import json,sys
rows=[json.loads(l) for l in open(sys.argv[1]) if l.strip()]
rows[3]["cnf_sha256"]="0"*64
open(sys.argv[2],"w").write("".join(json.dumps(r)+"\n" for r in rows))
PY
expect_fail "mutated cnf hash" python3 audit_coverage.py 53 5 $T/badhash.jsonl
# 3. cake_lpr verdict flipped to FAILED on one row
python3 - $L $T/nocake.jsonl <<'PY'
import json,sys
rows=[json.loads(l) for l in open(sys.argv[1]) if l.strip()]
rows[7]["cake_lpr"]="FAILED"; rows[7]["cake_lpr_rc"]=1
open(sys.argv[2],"w").write("".join(json.dumps(r)+"\n" for r in rows))
PY
expect_fail "unverified row" python3 audit_coverage.py 53 5 $T/nocake.jsonl
# 4. wrong p/k for the ledger
expect_fail "wrong k" python3 audit_coverage.py 53 6 $L
# 5. cover certificate hash mutated
python3 - $C $T/badcover.jsonl <<'PY'
import json,sys
rows=[json.loads(l) for l in open(sys.argv[1]) if l.strip()]
rows[0]["cnf_sha256"]="f"*64
open(sys.argv[2],"w").write("".join(json.dumps(r)+"\n" for r in rows))
PY
expect_fail "mutated cover hash" python3 check_cover.py 53 5 $L $T/badcover.jsonl
# 6. a witness with a unique sum must be refused
python3 - <<'PY'
import json,sys
sys.path.insert(0,"witnesses")
from check_witness import is_usf
assert not is_usf(53,[0,1,2,3,4,5,6,7,8,9,10,11,12,13]), "bad witness accepted"
assert is_usf(53,[0,1,5,7,14,16,18,28,32,35,36,39,43,51])
print("rejected: bad witness")
PY
[ $? -eq 0 ] || fails=$((fails+1))
# 7. verify_drat.sh must refuse a fake checker that exits 0 without the status line
mkdir -p $T/fake/drat-trim $T/fake/cake_lpr
printf '#!/bin/sh\nexit 0\n' > $T/fake/drat-trim/drat-trim; printf '#!/bin/sh\nexit 0\n' > $T/fake/cake_lpr/cake_lpr
chmod +x $T/fake/drat-trim/drat-trim $T/fake/cake_lpr/cake_lpr
printf 'p cnf 1 2\n1 0\n-1 0\n' > $T/t.cnf; printf '0\n' > $T/t.drat
expect_fail "fake checker" env DRAT_TRIM=$T/fake/drat-trim/drat-trim CAKE_LPR=$T/fake/cake_lpr/cake_lpr ./verify_drat.sh $T/t.cnf $T/t.drat
rm -rf $T
echo "negative controls: $fails not rejected"
exit $fails
