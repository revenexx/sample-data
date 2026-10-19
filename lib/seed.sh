# shellcheck shell=bash
# Shared helpers for load.sh and remove.sh: one HTTP wrapper, lookups by a
# natural key, and the upsert that every plain step uses.
#
# Nothing in the API upserts by code: a repeated POST answers 409 or creates a
# duplicate. So every record is looked up by its key first and then updated
# (PUT, which merges) or created (POST).
#
# Works with the bash 3.2 that ships with macOS (no associative arrays).

SEED_LIB=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=env.sh
source "$SEED_LIB/env.sh"
# shellcheck source=lock.sh
source "$SEED_LIB/lock.sh"
load_dotenv "$(dirname "${BASH_SOURCE[0]}")/../.env"

: "${REVENEXX_BASE_URL:=https://api.revenexx.com/v1}"
: "${REVENEXX_TENANT:?set REVENEXX_TENANT to your tenant slug}"
REVENEXX_BASE_URL=${REVENEXX_BASE_URL%/}
DRY_RUN=${DRY_RUN:-0}

# sha256 of a file or of stdin: shasum on macOS, sha256sum on most Linux.
if command -v sha256sum >/dev/null 2>&1; then sha256() { sha256sum "$@" | cut -d' ' -f1; }
elif command -v shasum >/dev/null 2>&1; then sha256() { shasum -a 256 "$@" | cut -d' ' -f1; }
else printf 'need sha256sum or shasum\n' >&2; exit 1; fi

SEED_TMP=$(mktemp -d)
trap 'rc=$?; rm -rf "$SEED_TMP"; run_lock_release "$rc"' EXIT
mkdir -p "$SEED_TMP/cache" "$SEED_TMP/lists"
# Credentials reach curl through a file, never its command line (ps shows that).
(
  umask 077; : > "$SEED_TMP/auth"
  if [ -n "${REVENEXX_API_KEY:-}" ]; then printf 'X-Revenexx-Api-Key: %s\n' "$REVENEXX_API_KEY" >> "$SEED_TMP/auth"; fi
  if [ -n "${REVENEXX_TOKEN:-}" ]; then printf 'Authorization: Bearer %s\n' "$REVENEXX_TOKEN" >> "$SEED_TMP/auth"; fi
)

# ---- output -------------------------------------------------------------------

say()  { printf '%s\n' "$*"; }
ok()   { printf '  \342\234\223 %s\n' "$*"; ev_msg ok "$*"; }
warn() { printf '  ! %s\n' "$*" >&2; ev_msg warn "$*"; }
die()  { printf '  \342\234\227 %s\n' "$*" >&2; ev_msg error "$*"; exit 1; }

# ---- progress events (opt-in) -----------------------------------------------------
# With SEED_EVENTS=<file> every step start and finish, every few records of a
# step, every rate-limit wait and every result line is also written there as one
# JSON line, for the terminal UI in tui/. Unset, the run's lock (lib/lock.sh)
# picks .run/events-<time>.jsonl, so a run started from a script can be followed
# too. The normal output above is the same as ever.
SEED_EVENTS=${SEED_EVENTS:-}

ev() { # ev JSON
  [ -n "$SEED_EVENTS" ] || return 0
  printf '%s\n' "$1" >> "$SEED_EVENTS" 2>/dev/null || true
}

ev_msg() { # ev_msg KIND TEXT
  [ -n "$SEED_EVENTS" ] || return 0
  ev "$(jq -cn --arg ev "$1" --arg text "$2" '{ev: $ev, text: $text}')"
}

# ev_progress DONE TOTAL [EVERY]: one line per EVERY records (default 5) and at the end.
ev_progress() {
  [ -n "$SEED_EVENTS" ] || return 0
  [ $(($1 % ${3:-5})) = 0 ] || [ "$1" = "$2" ] || return 0
  ev "{\"ev\":\"progress\",\"done\":$1,\"total\":$2}"
}

# ev_scope ACTION DIR STEPS: a manifest starts ("base" or the pack's name).
ev_scope() {
  [ -n "$SEED_EVENTS" ] || return 0
  ev "$(jq -cn --arg action "$1" --arg scope "$(basename "$2")" --argjson steps "$3" '{ev: "scope", action: $action, scope: $scope, steps: $steps}')"
}

# ev_step start|end INDEX STEP_JSON: INDEX is the step's place in its manifest.
ev_step() {
  [ -n "$SEED_EVENTS" ] || return 0
  ev "$(jq -cn --arg ev "step_$1" --argjson i "$2" --argjson step "$3" '{ev: $ev, i: $i, name: $step.name, kind: ($step.kind // "upsert")}')"
}

# ---- HTTP ---------------------------------------------------------------------

