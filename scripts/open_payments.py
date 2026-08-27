#!/usr/bin/env python3
"""Query CMS Open Payments (Sunshine Act) general payments by manufacturer/product.

Stdlib only, no key. https://openpaymentsdata.cms.gov

Discovery:
    python3 open_payments.py --discover 2025
Query and summarise:
    python3 open_payments.py --dataset-id <id> --manufacturer "Eli Lilly" \
        --product MOUNJARO --summarise

Cadence: full prior program year published on or before 30 June, refreshed each
January. This is a STRUCTURAL signal, not a tradeable one.
"""
import argparse, collections, json, sys, urllib.parse, urllib.request

from _ua import user_agent

BASE = "https://openpaymentsdata.cms.gov"
UA = user_agent("open-payments")


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode("utf-8"))


def discover(year):
    url = f"{BASE}/api/1/search/?fulltext={urllib.parse.quote('General Payment Data ' + str(year))}"
    res = get(url)
    out = []
    for _, ds in (res.get("results") or {}).items():
        for dist in ds.get("distribution", []) or []:
            out.append({"title": ds.get("title"), "dataset_id": dist.get("identifier")})
    return out


def query(dataset_id, conditions, limit, max_rows):
    rows, offset = [], 0
    while offset < max_rows:
        params = {"limit": str(limit), "offset": str(offset)}
        for i, (prop, op, val) in enumerate(conditions):
            params[f"conditions[{i}][property]"] = prop
            params[f"conditions[{i}][operator]"] = op
            params[f"conditions[{i}][value]"] = val
        url = f"{BASE}/api/1/datastore/query/{dataset_id}/0?" + urllib.parse.urlencode(params)
        batch = get(url).get("results") or []
        rows.extend(batch)
        if len(batch) < limit:
            break
        offset += limit
    return rows


NATURE_MEANING = {
    "compensation for services other than consulting": "promotional push (speaker programmes)",
    "consulting fee": "advisory-board work; leads promotional spend by 2-4 quarters",
    "food and beverage": "detailing intensity / rep activity proxy",
    "travel and lodging": "mixed",
    "grant": "may be medical affairs, not commercial -- do not read as promotional",
}


def summarise(rows):
    by_nature = collections.defaultdict(float)
    recipients = set()
    total = 0.0
    for r in rows:
        try:
            amt = float(r.get("total_amount_of_payment_usdollars") or 0)
        except ValueError:
            amt = 0.0
        total += amt
        nature = (r.get("nature_of_payment_or_transfer_of_value") or "unknown").lower()
        by_nature[nature] += amt
        rid = r.get("covered_recipient_profile_id") or r.get("covered_recipient_npi")
        if rid:
            recipients.add(rid)
    n = len(recipients)
    return {
        "total_usd": round(total, 2),
        "distinct_recipients": n,
        "usd_per_recipient": round(total / n, 2) if n else None,
        "by_nature": [{"nature": k, "usd": round(v, 2), "reads_as": NATURE_MEANING.get(k, "")}
                      for k, v in sorted(by_nature.items(), key=lambda x: -x[1])],
        "reading": "Count recipients, not just dollars: breadth tracks sales-force reach. "
                   "Rising usd_per_recipient with falling recipient count = programme "
                   "narrowing to a core KOL group. Benchmark against a named analogue "
                   "launch -- absolute dollars mean nothing alone.",
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--discover", metavar="YEAR")
    ap.add_argument("--dataset-id")
    ap.add_argument("--manufacturer")
    ap.add_argument("--product")
    ap.add_argument("--limit", type=int, default=5000)
    ap.add_argument("--max-rows", type=int, default=200000)
    ap.add_argument("--summarise", action="store_true")
    a = ap.parse_args()

    if a.discover:
        json.dump(discover(a.discover), sys.stdout, indent=2); print(); return
    if not a.dataset_id or not (a.manufacturer or a.product):
        ap.error("--dataset-id and one of --manufacturer / --product are required")

    cond = []
    if a.manufacturer:
        cond.append(("applicable_manufacturer_or_applicable_gpo_making_payment_name",
                     "contains", a.manufacturer))
    if a.product:
        cond.append(("name_of_drug_or_biological_or_device_or_medical_supply_1",
                     "contains", a.product))

    rows = query(a.dataset_id, cond, a.limit, a.max_rows)
    if not rows:
        sys.stderr.write("NO ROWS. Check manufacturer legal entity name (it is often "
                         "not the ticker name) and product spelling.\n")
        sys.exit(2)
    sys.stderr.write(f"rows={len(rows)}\n")
    json.dump(summarise(rows) if a.summarise else rows, sys.stdout, indent=2); print()


if __name__ == "__main__":
    main()
