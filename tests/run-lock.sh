#!/usr/bin/env bash
# Tests of the one-run-at-a-time lock (lib/lock.sh) and ./sample-data --status / --stop.
# No tenant and no API needed: the "runs" are shell processes that take the lock and sleep.
#   tests/run-lock.sh
set -u
cd "$(dirname "$0")/.."
export SAMPLE_DATA_RUN_DIR=$(mktemp -d)
trap 'kill $(jobs -p) 2>/dev/null; rm -rf "$SAMPLE_DATA_RUN_DIR"' EXIT
FAILS=0
check() { # check NAME CONDITION-RESULT(0 = ok)
  if [ "$2" = 0 ]; then echo "ok   $1"; else echo "FAIL $1"; FAILS=$((FAILS + 1)); fi
}
# A fake run: takes the lock the way the engines do, then waits.
holder() { bash -c 'source lib/lock.sh; run_lock_acquire "$1" "$2"; sleep 60' _ "$@" & HOLDER=$!; sleep 0.5; }

# 1. a second run refuses while the first holds the lock
holder remove office
out=$(bash -c 'source lib/lock.sh; run_lock_acquire load industrial' 2>&1); code=$?
check "second run exits 3" "$([ "$code" = 3 ] && echo 0 || echo 1)"
case "$out" in "a run is already going: remove office since "*"(pid $HOLDER); wait for it or stop it with ./sample-data --stop") r=0 ;; *) r=1; echo "  got: $out" ;; esac
check "refusal names the run and the way out" "$r"
out=$(./sample-data --load office 2>&1); code=$?
check "the --load flag refuses too" "$([ "$code" = 3 ] && [ "${out#a run is already going}" != "$out" ] && echo 0 || echo 1)"
out=$(./sample-data --status); check "--status shows the run" "$([ "${out#remove office since }" != "$out" ] && echo 0 || echo 1)"

# 2. kill -9 leaves a stale lock; the next run takes it over with a note
pkill -KILL -P $HOLDER 2>/dev/null; kill -9 $HOLDER; wait $HOLDER 2>/dev/null
check "lock dir is still there after kill -9" "$([ -d "$SAMPLE_DATA_RUN_DIR/lock" ] && echo 0 || echo 1)"
out=$(./sample-data --status); check "--status says no run for a stale lock" "$([ "$out" = "no run" ] && echo 0 || echo 1)"
out=$(bash -c 'source lib/lock.sh; run_lock_acquire load industrial; echo took it' 2>&1); code=$?
check "next run takes over the stale lock" "$([ "$code" = 0 ] && [ "${out#note: taking over}" != "$out" ] && echo 0 || echo 1)"
check "and releases it on exit" "$([ ! -d "$SAMPLE_DATA_RUN_DIR/lock" ] && echo 0 || echo 1)"
check "last.json records code 0" "$([ "$(jq -r .code "$SAMPLE_DATA_RUN_DIR/last.json")" = 0 ] && echo 0 || echo 1)"

# 3. --stop ends a run cleanly and releases the lock
holder load office
out=$(./sample-data --stop); check "--stop reports it" "$([ "${out#stopped: load office}" != "$out" ] && echo 0 || echo 1)"
wait $HOLDER 2>/dev/null
check "lock is gone after --stop" "$([ ! -d "$SAMPLE_DATA_RUN_DIR/lock" ] && echo 0 || echo 1)"
check "last.json records code 143" "$([ "$(jq -r .code "$SAMPLE_DATA_RUN_DIR/last.json")" = 143 ] && echo 0 || echo 1)"
out=$(./sample-data --stop); check "--stop with no run says so" "$([ "$out" = "no run" ] && echo 0 || echo 1)"

# 4. two runs started at once: exactly one wins
for i in 1 2 3 4; do (bash -c 'source lib/lock.sh; run_lock_acquire load x; sleep 2' >/dev/null 2>&1; echo $? >> "$SAMPLE_DATA_RUN_DIR/codes") & done
wait
check "of four simultaneous runs one gets the lock" "$([ "$(grep -c '^0$' "$SAMPLE_DATA_RUN_DIR/codes")" = 1 ] && [ "$(grep -c '^3$' "$SAMPLE_DATA_RUN_DIR/codes")" = 3 ] && echo 0 || echo 1)"

[ "$FAILS" = 0 ] && echo "all passed" || { echo "$FAILS failed"; exit 1; }