# send CURL_ARGS...  ->  sets API_STATUS and API_BODY. A 429 (storage allows
# 60 uploads a minute per tenant) is retried after the wait the API asks for.
send() {
  local out tries=0 wait
  while :; do
    out=$(curl -D "$SEED_TMP/headers" "$@") || die "network error on $3 $4"
    API_STATUS=${out##*$'\n'}
    API_BODY=${out%$'\n'*}
    [ "$API_STATUS" = 429 ] && [ "$tries" -lt 10 ] || return 0
    wait=$(tr -d '\r' < "$SEED_TMP/headers" | awk -F': *' 'tolower($1) == "retry-after" { print $2 + 0 }' | tail -1)
    [ -n "$wait" ] && [ "$wait" -gt 0 ] || wait=5
    [ "$wait" -gt 60 ] && wait=60
    [ "$tries" = 0 ] && warn "rate limited, waiting ${wait}s"
    ev "{\"ev\":\"ratelimit\",\"wait\":$wait}"
    sleep "$wait"; tries=$((tries + 1))
  done
}

# api METHOD PATH [BODY_JSON]  ->  sets API_STATUS and API_BODY
api() {
  local method=$1 path=$2 body=${3:-}
  local args=(-sS -X "$method" "$REVENEXX_BASE_URL$path"
    -H "X-Revenexx-Tenant: $REVENEXX_TENANT" -H 'Accept: application/json'
    -H "@$SEED_TMP/auth" -w '\n%{http_code}')
  if [ -n "$body" ]; then
    printf '%s' "$body" > "$SEED_TMP/body.json"
    args+=(-H 'Content-Type: application/json' --data-binary "@$SEED_TMP/body.json")
  fi
  send "${args[@]}"
}

# The error message of the last response, for a one-line report.
api_error() {
  printf '%s' "$API_BODY" | jq -r '(.message // .error.message // .error // .) | tostring' 2>/dev/null | cut -c1-300
}

uri() { jq -rn --arg v "$1" '$v|@uri'; }

# ---- lookups --------------------------------------------------------------------

# cache_file ROUTE QUERY  ->  the lookup cache file for that key, named after the key
# itself (only "/" replaced), so no hashing process is started per record.
cache_file() { local k="$1?$2"; printf '%s/cache/%s' "$SEED_TMP" "${k//\//%2F}"; }

# lookup ROUTE QUERY  ->  prints the id of the single match, or nothing.
# QUERY is an exact-match query string such as "code=demo_de". Two matches
# stop the run: updating or deleting either one could hit the wrong record.
lookup() {
  local route=$1 query=$2
  local cache; cache=$(cache_file "$route" "$query")
  if [ -f "$cache" ]; then cat "$cache"; return; fi
  api GET "$route?$query&limit=2"
  [ "$API_STATUS" = 200 ] || die "lookup $route?$query answered $API_STATUS: $(api_error)"
  local id
  id=$(printf '%s' "$API_BODY" | jq -r '(.items // .data // .) | if length > 1 then "MANY" else (.[0].id // empty) end')
  [ "$id" = MANY ] && die "more than one record at $route matches $query: remove the duplicate first"
  if [ -n "$id" ]; then
    printf '%s' "$id" > "$cache"
    # the record itself, so an upsert can tell whether anything would change
    printf '%s' "$API_BODY" | jq -c '(.items // .data // .)[0]' > "$cache.rec"
  fi
  printf '%s' "$id"
}

# reset_lists: forget the lists read so far (records were created since).
reset_lists() { rm -rf "$SEED_TMP/lists"; mkdir -p "$SEED_TMP/lists"; }

# fetch_list ROUTE: read the whole list at ROUTE once (200 a page) into a file, one
# record per line, and set LIST_FILE to it. Returns 1 when it could not be read
# whole (or ROUTE has a {placeholder}). A list read earlier since the last
# reset_lists is reused.
fetch_list() {
  local route=$1 offset=0 more=true
  LIST_FILE="$SEED_TMP/lists/${route//\//%2F}"
  case "$route" in *"{"*|*"<"*) : > "$LIST_FILE"; return 1 ;; esac
  [ -f "$LIST_FILE.ok" ] && return 0
  [ -f "$LIST_FILE.fail" ] && return 1
  : > "$LIST_FILE"
  while [ "$more" = true ] && [ "$offset" -lt 20000 ]; do
    api GET "$route?limit=200&offset=$offset"
    [ "$API_STATUS" = 200 ] || { : > "$LIST_FILE.fail"; return 1; }
    printf '%s' "$API_BODY" | jq -c '(.items // .data // .)[]' >> "$LIST_FILE" 2>/dev/null || { : > "$LIST_FILE.fail"; return 1; }
    more=$(printf '%s' "$API_BODY" | jq -r '.page.hasMore // false')
    offset=$((offset + 200))
  done
  [ "$more" = true ] && { : > "$LIST_FILE.fail"; return 1; }
  : > "$LIST_FILE.ok"
}

# prefetch STEP_JSON ROUTE: read the list at ROUTE and fill the lookup cache with
# every record's id and body under its key, for the records that are looked up one
# by one. Keys that occur twice are left out (lookup then finds the duplicate and
# stops); keys not listed are still looked up one by one. Routes with a
# {placeholder} are skipped.
prefetch() {
  local step=$1 route=$2
  case "$route" in *"{"*|*"<"*) return 0 ;; esac
  fetch_list "$route" || true
  jq -rs --argjson step "$step" '
    ($step.key | if type == "array" then . else [.] end) as $keys
    | [.[] | . as $r | {q: ($keys | map(. as $k | "\($k)=\($r[$k] | tostring | @uri)") | join("&")), r: .}] as $rows
    | ($rows | group_by(.q) | map(select(length == 1) | .[0]))[]
    | "\(.q)\t\(.r.id)\t\(.r | tojson)"' "$LIST_FILE" 2>/dev/null |
  while IFS=$'\t' read -r q id rec; do
    [ -n "$id" ] && [ "$id" != null ] || continue
    local c; c=$(cache_file "$route" "$q")
    printf '%s' "$id" > "$c"; printf '%s' "$rec" > "$c.rec"
  done
}

# unchanged ROUTE QUERY BODY  ->  true when the record lookup found already holds
# every field of BODY with the same value. Numbers sent as text count as equal
# ("18" = 18), key order does not matter, fields the API adds are ignored.
# Without a stored record (just created, or not looked up) it is false.
unchanged() {
  local rec; rec="$(cache_file "$1" "$2").rec"
  [ -s "$rec" ] || return 1
  jq -en --slurpfile have "$rec" --argjson want "$3" '
    def norm: if type == "string" and test("^-?[0-9]+(\\.[0-9]+)?$") then tonumber else . end;
    def same($a; $b):
      if ($b | type) == "object" then
        ($a | type) == "object" and all($b | keys[]; . as $k | same($a[$k]; $b[$k]))
      elif ($b | type) == "array" then
        ($a | type) == "array" and ($a | length) == ($b | length)
        and all(range(0; $b | length); . as $i | same($a[$i]; $b[$i]))
      else ($a | norm) == ($b | norm) end;
    same($have[0]; $want)' >/dev/null 2>&1
}

remember() { # remember ROUTE QUERY ID
  printf '%s' "$3" > "$(cache_file "$1" "$2")"
}

forget() { # forget ROUTE QUERY (the id and the stored record)
  local c; c=$(cache_file "$1" "$2")
  rm -f "$c" "$c.rec"
}

# key_query STEP_JSON RECORD_JSON  ->  "code=demo_de" (or "a=1&b=2" for composite keys)
key_query() {
  jq -rn --argjson step "$1" --argjson rec "$2" '
    ($step.key | if type == "array" then . else [.] end)
    | map(. as $k | "\($k)=\($rec[$k] | tostring | @uri)") | join("&")'
}

# ---- references -------------------------------------------------------------------

