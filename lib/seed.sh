# shellcheck shell=bash
# Shared helpers for seed.sh and remove.sh: one HTTP wrapper, lookups by a
# natural key, and the upsert that every plain step uses.
#
# Nothing in the API upserts by code: a repeated POST answers 409 or creates a
# duplicate. So every record is looked up by its key first and then updated
# (PUT, which merges) or created (POST).
#
# Works with the bash 3.2 that ships with macOS (no associative arrays).

: "${REVENEXX_BASE_URL:=https://api.revenexx.com/v1}"
: "${REVENEXX_TENANT:?set REVENEXX_TENANT to your tenant slug}"
REVENEXX_BASE_URL=${REVENEXX_BASE_URL%/}
DRY_RUN=${DRY_RUN:-0}

# sha256 of a file or of stdin: shasum on macOS, sha256sum on most Linux.
if command -v sha256sum >/dev/null 2>&1; then sha256() { sha256sum "$@" | cut -d' ' -f1; }
elif command -v shasum >/dev/null 2>&1; then sha256() { shasum -a 256 "$@" | cut -d' ' -f1; }
else printf 'need sha256sum or shasum\n' >&2; exit 1; fi

SEED_TMP=$(mktemp -d)
trap 'rm -rf "$SEED_TMP"' EXIT
mkdir -p "$SEED_TMP/cache"
# Credentials reach curl through a file, never its command line (ps shows that).
(
  umask 077; : > "$SEED_TMP/auth"
  if [ -n "${REVENEXX_API_KEY:-}" ]; then printf 'X-Revenexx-Api-Key: %s\n' "$REVENEXX_API_KEY" >> "$SEED_TMP/auth"; fi
  if [ -n "${REVENEXX_TOKEN:-}" ]; then printf 'Authorization: Bearer %s\n' "$REVENEXX_TOKEN" >> "$SEED_TMP/auth"; fi
)

# ---- output -------------------------------------------------------------------

say()  { printf '%s\n' "$*"; }
ok()   { printf '  \342\234\223 %s\n' "$*"; }
warn() { printf '  ! %s\n' "$*" >&2; }
die()  { printf '  \342\234\227 %s\n' "$*" >&2; exit 1; }

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

# lookup ROUTE QUERY  ->  prints the id of the single match, or nothing.
# QUERY is an exact-match query string such as "code=demo_de". Two matches
# stop the run: updating or deleting either one could hit the wrong record.
lookup() {
  local route=$1 query=$2
  local cache="$SEED_TMP/cache/$(printf '%s?%s' "$route" "$query" | sha256)"
  if [ -f "$cache" ]; then cat "$cache"; return; fi
  api GET "$route?$query&limit=2"
  [ "$API_STATUS" = 200 ] || die "lookup $route?$query answered $API_STATUS: $(api_error)"
  local id
  id=$(printf '%s' "$API_BODY" | jq -r '(.items // .data // .) | if length > 1 then "MANY" else (.[0].id // empty) end')
  [ "$id" = MANY ] && die "more than one record at $route matches $query: remove the duplicate first"
  [ -n "$id" ] && printf '%s' "$id" > "$cache"
  printf '%s' "$id"
}

remember() { # remember ROUTE QUERY ID
  printf '%s' "$3" > "$SEED_TMP/cache/$(printf '%s?%s' "$1" "$2" | sha256)"
}

forget() { # forget ROUTE QUERY
  rm -f "$SEED_TMP/cache/$(printf '%s?%s' "$1" "$2" | sha256)"
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

# run_upsert STEP_JSON DIR
run_upsert() {
  local step=$1 dir=$2
  local name file count i rec resolved route body query id created=0 updated=0 mode
  name=$(jq -r '.name' <<<"$step")
  # "ensure": create when missing, never touch an existing record. For generic
  # codes (name, description, asset families) a tenant may already have.
  mode=$(jq -r '.mode // "upsert"' <<<"$step")
  file="$dir/$(jq -r '.file' <<<"$step")"
  count=$(jq 'length' "$file")
  for ((i = 0; i < count; i++)); do
    rec=$(jq -c ".[$i]" "$file")
    resolved=$(resolve_refs "$step" "$rec")
    route=${resolved%%$'\t'*}
    body=${resolved#*$'\t'}
    query=$(key_query "$step" "$body")
    # In a dry run a parent that does not exist yet leaves a placeholder in
    # the route; its children are all new.
    case "$DRY_RUN$route$body" in 1*"<"*) id="" ;; *) id=$(lookup "$route" "$query") ;; esac
    if [ "$DRY_RUN" = 1 ]; then
      [ -n "$id" ] && updated=$((updated + 1)) || created=$((created + 1))
      continue
    fi
    if [ -n "$id" ] && [ "$mode" = ensure ]; then
      updated=$((updated + 1))
    elif [ -n "$id" ]; then
      api PUT "$route/$id" "$body"
      [ "$API_STATUS" = 200 ] || die "$name: update $query answered $API_STATUS: $(api_error)"
      updated=$((updated + 1))
    else
      api POST "$route" "$body"
      case "$API_STATUS" in
        200|201) ;;
        409) die "$name: $query exists but is not listed (in the trash?): $(api_error)" ;;
        *) die "$name: create $query answered $API_STATUS: $(api_error)" ;;
      esac
      id=$(printf '%s' "$API_BODY" | jq -r '(.data // .).id // empty')
      [ -n "$id" ] && remember "$route" "$query" "$id"
      created=$((created + 1))
    fi
  done
  if [ "$mode" = ensure ]; then
    ok "$(printf '%-22s %s created, %s already there' "$name" "$created" "$updated")"
  else
    ok "$(printf '%-22s %s created, %s updated' "$name" "$created" "$updated")"
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

