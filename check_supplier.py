"""UK supplier and competitor check with the Crawlwren UK Company Profile actor on Apify.

Live (needs APIFY_TOKEN, about $0.03 per resolved company):
    python check_supplier.py 02099533 02174990

Offline, free, using a saved profile:
    python check_supplier.py --from-file examples/kier-construction-02099533.json
"""
import argparse
import json
import os
import sys
from datetime import date
from decimal import Decimal

ACTOR = "crawlwren/uk-company-profile"


def gbp(x):
    if x is None:
        return "no value published"
    if x >= 1e9:
        return f"£{x / 1e9:,.1f}bn"
    if x >= 1e6:
        return f"£{x / 1e6:,.1f}m"
    return f"£{x:,.0f}"


def months_between(a, b):
    return (b.year - a.year) * 12 + (b.month - a.month)


def report(row, as_of, horizon_months):
    if row.get("recordType") != "profile":
        # Unknown numbers and ambiguous names come back as free rows with candidates.
        print("Not resolved (free):", json.dumps(row)[:300])
        return
    f = row["flags"]
    print(f'\n{row["companyName"]} ({row["companyNumber"]})')
    print(f'  Health: active={f["active"]}, accounts overdue={f["accountsOverdue"]}, '
          f'insolvency history={f["hasInsolvencyHistory"]}, outstanding charges={f["hasOutstandingCharges"]}')

    c = row.get("ukPublicContracts") or {}
    if not c.get("checked"):
        print("  UK contracts: not checked")
        return
    cov = c.get("coverage", {}).get("find_a_tender", {})
    print(f'  Coverage: award notices {cov.get("from", "?")[:10]} to {cov.get("to", "?")[:10]}')
    print(f'  Direct contracts and call-offs: {c["totalContracts"]}, {gbp(c["totalValueGbp"])}, '
          f'from {c["distinctBuyers"]} buyers (frameworks excluded)')
    print("  Top buyers: " + ", ".join(f'{b["buyerName"]} ({b["contracts"]})' for b in c.get("topBuyers", [])))

    listed = c.get("contracts", [])
    values = sorted(x["valueAmount"] for x in listed if x.get("valueAmount"))
    if values:
        print(f'  Award values in the {len(listed)} newest contracts listed: {gbp(values[0])} to {gbp(values[-1])}')

    ending = []
    for x in listed + c.get("frameworks", []):
        end = x.get("contractEnd")
        if not end:
            continue
        d = date.fromisoformat(end[:10])
        if as_of <= d and months_between(as_of, d) <= horizon_months:
            ending.append((d, x))
    if ending:
        print(f"  Ending within {horizon_months} months of {as_of} (possible re-tender or follow-on work):")
        for d, x in sorted(ending, key=lambda t: t[0]):
            kind = "framework" if x.get("isFramework") else "contract"
            print(f'    {d}  {x["buyerName"]}: {x["title"][:70]} ({kind}, {gbp(x.get("valueAmount"))})')

    fw = c.get("frameworks", [])
    if fw:
        print(f'  Framework places: {c["frameworkContracts"]} (ceilings total {gbp(c["frameworkCeilingGbp"])}, '
              f"shared by every supplier on them, not spend)")
        for x in fw:
            print(f'    {x["buyerName"]}: {x["title"][:70]} (ends {(x.get("contractEnd") or "?")[:10]})')


def fetch_live(numbers, max_charge):
    from apify_client import ApifyClient

    client = ApifyClient(os.environ["APIFY_TOKEN"])
    run = client.actor(ACTOR).call(
        run_input={
            "companyNumbers": numbers,
            "includeLei": True,
            "includeUkContracts": True,
            "includeUsFederal": False,
            "maxContractsPerCompany": 100,
        },
        max_total_charge_usd=Decimal(max_charge),  # hard spending cap for this run
    )
    if run is None:
        sys.exit("The run did not start or finish. Check it in Apify Console.")
    return list(client.dataset(run.default_dataset_id).iterate_items())


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("company_numbers", nargs="*", help="UK company numbers, e.g. 02099533")
    p.add_argument("--from-file", help="read a saved profile (JSON object or list) instead of calling the actor")
    p.add_argument("--max-charge", default="0.50", help="spending cap in USD for a live run (default 0.50)")
    p.add_argument("--months", type=int, default=24, help="flag contracts ending within this many months")
    p.add_argument("--as-of", default=None, help="date to count from, YYYY-MM-DD (default today)")
    a = p.parse_args()

    if a.from_file:
        data = json.load(open(a.from_file, encoding="utf-8"))
        rows = data if isinstance(data, list) else [data]
    elif a.company_numbers:
        if "APIFY_TOKEN" not in os.environ:
            sys.exit("Set APIFY_TOKEN first (from console.apify.com). Never commit it.")
        rows = fetch_live(a.company_numbers, a.max_charge)
    else:
        p.print_help()
        return

    as_of = date.fromisoformat(a.as_of) if a.as_of else date.today()
    for row in rows:
        report(row, as_of, a.months)


if __name__ == "__main__":
    main()