# resolve_refs STEP_JSON RECORD_JSON  ->  prints "ROUTE<TAB>RECORD" with every
# reference replaced by an id. A step declares its references as
#   "refs": { "<target>": { "field": "<field in record>", "route": "...", "key": "code", "in": "body"|"path" } }
# "path" targets replace {target} in the step's route and leave the body.
# "where" adds fixed fields to the lookup, e.g. {"entity_type": "product"}.
# It always runs in $(...), where set -e is off: a failed lookup must return.
resolve_refs() {
  local step=$1 rec=$2
  local route
  route=$(jq -r '.route' <<<"$step")
  local targets target spec field value refroute refkey place where id
  targets=$(jq -r '.refs // {} | keys[]' <<<"$step")
  for target in $targets; do
    spec=$(jq -c --arg t "$target" '.refs[$t]' <<<"$step")
    field=$(jq -r '.field' <<<"$spec")
    refroute=$(jq -r '.route' <<<"$spec")
    refkey=$(jq -r '.key // "code"' <<<"$spec")
    place=$(jq -r '.in // "body"' <<<"$spec")
    where=$(jq -r '.where // {} | to_entries | map("&\(.key)=\(.value | tostring | @uri)") | join("")' <<<"$spec")
    value=$(jq -r --arg f "$field" '.[$f] // empty' <<<"$rec")
    rec=$(jq -c --arg f "$field" 'del(.[$f])' <<<"$rec")
    [ -z "$value" ] && continue
    # A reference route can itself depend on an earlier path target.
    refroute=$(substitute_path "$refroute" "$rec")
    id=$(lookup "$refroute" "$refkey=$(uri "$value")$where") || return 1
    if [ -z "$id" ]; then
      [ "$DRY_RUN" = 1 ] && id="<$field:$value>" || die "$field '$value' not found at $refroute"
    fi
    if [ "$place" = path ]; then
      route=${route//\{$target\}/$id}
      rec=$(jq -c --arg t "$target" --arg id "$id" '. + {("__path_" + $t): $id}' <<<"$rec")
    else
      rec=$(jq -c --arg t "$target" --arg id "$id" '.[$t] = $id' <<<"$rec")
    fi
  done
  printf '%s\t%s' "$route" "$(jq -c 'with_entries(select(.key | startswith("__path_") | not))' <<<"$rec")"
}

# Replace {name} in a route with the value of __path_name from the record.
substitute_path() {
  local route=$1 rec=$2 name value
  for name in $(printf '%s' "$route" | grep -oE '\{[a-z_]+\}' | tr -d '{}'); do
    value=$(jq -r --arg n "__path_$name" '.[$n] // empty' <<<"$rec")
    [ -n "$value" ] && route=${route//\{$name\}/$value}
  done
  printf '%s' "$route"
}

# ---- the plain upsert step ------------------------------------------------------

# classify_upsert STEP FILE ONLY: write the decision for every record of FILE (or
# only the indexes in ONLY, a JSON array, when not "null") to stdout, one jq run
# for the step (lib/upsert.jq). References are resolved from the lists of the
# referenced routes, not one request per record.
classify_upsert() {
  local step=$1 file=$2 only=$3 own_ok=false names='{}' oks='{}' route r n=0 ok
  local args=()
  route=$(jq -r '.route' <<<"$step")
  fetch_list "$route" && own_ok=true
  local own=$LIST_FILE
  for r in $(jq -r '[.refs // {} | .[] | .route] | unique[]' <<<"$step"); do
    ok=false; fetch_list "$r" && ok=true
    names=$(jq -c --arg r "$r" --arg n "L$n" '. + {($r): $n}' <<<"$names")
    oks=$(jq -c --arg r "$r" --argjson ok "$ok" '. + {($r): $ok}' <<<"$oks")
    args+=(--slurpfile "L$n" "$LIST_FILE")
    n=$((n + 1))
  done
  jq -nr --argjson step "$step" --slurpfile recs "$file" --argjson only "$only" \
    --slurpfile own "$own" --argjson own_ok "$own_ok" --argjson names "$names" --argjson oks "$oks" \
    ${args[@]+"${args[@]}"} -f "$SEED_LIB/upsert.jq"
}

# upsert_one STEP FILE INDEX: one record on its own, with lookups by request (the
# way for what classify_upsert could not decide). Counts into the caller's
# created/updated/same; name, mode, wl and cl are the caller's too.
upsert_one() {
  local step=$1 file=$2 i=$3 rec resolved route body query id
  rec=$(jq -c ".[$i]" "$file")
  resolved=$(resolve_refs "$step" "$rec")
  route=${resolved%%$'\t'*}
  body=${resolved#*$'\t'}
  query=$(key_query "$step" "$body")
  # In a dry run a parent that does not exist yet leaves a placeholder in
  # the route; its children are all new.
  case "$DRY_RUN$route$body" in 1*"<"*) id="" ;; *) id=$(lookup "$route" "$query") ;; esac
  if [ "$DRY_RUN" = 1 ]; then
    if [ -z "$id" ]; then created=$((created + 1))
    elif [ "$mode" = ensure ] || unchanged "$route" "$query" "$body"; then same=$((same + 1))
    else updated=$((updated + 1)); fi
    return 0
  fi
  if [ -n "$id" ] && [ "$mode" = ensure ]; then
    same=$((same + 1))
  elif [ -n "$id" ] && unchanged "$route" "$query" "$body"; then
    same=$((same + 1))
  elif [ -n "$id" ]; then
    api PUT "$route/$id" "$body"
    [ "$API_STATUS" = 200 ] || die "$name: $wl $query answered $API_STATUS: $(api_error)"
    updated=$((updated + 1))
  else
    api POST "$route" "$body"
    case "$API_STATUS" in
      200|201) ;;
      409) die "$name: $query exists but is not listed (in the trash?): $(api_error)" ;;
      *) die "$name: $cl $query answered $API_STATUS: $(api_error)" ;;
    esac
    id=$(printf '%s' "$API_BODY" | jq -r '(.data // .).id // empty')
    [ -n "$id" ] && remember "$route" "$query" "$id"
    created=$((created + 1))
  fi
}

# apply_upsert STEP FILE WRITE_LABEL CREATE_LABEL: upsert every record of FILE.
# One jq run decides all of them from the lists read up front; only records that
# change cost a request. Records that need an id created in this very step (a
# variant and its parent) are decided again after the first round, and what
# still cannot be decided from the lists (a key listed twice, a reference not
# listed) goes through upsert_one. Counts into the caller's created/updated/same.
apply_upsert() {
  local step=$1 file=$2 wl=$3 cl=$4
  local route count only=null round=0 i st id query body made slow
  route=$(jq -r '.route' <<<"$step")
  count=$(jq 'length' "$file")
  reset_lists
  prefetch "$step" "$route"
  # A route or reference with a {placeholder} is resolved per record.
  if jq -e '(.route | test("[{<]")) or ([.refs // {} | .[] | select((.in // "body") == "path" or (.route | test("[{<]")))] | length > 0)' <<<"$step" >/dev/null; then
    for ((i = 0; i < count; i++)); do
      ev_progress "$i" "$count"
      upsert_one "$step" "$file" "$i"
    done
    return
  fi
  while :; do
    classify_upsert "$step" "$file" "$only" > "$SEED_TMP/plan.txt" || die "$name: could not plan the records"
    made=0; slow=""
    while IFS=$'\037' read -r i st id query body; do
      [ -n "$i" ] || continue
      ev_progress "$i" "$count"
      case "$st" in
        S) same=$((same + 1)) ;;
        L) slow="$slow${slow:+,}$i" ;;
        U)
          if [ "$DRY_RUN" = 1 ]; then updated=$((updated + 1)); continue; fi
          api PUT "$route/$id" "$body"
          [ "$API_STATUS" = 200 ] || die "$name: $wl $query answered $API_STATUS: $(api_error)"
          updated=$((updated + 1)) ;;
        C)
          if [ "$DRY_RUN" = 1 ]; then created=$((created + 1)); continue; fi
          api POST "$route" "$body"
          case "$API_STATUS" in
            200|201) ;;
            # listed under another view, or in the trash: the one-by-one path knows which
            409) upsert_one "$step" "$file" "$i"; continue ;;
            *) die "$name: $cl $query answered $API_STATUS: $(api_error)" ;;
          esac
          id=$(printf '%s' "$API_BODY" | jq -r '(.data // .).id // empty')
          [ -n "$id" ] && remember "$route" "$query" "$id"
          created=$((created + 1)); made=1 ;;
      esac
    done < "$SEED_TMP/plan.txt"
    [ -n "$slow" ] || break
    if [ "$made" = 1 ] && [ "$round" -lt 3 ]; then
      only="[$slow]"; round=$((round + 1)); reset_lists
      continue
    fi
    for i in ${slow//,/ }; do upsert_one "$step" "$file" "$i"; done
    break
  done
}

