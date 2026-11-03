"""Write the content pages (base/pages.json, packs/<pack>/pages.json).

Development tool only: the JSON files are committed and the seeder reads only
them. The seeder posts them to the pages app's seed route, which creates a page
only when its slug is free and publishes it at once.

    python3 tools/build-pages.py            # base and every pack
    python3 tools/build-pages.py office     # one scope

Pages are written in German with an English translation. The blocks are the
ones the storefront theme renders (marketing_banner, badge, title_description,
cta, title, text, accordion). Links are plain storefront paths.

Base pages sit at the slugs the theme's footer already links to (/contact,
/legal/...); every pack adds its own landing, about and contact page under
/<pack>. The landing page shows the pack as a shop window: banner with a photo,
promises, category tiles, a product grid, photos in use, the makers, quick
order and the FAQ, filled with the pack's own data. Images point at the storage paths the files
step uploads to (sample-data/<pack>/<file name>). Every page carries meta.sample_data = <scope>, so removal deletes only
pages this data created, never a page of the same slug a tenant wrote.
"""
import json
import re
import sys
from collections import Counter
from urllib.parse import urlencode
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def block(bundle, de=None, en=None, options=None, children=None):
    b = {"bundle": bundle, "props": de or {}}
    if en:
        b["props_i18n"] = {"en": en}
    if options:
        b["options"] = options
    if children:
        b["children"] = children
    return b


def title(de, en, size="h2"):
    return block("title", {"title": de}, {"title": en}, {"size": size})


def text(de, en):
    return block("text", {"text": de}, {"text": en})


def cta(de, en, url, variant="solid"):
    return block("cta", {"label": de}, {"label": en}, {"url": url, "variant": variant, "color": "primary", "size": "lg"})


def banner(badge_de, badge_en, head_de, head_en, desc_de, desc_en, buttons, image=None):
    content = [
        block("badge", {"label": badge_de}, {"label": badge_en}),
        block("title_description", {"headline": head_de, "description": desc_de}, {"headline": head_en, "description": desc_en},
              {"titleSize": "h1", "titleColor": "primary", "descriptionSize": "lg", "descriptionColor": "primary"}),
        *buttons,
    ]
    if image:
        # The banner has no background image; a row puts the photo beside the text (7 + 5 of 12 columns), and the
        # buttons go inline so they sit side by side in the column.
        for b in buttons:
            b["options"]["inlineBlock"] = True
        content = [block("row", options={"gap": "lg"}, children={"content": [
            block("column", options={"width": "7"}, children={"content": content}),
            block("column", options={"width": "5"}, children={"content": [
                block("image", {"filePath": image, "alt": head_de}, {"alt": head_en}, {"maxWidth": "full"})]}),
        ]})]
    # Its default content width is narrow; beside a photo the text and the image need the whole width.
    return block("marketing_banner", options={"contentWidth": "full"} if image else None, children={"content": content})


def faq(items):
    return block("accordion", {"type": "single", "openFirst": True}, children={"items": [
        block("accordion_item", {"label": q_de, "content": a_de}, {"label": q_en, "content": a_en})
        for q_de, q_en, a_de, a_en in items]})


def page(scope, slug, title_de, title_en, blocks):
    return {"slug": slug, "title": title_de, "bundle": "standard", "sourceLanguage": "de",
            "translations": [{"langcode": "en", "title": title_en, "slug": slug}],
            "meta": {"sample_data": scope}, "blocks": blocks}


SAMPLE_DE = "Beispieldaten"
SAMPLE_EN = "Sample data"
NOTE_DE = ("<p><em>Diese Seite gehört zu den revenexx-Beispieldaten. Shop, Firmen, Marken und Produkte sind erfunden. "
           "Ersetzen oder löschen Sie sie, bevor Ihr Shop live geht.</em></p>")
NOTE_EN = ("<p><em>This page is part of the revenexx sample data. The shop, companies, brands and products are fictional. "
           "Replace or delete it before your shop goes live.</em></p>")
