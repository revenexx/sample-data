"""Write a pack's data files and manifest from its spec in tools/packs/<pack>.py.

Development tool only: the JSON files are committed and seed.sh reads only
them. One spec per pack keeps every pack in the same shape.

    python3 tools/build-pack.py industrial
"""
import importlib.util
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_spec(pack):
    path = ROOT / "tools" / "packs" / f"{pack}.py"
    spec = importlib.util.spec_from_file_location(f"pack_{pack}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.PACK


def write(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    WRITTEN.add(path)


WRITTEN = set()


def prune(out, assets):
    """Delete what this build no longer produces, so nothing stale is committed
    or loaded: data files it did not write, and asset files no record names."""
    keep = {out / a["file"] for a in assets}
    for path in sorted(out.rglob("*")):
        if path.is_file() and path not in WRITTEN and path not in keep and (path.suffix == ".json" or "assets" in path.relative_to(out).parts):
            path.unlink()
            print(f"  pruned {path.relative_to(ROOT)}")
    for path in sorted(out.rglob("*"), reverse=True):
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()


def L(de, en):
    return {"de-DE": de, "en-US": en}


def ref(field, route, key="code", place="body", where=None):
    return {"field": field, "route": route, "key": key, "in": place, **({"where": where} if where else {})}


def build(pack):
    P = load_spec(pack)
    out = ROOT / "packs" / pack
    out.mkdir(parents=True, exist_ok=True)
    pre, attr_pre = P["prefix"], P["attr_prefix"]
    family = P["family"]["code"]

    write(out / "categories.json", [
        {"code": c["code"], **({"parent": c["parent"]} if c.get("parent") else {}), "labels": L(*c["labels"]),
         "position": c["position"], "external_id": c["code"]} for c in P["categories"]])
    write(out / "attribute-groups.json", [
        {"code": f"{attr_pre}{g}", "labels": L(*labels), "position": i} for i, (g, labels) in enumerate(P["groups"])])

    attrs = []
    for i, a in enumerate(P["attributes"]):
        rec = {"code": f"{attr_pre}{a['code']}", "entity_type": "product", "type": a["type"], "group": f"{attr_pre}{a['group']}",
               "labels": L(*a["labels"]), "position": i, "external_id": f"{attr_pre}{a['code']}"}
        if a.get("units"):
            rec["config"] = {"units": a["units"]}
        if a.get("filterable"):
            rec["is_filterable"] = True
        attrs.append(rec)
    for j, (code, family_code, labels) in enumerate([("images", "product_images", ("Bilder", "Images")),
                                                     ("drawings", "technical_drawings", ("Technische Zeichnungen", "Technical drawings")),
                                                     ("downloads", "downloads", ("Downloads", "Downloads"))]):
        attrs.append({"code": f"{attr_pre}{code}", "entity_type": "product", "type": "asset_collection", "entity_ref": family_code,
                      "group": f"{attr_pre}media", "labels": L(*labels), "position": 20 + j, "external_id": f"{attr_pre}{code}",
                      "config": {"asset_family": family_code}})
    write(out / "attributes.json", attrs)

    write(out / "attribute-options.json", [
        {"attribute": f"{attr_pre}{attr}", "code": code, "labels": L(*labels), "position": i}
        for attr, options in P["options"].items() for i, (code, labels) in enumerate(options)])

    write(out / "families.json", [{"code": family, "labels": L(*P["family"]["labels"]), "label_attribute": "name", "external_id": family}])
    fam_attrs = ["name", "description", "image"] + [f"{attr_pre}{a['code']}" for a in P["attributes"]]
    fam_attrs += [f"{attr_pre}images", f"{attr_pre}drawings", f"{attr_pre}downloads"]
    # demo_has_cad lives in the base (one filter across every pack): products with a STEP model.
    fam_attrs.append("demo_has_cad")
    write(out / "family-attributes.json", [{"family": family, "attribute": a, "position": i, "is_required": a == "name"}
                                           for i, a in enumerate(fam_attrs)])
    v = P["variant"]
    write(out / "family-variants.json", [{"family": family, "code": v["code"], "labels": L(*v["labels"]),
                                          "axes": [f"{attr_pre}{v['axis']}"], "external_id": v["code"]}])
    write(out / "manufacturers.json", [
        {"code": m["code"], "name": m["name"], "legal_name": f"{m['legal_name']} (fictional)", "country": "DE", "city": "Musterstadt",
         "external_id": m["code"], "descriptions": L(*m["about"])} for m in P["makers"]])
    # The logo is a file, so it can only be set after the files step has uploaded it: a second
    # manufacturers step (after files) PUTs just the logo onto the same records.
    write(out / "manufacturer-logos.json", [{"code": m["code"], "logo": f"{m['code']}-LOGO"} for m in P["makers"]])

    # Products: the model's variants are generated from the axis options.
    products, links = [], []
    def product(sku, kind, p, values, de, en, parent=None):
        common = {f"{attr_pre}{k}": val for k, val in values.items()}
        # The main image as a storage key (folder/file, no tenant): what a
        # storefront reads to show the product, next to the asset collection.
        common["image"] = f"sample-data/{pack}/{sku.lower()}.jpg"
        rec = {"sku": sku, "kind": kind, "family": family, "manufacturer": p["maker"], "tax_class": p.get("tax_class", "standard"),
               "enabled": True, "external_id": sku,
               "attribute_values": {"common": common, "locale_specific": {
                   "de-DE": {"name": de, "description": p["text"][0]}, "en-US": {"name": en, "description": p["text"][1]}}}}
        if kind != "simple":
            rec["family_variant"] = v["code"]
        if parent:
            rec["parent"] = parent
        products.append(rec)
        links.append((sku, p["category"]))
    for p in P["products"]:
        if p.get("variants"):
            product(p["sku"], "model", p, p["values"], *p["name"])
            for code, label in p["variants"]:
                vp = {**p, "text": p.get("variant_text", p["text"])}
                de, en = label if isinstance(label, tuple) else (label, label)
                product(f"{p['sku']}-{code.upper()}", "variant", vp, {**p["values"], v["axis"]: code},
                        p["variant_name"][0].format(de), p["variant_name"][1].format(en), parent=p["sku"])
        else:
            product(p["sku"], "simple", p, p["values"], *p["name"])

    # Media: one image per product; drawings, CAD and data sheets as listed.
    assets, media = [], {}
    def asset(code, family_code, file):
        assets.append({"code": code, "family": family_code, "file": f"assets/{file}", "external_id": code})
        return code
    for rec in products:
        sku = rec["sku"]
        images = [asset(f"{sku}-IMG", "product_images", f"images/{sku.lower()}.jpg")]
        # The second image, the product in use (tools/build-scenes.py), when it exists.
        if (out / "assets" / "images" / f"{sku.lower()}-2.jpg").exists():
            images.append(asset(f"{sku}-IMG-2", "product_images", f"images/{sku.lower()}-2.jpg"))
        media.setdefault(sku, {})[f"{attr_pre}images"] = images
    # Automatic drawings (tools/build-drawings.py) for SKUs without a hand-made one.
    hand = set(P.get("drawings", {}).values())
    for rec in products:
        sku = rec["sku"]
        name = sku.lower() + "-drawing"
        if sku in hand or not (out / "assets" / "drawings" / f"{name}.pdf").exists():
            continue
        base = sku + "-DRW"
        media[sku][f"{attr_pre}drawings"] = [asset(f"{base}-PDF", "technical_drawings", f"drawings/{name}.pdf"),
                                             asset(f"{base}-SVG", "technical_drawings", f"drawings/{name}.svg")]
    for name, sku in P.get("drawings", {}).items():
        base = name.upper()
        media[sku][f"{attr_pre}drawings"] = [asset(f"{base}-PDF", "technical_drawings", f"drawings/{name}.pdf"),
                                             asset(f"{base}-SVG", "technical_drawings", f"drawings/{name}.svg")]
    for name, sku in P.get("cad", {}).items():
        media[sku].setdefault(f"{attr_pre}downloads", []).append(asset(f"{name.upper()}-STEP", "downloads", f"cad/{name}.step"))
    for name, sku in P.get("datasheets", {}).items():
        media[sku].setdefault(f"{attr_pre}downloads", []).append(asset(name.upper(), "downloads", f"downloads/{name}.pdf"))
    # Automatic data sheets (tools/build-datasheets.mjs) for parents without a hand-made one. One asset per
    # parent, linked to the parent and to each of its variants.
    hand_sheets = set(P.get("datasheets", {}).values())
    for rec in products:
        sku = rec["sku"]
        name = sku.lower() + "-data-sheet"
        if rec.get("parent") or sku in hand_sheets or not (out / "assets" / "downloads" / f"{name}.pdf").exists():
            continue
        sheet = asset(f"{sku}-DS", "downloads", f"downloads/{name}.pdf")
        for linked in [sku] + [r["sku"] for r in products if r.get("parent") == sku]:
            media[linked].setdefault(f"{attr_pre}downloads", []).append(sheet)
    # Manufacturer logos (tools/build-logos.py): the SVG is the logo, the PNG a raster copy.
    for m in P["makers"]:
        stem = m["code"].lower()
        asset(f"{m['code']}-LOGO", "manufacturer_logos", f"logos/{stem}.svg")
        asset(f"{m['code']}-LOGO-PNG", "manufacturer_logos", f"logos/{stem}.png")
    # Category images (tools/build-categories.py), set after the files step like the logos.
    cat_images = []
    for c in P["categories"]:
        if (out / "assets" / "categories" / f"{c['code'].lower()}.jpg").exists():
            asset(f"{c['code']}-IMG", "category_images", f"categories/{c['code'].lower()}.jpg")
            cat_images.append({"code": c["code"], "values": {"image": f"{c['code']}-IMG"}})
    write(out / "category-images.json", cat_images)
    order = ["images", "drawings", "downloads"]
    for rec in products:
        for key in order:
            if f"{attr_pre}{key}" in media.get(rec["sku"], {}):
                rec["attribute_values"]["common"][f"{attr_pre}{key}"] = media[rec["sku"]][f"{attr_pre}{key}"]
        rec["attribute_values"]["common"]["demo_has_cad"] = rec["sku"] in P.get("cad", {}).values()
    write(out / "products.json", products)
    write(out / "product-categories.json", [{"product": sku, "category": cat, "position": i} for i, (sku, cat) in enumerate(links)])
    write(out / "assets.json", assets)

    write(out / "price-lists.json", [
        {"code": f"{pre}LIST", "name": P["price_lists"]["list"][1], "labels": L(*P["price_lists"]["list"]), "currency": "EUR",
         "status": "active", "priority": 10, "tax_basis": "net", "external_id": f"{pre}LIST"},
        {"code": f"{pre}CONTRACT", "name": P["price_lists"]["contract"][1], "labels": L(*P["price_lists"]["contract"]),
         "organization": "DEMO-C-1001", "currency": "EUR", "status": "active", "priority": 100, "tax_basis": "net",
         "external_id": f"{pre}CONTRACT"}])
    entries = []
    for sku, prices in P["prices"].items():
        for qmin, price in prices:
            entries.append({"sku": sku, "quantity_min": qmin, "unit_price": price})
    write(out / "price-entries.json", [
        {"list": f"{pre}LIST", "entries": entries},
        {"list": f"{pre}CONTRACT", "entries": [{"sku": s, "quantity_min": 1, "unit_price": p} for s, p in P["contract"].items()]}])
    write(out / "stock.json", [{"sku": sku, "location": "main", "on_hand": n, **({"reorder_point": r} if r is not None else {})}
                               for sku, (n, r) in P["stock"].items()])

    write(out / "manifest.json", {"steps": [
        {"name": "categories", "route": "/products/categories", "key": "code", "file": "categories.json",
         "refs": {"parent_id": ref("parent", "/products/categories")}},
        {"name": "attribute groups", "route": "/products/attribute_groups", "key": "code", "file": "attribute-groups.json"},
        {"name": "shared attributes", "mode": "ensure", "route": "/products/attributes", "key": ["entity_type", "code"],
         "file": "../../base/shared-attributes.json"},
        {"name": "attributes", "route": "/products/attributes", "key": ["entity_type", "code"], "file": "attributes.json",
         "refs": {"group_id": ref("group", "/products/attribute_groups")}},
        {"name": "attribute options", "route": "/products/attribute_options", "key": ["attribute_id", "code"], "file": "attribute-options.json",
         "refs": {"attribute_id": ref("attribute", "/products/attributes", where={"entity_type": "product"})}},
        {"name": "family", "route": "/products/families", "key": "code", "file": "families.json"},
        {"name": "family attributes", "route": "/products/family_attributes", "key": ["family_id", "attribute_id"], "file": "family-attributes.json",
         "refs": {"family_id": ref("family", "/products/families"), "attribute_id": ref("attribute", "/products/attributes", where={"entity_type": "product"})}},
        {"name": "family variants", "route": "/products/family_variants", "key": "code", "file": "family-variants.json",
         "refs": {"family_id": ref("family", "/products/families")}},
        {"name": "manufacturers", "route": "/products/manufacturers", "key": "code", "file": "manufacturers.json"},
        {"name": "asset families", "mode": "ensure", "route": "/products/asset_families", "key": "code", "file": "../../base/asset-families.json"},
        {"name": "files", "kind": "files", "folder": f"sample-data/{pack}", "tags": ["revenexx-sample-data", f"pack-{pack}"],
         "route": "/products/assets", "key": ["asset_family_id", "code"], "file": "assets.json",
         "refs": {"asset_family_id": {"field": "family", "route": "/products/asset_families", "key": "code", "in": "body"}}},
        # Only sets the logo (PUT merges). "remove": "with_parent" = not removed on its own: the maker goes with
        # the "manufacturers" step, which remove.sh runs after this one.
        {"name": "manufacturer logos", "route": "/products/manufacturers", "key": "code", "file": "manufacturer-logos.json",
         "remove": "with_parent"},
        # Only sets the category image; the category goes with the "categories" step.
        {"name": "category images", "route": "/products/categories", "key": "code", "file": "category-images.json",
         "remove": "with_parent"},
        {"name": "products", "route": "/products", "key": "sku", "file": "products.json",
         "refs": {"family_id": ref("family", "/products/families"), "manufacturer_id": ref("manufacturer", "/products/manufacturers"),
                  "family_variant_id": ref("family_variant", "/products/family_variants"), "parent_id": ref("parent", "/products", "sku")}},
        {"name": "product categories", "route": "/products/product_categories", "key": ["product_id", "category_id"],
         "file": "product-categories.json",
         "refs": {"product_id": ref("product", "/products", "sku"), "category_id": ref("category", "/products/categories")}},
        {"name": "price lists", "route": "/prices/lists", "key": "code", "file": "price-lists.json",
         "refs": {"organization_id": ref("organization", "/customers/organizations", "customer_number")}},
        {"name": "price entries", "kind": "price_entries", "file": "price-entries.json"},
        {"name": "stock", "kind": "stock", "file": "stock.json"},
    ]})
    prune(out, assets)
    print(f"  packs/{pack}: {len(products)} products, {len(assets)} assets")


if __name__ == "__main__":
    specs = sorted(p.stem for p in (ROOT / "tools" / "packs").glob("*.py"))
    for name in sys.argv[1:] or specs:
        build(name)
    # A pack without a spec is gone: remove its folder too.
    if not sys.argv[1:]:
        for folder in sorted((ROOT / "packs").iterdir()):
            if folder.is_dir() and folder.name not in specs:
                shutil.rmtree(folder)
                print(f"  pruned packs/{folder.name}")
