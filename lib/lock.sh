# shellcheck shell=bash
# One run at a time. Every engine (load, remove, test order) takes the lock in
# .run/lock before it touches the tenant; a second run refuses while it is held.
#
#   .run/lock/info     key=value lines: pid, pidstart, pgid, action, scopes, started, dry, events
#   .run/last.json     how the last run ended (code, events file), written before the lock goes
#   .run/events-*.jsonl  the run's progress events (what the terminal UI follows)
#
# The lock is a directory: mkdir is atomic. A lock whose process is gone (kill -9,
# power loss) is stale and is taken over. Bash 3.2 compatible.

RUN_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
RUN_DIR=${SAMPLE_DATA_RUN_DIR:-$RUN_ROOT/.run}
RUN_LOCK=$RUN_DIR/lock
RUN_HELD=0
RUN_BUSY_EXIT=3

run_time() { date -r "$1" +%H:%M 2>/dev/null || date -d "@$1" +%H:%M 2>/dev/null || echo "$1"; }

# Start time of a process, as ps prints it; empty when the process is gone.
run_pid_start() { ps -o lstart= -p "$1" 2>/dev/null | sed 's/^ *//; s/ *$//'; }

run_info() { sed -n "s/^$1=//p" "$RUN_LOCK/info" 2>/dev/null | head -n 1; }

# none | starting (lock without its info yet) | live | stale
run_lock_state() {
  [ -d "$RUN_LOCK" ] || { echo none; return 0; }
  [ -f "$RUN_LOCK/info" ] || { echo starting; return 0; }
  local pid; pid=$(run_info pid)
  if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null && [ "$(run_pid_start "$pid")" = "$(run_info pidstart)" ]; then
    echo live
  else
    echo stale
  fi
}

# "remove office (dry run) since 16:12 (pid 1234)"
run_describe() {
  local action scopes what
  action=$(run_info action); scopes=$(run_info scopes)
  case "$action" in order) what="test order" ;; *) what="$action${scopes:+ $scopes}" ;; esac
  [ "$(run_info dry)" != 1 ] || what="$what (dry run)"
  printf '%s since %s (pid %s)' "$what" "$(run_time "$(run_info started)")" "$(run_info pid)"
}

run_refuse() {
  printf 'a run is already going: %s; wait for it or stop it with ./sample-data --stop\n' "$(run_describe)" >&2
}

# Exit with a clear line when a run is going (for callers that want to ask nothing first).
run_lock_check() {
  [ "$(run_lock_state)" = live ] || return 0
  run_refuse
  exit "$RUN_BUSY_EXIT"
}

run_status() {
  case "$(run_lock_state)" in
    live) run_describe; echo ;;
    starting) echo "a run is starting" ;;
    *) echo "no run" ;;
  esac
}