PLACEHOLDER_DE = "<p><strong>Platzhalter.</strong> Kein gültiger Rechtstext: ersetzen Sie ihn durch Ihren eigenen, bevor Ihr Shop live geht.</p>"
PLACEHOLDER_EN = "<p><strong>Placeholder.</strong> Not a valid legal text: replace it with your own before your shop goes live.</p>"


# ---- base: the pages the theme's footer links to -------------------------------------------

def base_pages():
    s = "base"
    return [
        page(s, "contact", "Kontakt", "Contact", [
            title("Kontakt", "Contact", "h1"),
            text("<p>Fragen zu einem Angebot, einer Bestellung oder Ihrem Firmenkonto? Schreiben Sie uns, wir antworten "
                 "werktags innerhalb eines Tages.</p>"
                 "<p>E-Mail: <a href=\"mailto:kontakt@beispiel-shop.example\">kontakt@beispiel-shop.example</a><br>"
                 "Telefon: +49 000 0000000 (Platzhalter)<br>Montag bis Freitag, 8 bis 17 Uhr</p>",
                 "<p>Questions about a quote, an order or your company account? Write to us; we answer within one "
                 "working day.</p>"
                 "<p>Email: <a href=\"mailto:kontakt@beispiel-shop.example\">kontakt@beispiel-shop.example</a><br>"
                 "Phone: +49 000 0000000 (placeholder)<br>Monday to Friday, 8 am to 5 pm</p>"),
            text(NOTE_DE, NOTE_EN),
        ]),
        page(s, "legal/imprint", "Impressum", "Imprint", [
            title("Impressum", "Imprint", "h1"),
            text(PLACEHOLDER_DE, PLACEHOLDER_EN),
            text("<p>[Firmenname]<br>[Straße und Hausnummer]<br>[PLZ und Ort]<br>Deutschland</p>"
                 "<p>Vertreten durch: [Geschäftsführung]<br>Registergericht: [Amtsgericht], [Registernummer]<br>"
                 "USt-IdNr.: [Umsatzsteuer-Identifikationsnummer]</p>"
                 "<p>E-Mail: kontakt@beispiel-shop.example</p>",
                 "<p>[Company name]<br>[Street and number]<br>[Postcode and town]<br>Germany</p>"
                 "<p>Represented by: [Managing directors]<br>Register court: [Local court], [Register number]<br>"
                 "VAT ID: [VAT identification number]</p>"
                 "<p>Email: kontakt@beispiel-shop.example</p>"),
        ]),
        page(s, "legal/terms", "Allgemeine Geschäftsbedingungen", "Terms and conditions", [
            title("Allgemeine Geschäftsbedingungen", "Terms and conditions", "h1"),
            text(PLACEHOLDER_DE, PLACEHOLDER_EN),
            text("<h3>1. Geltungsbereich</h3><p>[Für wen und welche Bestellungen diese Bedingungen gelten. Dieser Shop "
                 "richtet sich an Unternehmen.]</p>"
                 "<h3>2. Vertragsschluss</h3><p>[Wann ein Vertrag zustande kommt, z. B. mit der Auftragsbestätigung.]</p>"
                 "<h3>3. Preise und Zahlung</h3><p>[Nettopreise zzgl. Umsatzsteuer, Zahlungsziel, Zahlung auf Rechnung.]</p>"
                 "<h3>4. Lieferung</h3><p>[Lieferzeiten, Versandkosten, Gefahrübergang.]</p>"
                 "<h3>5. Gewährleistung</h3><p>[Ihre Regelung.]</p>",
                 "<h3>1. Scope</h3><p>[Whom and which orders these terms apply to. This shop serves businesses.]</p>"
                 "<h3>2. Conclusion of contract</h3><p>[When a contract is made, e.g. with the order confirmation.]</p>"
                 "<h3>3. Prices and payment</h3><p>[Net prices plus VAT, payment term, payment by invoice.]</p>"
                 "<h3>4. Delivery</h3><p>[Delivery times, shipping costs, transfer of risk.]</p>"
                 "<h3>5. Warranty</h3><p>[Your terms.]</p>"),
        ]),
        page(s, "legal/privacy", "Datenschutz", "Privacy policy", [
            title("Datenschutzerklärung", "Privacy policy", "h1"),
            text(PLACEHOLDER_DE, PLACEHOLDER_EN),
            text("<h3>Verantwortlicher</h3><p>[Firmenname, Anschrift, E-Mail]</p>"
                 "<h3>Welche Daten wir verarbeiten</h3><p>[Kontodaten, Bestelldaten, Server-Logs, Cookies.]</p>"
                 "<h3>Zwecke und Rechtsgrundlagen</h3><p>[Vertragserfüllung, berechtigtes Interesse, Einwilligung.]</p>"
                 "<h3>Ihre Rechte</h3><p>[Auskunft, Berichtigung, Löschung, Widerspruch, Beschwerde bei der Aufsichtsbehörde.]</p>",
                 "<h3>Controller</h3><p>[Company name, address, email]</p>"
                 "<h3>What data we process</h3><p>[Account data, order data, server logs, cookies.]</p>"
                 "<h3>Purposes and legal bases</h3><p>[Performance of contract, legitimate interest, consent.]</p>"
                 "<h3>Your rights</h3><p>[Access, rectification, erasure, objection, complaint to the supervisory authority.]</p>"),
        ]),
        page(s, "legal/cookies", "Cookies", "Cookies", [
            title("Cookie-Richtlinie", "Cookie policy", "h1"),
            text(PLACEHOLDER_DE, PLACEHOLDER_EN),
            text("<p>[Welche Cookies der Shop setzt, wozu, wie lange, und wie Besucher ihre Einwilligung ändern.]</p>",
                 "<p>[Which cookies the shop sets, what for, for how long, and how visitors change their consent.]</p>"),
        ]),
    ]


