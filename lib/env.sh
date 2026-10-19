# shellcheck shell=bash
# load_dotenv FILE: read REVENEXX_* settings from a plain KEY=value file.
# It is parsed, never sourced: no expansion, no commands. Blank lines and #
# comments are skipped, an optional `export ` and one pair of quotes are
# stripped. A variable that is already set in the environment wins.
load_dotenv() {
  local file=$1 line key val
  [ -f "$file" ] || return 0
  while IFS= read -r line || [ -n "$line" ]; do
    line=${line%$'\r'}
    line=${line#"${line%%[![:space:]]*}"}
    case "$line" in ""|"#"*) continue ;; esac
    line=${line#export }
    key=${line%%=*}; val=${line#*=}
    [ "$key" != "$line" ] || continue
    key=${key%"${key##*[![:space:]]}"}
    case "$key" in REVENEXX_[A-Z_]*) ;; *) continue ;; esac
    case "$key" in *[!A-Z_]*) continue ;; esac
    val=${val#"${val%%[![:space:]]*}"}
    val=${val%"${val##*[![:space:]]}"}
    case "$val" in
      \"*\") val=${val#\"}; val=${val%\"} ;;
      \'*\') val=${val#\'}; val=${val%\'} ;;
      *) val=${val%%[[:space:]]#*}; val=${val%"${val##*[![:space:]]}"} ;;
    esac
    printenv "$key" >/dev/null 2>&1 || export "$key=$val"
  done < "$file"
}
