#!/bin/bash
# Rebuild SHA256SUMS over everything a referee needs: code, ledgers, covers,
# witnesses, tests. Run before every tag.
cd "$(dirname "$0")"
find gen_cnf.py cubes.py audit_coverage.py check_cover.py cover_cert.py export_ledger.py verify_drat.sh \
     ledgers witnesses encoding-tests tests -type f ! -name '*.gz' ! -name '.DS_Store' | sort \
  | xargs shasum -a 256 > SHA256SUMS
wc -l SHA256SUMS