# ---- packs -------------------------------------------------------------------------------------

PACKS = {
    "industrial": {
        "root": "DEMO-IND",
        "pitch": ("Werkzeug, Befestigung und Arbeitsschutz für Werkstatt und Fertigung, mit Staffelpreisen und Lieferung "
                  "ab Lager.",
                  "Tools, fasteners and safety gear for workshop and production, with quantity prices and delivery "
                  "from stock."),
        "story": ("<p>Wir beliefern Werkstätten, Instandhaltung und Fertigungsbetriebe mit allem, was täglich gebraucht "
                  "wird: vom Akku-Bohrschrauber bis zur Schraube, vom Schleifmittel bis zur Schutzbrille.</p>"
                  "<p>Unsere Eigenmarken <strong>Brakkwerk</strong> (Elektrowerkzeug und Werkstattausstattung) und "
                  "<strong>Hartfell</strong> (Arbeitsschutz und Verbrauchsmaterial) sind auf den harten Alltag im "
                  "Betrieb ausgelegt.</p>",
                  "<p>We supply workshops, maintenance teams and production sites with what they use every day: from "
                  "the cordless drill to the screw, from abrasives to safety glasses.</p>"
                  "<p>Our own brands <strong>Brakkwerk</strong> (power tools and workshop equipment) and "
                  "<strong>Hartfell</strong> (safety and consumables) are built for daily use on the shop floor.</p>"),
        "mail": "werkstatt@beispiel-shop.example",
    },
    "electrical": {
        "root": "DEMO-ELE",
        "pitch": ("Kabel, Schalter, Leuchten und Verteilertechnik für Elektroinstallateure, mit Projektpreisen und "
                  "Lieferung auf die Baustelle.",
                  "Cables, switches, lighting and distribution gear for electricians, with project prices and "
                  "delivery to the site."),
        "story": ("<p>Wir sind Großhändler für Elektroinstallation: Installationskabel, Schalterprogramme, Leuchtmittel, "
                  "Schutzgeräte und das Werkzeug, mit dem sie montiert werden.</p>"
                  "<p>Unsere Eigenmarken <strong>Kabelfux</strong> (Kabel und Installationsmaterial) und "
                  "<strong>Hellgrund</strong> (Licht und Schalter) liefern wir ab Lager in ganzen Ringen und "
                  "Verpackungseinheiten.</p>",
                  "<p>We are an electrical wholesaler: installation cable, switch ranges, lamps, protective devices "
                  "and the tools to fit them.</p>"
                  "<p>Our own brands <strong>Kabelfux</strong> (cable and installation material) and "
                  "<strong>Hellgrund</strong> (lighting and switches) ship from stock in full coils and packs.</p>"),
        "mail": "elektro@beispiel-shop.example",
    },
    "office": {
        "root": "DEMO-OFF",
        "pitch": ("Papier, Schreibwaren, Büro- und Pausenraumbedarf für Unternehmen, auf Rechnung und mit "
                  "Kostenstellen.",
                  "Paper, stationery, office and breakroom supplies for businesses, on invoice and with cost "
                  "centres."),
        "story": ("<p>Wir versorgen Büros, Praxen und Verwaltungen mit Verbrauchsmaterial: Papier und Ablage, "
                  "Schreibwaren, Reinigungs- und Pausenraumbedarf, Versandmaterial.</p>"
                  "<p>Unsere Eigenmarken <strong>Klarbüro</strong> (Schreibtisch und Ablage) und <strong>Folianta</strong> "
                  "(Papier und Versand) gibt es in Mengen, die zu einem Büro passen.</p>",
                  "<p>We supply offices, practices and administrations with consumables: paper and filing, stationery, "
                  "cleaning and breakroom supplies, mailing material.</p>"
                  "<p>Our own brands <strong>Klarbüro</strong> (desk and filing) and <strong>Folianta</strong> "
                  "(paper and mailing) come in quantities that suit an office.</p>"),
        "mail": "buero@beispiel-shop.example",
    },
    "lab": {
        "root": "DEMO-LAB",
        "pitch": ("Geräte, Pipetten, Glaswaren und Verbrauchsmaterial für Labore in Forschung, Analytik und "
                  "Qualitätssicherung.",
                  "Instruments, pipettes, glassware and consumables for labs in research, analytics and quality "
                  "control."),
        "story": ("<p>Wir beliefern Labore in Forschung, Analytik und Qualitätssicherung: Laborgeräte, Pipetten und "
                  "Spitzen, Glaswaren, Verbrauchsmaterial und Laborsicherheit.</p>"
                  "<p>Unsere Eigenmarken <strong>Probara</strong> (Geräte und Glaswaren) und <strong>Pipetrix</strong> "
                  "(Pipetten und Spitzen) gibt es in Packungsgrößen für den Laboralltag.</p>",
                  "<p>We supply labs in research, analytics and quality control: instruments, pipettes and tips, "
                  "glassware, consumables and lab safety.</p>"
                  "<p>Our own brands <strong>Probara</strong> (instruments and glassware) and <strong>Pipetrix</strong> "
                  "(pipettes and tips) come in pack sizes made for daily lab work.</p>"),
        "mail": "labor@beispiel-shop.example",
    },
}

