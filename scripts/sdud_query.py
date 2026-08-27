#!/usr/bin/env python3
"""Query CMS Medicaid State Drug Utilization Data (SDUD) from data.medicaid.gov.

Stdlib only. No API key required.

Discovery:
    python3 sdud_query.py --discover 2023
Query by NDC:
    python3 sdud_query.py --dataset-id <id> --ndc 00002143380 --format csv
Query by product name (label search, slower and fuzzier):
    python3 sdud_query.py --dataset-id <id> --product MOUNJARO

Notes
-----
* One SDUD dataset exists per calendar year; distribution IDs change when CMS
  reposts. Always run --discover for the year you need rather than hardcoding.
* Cells with fewer than 11 prescriptions are suppressed. This script reports the
  count of suppressed rows separately -- do not compute a growth rate without it.
* Files cover Fee-For-Service and Managed Care. Check the 'utilization_type'
  column (FFSU / MCOU) and state which you used.
"""
import argparse, csv, json, sys, urllib.parse, urllib.request

from _ua import user_agent

BASE = "https://data.medicaid.gov"
UA = user_agent("sdud-query")


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def discover(year):
    url = f"{BASE}/api/1/search/?fulltext={urllib.parse.quote('State Drug Utilization Data ' + str(year))}"
    res = get(url)
    out = []
    for _, ds in (res.get("results") or {}).items():
        title = ds.get("title", "")
        for dist in ds.get("distribution", []) or []:
            out.append({"title": title,
                        "dataset_id": dist.get("identifier"),
                        "modified": ds.get("modified")})
    return out


def query(dataset_id, conditions, limit, offset):
    params = {"limit": str(limit), "offset": str(offset)}
    for i, (prop, op, val) in enumerate(conditions):
        params[f"conditions[{i}][property]"] = prop
        params[f"conditions[{i}][operator]"] = op
        params[f"conditions[{i}][value]"] = val
    url = f"{BASE}/api/1/datastore/query/{dataset_id}/0?" + urllib.parse.urlencode(params)
    return get(url)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--discover", metavar="YEAR", help="list dataset ids for a year and exit")
    ap.add_argument("--dataset-id")
    ap.add_argument("--ndc", help="NDC-11, digits only")
    ap.add_argument("--product", help="product name substring (case-insensitive)")
    ap.add_argument("--state", help="two-letter state code, or XX for national row")
    ap.add_argument("--utilization-type", choices=["FFSU", "MCOU"],
                    help="fee-for-service or managed care; omit for both")
    ap.add_argument("--limit", type=int, default=5000)
    ap.add_argument("--max-rows", type=int, default=50000)
    ap.add_argument("--format", choices=["json", "csv"], default="json")
    a = ap.parse_args()

    if a.discover:
        json.dump(discover(a.discover), sys.stdout, indent=2)
        print()
        return

    if not a.dataset_id or not (a.ndc or a.product):
        ap.error("--dataset-id and one of --ndc / --product are required")

    cond = []
    if a.ndc:
        cond.append(("ndc", "=", a.ndc))
    if a.product:
        cond.append(("product_name", "contains", a.product.upper()))
    if a.state:
        cond.append(("state", "=", a.state.upper()))
    if a.utilization_type:
        cond.append(("utilization_type", "=", a.utilization_type))

    rows, offset = [], 0
    while offset < a.max_rows:
        res = query(a.dataset_id, cond, a.limit, offset)
        batch = res.get("results") or []
        rows.extend(batch)
        if len(batch) < a.limit:
            break
        offset += a.limit

    if not rows:
        sys.stderr.write("NO ROWS RETURNED. This is not evidence of zero utilisation -- "
                         "check the dataset id, the NDC format (11 digits, no dashes) "
                         "and the year before reporting anything.\n")
        sys.exit(2)

    suppressed = sum(1 for r in rows
                     if str(r.get("suppression_used", "")).lower() in ("true", "1", "yes"))
    sys.stderr.write(f"rows={len(rows)} suppressed_cells={suppressed} "
                     f"({100.0*suppressed/len(rows):.1f}%) -- report this alongside any trend\n")

    if a.format == "csv":
        w = csv.DictWriter(sys.stdout, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    else:
        json.dump(rows, sys.stdout, indent=2)
        print()


if __name__ == "__main__":
    main()
