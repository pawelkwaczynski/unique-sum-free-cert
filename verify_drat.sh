#!/bin/bash
# verify_drat.sh CNF DRAT [--keep-lrat]
# Chain: drat-trim (checks the DRAT, emits LRAT) -> cake_lpr (formally
# verified checker, HOL4). PASS only when both tools exit 0 AND print their
# status line; an exit code alone proved too weak in review.
# Output: one JSON line {cnf, cnf_sha256, drat_sha256, drat_trim, drat_trim_rc,
# drat_trim_s, cake_lpr, cake_lpr_rc, cake_lpr_s, lrat_mb, verdict}
# Exit code: 0 = PASS, 1 = FAIL, 2 = usage or missing tools
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
DRAT_TRIM="${DRAT_TRIM:-$HERE/tools/drat-trim/drat-trim}"
CAKE_LPR="${CAKE_LPR:-$HERE/tools/cake_lpr/cake_lpr}"

CNF="${1:-}"; DRAT="${2:-}"; KEEP="${3:-}"
[ -f "$CNF" ] && [ -f "$DRAT" ] || { echo "usage: verify_drat.sh CNF DRAT [--keep-lrat]" >&2; exit 2; }
[ -x "$DRAT_TRIM" ] && [ -x "$CAKE_LPR" ] || { echo "tools missing, see tools/README.md" >&2; exit 2; }

LRAT="$(mktemp "${TMPDIR:-/tmp}/vd_lrat_XXXXXX")" || exit 2
DTOUT="$(mktemp "${TMPDIR:-/tmp}/vd_dt_XXXXXX")" || exit 2
trap 'rm -f "$DTOUT"; [ "$KEEP" = "--keep-lrat" ] || rm -f "$LRAT"' EXIT

SHA=$(shasum -a 256 "$DRAT" | cut -d' ' -f1)
CNFSHA=$(shasum -a 256 "$CNF" | cut -d' ' -f1)

T0=$(date +%s.%N)
"$DRAT_TRIM" "$CNF" "$DRAT" -L "$LRAT" >"$DTOUT" 2>&1
DT_RC=$?
T1=$(date +%s.%N)
DT=FAILED
# drat-trim ends its lines with \r on some builds; strip before matching
if [ $DT_RC -eq 0 ] && tr -d '\r' <"$DTOUT" | grep -qx "s VERIFIED"; then DT=VERIFIED; fi

CL=SKIPPED; CL_RC=-1
if [ "$DT" = VERIFIED ]; then
    "$CAKE_LPR" "$CNF" "$LRAT" >"$DTOUT" 2>&1
    CL_RC=$?
    T2=$(date +%s.%N)
    CL=FAILED
    if [ $CL_RC -eq 0 ] && tr -d '\r' <"$DTOUT" | grep -qx "s VERIFIED UNSAT"; then CL=VERIFIED; fi
fi

if [ "$DT" = VERIFIED ] && [ "$CL" = VERIFIED ]; then VERDICT=PASS; RC=0; else VERDICT=FAIL; RC=1; fi
# per-stage timing: without it you cannot tell whether drat-trim or cake_lpr
# is the bottleneck
T2=${T2:-$T1}
DT_S=$(echo "$T1 - $T0" | bc)
CL_S=$(echo "$T2 - $T1" | bc)
LRAT_MB=$(( ($(wc -c <"$LRAT" 2>/dev/null || echo 0) + 524288) / 1048576 ))
printf '{"cnf":"%s","cnf_sha256":"%s","drat_sha256":"%s","drat_trim":"%s","drat_trim_rc":%d,"drat_trim_s":%.2f,"cake_lpr":"%s","cake_lpr_rc":%d,"cake_lpr_s":%.2f,"lrat_mb":%d,"verdict":"%s"}\n' \
    "$(basename "$CNF")" "$CNFSHA" "$SHA" "$DT" "$DT_RC" "$DT_S" "$CL" "$CL_RC" "$CL_S" "$LRAT_MB" "$VERDICT"
exit $RC