# Answers that hold for every pack, because the base sets them up: the list price
# list has quantity breaks, the buyer company has contract prices and net 30, the
# automatic promotion takes 5 % off from 100 EUR, shipping is priced by weight.
FAQ = [
    ("Gibt es Staffelpreise?", "Are there quantity prices?",
     "<p>Ja. Ab bestimmten Mengen sinkt der Stückpreis; Firmenkunden mit Rahmenvertrag sehen ihre Vertragspreise.</p>",
     "<p>Yes. The unit price drops at set quantities; company customers with a contract see their contract prices.</p>"),
    ("Kann ich auf Rechnung bestellen?", "Can I pay on invoice?",
     "<p>Ja, Firmenkunden zahlen auf Rechnung mit 30 Tagen Zahlungsziel.</p>",
     "<p>Yes, company customers pay on invoice with 30 days' payment terms.</p>"),
    ("Was kostet der Versand?", "What does shipping cost?",
     "<p>Die Versandkosten richten sich nach dem Gewicht der Bestellung und werden im Warenkorb angezeigt.</p>",
     "<p>Shipping is priced by the weight of the order and shown in the cart.</p>"),
    ("Gibt es Rabatte?", "Are there discounts?",
     "<p>Ab 100 € Bestellwert ziehen wir automatisch 5 % ab. Gutscheincodes lösen Sie im Warenkorb ein.</p>",
     "<p>From an order value of 100 € we take 5 % off automatically. Redeem voucher codes in the cart.</p>"),
]