# run_upsert STEP_JSON DIR
run_upsert() {
  local step=$1 dir=$2
  local name file created=0 updated=0 same=0 mode
  name=$(jq -r '.name' <<<"$step")
  # "ensure": create when missing, never touch an existing record. For generic
  # codes (name, description, asset families) a tenant may already have.
  mode=$(jq -r '.mode // "upsert"' <<<"$step")
  file="$dir/$(jq -r '.file' <<<"$step")"
  apply_upsert "$step" "$file" update create
  if [ "$mode" = ensure ]; then
    ok "$(printf '%-22s %s created, %s already there' "$name" "$created" "$same")"
  else
    ok "$(printf '%-22s %s created, %s updated, %s unchanged' "$name" "$created" "$updated" "$same")"
  fi
}

# ---- replaced sets ----------------------------------------------------------------------

# run_replace STEP_JSON DIR: one PUT per record that replaces a whole set under
# its parent (e.g. a shipping method's rate tiers), so a re-run writes the same
# set again and never adds to it.
run_replace() {
  local step=$1 dir=$2 name file count i rec resolved route body n=0
  name=$(jq -r '.name' <<<"$step")
  file="$dir/$(jq -r '.file' <<<"$step")"
  count=$(jq 'length' "$file")
  for ((i = 0; i < count; i++)); do
    ev_progress "$i" "$count"
    rec=$(jq -c ".[$i]" "$file")
    resolved=$(resolve_refs "$step" "$rec")
    route=${resolved%%$'\t'*}
    body=${resolved#*$'\t'}
    if [ "$DRY_RUN" != 1 ]; then
      api PUT "$route" "$body"
      [ "$API_STATUS" = 200 ] || die "$name: replacing $route answered $API_STATUS: $(api_error)"
    fi
    n=$((n + 1))
  done
  ok "$(printf '%-22s %s sets replaced' "$name" "$n")"
}

# ---- price entries ----------------------------------------------------------------------

# run_price_entries STEP_JSON DIR: the file holds one object per price list,
# {"list": "<code>", "entries": [...]}; the bulk route upserts by
# sku + quantity_min, which is what makes a re-run safe here.
run_price_entries() {
  local step=$1 dir=$2 file count i list id n=0
  file="$dir/$(jq -r '.file' <<<"$step")"
  count=$(jq 'length' "$file")
  for ((i = 0; i < count; i++)); do
    ev_progress "$i" "$count" 1
    list=$(jq -r ".[$i].list" "$file")
    id=$(lookup /prices/lists "code=$(uri "$list")")
    [ -z "$id" ] && { [ "$DRY_RUN" = 1 ] || die "price list '$list' not found"; }
    if [ "$DRY_RUN" != 1 ]; then
      api POST "/prices/lists/$id/entries/bulk" "$(jq -c --argjson i "$i" '.[$i] | {mode: "upsert", entries: .entries}' "$file")"
      case "$API_STATUS" in 200|201) ;; *) die "price entries for $list answered $API_STATUS: $(api_error)" ;; esac
    fi
    n=$((n + $(jq ".[$i].entries | length" "$file")))
  done
  ok "$(printf '%-22s %s entries upserted' "$(jq -r '.name' <<<"$step")" "$n")"
}

# ---- stock ---------------------------------------------------------------------------------

# stock_one STEP FILE INDEX: one record on its own (locations and rows looked up
# by request). Counts into the caller's moved/same.
stock_one() {
  local file=$2 i=$3 rec sku loc target locid row rowid current delta extra
  rec=$(jq -c ".[$i]" "$file")
  sku=$(jq -r '.sku' <<<"$rec"); loc=$(jq -r '.location' <<<"$rec"); target=$(jq -r '.on_hand' <<<"$rec")
  locid=$(lookup /inventories/locations "code=$(uri "$loc")")
  [ -z "$locid" ] && { [ "$DRY_RUN" = 1 ] || die "stock location '$loc' not found"; }
  current=0; rowid=""
  if [ -n "$locid" ]; then
    api GET "/inventories/stock?sku=$(uri "$sku")&location_id=$locid&limit=1"
    [ "$API_STATUS" = 200 ] || die "stock lookup $sku answered $API_STATUS: $(api_error)"
    row=$(printf '%s' "$API_BODY" | jq -c '(.items // .data // .)[0] // empty')
    [ -n "$row" ] && { current=$(jq -r '.on_hand // 0' <<<"$row"); rowid=$(jq -r '.id' <<<"$row"); }
  fi
  delta=$(jq -n --argjson t "$target" --argjson c "$current" '$t - $c')
  if [ "$delta" = 0 ]; then same=$((same + 1)); else moved=$((moved + 1)); fi
  [ "$DRY_RUN" = 1 ] && return 0
  stock_write "$rec" "$sku" "$loc" "$locid" "$rowid" "$delta" 1
}

