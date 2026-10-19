# One pass over a whole upsert step: decides for every record whether it is
# the same (S), needs an update (U), a create (C) or has to be looked up on its
# own (L), from the lists lib/seed.sh read before. Emits one line per record,
# fields joined by the unit separator: index, status, id, key query, body.
#
# Arguments: $step, $recs (the record file), $only (null or the indexes to
# decide), $own (the step's own list) and $own_ok (whether it was read whole),
# $names (reference route -> argument name) with $oks (route -> read whole), and
# one argument per reference list.
def norm: if type == "string" and test("^-?[0-9]+(\\.[0-9]+)?$") then tonumber else . end;
def same($a; $b):
  if ($b | type) == "object" then
    ($a | type) == "object" and all($b | keys[]; . as $k | same($a[$k]; $b[$k]))
  elif ($b | type) == "array" then
    ($a | type) == "array" and ($a | length) == ($b | length)
    and all(range(0; $b | length); . as $i | same($a[$i]; $b[$i]))
  else ($a | norm) == ($b | norm) end;

($step.key | if type == "array" then . else [.] end) as $keys
| def kq($r): $keys | map(. as $k | "\($k)=\($r[$k] | tostring | @uri)") | join("&");
($step.mode // "upsert") as $mode
| ($step.refs // {}) as $refs
# per reference target: value of its lookup key -> the ids of the records that have it
| (reduce ($refs | keys[]) as $t ({};
    $refs[$t] as $s
    | ($s.key // "code") as $rk
    | ($ARGS.named[$names[$s.route] // "none"] // []) as $list
    | .[$t] = (reduce $list[] as $r ({};
        if all(($s.where // {}) | to_entries[]; ($r[.key] | tostring) == (.value | tostring))
        then .[($r[$rk] | tostring)] += [$r.id] else . end)))) as $refidx
| (reduce $own[] as $r ({}; .[kq($r)] += [$r])) as $ownidx
| ($only // [] | map({(tostring): true}) | add // {}) as $set
| $recs[0] | to_entries[]
| select($only == null or $set[(.key | tostring)])
| .key as $i | .value as $rec
| (reduce ($refs | keys[]) as $t ({rec: $rec, ok: true};
    $refs[$t] as $s
    | .rec[$s.field] as $v
    | .rec |= del(.[$s.field])
    | if ($v == null or $v == false or $v == "") then .
      else ($refidx[$t][($v | tostring)] // []) as $ids
        | if ($oks[$s.route] == true) and ($ids | length) == 1 then .rec[$t] = $ids[0] else .ok = false end
      end)) as $x
| if ($x.ok | not) then [$i, "L", "", "", ""]
  else
    kq($x.rec) as $q
    | ($ownidx[$q] // []) as $m
    | if ($m | length) > 1 then [$i, "L", "", "", ""]
      elif ($m | length) == 1 then
        if $mode == "ensure" or same($m[0]; $x.rec) then [$i, "S", "", "", ""]
        else [$i, "U", $m[0].id, $q, ($x.rec | tojson)] end
      elif $own_ok then [$i, "C", "", $q, ($x.rec | tojson)]
      else [$i, "L", "", "", ""] end
  end
| map(tostring) | join("\u001f")
