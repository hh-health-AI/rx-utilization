#!/usr/bin/env python3
"""Query Medicare Part D Prescribers by Provider and Drug (data.cms.gov).

Stdlib only, no key.

Discovery:
    python3 partd_prescribers.py --discover
Query:
    python3 partd_prescribers.py --dataset-id <uuid> --brand ELIQUIS --format csv
    python3 partd_prescribers.py --dataset-id <uuid> --brand ELIQUIS --summarise

Caveats: annual file, ~5 month lag, Medicare only, counts under 11 suppressed.
Claim counts are not revenue.
"""
import argparse, collections, csv, json, sys, urllib.parse, urllib.request

from _ua import user_agent

BASE = "https://data.cms.gov"
UA = user_agent("partd-prescribers")


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def discover():
    cat = get(f"{BASE}/data.json")
    out = []
    for ds in cat.get("dataset", []):
        t = ds.get("title", "")
        if "Part D Prescribers" in t:
            ident = ds.get("identifier", "")
            out.append({"title": t, "identifier": ident, "modified": ds.get("modified")})
    return out


def fetch(dataset_id, filters, size, max_rows):
    rows, offset = [], 0
    while offset < max_rows:
        params = {"size": str(size), "offset": str(offset)}
        for k, v in filters.items():
            params[f"filter[{k}]"] = v
        url = f"{BASE}/data-api/v1/dataset/{dataset_id}/data?" + urllib.parse.urlencode(params)
        batch = get(url)
        if not isinstance(batch, list) or not batch:
            break
        rows.extend(batch)
        if len(batch) < size:
            break
        offset += size
    return rows


def summarise(rows):
    def num(r, *keys):
        for k in keys:
            v = r.get(k)
            if v not in (None, "", "*"):
                try:
                    return float(v)
                except ValueError:
                    pass
        return 0.0

    by_spec = collections.Counter()
    claims_by_npi = collections.Counter()
    total = 0.0
    for r in rows:
        c = num(r, "Tot_Clms", "total_claim_count")
        total += c
        npi = r.get("Prscrbr_NPI") or r.get("npi")
        claims_by_npi[npi] += c
        spec = r.get("Prscrbr_Type") or r.get("specialty_description") or "unknown"
        by_spec[spec] += c
    n = len(claims_by_npi)
    ranked = sorted(claims_by_npi.values(), reverse=True)
    top_decile = sum(ranked[:max(1, n // 10)])
    return {
        "prescribers": n,
        "total_claims": round(total, 1),
        "claims_per_prescriber": round(total / n, 2) if n else 0,
        "top_decile_share_of_claims": round(top_decile / total, 3) if total else None,
        "top_specialties": by_spec.most_common(10),
        "reading": "Rising prescriber count with flat claims-per-prescriber = broadening "
                   "(durable). Flat count with rising claims-per-prescriber = deepening "
                   "(fragile, caps peak sales). Top-decile share >0.60 = concentration risk.",
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--discover", action="store_true")
    ap.add_argument("--dataset-id")
    ap.add_argument("--brand", help="brand name as CMS spells it, upper case")
    ap.add_argument("--generic", help="generic name")
    ap.add_argument("--state")
    ap.add_argument("--size", type=int, default=5000)
    ap.add_argument("--max-rows", type=int, default=100000)
    ap.add_argument("--summarise", action="store_true")
    ap.add_argument("--format", choices=["json", "csv"], default="json")
    a = ap.parse_args()

    if a.discover:
        json.dump(discover(), sys.stdout, indent=2); print(); return
    if not a.dataset_id or not (a.brand or a.generic):
        ap.error("--dataset-id and one of --brand / --generic are required")

    f = {}
    if a.brand:
        f["Brnd_Name"] = a.brand.upper()
    if a.generic:
        f["Gnrc_Name"] = a.generic.upper()
    if a.state:
        f["Prscrbr_State_Abrvtn"] = a.state.upper()

    rows = fetch(a.dataset_id, f, a.size, a.max_rows)
    if not rows:
        sys.stderr.write("NO ROWS. Check spelling of the brand as CMS records it "
                         "(and the year of the dataset) before concluding anything.\n")
        sys.exit(2)
    sys.stderr.write(f"rows={len(rows)}\n")

    if a.summarise:
        json.dump(summarise(rows), sys.stdout, indent=2); print(); return
    if a.format == "csv":
        w = csv.DictWriter(sys.stdout, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    else:
        json.dump(rows, sys.stdout, indent=2); print()


if __name__ == "__main__":
    main()
