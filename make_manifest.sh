#!/bin/bash
# Rebuild SHA256SUMS over everything a referee needs: code, ledgers, covers,
# witnesses, class lists and their certificates, tests. Run before every tag.
# classes/ was outside the manifest until 2026-09-24, so the two class certificates
# shipped without a checksum; they are the part a referee is most likely to re-run.
cd "$(dirname "$0")"
find gen_cnf.py cubes.py audit_coverage.py check_cover.py cover_cert.py export_ledger.py verify_drat.sh verify_lrat.sh \
     ledgers witnesses classes encoding-tests tests -type f ! -name '.DS_Store' | sort \
  | xargs shasum -a 256 > SHA256SUMS
wc -l SHA256SUMS