def subcategories(pack, root):
    cats = json.loads((ROOT / "packs" / pack / "categories.json").read_text(encoding="utf-8"))
    return [(c["code"], c["labels"]["de-DE"], c["labels"]["en-US"]) for c in cats if c.get("parent") == root]


def category_tiles(pack, root, subs):
    """The subcategories as photo tiles, three to a row, each linking to its category."""
    files = asset_files(pack)
    images = {c["code"]: c["values"]["image"]
              for c in json.loads((ROOT / "packs" / pack / "category-images.json").read_text(encoding="utf-8"))}
    tiles = [block("column", options={"width": "4"}, children={"content": [
        block("image_teaser", {"filePath": files[images[code]], "alt": de, "headline": de, "description": "Zur Kategorie"},
              {"alt": en, "headline": en, "description": "Go to the category"},
              {"url": f"/category/{root}/{code}", "ratio": "4x3", "showText": True, "textColor": "light"})]})
        for code, de, en in subs if code in images]
    return [block("row", options={"gap": "lg"}, children={"content": tiles[i:i + 3]}) for i in range(0, len(tiles), 3)]


def varied(pack, subs):
    """The subcategories without variants (a grid of one glove in S, M and L shows the same photo four times),
    most varied first: the share of different kinds of thing among their products (electrical's cables are five
    sizes of one cable). The search index decides the grid's order and ignores the price sort, so the category is
    the only lever."""
    load = lambda f: json.loads((ROOT / "packs" / pack / f).read_text(encoding="utf-8"))
    products = {p["sku"]: p for p in load("products.json")}
    links = load("product-categories.json")
    kind = lambda sku: products[sku]["attribute_values"]["locale_specific"]["de-DE"]["name"].split()[0].rstrip(",")
    score = {}
    for code, _, _ in subs:
        skus = [l["product"] for l in links if l["category"] == code]
        if skus and all(products[sku]["kind"] == "simple" for sku in skus):
            score[code] = len({kind(sku) for sku in skus}) / len(skus)
    return sorted(score, key=score.get, reverse=True)


def maker_cards(pack):
    """The pack's own makers as cards: logo, what they make, the item count and a link to their products. The
    theme's brand grid cannot filter by pack, so on electrical it showed one own maker and three foreign ones
    (owner's pick A, 2026-11-02)."""
    load = lambda f: json.loads((ROOT / "packs" / pack / f).read_text(encoding="utf-8"))
    files = asset_files(pack)
    logos = {l["code"]: l["logo"] for l in load("manufacturer-logos.json")}
    counts = Counter(p["manufacturer"] for p in load("products.json"))
    trim = lambda text, pattern: (lambda t: t[0].upper() + t[1:])(re.sub(pattern, "", text))  # "Hersteller von …"
    cards = []
    for m in load("manufacturers.json"):
        name, n = m["name"], counts[m["code"]]
        logo = files[f"{logos[m['code']]}-CARD"]
        what_de = trim(m["descriptions"]["de-DE"], r"^Fiktive[rn]? | \(Beispieldaten\)\.$")
        what_en = trim(m["descriptions"]["en-US"], r"^Fictional | \(sample data\)\.$")
        search = "/search?" + urlencode({"q": name, "manufacturer": name})
        cards.append(block("column", options={"width": "4"}, children={"content": [
            # Full column width (a third of the row): the image block centres anything narrower, and the text and
            # button sit on the left. The link is a cta, not a link in the text: only the cta gets the storefront's
            # language prefix (/de/...).
            block("image", {"filePath": logo, "alt": name}, {"alt": name}, {"maxWidth": "full"}),
            text(f"<p>{what_de} · {n} Artikel</p>", f"<p>{what_en} · {n} items</p>"),
            cta(f"Alle Produkte von {name}", f"All products by {name}", search, "outline"),
        ]}))
    return [block("spacer", options={"size": "lg"}), title("Unsere Marken", "Our makers"),
            block("row", options={"gap": "lg"}, children={"content": cards}), block("spacer", options={"size": "lg"})]