# stock_write REC SKU LOC LOCID ROWID DELTA PUT: book the delta, then write the
# plain fields (PUT 1 = they differ or there is no row yet).
stock_write() {
  local rec=$1 sku=$2 loc=$3 locid=$4 rowid=$5 delta=$6 put=$7 extra
  if [ "$delta" != 0 ]; then
    api POST /inventories/adjust "$(jq -cn --arg l "$loc" --arg s "$sku" --argjson q "$delta" '{location_code: $l, reason: "sample data", items: [{sku: $s, quantity: $q}]}')"
    case "$API_STATUS" in 200|201) ;; *) die "stock $sku answered $API_STATUS: $(api_error)" ;; esac
  fi
  # Everything except the quantity (reorder point, availability) is a plain field.
  extra=$(jq -c 'del(.sku, .location, .on_hand)' <<<"$rec")
  if [ "$extra" != '{}' ] && [ "$put" = 1 ]; then
    [ -z "$rowid" ] && rowid=$(lookup /inventories/stock "sku=$(uri "$sku")&location_id=$locid")
    if [ -n "$rowid" ]; then
      api PUT "/inventories/stock/$rowid" "$extra"
      [ "$API_STATUS" = 200 ] || die "stock $sku fields answered $API_STATUS: $(api_error)"
    else
      # A target of 0 moves nothing, so no stock row exists yet: create it.
      api POST /inventories/stock "$(jq -c --arg s "$sku" --arg l "$locid" '{sku: $s, location_id: $l, on_hand: 0} + .' <<<"$extra")"
      case "$API_STATUS" in 200|201) ;; *) die "stock $sku answered $API_STATUS: $(api_error)" ;; esac
    fi
  fi
}

# run_stock STEP_JSON DIR: bring each SKU's on-hand at a location to a target.
# Stock moves by delta (receive/adjust add), so the step reads what is there
# and books only the difference; a re-run books nothing. The locations and the
# stock rows are read as two lists and one jq run (lib/stock.jq) decides every
# record; only records that differ cost a request.
run_stock() {
  local step=$1 dir=$2 file count i st locid rowid delta put rec locs_ok=false stock_ok=false slow=""
  local moved=0 same=0
  file="$dir/$(jq -r '.file' <<<"$step")"
  count=$(jq 'length' "$file")
  reset_lists
  fetch_list /inventories/locations && locs_ok=true
  local locs=$LIST_FILE
  fetch_list /inventories/stock && stock_ok=true
  jq -nr --slurpfile recs "$file" --slurpfile locs "$locs" --slurpfile stock "$LIST_FILE" \
    --argjson locs_ok "$locs_ok" --argjson stock_ok "$stock_ok" -f "$SEED_LIB/stock.jq" > "$SEED_TMP/plan.txt" \
    || die "stock: could not plan the records"
  while IFS=$'\037' read -r i st locid rowid delta put; do
    [ -n "$i" ] || continue
    ev_progress "$i" "$count"
    if [ "$st" = L ]; then slow="$slow $i"; continue; fi
    if [ "$delta" = 0 ]; then same=$((same + 1)); else moved=$((moved + 1)); fi
    [ "$DRY_RUN" = 1 ] && continue
    if [ "$delta" != 0 ] || [ "$put" = 1 ]; then
      rec=$(jq -c ".[$i]" "$file")
      stock_write "$rec" "$(jq -r '.sku' <<<"$rec")" "$(jq -r '.location' <<<"$rec")" "$locid" "$rowid" "$delta" "$put"
    fi
  done < "$SEED_TMP/plan.txt"
  for i in $slow; do stock_one "$step" "$file" "$i"; done
  ok "$(printf '%-22s %s adjusted, %s already at target' "$(jq -r '.name' <<<"$step")" "$moved" "$same")"
}

# ---- files in storage ---------------------------------------------------------------------

# storage_folder PATH  ->  id of the storage folder at PATH ("a/b"), created when missing.
storage_folder() {
  local path=$1 parent="" sofar="" segment id
  api GET /storage/folders
  [ "$API_STATUS" = 200 ] || die "storage folders answered $API_STATUS: $(api_error)"
  local folders=$API_BODY
  for segment in $(printf '%s' "$path" | tr '/' ' '); do
    sofar=${sofar:+$sofar/}$segment
    id=$(printf '%s' "$folders" | jq -r --arg p "$sofar" '(.data // .)[] | select(.path == ("/" + $p + "/")) | .id' | head -1)
    if [ -z "$id" ]; then
      api POST /storage/folders "$(jq -cn --arg n "$segment" --arg p "$parent" '{name: $n} + (if $p == "" then {} else {parent_id: $p} end)')"
      case "$API_STATUS" in 200|201) ;; *) die "creating storage folder $sofar answered $API_STATUS: $(api_error)" ;; esac
      id=$(printf '%s' "$API_BODY" | jq -r '(.data // .).id')
    fi
    parent=$id
  done
  printf '%s' "$parent"
}

# folder_assets FOLDER_ID  ->  sets API_STATUS, and API_BODY to every file in
# the folder as {"data": [...]}. Storage pages at most 200 files at a time, so a
# folder that holds more is read page by page, sorted by name: the default
# sort (upload time) ties within a batch, and pages would overlap.
folder_assets() {
  local folder=$1 page=1 last all='[]'
  while :; do
    api GET "/storage/assets?filter%5Bfolder_id%5D=$folder&limit=200&sort=original_name&page=$page"
    [ "$API_STATUS" = 200 ] || return 0
    all=$(jq -c --argjson a "$all" '$a + (.data // .)' <<<"$API_BODY")
    last=$(jq -r '.meta.last_page // 1' <<<"$API_BODY")
    [ "$page" -ge "$last" ] && break
    page=$((page + 1))
  done
  API_BODY=$(jq -c '{data: unique_by(.id)}' <<<"$all")
}

# upload FILE FOLDER_ID TAGS_JSON  ->  sets API_STATUS / API_BODY
upload() {
  local file=$1 folder=$2 tags=$3 tag
  local args=(-sS -X POST "$REVENEXX_BASE_URL/storage/assets"
    -H "X-Revenexx-Tenant: $REVENEXX_TENANT" -H 'Accept: application/json' -H "@$SEED_TMP/auth" -w '\n%{http_code}'
    -F "file=@$file" -F "folder_id=$folder")
  for tag in $(jq -r '.[]' <<<"$tags"); do args+=(-F "tags[]=$tag"); done
  send "${args[@]}"
}

