#!/usr/bin/env bash
# Engine behind `./sample-data --load`: loads the sample data into a revenexx tenant.
# Run it through ./sample-data; the options below are the engine's own.
#
#   REVENEXX_BASE_URL=https://api.revenexx.com/v1 \
#   REVENEXX_TENANT=<your-tenant> REVENEXX_API_KEY=<key> \
#   lib/load.sh --pack industrial        # base + one pack
#   lib/load.sh --pack all               # base + every pack
#   lib/load.sh --pack industrial --dry-run
#
# --no-base skips the base; --skip-base-if-complete skips it when every base
# record is already there.
#
# Safe to run again: every record is looked up by its code first and updated,
# never duplicated.
set -euo pipefail
cd "$(dirname "$0")/.."

PACKS=""; BASE_MODE=always
while [ $# -gt 0 ]; do
  case "$1" in
    --pack) case "${2:-}" in ""|-*) echo "--pack needs a name" >&2; exit 2 ;; esac; PACKS="$PACKS $2"; shift 2 ;;
    --dry-run) export DRY_RUN=1; shift ;;
    --no-base) BASE_MODE=never; shift ;;
    --skip-base-if-complete) BASE_MODE=if-missing; shift ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
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
run_lock_acquire load "$([ "$BASE_MODE" = never ] || echo "base ")$(echo $PACKS)"

[ -z "$SEED_EVENTS" ] || ev "$(jq -cn --arg tenant "$REVENEXX_TENANT" --argjson dry "$DRY_RUN" --arg packs "$PACKS" '{ev: "start", action: "seed", tenant: $tenant, dry: ($dry == 1), packs: ($packs | split(" ") | map(select(. != "")))}')"
say "Seeding tenant $REVENEXX_TENANT$([ "$DRY_RUN" = 1 ] && echo " (dry run)")"
if [ "$BASE_MODE" = if-missing ] && base_complete; then BASE_MODE=never; fi
if [ "$BASE_MODE" = never ]; then
  ok "base already loaded, skipped"
else
  say "base"
  run_manifest base/manifest.json
fi
for pack in $PACKS; do
  say "pack: $pack"
  run_manifest "packs/$pack/manifest.json"
done
say "done"
ev '{"ev":"done"}'