def promises(pack):
    """A row of four icon labels under the banner, with the pack's own numbers: stock, quantity prices, invoice,
    technical documents. Every product has photos; most have a data sheet, many a drawing and some a CAD model."""
    load = lambda f: json.loads((ROOT / "packs" / pack / f).read_text(encoding="utf-8"))
    tiers = [e for pl in load("price-entries.json") for e in pl["entries"] if e["quantity_min"] > 1]
    tiered, from_qty = len({e["sku"] for e in tiers}), min(e["quantity_min"] for e in tiers)
    codes = [a["code"] for a in load("assets.json")]
    sheets = sum(c.endswith("-DS") for c in codes)
    cad = sum(a["file"].startswith("assets/cad/") for a in load("assets.json"))
    docs_de = f"{sheets} Datenblätter" + (f", {cad} CAD-Dateien" if cad else "")
    docs_en = f"{sheets} data sheets" + (f", {cad} CAD files" if cad else "")
    items = [
        ("delivery", "Ab Lager", "From stock", "Lieferung in 1–2 Werktagen", "Delivery in 1–2 working days"),
        ("offer", "Staffelpreise", "Quantity prices", f"für {tiered} Artikel, ab {from_qty} Stück",
         f"on {tiered} items, from {from_qty} pieces"),
        ("payment", "Auf Rechnung", "On invoice", "30 Tage Zahlungsziel", "30 days' payment terms"),
        ("file", "Technische Unterlagen", "Technical documents", docs_de, docs_en),
    ]
    return block("row", options={"gap": "md"}, children={"content": [
        block("column", options={"width": "3"}, children={"content": [
            block("icon_label", {"heading": h_de, "label": l_de}, {"heading": h_en, "label": l_en}, {"icon": icon})]})
        for icon, h_de, h_en, l_de, l_en in items]})


def in_use(pack, root, subs):
    """The second product photos (the product in use, close up) as four square tiles in a row, one product from
    each of four subcategories, each linking to its category. A full-width slider of them was the first try; the
    owner disliked it (2026-11-02): one blurred close-up filled the screen."""
    load = lambda f: json.loads((ROOT / "packs" / pack / f).read_text(encoding="utf-8"))
    files = asset_files(pack)
    products = {p["sku"]: p for p in load("products.json")}
    links = sorted(load("product-categories.json"), key=lambda l: l["position"])
    slides = []
    for code, de, en in subs:
        sku = next((l["product"] for l in links if l["category"] == code and f"{l['product']}-IMG-2" in files
                    and products[l["product"]]["kind"] == "simple"), None)
        if not sku:
            continue
        names = products[sku]["attribute_values"]["locale_specific"]
        name_de, name_en = names["de-DE"]["name"], names["en-US"]["name"]
        slides.append(block("column", options={"width": "3"}, children={"content": [
            block("image_teaser", {"filePath": files[f"{sku}-IMG-2"], "alt": name_de, "headline": de,
                                   "description": name_de},
                  {"alt": name_en, "headline": en, "description": name_en},
                  {"url": f"/category/{root}/{code}", "ratio": "1x1", "showText": True, "textColor": "light"})]}))
        if len(slides) == 4:
            break
    return [block("spacer", options={"size": "lg"}), title("Aus der Praxis", "In practice"),
            block("row", options={"gap": "md"}, children={"content": slides})]