# run_files STEP_JSON DIR: upload each file to the pack's storage folder
# (skipped when a file of that name and content is already there, replaced when
# its content changed), then upsert the product asset that points at it.
run_files() {
  local step=$1 dir=$2
  local name file count i rec path base hash folder tags existing sid ohash uploaded=0 kept=0 created=0 updated=0 same=0 mode=upsert
  name=$(jq -r '.name' <<<"$step")
  file="$dir/$(jq -r '.file' <<<"$step")"
  tags=$(jq -c '.tags // []' <<<"$step")
  count=$(jq 'length' "$file")
  if [ "$DRY_RUN" = 1 ]; then
    ok "$(printf '%-22s %s files (dry run: no upload)' "$name" "$count")"
    return
  fi
  folder=$(storage_folder "$(jq -r '.folder' <<<"$step")")
  folder_assets "$folder"
  [ "$API_STATUS" = 200 ] || die "listing storage folder answered $API_STATUS: $(api_error)"
  existing=$API_BODY
  # One pass for the whole step: every file's checksum (one process) and what
  # storage already holds under its name, instead of several processes per file.
  local rel plan hashes
  while IFS= read -r rel; do [ -f "$dir/$rel" ] || die "$name: missing file $dir/$rel"; done < <(jq -r '.[].file' "$file")
  hashes=$(jq -r '.[].file' "$file" | (cd "$dir" && tr '\n' '\0' | xargs -0 sh -c 'if command -v sha256sum >/dev/null 2>&1; then sha256sum "$@"; else shasum -a 256 "$@"; fi' sh))
  printf '%s' "$existing" > "$SEED_TMP/existing.json"
  printf '%s' "$hashes" > "$SEED_TMP/hashes.txt"
  plan=$(jq -rn --slurpfile recs "$file" --slurpfile exs "$SEED_TMP/existing.json" --rawfile hs "$SEED_TMP/hashes.txt" '
    ($hs | split("\n") | map(select(length > 0) | capture("^(?<h>[0-9a-f]+) [ *]?(?<p>.*)$") | {(.p): .h}) | add // {}) as $H
    | $exs[0] as $ex
    | (reduce ($ex.data // $ex)[] as $a ({}; if has($a.original_name) then . else . + {($a.original_name): {id: $a.id, h: ($a.content_hash // "")}} end)) as $E
    | $recs[0] | to_entries[] | .value.file as $p | ($p | split("/") | last) as $b
    | [.key, $p, $b, ($H[$p] // ""), ($E[$b].id // ""), ($E[$b].h // "")] | @tsv')
  : > "$SEED_TMP/sids.tsv"
  while IFS=$'\t' read -r i path base hash sid ohash; do
    ev_progress "$i" "$count" 1
    path="$dir/$path"
    if [ -n "$sid" ] && [ "$ohash" = "$hash" ]; then
      kept=$((kept + 1))
    else
      if [ -n "$sid" ]; then
        api DELETE "/storage/assets/$sid"
        case "$API_STATUS" in 200|202|204|404) ;; *) die "$name: replacing $base: delete answered $API_STATUS: $(api_error)" ;; esac
        api DELETE "/storage/assets/$sid/permanent"
      fi
      upload "$path" "$folder" "$tags"
      case "$API_STATUS" in 200|201) ;; *) die "$name: uploading $base answered $API_STATUS: $(api_error)" ;; esac
      sid=$(printf '%s' "$API_BODY" | jq -r '(.data // .).id')
      uploaded=$((uploaded + 1))
    fi
    printf '%s\t%s\n' "$i" "$sid" >> "$SEED_TMP/sids.tsv"
  done <<<"$plan"
  # The product assets: the catalogue's record of each file, keyed by family + code.
  jq -c --rawfile s "$SEED_TMP/sids.tsv" '
    ($s | split("\n") | map(select(length > 0) | split("\t") | {(.[0]): .[1]}) | add // {}) as $S
    | to_entries | map(.key as $i | .value | del(.file) + {source: "storage", storage_asset_id: $S[($i | tostring)]})' "$file" > "$SEED_TMP/assets.json"
  apply_upsert "$step" "$SEED_TMP/assets.json" asset asset
  ok "$(printf '%-22s %s uploaded, %s unchanged; %s assets created, %s updated, %s unchanged' "$name" "$uploaded" "$kept" "$created" "$updated" "$same")"
}

# ---- children without a key ------------------------------------------------------------

# run_children STEP_JSON DIR: records that have no natural key of their own
# (promotion effects and conditions). They are created only for a parent that
# has none yet, so a re-run neither duplicates nor overwrites what a user
# changed. The step names the parent reference in "parent", e.g. "promotion_id".
run_children() {
  local step=$1 dir=$2
  local name file parent field count i rec resolved route body pid have want created=0 skipped=0 seen=""
  name=$(jq -r '.name' <<<"$step")
  file="$dir/$(jq -r '.file' <<<"$step")"
  parent=$(jq -r '.parent' <<<"$step")
  field=$(jq -r --arg p "$parent" '.refs[$p].field' <<<"$step")
  count=$(jq 'length' "$file")
  for ((i = 0; i < count; i++)); do
    ev_progress "$i" "$count"
    rec=$(jq -c ".[$i]" "$file")
    resolved=$(resolve_refs "$step" "$rec")
    route=${resolved%%$'\t'*}
    body=${resolved#*$'\t'}
    pid=$(jq -r --arg p "$parent" '.[$p]' <<<"$body")
    # Decide once per parent, before its first child is written.
    case " $seen " in
      *" $pid=new "*) ;;
      *" $pid=has "*) skipped=$((skipped + 1)); continue ;;
      *)
        if case "$pid" in "<"*) true ;; *) false ;; esac; then
          seen="$seen $pid=new"
        else
          api GET "$route?$parent=$(uri "$pid")&limit=100"
          [ "$API_STATUS" = 200 ] || die "$name: listing for $field answered $API_STATUS: $(api_error)"
          have=$(printf '%s' "$API_BODY" | jq '(.items // .data // .) | length')
          if [ "$have" -gt 0 ]; then
            want=$(jq --arg f "$field" --argjson r "$rec" '[.[] | select(.[$f] == $r[$f])] | length' "$file")
            [ "$have" -lt "$want" ] && warn "$name: $(jq -r --arg f "$field" '.[$f]' <<<"$rec") has $have of $want; kept as is (delete them to have all $want created again)"
            seen="$seen $pid=has"; skipped=$((skipped + 1)); continue
          fi
          seen="$seen $pid=new"
        fi ;;
    esac
    if [ "$DRY_RUN" != 1 ]; then
      api POST "$route" "$body"
      case "$API_STATUS" in 200|201) ;; *) die "$name: create answered $API_STATUS: $(api_error)" ;; esac
    fi
    created=$((created + 1))
  done
  ok "$(printf '%-22s %s created, %s kept' "$name" "$created" "$skipped")"
}

# ---- tenant defaults ------------------------------------------------------------------

# run_defaults STEP_JSON DIR: POST each idempotent /…/defaults route once.
run_defaults() {
  local step=$1 dir=$2 file route n=0
  file="$dir/$(jq -r '.file' <<<"$step")"
  for route in $(jq -r '.[]' "$file"); do
    if [ "$DRY_RUN" != 1 ]; then
      api POST "$route" '{}'
      case "$API_STATUS" in 200|201) ;; *) die "defaults: $route answered $API_STATUS: $(api_error)" ;; esac
    fi
    n=$((n + 1))
  done
  ok "$(printf '%-22s %s routes called' "$(jq -r '.name' <<<"$step")" "$n")"
}

