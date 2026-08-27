#!/bin/bash
# verify_lrat.sh CNF LRAT
# Lancuch natywny: cake_lpr (formalnie zweryfikowany checker, HOL4) czyta LRAT
# wprost z solvera (cadical --lrat, format binarny lub tekstowy). Bez drat-trima:
# jedno narzedzie zaufane mniej, brak etapu DRAT->LRAT, ktory byl waskim gardlem
# (pomiar 26.08: 330 s -> 50 s na tej samej kostce).
# PASS tylko gdy cake_lpr konczy rc=0 I wypisuje "s VERIFIED UNSAT".
# Wyjscie na stdout: jedna linia JSON, pola jak w verify_drat.sh gdzie ma to sens,
# plus chain, lrat_sha256, lrat_mb; drat_trim="SKIPPED" mowi wprost, ze go nie bylo.
# rc: 0=PASS, 1=FAIL, 2=blad uzycia/narzedzi
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
CAKE_LPR="$HERE/tools/cake_lpr/cake_lpr"

CNF="${1:-}"; LRAT="${2:-}"
[ -f "$CNF" ] && [ -f "$LRAT" ] || { echo "uzycie: verify_lrat.sh CNF LRAT" >&2; exit 2; }
[ -x "$CAKE_LPR" ] || { echo "brak cake_lpr w $HERE/tools" >&2; exit 2; }

OUT="$(mktemp "${TMPDIR:-/tmp}/vl_out_XXXXXX")" || exit 2
trap 'rm -f "$OUT"' EXIT

SHA=$(shasum -a 256 "$LRAT" | cut -d' ' -f1)
CNFSHA=$(shasum -a 256 "$CNF" | cut -d' ' -f1)

T0=$(date +%s.%N)
"$CAKE_LPR" "$CNF" "$LRAT" >"$OUT" 2>&1
CL_RC=$?
T1=$(date +%s.%N)
CL=FAILED
if [ $CL_RC -eq 0 ] && tr -d '\r' <"$OUT" | grep -qx "s VERIFIED UNSAT"; then CL=VERIFIED; fi

if [ "$CL" = VERIFIED ]; then VERDICT=PASS; RC=0; else VERDICT=FAIL; RC=1; fi
CL_S=$(echo "$T1 - $T0" | bc)
LRAT_MB=$(( ($(wc -c <"$LRAT" 2>/dev/null || echo 0) + 524288) / 1048576 ))
printf '{"cnf":"%s","cnf_sha256":"%s","chain":"cadical-lrat-cake_lpr","lrat_sha256":"%s","drat_trim":"SKIPPED","drat_trim_rc":-1,"cake_lpr":"%s","cake_lpr_rc":%d,"cake_lpr_s":%.2f,"lrat_mb":%d,"verdict":"%s"}\n' \
    "$(basename "$CNF")" "$CNFSHA" "$SHA" "$CL" "$CL_RC" "$CL_S" "$LRAT_MB" "$VERDICT"
exit $RC