def pack_pages(pack):
    P = PACKS[pack]
    root = P["root"]
    cats = json.loads((ROOT / "packs" / pack / "categories.json").read_text(encoding="utf-8"))
    name_de, name_en = next((c["labels"]["de-DE"], c["labels"]["en-US"]) for c in cats if c["code"] == root)
    subs = subcategories(pack, root)
    pitch_de, pitch_en = P["pitch"]
    story_de, story_en = P["story"]
    mail = P["mail"]
    top = varied(pack, subs)[0]
    root_image = next(c["values"]["image"] for c in json.loads(
        (ROOT / "packs" / pack / "category-images.json").read_text(encoding="utf-8")) if c["code"] == root)
    sub_label = {code: de for code, de, _ in subs}
    s = pack
    return [
        page(s, pack, name_de, name_en, [
            banner(SAMPLE_DE, SAMPLE_EN, name_de, name_en, pitch_de, pitch_en, [
                cta("Zum Sortiment", "Browse the range", f"/category/{root}"),
                cta("Über uns", "About us", f"/{pack}/about", "outline"),
            ], image=asset_files(pack)[root_image]),
            promises(pack),
            block("spacer", options={"size": "md"}),
            # Shop window (owner's pick L1, 2026-11-01, after "das soll ne landing page sein? das ist schon sehr
            # schwach" about a banner, a list of links and the FAQ): the subcategories as photo tiles, popular
            # products, the makers, then the FAQ.
            title("Unser Sortiment", "Our range"),
            *category_tiles(pack, root, subs),
            block("product_grid", options={"category": json.dumps({"slug": top, "label": sub_label[top]},
                                                                  ensure_ascii=False),
                                           "title": "Beliebt", "rows": "1", "perRow": "4", "buttonAction": "order",
                                           "sort": "relevance"}),
            *in_use(pack, root, subs),
            *maker_cards(pack),
            block("quick_order", options={"icon": "keyboard"}),
            block("spacer", options={"size": "lg"}),
            title("Häufige Fragen", "Frequently asked questions"),
            faq(FAQ),
            cta("Kontakt aufnehmen", "Get in touch", f"/{pack}/contact", "outline"),
        ]),
        page(s, f"{pack}/about", f"Über uns: {name_de}", f"About us: {name_en}", [
            title("Über uns", "About us", "h1"),
            text(story_de, story_en),
            cta("Zum Sortiment", "Browse the range", f"/category/{root}"),
            text(NOTE_DE, NOTE_EN),
        ]),
        page(s, f"{pack}/contact", f"Kontakt: {name_de}", f"Contact: {name_en}", [
            title("Kontakt", "Contact", "h1"),
            text(f"<p>Ihr Ansprechpartner für {name_de}: schreiben Sie an "
                 f"<a href=\"mailto:{mail}\">{mail}</a>, oder rufen Sie an unter +49 000 0000000 (Platzhalter), "
                 "Montag bis Freitag, 8 bis 17 Uhr.</p>"
                 "<p>Für Angebote über größere Mengen nennen Sie uns Artikelnummern und Mengen; wir antworten innerhalb "
                 "eines Werktags.</p>",
                 f"<p>Your contact for {name_en.lower()}: write to <a href=\"mailto:{mail}\">{mail}</a>, or call "
                 "+49 000 0000000 (placeholder), Monday to Friday, 8 am to 5 pm.</p>"
                 "<p>For quotes on larger quantities, send us item numbers and quantities; we answer within one "
                 "working day.</p>"),
            text(NOTE_DE, NOTE_EN),
        ]),
    ]


# ---- files ------------------------------------------------------------------------------------

def asset_files(pack):
    """code -> storage path of every file the pack uploads (folder sample-data/<pack>, original name)."""
    assets = json.loads((ROOT / "packs" / pack / "assets.json").read_text(encoding="utf-8"))
    return {a["code"]: f"sample-data/{pack}/{Path(a['file']).name}" for a in assets}


def write(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  {path.relative_to(ROOT)}: {len(data)} pages")


if __name__ == "__main__":
    for scope in sys.argv[1:] or ["base", *PACKS]:
        if scope == "base":
            write(ROOT / "base" / "pages.json", base_pages())
        elif scope in PACKS:
            write(ROOT / "packs" / scope / "pages.json", pack_pages(scope))
        else:
            sys.exit(f"unknown scope '{scope}' (have: base, {', '.join(PACKS)})")