# ---- manifests ---------------------------------------------------------------------------

# run_manifest FILE: run every step of one manifest in order.
run_manifest() {
  local manifest=$1 dir count i step kind
  dir=$(dirname "$manifest")
  count=$(jq '.steps | length' "$manifest")
  ev_scope seed "$dir" "$count"
  for ((i = 0; i < count; i++)); do
    step=$(jq -c ".steps[$i]" "$manifest")
    kind=$(jq -r '.kind // "upsert"' <<<"$step")
    ev_step start "$i" "$step"
    case "$kind" in
      upsert) run_upsert "$step" "$dir" ;;
      defaults) run_defaults "$step" "$dir" ;;
      children) run_children "$step" "$dir" ;;
      price_entries) run_price_entries "$step" "$dir" ;;
      replace) run_replace "$step" "$dir" ;;
      stock) run_stock "$step" "$dir" ;;
      files) run_files "$step" "$dir" ;;
      *) die "unknown step kind '$kind' in $manifest" ;;
    esac
    ev_step end "$i" "$step"
  done
}

# base_complete: every record of base/ (market, company with contacts and
# addresses, promotions with voucher batches and vouchers, shipping method) is
# in the tenant, found by its key. Read-only.
base_complete() {
  local spec route key file v
  for spec in "/markets|code|markets.json" \
    "/customers/organizations|customer_number|organizations.json" \
    "/customers/contacts|external_id|contacts.json" \
    "/customers/addresses|external_id|addresses.json" \
    "/promotions/promotions|code|promotions.json" \
    "/promotions/batches|request_ref|voucher-batches.json" \
    "/promotions/vouchers|code|vouchers.json" \
    "/shipping/methods|code|shipping-methods.json"; do
    IFS='|' read -r route key file <<<"$spec"
    while IFS= read -r v; do
      api GET "$route?$key=$(jq -rn --arg v "$v" '$v | @uri')&limit=1"
      [ "$API_STATUS" = 200 ] || return 1
      printf '%s' "$API_BODY" | jq -e '(.items // .data // []) | length > 0' >/dev/null || return 1
    done < <(jq -r --arg k "$key" '.[] | .[$k]' "base/$file")
  done
}

# ---- removal ---------------------------------------------------------------------------------

# delete_for_good ROUTE ID: DELETE, then DELETE again for apps that keep a
# trash, so the code is free for a later seed. A 404 on the second call means
# the app has no trash and the first call was final.
delete_for_good() {
  api DELETE "$1/$2"
  case "$API_STATUS" in 200|202|204|404) ;; 409) return 2 ;; *) failed "delete $1/$2 answered $API_STATUS: $(api_error)"; return 1 ;; esac
  api DELETE "$1/$2"
  case "$API_STATUS" in
    200|202|204|404|410) ;;
    409)
      # Still referenced (a company with open orders): it may not leave the
      # trash for good. Bring it back so the caller can deactivate it instead,
      # and a later seed finds it under its code.
      api POST "$1/$2/restore" '{}'
      case "$API_STATUS" in 200|201|204) ;; *) failed "restoring $1/$2 from the trash answered $API_STATUS: $(api_error)" ;; esac
      forget_all
      return 2 ;;
    *) failed "emptying the trash for $1/$2 answered $API_STATUS: $(api_error)"; forget_all; return 1 ;;
  esac
  forget_all
  return 0
}

# Removals that failed; remove.sh exits non-zero when there are any.
REMOVE_FAILED=0
failed() { warn "$*"; REMOVE_FAILED=$((REMOVE_FAILED + 1)); }

# Lookups are cached per run; after a delete the cache may point at a gone id.
forget_all() { rm -f "$SEED_TMP/cache/"*; }

# remove_upsert STEP_JSON DIR: delete every record of the step, last first.
remove_upsert() {
  local step=$1 dir=$2 name file count i rec resolved route body query id n=0 gone=0 off=0 in_use rc
  name=$(jq -r '.name' <<<"$step")
  file="$dir/$(jq -r '.file' <<<"$step")"
  # What to write instead when the app refuses the delete because the record is
  # in use (a redeemed voucher, a company with orders): history keeps it.
  in_use=$(jq -c '.if_in_use // empty' <<<"$step")
  count=$(jq 'length' "$file")
  for ((i = count - 1; i >= 0; i--)); do
    ev_progress "$((count - 1 - i))" "$count"
    rec=$(jq -c ".[$i]" "$file")
    resolved=$(DRY_RUN=1 resolve_refs "$step" "$rec")
    route=${resolved%%$'\t'*}
    body=${resolved#*$'\t'}
    case "$route$body" in *"<"*) gone=$((gone + 1)); continue ;; esac
    query=$(key_query "$step" "$body")
    id=$(lookup "$route" "$query")
    if [ -z "$id" ]; then gone=$((gone + 1)); continue; fi
    if [ "$DRY_RUN" = 1 ]; then n=$((n + 1)); continue; fi
    rc=0; delete_for_good "$route" "$id" || rc=$?
    if [ "$rc" = 0 ]; then n=$((n + 1))
    elif [ "$rc" = 2 ] && [ -n "$in_use" ]; then
      api PUT "$route/$id" "$in_use"
      [ "$API_STATUS" = 200 ] && off=$((off + 1)) || failed "$name: $query is in use and could not be deactivated ($API_STATUS: $(api_error))"
    elif [ "$rc" = 2 ]; then failed "$name: $query is still in use: $(api_error)"
    fi
  done
  if [ "$off" -gt 0 ]; then
    ok "$(printf '%-22s %s removed, %s kept but deactivated (in use), %s not there' "$name" "$n" "$off" "$gone")"
  else
    ok "$(printf '%-22s %s removed, %s not there' "$name" "$n" "$gone")"
  fi
}

