#!/usr/bin/env bash
# Place a test order for the sample company along the path a shop takes:
# prices -> promotions -> shipping -> payment -> order -> redeem the voucher.
# Needs the base and the industrial pack (./seed.sh --pack industrial).
#
#   REVENEXX_BASE_URL=... REVENEXX_TENANT=... REVENEXX_API_KEY=... \
#   ./examples/place-test-order.sh               # with voucher DEMO-CREDIT150
#   VOUCHER= ./examples/place-test-order.sh      # without a voucher
#
# Every run places a new order and, with a voucher, spends some of its value.
set -euo pipefail
cd "$(dirname "$0")/.."
source lib/seed.sh

VOUCHER=${VOUCHER-DEMO-CREDIT150}
CURRENCY=EUR
# The cart: a drill (contract price for this company), twelve boxes of bolts
# (the quantity break from ten) and ten safety glasses.
CART='[{"sku":"DEMO-IND-1001","quantity":1},{"sku":"DEMO-IND-2002","quantity":12},{"sku":"DEMO-IND-3002","quantity":10}]'

get_one() { api GET "$1"; [ "$API_STATUS" = 200 ] || die "GET $1 answered $API_STATUS: $(api_error)"; printf '%s' "$API_BODY" | jq -c '(.items // .data // .)[0] // empty'; }
post() { api POST "$1" "$2"; case "$API_STATUS" in 200|201) ;; *) die "POST $1 answered $API_STATUS: $(api_error)" ;; esac; printf '%s' "$API_BODY"; }

say "1  the buyer"
org=$(get_one "/customers/organizations?customer_number=DEMO-C-1001")
[ -n "$org" ] || die "the sample company is missing: run ./seed.sh first"
org_id=$(jq -r .id <<<"$org")
buyer=$(get_one "/customers/contacts?external_id=DEMO-P-1001")
bill=$(get_one "/customers/addresses?external_id=DEMO-A-1001-BILL")
ship=$(get_one "/customers/addresses?external_id=DEMO-A-1001-SHIP")
ok "$(jq -r '.name' <<<"$org"), buyer $(jq -r '"\(.first_name) \(.last_name)"' <<<"$buyer")"

say "2  prices for this company"
prices=$(post /prices/resolve "$(jq -cn --arg o "$org_id" --argjson items "$CART" '{organization_id: $o, items: $items}')")
lines=$(jq -c '[.prices[] | {sku, quantity, unit_price, line_total, tax_rate, price_list: .price_list.code}]' <<<"$prices")
jq -r '.[] | "  \(.sku) × \(.quantity) at \(.unit_price) € (\(.price_list))"' <<<"$lines"
missing=$(jq -rn --argjson c "$CART" --argjson l "$lines" '[$c[] | select(. as $i | $l | map(select(.sku == $i.sku and .quantity == $i.quantity and .unit_price != null)) | length == 0) | .sku] | join(", ")')
[ -z "$missing" ] || die "no price for $missing: run ./seed.sh --pack industrial"
subtotal=$(jq '[.[].line_total] | add' <<<"$lines")

say "3  promotions${VOUCHER:+ and voucher $VOUCHER}"
evaluation=$(post /promotions/evaluate "$(jq -cn --arg c "$CURRENCY" --arg o "$org_id" --arg p "$(jq -r .id <<<"$buyer")" --arg v "$VOUCHER" --argjson lines "$lines" \
  '{currency: $c, organization_id: $o, contact_id: $p, codes: (if $v == "" then [] else [$v] end), lines: [$lines[] | {sku, quantity, unit_price, line_total}]}')")
applied=$(jq -c '[.applied[]? | select(.preview | not)]' <<<"$evaluation")
jq -r '.[] | "  \(.promotion_name)\(if .voucher_code then " (" + .voucher_code + ")" else "" end): -\(.amount) €"' <<<"$applied"
discount=$(jq '[.[].amount] | add // 0' <<<"$applied")
net=$(jq -n --argjson s "$subtotal" --argjson d "$discount" '$s - $d')

