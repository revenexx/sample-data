# revenexx sample data

A ready-made B2B shop for your revenexx tenant: four industry catalogues with prices, stock, images, drawings and 3D models, plus a buyer company and promotions. One script loads it, another removes it again.

Use it to see revenexx working with realistic data before your own catalogue is in, to follow a B2B order from price to placement, or to test an ERP or PIM integration against records you know.

- [What you get](#what-you-get)
- [Before you start](#before-you-start)
- [Load it](#load-it)
- [Try these](#try-these)
- [Remove it](#remove-it)
- [How it works](#how-it-works)
- [What it changes on your tenant](#what-it-changes-on-your-tenant)
- [Build your own pack](#build-your-own-pack)
- [Licence](#licence)

## What you get

Every load brings the **base**, plus the **packs** you choose.

| | What's in it |
| --- | --- |
| **Base** | A market `demo_de` (Germany, EUR, German and English, 19 % and 7 % VAT) and the buyer company *Muster Bau & Technik GmbH*, with a buyer, an approver, and billing and shipping addresses. Also an automatic promotion (5 % off from 100 €), two voucher codes and a shipping method priced by weight. The base also calls your tenant's setup routes, which create the standard sales channel and channel types, shipping carriers and methods, payment methods, order and return number ranges, customer roles and value lists (payment terms, lifecycle stages), the standard price list, and the stock location `main` with its availability states if they are missing, and leave existing ones alone. |
| **`industrial`** | Workshop and industrial supply: power tools, fasteners, safety gear. 10 products, including work gloves in 4 sizes. |
| **`electrical`** | Electrical installation: cables, switches and sockets, lighting. 10 products, including a socket outlet in 3 colours. |
| **`office`** | Office and facility supplies: paper and filing, writing, breakroom. 10 products, including a ring binder in 3 colours. |
| **`lab`** | Laboratory supplies: centrifuges, pipettes, tips and tubes. 10 products, including a pipette in 3 volume ranges. |

Each pack has the following:

- **3 categories** under its own root category.
- **Typed attributes** (with units and options) on one product family.
- **Two fictional manufacturers.**
- **A list price list** with quantity breaks, plus contract prices for the buyer company.
- **Stock**, with one product below its reorder point.
- **About 20 files:** an illustration for every product, dimension drawings (SVG and PDF), a data sheet (PDF) and, in every pack except `office`, 3D models (STEP).

A model and each of its variants are separate product records, so `seed.sh` reports 13 or 14 products per pack.

All names, products and companies are invented. Every record you look up by code carries the prefix `DEMO-` (`demo_` where a code takes no hyphen, such as attributes and the market `demo_de`), so you can tell sample data from your own as long as you don't use these prefixes yourself. Values inside those records, such as option codes (`black`, `a4`), the market's tax classes (`standard`, `reduced`), locales and the currency, are plain. [What it changes on your tenant](#what-it-changes-on-your-tenant) lists everything it writes.

## Before you start

You need:

1. **A tenant you can experiment on, not your production tenant.** A playground tenant is ideal; [Get a test tenant](https://revenexx.dev/docs/getting-started/prerequisites#get-a-test-tenant) explains how to get one, with its **slug** and an **API key**. On a test tenant a development key with the `*` scope is simplest. A narrower key needs `products.*`, `prices.*`, `inventories.*`, `customers.*`, `promotions.*`, `markets.*`, `channels.*`, `shipping.*`, `payments.*`, `orders.*`, `carts.*` and `storage`.
2. **The commerce apps installed** on that tenant: Products, Pricing, Inventories, Customers, Promotions, Markets, Channels, Shipping, Payments, Orders and Carts. Install them from the Marketplace in Cockpit, the revenexx back office. If one is missing, `seed.sh` stops at the first step that needs it and prints the error.
3. **`bash`, `curl` and `jq`.** `bash` and `curl` come with macOS and Linux; install `jq` if it is missing (`brew install jq`, `apt install jq`). On Windows, use WSL.

```bash
git clone https://github.com/revenexx/sample-data.git
cd sample-data

export REVENEXX_TENANT=<your-tenant-slug>
export REVENEXX_API_KEY=<your-api-key>
```

The scripts call `https://api.revenexx.com/v1`; set `REVENEXX_BASE_URL` only if you were given a different API address.

## Load it

Every load includes the base; `--pack` adds packs: `industrial`, `electrical`, `office`, `lab` or `all`.

```bash
./seed.sh --pack industrial          # the base and one pack
./seed.sh --pack all                 # the base and every pack
./seed.sh --pack lab --dry-run       # show what would happen, change nothing
```

Loading the base and one pack takes well under a minute. You see one line per step:

```
Seeding tenant your-tenant
base
  ✓ tenant defaults        9 routes called
  ✓ market                 1 created, 0 updated
  …
pack: industrial
  ✓ categories             4 created, 0 updated
  ✓ files                  24 uploaded, 0 unchanged; 24 assets created, 0 updated
  ✓ products               14 created, 0 updated
  …
done
```

**Running it again is safe.** Every record is looked up by its code and updated, never duplicated. Files are uploaded only when they changed, and stock is set to its target, not added on top. A second run reports `0 created`. It also puts back what you changed by hand on sample products, prices, companies and the like; promotion effects and conditions you changed are kept, and so is a voucher's used value. If a run stops halfway, fix the cause and run it again.

Then open Cockpit: the products are under *Commerce Studio → Products*, the companies under *CRM*, and the promotions under *Marketing*.

## Try these

The calls below use a small helper. Paste it into your shell once:

```bash
api() { curl -s "${REVENEXX_BASE_URL:-https://api.revenexx.com/v1}$1" -H "X-Revenexx-Tenant: $REVENEXX_TENANT" \
  -H "X-Revenexx-Api-Key: $REVENEXX_API_KEY" -H 'Content-Type: application/json' "${@:2}"; }
ORG=$(api '/customers/organizations?customer_number=DEMO-C-1001' | jq -r '.items[0].id')
echo "$ORG"    # an id; "null" means the base is not loaded, or the tenant or key is wrong
```

All prices in this data are net, in EUR.

### 1. List price, quantity break, contract price

Twelve boxes of M8 bolts cost less per box than one. For *Muster Bau* the contract price beats both.

```bash
CART='[{"sku":"DEMO-IND-2002","quantity":1},{"sku":"DEMO-IND-2002","quantity":12}]'
api /prices/resolve -d "{\"items\":$CART}" | jq -r '.prices[] | "\(.quantity) × \(.unit_price) € (\(.price_list.code))"'
api /prices/resolve -d "{\"organization_id\":\"$ORG\",\"items\":$CART}" | jq -r '.prices[] | "\(.quantity) × \(.unit_price) € (\(.price_list.code))"'
```

```
1 × 12.5 € (DEMO-IND-LIST)
12 × 10.9 € (DEMO-IND-LIST)
1 × 8.9 € (DEMO-IND-CONTRACT)
12 × 8.9 € (DEMO-IND-CONTRACT)
```

Every price also comes with its gross amount (`unit_price_gross`) and all quantity breaks (`tiers`).

### 2. A promotion that applies by itself

From 100 € order value, the cart gets 5 % off without a code. Below that, nothing applies.

The cart below is a single drill at its list price, 129 €.

```bash
api /promotions/evaluate -d '{"currency":"EUR","lines":[{"sku":"DEMO-IND-1001","quantity":1,"unit_price":129,"line_total":129}]}' \
  | jq -r '.applied[] | "\(.promotion_name): -\(.amount) €"'
```

```
5 % off from 100 € order value: -6.45 €
```

### 3. Voucher codes

`DEMO-WELCOME10` takes 10 % off. `DEMO-CREDIT150` is a 150 € voucher that takes at most 50 € per order and draws down until nothing is left.

```bash
api /promotions/codes/check -d '{"code":"DEMO-CREDIT150"}' | jq '{usable, remaining_value}'
```

```json
{
  "usable": true,
  "remaining_value": 150
}
```

That's the state right after the first load. A spent value stays spent: neither `seed.sh` nor `remove.sh` followed by `seed.sh` refills the voucher, because what was redeemed belongs to the order history.

### 4. Place a test order

`examples/place-test-order.sh` takes the path a shop takes. It needs the `industrial` pack, uses the same environment variables as `seed.sh` and the voucher `DEMO-CREDIT150` by default. It resolves prices for the company, evaluates promotions with a voucher, picks a shipping rate and an eligible payment method, places the order, then redeems the voucher.

**What a test order does on your tenant.** It is a real order: it appears in Cockpit under *Order management*, it cannot be deleted, only cancelled, and it stays on the tenant for good. It is placed through the API with your key, not as a signed-in buyer, so no approval step applies. It is paid by invoice (or the first eligible method if invoice is switched off), so nothing is charged. revenexx publishes the usual order events, so a webhook or an ERP connection on the tenant sees the order like any other; use a tenant without live integrations. `./remove.sh --base` cancels the open test orders and gives their discounts back (the voucher regains its value), then removes the company and contact; the cancelled orders stay (see [Remove it](#remove-it)). Only deleting the tenant removes them.

```bash
./examples/place-test-order.sh
```

```
2  prices for this company
  DEMO-IND-1001 × 1 at 109 € (DEMO-IND-CONTRACT)
  DEMO-IND-2002 × 12 at 8.9 € (DEMO-IND-CONTRACT)
  DEMO-IND-3002 × 10 at 5.4 € (DEMO-IND-LIST)
3  promotions and voucher DEMO-CREDIT150
  150 € voucher, up to 50 € per order (DEMO-CREDIT150): -50 €
  5 % off from 100 € order value: -10.99 €
…
6  the order
  ✓ ORD-000001: 248.48 EUR incl. tax
7  redeem the promotions
  ✓ DEMO-CREDIT150 has 100 € left
```

Run it three times to watch the voucher run out. Your order numbers depend on how many orders the tenant already has. To order without a voucher, set the variable to empty: `VOUCHER= ./examples/place-test-order.sh`.


### 5. Shipping by weight

Next to the tenant's standard methods (standard 4.90 €, free from 100 €; express 9.90 €; pickup), the base adds *Freight by weight*: 6.90 € up to 5 kg, 9.90 € from 5 kg, 14.90 € from 20 kg and 29.90 € from 50 kg.

```bash
api /shipping/rates -d '{"country":"DE","currency":"EUR","order_value":80,"weight":25,"weight_unit":"kg"}' \
  | jq -r '.rates[] | "\(.method_code // .code): \(.price) €"'
```

```
standard: 4.9 €
express: 9.9 €
pickup: 0 €
DEMO-FREIGHT-WEIGHT: 14.9 €
```

### 6. Buyer and approver

At *Muster Bau*, Anna Becker is a buyer: she places orders. Jonas Keller is an approver: he may sign off other people's orders up to 5 000 €. Whether an order needs his sign-off is decided by your tenant's approval settings, which the sample data leaves alone.

```bash
api "/customers/contacts?organization_id=$ORG" | jq -r '.items[] | "\(.first_name) \(.last_name): \(.role), approval \(.order_approval_mode) \(.order_approval_limit // "")"'
```

### 7. Low stock

Each pack has one product below its reorder point. In the industrial pack it's the cutting discs.

```bash
api '/inventories/stock?sku=DEMO-IND-2003' | jq '.items[0] | {sku, on_hand, reorder_point}'
```

### 8. Variants

The work gloves are one product model with four size variants. In the other packs: the socket outlet (colour), the ring binder (colour) and the pipette (volume range).

```bash
MODEL=$(api '/products?sku=DEMO-IND-3001' | jq -r '.items[0].id')
api "/products?parent_id=$MODEL" | jq -r '.items[] | "\(.sku): \(.label)"'
```

### 9. Images, drawings, data sheets and 3D models

Every product has an image. Selected parts also have a dimension drawing, a data sheet or a 3D model (STEP), uploaded to your tenant's storage in the folder `sample-data/<pack>` (0.3 to 0.55 MB per pack). In Cockpit, open the media library and pick `demo-ind-2002-hex-bolt-m8x40.step`. The bolt opens in the 3D viewer, at real size (15 × 13 × 45.3 mm); on a phone it opens in AR. Data sheets are PDFs, drawings come as SVG and PDF, and all of them are marked *SAMPLE — fictional product*.

### 10. Your ERP keys

Products, categories, companies, contacts, addresses, price lists, manufacturers, families and the shipping method carry an `external_id` (`DEMO-IND-1001`, `DEMO-C-1001`, …), the place where an ERP keeps its own key. Look a record up by it. To change the sample data, edit the JSON files and run `seed.sh` again: the change is applied to the same record.

```bash
api '/products?external_id=DEMO-IND-1001' | jq -r '.items[0].sku'
```

## Remove it

```bash
./remove.sh --pack industrial         # one pack
./remove.sh --pack all --base         # everything, including the market, company and promotions
./remove.sh --pack all --base --dry-run
```

`remove.sh` uses the same environment variables as `seed.sh`. It deletes exactly the records `seed.sh` created, found by their codes, and deletes them permanently (not just to the trash), so you can load the data again later. Uploaded files are deleted too. Remove packs before or together with the base: the packs' contract prices belong to the base's company.

What stays, on purpose:

- **Your tenant's own settings:** channel, shipping and payment methods, order numbers, roles, stock locations.
- **Shared fields:** the `name`, `description` and `image` attributes and the asset families. Your own data may use them.
- **Orders and what they refer to.** Orders cannot be deleted. `--base` first cancels the open orders the example script placed (they carry the reference `SAMPLE-TEST`) and gives their discounts back; the cancelled orders stay. Orders you placed yourself are never touched. A voucher or promotion that was ever redeemed is disabled or archived instead of deleted, and a company or contact with other open orders is blocked, so your order history stays intact. Loading the data again reactivates these records. A spotless tenant takes deleting the tenant.

## How it works

- **Plain files.** Every record is JSON under `base/` and `packs/<pack>/`.
- **Manifests.** A `manifest.json` per folder lists the steps in load order: the market first, then the records that depend on it.
- **One loader.** `seed.sh` reads the manifests and calls the revenexx API. It needs only `bash`, `curl` and `jq`, and nothing is tied to one tenant.

## What it changes on your tenant

Everything `seed.sh` writes:

- **Records with a `DEMO-` or `demo_` code** (a record of yours that already carries one of these codes is treated as sample data): the market with its currency, locales and tax classes; the company, contacts and addresses; promotions, their effects and conditions, the voucher batch and vouchers; the shipping method with its rate tiers; and per pack the categories, attribute groups, attributes and options, family and variants, manufacturers, products and their category links, product assets, price lists and entries, and stock levels. `remove.sh` deletes these again.
- **Files** in the storage folder `sample-data/<pack>`. `remove.sh` deletes the whole folder, including any file you put there yourself.
- **Created only if missing, never changed:** the product attributes `name`, `description` and `image` (the main picture's storage key, which storefronts read), and the asset families `product_images`, `technical_drawings` and `downloads`. Your own data may use them, so `remove.sh` leaves them.
- **Your tenant's setup**, created through the setup routes if missing: the standard sales channel and channel types, shipping carriers and methods, payment methods, order and return number ranges, customer roles and value lists (payment terms, lifecycle stages), the standard price list, and the stock location `main` with its availability states. Stock goes to the location `main`. `remove.sh` leaves all of these.

Orders you place yourself, for example with `examples/place-test-order.sh`, are yours: neither script touches them. Apart from that, it never changes or deletes any other record of yours.

## Build your own pack

Each pack is generated from a short spec in `tools/packs/<pack>.py`. To add one:

1. Copy a spec to `tools/packs/<yours>.py`. Use your own prefix, categories, attributes and products.
2. Run `python3 tools/build-pack.py <yours>` to write `packs/<yours>/`.
3. Add illustrations in `tools/art/<yours>.mjs`, then run `node tools/build-art.mjs <yours>` (needs Google Chrome).
4. Add drawings and data sheets in `tools/docs/<yours>.mjs`, then run `node tools/build-docs.mjs <yours>`.
5. Optionally add 3D parts in `tools/cad/<yours>.py` (needs `pip install cadquery`).
6. Run `./seed.sh --pack <yours>` twice. The second run must report `0 created`.

Steps 3 to 5 are only for generating the files. Loading never needs them.

## Licence

- **Scripts:** MIT, see [LICENSE](LICENSE).
- **Data, images, drawings, data sheets and 3D models:** CC BY 4.0, see [LICENSE-DATA](LICENSE-DATA).
- **Assets:** every file was made for this repository by the scripts in `tools/`. [ASSETS.md](ASSETS.md) lists each file and how it was made.
- **Fictional content:** the products, manufacturers and companies are invented. Any resemblance to real products or companies is unintended.