# remove_files STEP_JSON DIR: the product assets, then the files in storage.
remove_files() {
  local step=$1 dir=$2 folder
  remove_upsert "$step" "$dir"
  [ "$DRY_RUN" = 1 ] && return
  local path=$(jq -r '.folder' <<<"$step") id sid n=0
  api GET /storage/folders
  [ "$API_STATUS" = 200 ] || { failed "storage folders answered $API_STATUS: $(api_error)"; return; }
  folder=$(printf '%s' "$API_BODY" | jq -r --arg p "/$path/" '(.data // .)[] | select(.path == $p) | .id' | head -1)
  [ -z "$folder" ] && return
  folder_assets "$folder"
  [ "$API_STATUS" = 200 ] || { failed "listing storage folder $path answered $API_STATUS: $(api_error)"; return; }
  for sid in $(printf '%s' "$API_BODY" | jq -r '(.data // .)[].id'); do
    api DELETE "/storage/assets/$sid"
    case "$API_STATUS" in 200|202|204|404) ;; *) failed "deleting file $sid answered $API_STATUS: $(api_error)"; continue ;; esac
    api DELETE "/storage/assets/$sid/permanent"; n=$((n + 1))
  done
  api DELETE "/storage/folders/$folder"
  case "$API_STATUS" in 200|202|204|404) ;; *) failed "deleting storage folder $path answered $API_STATUS: $(api_error)" ;; esac
  # The parent ("sample-data") goes with the last pack: storage refuses to
  # delete a folder that still holds anything, so a 409 means other packs remain.
  local parent=${path%/*}
  if [ "$parent" != "$path" ]; then
    api GET /storage/folders
    folder=$(printf '%s' "$API_BODY" | jq -r --arg p "/$parent/" '(.items // .data // .)[] | select(.path == $p) | .id' | head -1)
    if [ -n "$folder" ]; then
      api DELETE "/storage/folders/$folder"
      case "$API_STATUS" in 200|202|204|404|409) ;; *) failed "deleting storage folder $parent answered $API_STATUS: $(api_error)" ;; esac
    fi
  fi
  if [ "$n" -gt 0 ]; then ok "$(printf '%-22s %s files left in storage deleted' "" "$n")"; fi
}

# remove_stock STEP_JSON DIR: book each SKU back to zero, then drop its row.
remove_stock() {
  local step=$1 dir=$2 file count i rec sku loc locid row rowid current n=0
  file="$dir/$(jq -r '.file' <<<"$step")"
  count=$(jq 'length' "$file")
  for ((i = 0; i < count; i++)); do
    ev_progress "$i" "$count"
    rec=$(jq -c ".[$i]" "$file"); sku=$(jq -r '.sku' <<<"$rec"); loc=$(jq -r '.location' <<<"$rec")
    locid=$(lookup /inventories/locations "code=$(uri "$loc")"); [ -z "$locid" ] && continue
    api GET "/inventories/stock?sku=$(uri "$sku")&location_id=$locid&limit=1"
    [ "$API_STATUS" = 200 ] || { failed "stock lookup $sku answered $API_STATUS: $(api_error)"; continue; }
    row=$(printf '%s' "$API_BODY" | jq -c '(.items // .data // .)[0] // empty'); [ -z "$row" ] && continue
    current=$(jq -r '.on_hand // 0' <<<"$row"); rowid=$(jq -r '.id' <<<"$row")
    [ "$DRY_RUN" = 1 ] && { n=$((n + 1)); continue; }
    if [ "$current" != 0 ]; then
      api POST /inventories/adjust "$(jq -cn --arg l "$loc" --arg s "$sku" --argjson q "$current" '{location_code: $l, reason: "sample data removed", items: [{sku: $s, quantity: (0 - $q)}]}')"
      case "$API_STATUS" in 200|201) ;; *) failed "stock $sku: booking back to zero answered $API_STATUS: $(api_error)"; continue ;; esac
    fi
    api DELETE "/inventories/stock/$rowid"
    case "$API_STATUS" in 200|202|204|404) ;; *) failed "stock $sku: delete answered $API_STATUS: $(api_error)"; continue ;; esac
    n=$((n + 1))
  done
  ok "$(printf '%-22s %s rows back to zero and removed' "$(jq -r '.name' <<<"$step")" "$n")"
}

# The reference examples/place-test-order.sh puts on its orders.
TEST_ORDER_REF=SAMPLE-TEST

# cancel_test_orders: orders cannot be deleted, so the open test orders of the
# sample company are cancelled and their promotions released. Then they no
# longer hold the company and its contacts, which can be removed; promotions
# and vouchers with redemptions can only be archived. Orders placed by hand
# carry no such reference and are left alone.
cancel_test_orders() {
  local rows id status n=0
  # By the buyer snapshot on the order: the company may have been removed and
  # loaded again under a new id since.
  api GET "/orders?customer_order_number=$TEST_ORDER_REF&limit=100"
  [ "$API_STATUS" = 200 ] || { failed "listing the test orders answered $API_STATUS: $(api_error)"; return 0; }
  rows=$(printf '%s' "$API_BODY" | jq -r '(.items // .data // .)[] | select(.buyer.customer_number == "DEMO-C-1001" and .status != "completed") | "\(.id) \(.status)"')
  while read -r id status; do
    [ -z "$id" ] && continue
    [ "$status" != cancelled ] && n=$((n + 1))
    if [ "$DRY_RUN" != 1 ]; then
      if [ "$status" != cancelled ]; then
        api POST "/orders/$id/cancel" '{"reason":"sample data removed"}'
        case "$API_STATUS" in 200|201) ;; *) failed "cancelling test order $id answered $API_STATUS: $(api_error)"; continue ;; esac
      fi
      # Cancelling does not give the discounts back; releasing does (the
      # voucher regains its value). The redemptions stay as history.
      api POST /promotions/release "$(jq -cn --arg o "$id" '{order_id: $o, reason: "order_cancelled"}')"
      case "$API_STATUS" in 200|201) ;; *) failed "releasing the promotions of test order $id answered $API_STATUS: $(api_error)" ;; esac
    fi
  done <<<"$rows"
  ok "$(printf '%-22s %s cancelled (orders stay, cancelled)' "test orders" "$n")"
}

# remove_manifest FILE: undo one manifest, last step first.
remove_manifest() {
  local manifest=$1 dir count i step kind mode
  dir=$(dirname "$manifest")
  count=$(jq '.steps | length' "$manifest")
  ev_scope remove "$dir" "$count"
  for ((i = count - 1; i >= 0; i--)); do
    step=$(jq -c ".steps[$i]" "$manifest")
    kind=$(jq -r '.kind // "upsert"' <<<"$step")
    mode=$(jq -r '.mode // "upsert"' <<<"$step")
    [ "$mode" = ensure ] && continue          # generic records stay
    [ "$(jq -r '.remove // ""' <<<"$step")" = with_parent ] && continue   # deleted with their parent
    case "$kind" in defaults|price_entries|children|replace) continue ;; esac   # nothing to undo (see below)
    ev_step start "$i" "$step"
    case "$kind" in
      upsert) remove_upsert "$step" "$dir" ;;
      files) remove_files "$step" "$dir" ;;
      stock) remove_stock "$step" "$dir" ;;
      defaults|price_entries|children|replace) ;;   # tenant defaults stay; entries, children and sets go with their parent
      *) die "unknown step kind '$kind' in $manifest" ;;
    esac
    ev_step end "$i" "$step"
  done
}
