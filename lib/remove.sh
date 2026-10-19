#!/usr/bin/env bash
# Engine behind `./sample-data --remove`: removes the sample data again, exactly
# the records lib/load.sh created, found by their codes. The tenant defaults,
# the stock locations and generic records (the name and description attributes,
# the asset families) stay.
#
#   lib/remove.sh --pack industrial     # one pack
#   lib/remove.sh --pack all --base     # every pack and the base (market, company, promotions)
#   lib/remove.sh --pack industrial --dry-run
#
# Apps that keep a trash get a second delete, so the records are gone for good
# and a later load can use the same codes again.
set -euo pipefail
cd "$(dirname "$0")/.."

PACKS=""; BASE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --pack) case "${2:-}" in ""|-*) echo "--pack needs a name" >&2; exit 2 ;; esac; PACKS="$PACKS $2"; shift 2 ;;
    --base) BASE=1; shift ;;
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
[ -z "$PACKS" ] && [ "$BASE" = 0 ] && { echo "nothing to remove: pass --pack <name>, --pack all and/or --base" >&2; exit 2; }

source lib/seed.sh
run_lock_acquire remove "$(echo $PACKS)$([ "$BASE" = 0 ] || echo " base")"

[ -z "$SEED_EVENTS" ] || ev "$(jq -cn --arg tenant "$REVENEXX_TENANT" --argjson dry "$DRY_RUN" --argjson base "$BASE" --arg packs "$PACKS" '{ev: "start", action: "remove", tenant: $tenant, dry: ($dry == 1), base: ($base == 1), packs: ($packs | split(" ") | map(select(. != "")))}')"
say "Removing sample data from tenant $REVENEXX_TENANT$([ "$DRY_RUN" = 1 ] && echo " (dry run)")"
for pack in $PACKS; do
  say "pack: $pack"
  remove_manifest "packs/$pack/manifest.json"
done
if [ "$BASE" = 1 ]; then
  say "base"
  cancel_test_orders
  remove_manifest base/manifest.json
fi
[ "$REMOVE_FAILED" = 0 ] || die "$REMOVE_FAILED removals failed (see above); fix the cause and run it again"
say "done"
ev '{"ev":"done"}'
