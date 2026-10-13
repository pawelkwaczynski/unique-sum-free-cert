#!/bin/bash
# Fetch the ledgers that are too large for git (GitHub refuses files over 100 MB). Each such rung
# has an EXTERNAL_LEDGER file with the download URL and the sha256 of the compressed file; the file
# lands next to it as certified.jsonl.gz (ignored by git) and is refused if the hash differs.
set -euo pipefail
cd "$(dirname "$0")"
for f in ledgers/p*/k*/EXTERNAL_LEDGER; do
    [ -f "$f" ] || continue
    d=$(dirname "$f")
    url=$(awk '$1 == "url" {print $2}' "$f")
    want=$(awk '$1 == "sha256" {print $2}' "$f")
    out=$d/certified.jsonl.gz
    if [ ! -f "$out" ]; then
        echo "fetching $out"
        curl -fsSL --retry 3 -o "$out.part" "$url"
        mv "$out.part" "$out"
    fi
    got=$(shasum -a 256 "$out" | cut -c1-64)
    [ "$got" = "$want" ] || { echo "sha256 mismatch for $out: $got, expected $want"; rm -f "$out"; exit 1; }
    echo "ok $out"
done
