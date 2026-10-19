# One pass over a stock step: for every record the location, the stock row, the
# delta to book and whether the plain fields (reorder point, ...) need a PUT, or
# L when the record has to be looked up on its own. One line per record, fields
# joined by the unit separator: index, status, location id, row id, delta, put (0/1).
# Arguments: $recs, $locs and $stock (the lists), $locs_ok and $stock_ok.
def norm: if type == "string" and test("^-?[0-9]+(\\.[0-9]+)?$") then tonumber else . end;
def same($a; $b):
  if ($b | type) == "object" then
    ($a | type) == "object" and all($b | keys[]; . as $k | same($a[$k]; $b[$k]))
  elif ($b | type) == "array" then
    ($a | type) == "array" and ($a | length) == ($b | length)
    and all(range(0; $b | length); . as $i | same($a[$i]; $b[$i]))
  else ($a | norm) == ($b | norm) end;

(reduce $locs[] as $l ({}; .[($l.code | tostring)] += [$l.id])) as $locidx
| (reduce $stock[] as $s ({}; .[($s.sku | tostring) + "\u0000" + ($s.location_id | tostring)] += [$s])) as $rowidx
| $recs[0] | to_entries[]
| .key as $i | .value as $r
| ($locidx[($r.location | tostring)] // []) as $lids
| if ($lids | length) != 1 or ($locs_ok | not) then [$i, "L"]
  else
    $lids[0] as $lid
    | ($rowidx[($r.sku | tostring) + "\u0000" + $lid] // []) as $rows
    | if ($rows | length) > 1 or (($rows | length) == 0 and ($stock_ok | not)) then [$i, "L"]
      else
        ($rows[0] // null) as $row
        | ($r | del(.sku, .location, .on_hand)) as $extra
        | [$i, "O", $lid, ($row.id // ""), ($r.on_hand - ($row.on_hand // 0)),
           (if ($extra | length) > 0 and ($row == null or (same($row; $extra) | not)) then 1 else 0 end)]
      end
  end
| map(tostring) | join("\u001f")