# run_lock_acquire ACTION SCOPES: ACTION is load, remove or order; SCOPES the packs (and base) it visits.
run_lock_acquire() {
  local action=$1 scopes=${2:-} tries=0 spins=0 state started dead
  mkdir -p "$RUN_DIR" || { echo "cannot create $RUN_DIR" >&2; exit 1; }
  while ! mkdir "$RUN_LOCK" 2>/dev/null; do
    spins=$((spins + 1))
    [ "$spins" -le 100 ] || { echo "cannot take the run lock $RUN_LOCK" >&2; exit 1; }
    state=$(run_lock_state)
    case "$state" in
      live) run_refuse; exit "$RUN_BUSY_EXIT" ;;
      none) continue ;;
      starting) tries=$((tries + 1)); if [ "$tries" -le 30 ]; then sleep 0.1; continue; fi ;;
    esac
    # Stale (or stuck before it wrote its info): the rename is atomic, so one contender wins.
    dead=$RUN_DIR/lock.dead.$$
    if mv "$RUN_LOCK" "$dead" 2>/dev/null; then
      printf 'note: taking over the lock of a run that is gone (%s)\n' "$(RUN_LOCK=$dead run_describe)" >&2
      rm -rf "$dead"
    fi
  done
  started=$(date +%s)
  [ -n "${SEED_EVENTS:-}" ] || SEED_EVENTS=$RUN_DIR/events-$started-$$.jsonl
  : > "$SEED_EVENTS" 2>/dev/null || true
  {
    printf 'pid=%s\n' "$$"
    printf 'pidstart=%s\n' "$(run_pid_start $$)"
    printf 'pgid=%s\n' "$(ps -o pgid= -p $$ 2>/dev/null | tr -d ' ')"
    printf 'action=%s\n' "$action"
    printf 'scopes=%s\n' "$scopes"
    printf 'started=%s\n' "$started"
    printf 'dry=%s\n' "${DRY_RUN:-0}"
    printf 'events=%s\n' "$SEED_EVENTS"
  } > "$RUN_LOCK/info.tmp" && mv "$RUN_LOCK/info.tmp" "$RUN_LOCK/info"
  RUN_HELD=1
  RUN_ACTION=$action; RUN_SCOPES=$scopes; RUN_STARTED=$started
  trap 'run_lock_release "$?"' EXIT
  trap 'type ev_msg >/dev/null 2>&1 && ev_msg error "stopped"; exit 143' TERM
  trap 'exit 130' INT
  trap 'exit 129' HUP
  run_prune
}

# Keep the newest few event files (and the output files next to them).
run_prune() {
  local f
  ls -t "$RUN_DIR"/events-*.jsonl 2>/dev/null | tail -n +8 | while IFS= read -r f; do
    rm -f "$f" "$(printf '%s' "$f" | sed 's|/events-\(.*\)\.jsonl$|/out-\1.log|')"
  done
}

# run_lock_release EXIT_CODE: record how the run ended, then let go of the lock.
run_lock_release() {
  [ "$RUN_HELD" = 1 ] || return 0
  RUN_HELD=0
  [ "$(run_info pid)" = "$$" ] || return 0
  jq -cn --argjson pid "$$" --arg action "$RUN_ACTION" --arg scopes "$RUN_SCOPES" --argjson started "$RUN_STARTED" \
    --argjson ended "$(date +%s)" --argjson code "${1:-0}" --arg events "${SEED_EVENTS:-}" \
    '{pid: $pid, action: $action, scopes: $scopes, started: $started, ended: $ended, code: $code, events: $events}' \
    > "$RUN_DIR/last.json.tmp" 2>/dev/null && mv "$RUN_DIR/last.json.tmp" "$RUN_DIR/last.json"
  rm -rf "$RUN_LOCK"
}

# All descendants of a pid, deepest first.
run_descendants() {
  local c
  for c in $(pgrep -P "$1" 2>/dev/null); do run_descendants "$c"; echo "$c"; done
}

# run_signal SIG: to the run's process group when it leads one (the terminal UI starts runs that way),
# otherwise to the run and its children (never to a group that holds the caller).
run_signal() {
  local sig=$1 pid pgid p
  pid=$(run_info pid); pgid=$(run_info pgid)
  if [ -n "$pgid" ] && [ "$pgid" = "$pid" ]; then
    kill -s "$sig" -- "-$pid" 2>/dev/null || true
  else
    for p in $(run_descendants "$pid"); do kill -s "$sig" "$p" 2>/dev/null || true; done
    kill -s "$sig" "$pid" 2>/dev/null || true
  fi
}

run_stop() {
  local state i desc
  state=$(run_lock_state)
  case "$state" in
    live) ;;
    starting) echo "a run is starting; try again in a moment" >&2; return 1 ;;
    *) echo "no run"; return 0 ;;
  esac
  desc=$(run_describe)
  run_signal TERM
  for i in $(seq 1 75); do
    [ "$(run_lock_state)" = live ] || { echo "stopped: $desc"; return 0; }
    sleep 0.2
  done
  run_signal KILL
  sleep 0.3
  rm -rf "$RUN_LOCK"
  echo "killed: $desc (it did not stop in 15 s)"
}
