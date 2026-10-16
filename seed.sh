#!/usr/bin/env bash
# Load the sample data into a revenexx tenant.
#
#   REVENEXX_BASE_URL=https://api.revenexx.com/v1 \
#   REVENEXX_TENANT=<your-tenant> REVENEXX_API_KEY=<key> \
#   ./seed.sh --pack industrial        # base + one pack
#   ./seed.sh --pack all               # base + every pack
#   ./seed.sh --pack industrial --dry-run
#
# Safe to run again: every record is looked up by its code first and updated,
# never duplicated.
set -euo pipefail
cd "$(dirname "$0")"

PACKS=""
while [ $# -gt 0 ]; do
  case "$1" in
    --pack) case "${2:-}" in ""|-*) echo "--pack needs a name" >&2; exit 2 ;; esac; PACKS="$PACKS $2"; shift 2 ;;
    --dry-run) export DRY_RUN=1; shift ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done
case " $PACKS " in *" all "*) PACKS=$(ls packs) ;; esac
# Every pack name is checked before anything is written; each pack loads once.
PACKS=$(printf '%s\n' $PACKS | awk '!seen[$0]++')
for pack in $PACKS; do
  [ -f "packs/$pack/manifest.json" ] || { echo "no pack named '$pack' (have: $(ls packs | tr '\n' ' '))" >&2; exit 2; }
done

source lib/seed.sh

say "Seeding tenant $REVENEXX_TENANT$([ "$DRY_RUN" = 1 ] && echo " (dry run)")"
say "base"
run_manifest base/manifest.json
for pack in $PACKS; do
  say "pack: $pack"
  run_manifest "packs/$pack/manifest.json"
done
say "done"