say "4  shipping to $(jq -r '.city' <<<"$ship")"
rates=$(post /shipping/rates "$(jq -cn --arg c "$CURRENCY" --argjson v "$net" '{country: "DE", currency: $c, order_value: $v}')")
rate=$(jq -c '((.rates // .items // .) | map(select((.method_code // .code // .method) == "standard")) | .[0]) // (.rates // .items // .)[0]' <<<"$rates")
[ -n "$rate" ] && [ "$rate" != null ] || die "no shipping rate for DE: $(printf '%s' "$rates" | cut -c1-200)"
ship_method=$(jq -r '.method_code // .code // .method' <<<"$rate"); ship_price=$(jq -r '.price // .amount // empty' <<<"$rate")
[ -n "$ship_price" ] || die "the shipping rate $ship_method has no price: $(printf '%s' "$rate" | cut -c1-200)"
ok "$ship_method: $ship_price €"

say "5  payment"
methods=$(post /payments/methods/eligible "$(jq -cn --arg c "$CURRENCY" --argjson a "$net" '{amount: $a, country: "DE", currency: $c}')")
pay=$(jq -r '((.methods // .items // .) | map(.code) | if index("invoice") then "invoice" else .[0] end)' <<<"$methods")
[ -n "$pay" ] && [ "$pay" != null ] || die "no payment method is eligible: $(printf '%s' "$methods" | cut -c1-200)"
ok "$pay"

say "6  the order"
addr() { jq -c '{organization_name: .company, recipient_name: .name, address_line1: .street, postal_code: .zip, locality: .city, country_code: .country, email: .email, source_address_id: .id}' <<<"$1"; }
order=$(post /orders/place "$(jq -cn --arg c "$CURRENCY" --argjson lines "$lines" --argjson applied "$applied" \
  --argjson org "$org" --argjson buyer "$buyer" --argjson bill "$(addr "$bill")" --argjson ship "$(addr "$ship")" \
  --arg sm "$ship_method" --argjson sp "$ship_price" --arg pm "$pay" --arg ref "$TEST_ORDER_REF" '{
    currency: $c,
    organization_id: $org.id, contact_id: $buyer.id,
    buyer: {organization_id: $org.id, contact_id: $buyer.id, company: $org.name, customer_number: $org.customer_number, email: $buyer.email,
            name: "\($buyer.first_name) \($buyer.last_name)"},
    billing_address: $bill, shipping_address: $ship,
    items: [$lines[] | {type: "product", sku, quantity, unit_price, tax_rate}],
    discounts: [$applied[] | {promotion_id, promotion_name, amount, placement: "head"}],
    shipping: {method: $sm, price: $sp, tax_rate: 19},
    payment: {method: $pm, status: "pending"},
    customer_order_number: $ref
  }')")
order_id=$(jq -r '(.data // .).id' <<<"$order")
ok "$(jq -r '(.data // .) | "\(.order_number // .number // .id): \((.grand_total * 100 | round) / 100) \(.currency) incl. tax"' <<<"$order")"

if [ "$(jq length <<<"$applied")" -gt 0 ]; then
  say "7  redeem the promotions"
  post /promotions/commit "$(jq -cn --arg o "$order_id" --arg c "$CURRENCY" --arg org "$org_id" --arg p "$(jq -r .id <<<"$buyer")" --argjson applied "$applied" \
    '{order_id: $o, currency: $c, organization_id: $org, contact_id: $p, promotions: [$applied[] | {promotion_id, voucher_id, amount}]}')" >/dev/null
  if [ -n "$VOUCHER" ]; then
    left=$(post /promotions/codes/check "$(jq -cn --arg v "$VOUCHER" '{code: $v}')" | jq -r '.remaining_value // empty')
    [ -n "$left" ] && ok "$VOUCHER has $left € left" || ok "$VOUCHER redeemed"
  else
    ok "recorded"
  fi
fi
say "done"