# run_stock STEP_JSON DIR: bring each SKU's on-hand at a location to a target.
# Stock moves by delta (receive/adjust add), so the step reads what is there
# and books only the difference; a re-run books nothing.
run_stock() {
  local step=$1 dir=$2 file count i rec sku loc target locid row rowid current delta extra moved=0 same=0
  file="$dir/$(jq -r '.file' <<<"$step")"
  count=$(jq 'length' "$file")
  for ((i = 0; i < count; i++)); do
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
    [ "$DRY_RUN" = 1 ] && continue
    if [ "$delta" != 0 ]; then
      api POST /inventories/adjust "$(jq -cn --arg l "$loc" --arg s "$sku" --argjson q "$delta" '{location_code: $l, reason: "sample data", items: [{sku: $s, quantity: $q}]}')"
      case "$API_STATUS" in 200|201) ;; *) die "stock $sku answered $API_STATUS: $(api_error)" ;; esac
    fi
    # Everything except the quantity (reorder point, availability) is a plain field.
    extra=$(jq -c 'del(.sku, .location, .on_hand)' <<<"$rec")
    if [ "$extra" != '{}' ]; then
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
  done
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
  local name file count i rec path base hash folder tags existing sid ohash uploaded=0 kept=0 created=0 updated=0
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
  for ((i = 0; i < count; i++)); do
    rec=$(jq -c ".[$i]" "$file")
    path="$dir/$(jq -r '.file' <<<"$rec")"
    [ -f "$path" ] || die "$name: missing file $path"
    base=$(basename "$path")
    hash=$(sha256 "$path")
    sid=$(printf '%s' "$existing" | jq -r --arg n "$base" '[(.data // .)[] | select(.original_name == $n)][0].id // empty')
    ohash=$(printf '%s' "$existing" | jq -r --arg n "$base" '[(.data // .)[] | select(.original_name == $n)][0].content_hash // empty')
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
    # The product asset: the catalogue's record of the file, keyed by family + code.
    rec=$(jq -c --arg s "$sid" 'del(.file) + {source: "storage", storage_asset_id: $s}' <<<"$rec")
    local resolved route body query id
    resolved=$(resolve_refs "$step" "$rec")
    route=${resolved%%$'\t'*}
    body=${resolved#*$'\t'}
    query=$(key_query "$step" "$body")
    id=$(lookup "$route" "$query")
    if [ -n "$id" ]; then
      api PUT "$route/$id" "$body"; [ "$API_STATUS" = 200 ] || die "$name: asset $query answered $API_STATUS: $(api_error)"
      updated=$((updated + 1))
    else
      api POST "$route" "$body"
      case "$API_STATUS" in 200|201) ;; *) die "$name: asset $query answered $API_STATUS: $(api_error)" ;; esac
      created=$((created + 1))
    fi
  done
  ok "$(printf '%-22s %s uploaded, %s unchanged; %s assets created, %s updated' "$name" "$uploaded" "$kept" "$created" "$updated")"
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
  for ((i = 0; i < count; i++)); do
    step=$(jq -c ".steps[$i]" "$manifest")
    kind=$(jq -r '.kind // "upsert"' <<<"$step")
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
  for ((i = count - 1; i >= 0; i--)); do
    step=$(jq -c ".steps[$i]" "$manifest")
    kind=$(jq -r '.kind // "upsert"' <<<"$step")
    mode=$(jq -r '.mode // "upsert"' <<<"$step")
    [ "$mode" = ensure ] && continue          # generic records stay
    [ "$(jq -r '.remove // ""' <<<"$step")" = with_parent ] && continue   # deleted with their parent
    case "$kind" in
      upsert) remove_upsert "$step" "$dir" ;;
      files) remove_files "$step" "$dir" ;;
      stock) remove_stock "$step" "$dir" ;;
      defaults|price_entries|children|replace) ;;   # tenant defaults stay; entries, children and sets go with their parent
      *) die "unknown step kind '$kind' in $manifest" ;;
    esac
  done
}
