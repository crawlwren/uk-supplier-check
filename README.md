# UK competitor and supplier check: public contracts won, buyers and frameworks in one call

See what any UK company has won from the public sector, who it wins from, what the work was worth and when it ends. One call to the [UK Company Profile](https://apify.com/crawlwren/uk-company-profile) actor returns a structured profile built from official open data: Find a Tender, Contracts Finder, Companies House and GLEIF. This repo is a small Python script that turns that profile into a bid-ready brief, plus a saved example you can run for free.

Made by Crawlwren, the maker of the actor it calls.

## What you can do with the data

**Size up the incumbent before a bid/no-bid call.** How many contracts does the current supplier hold with this buyer, how big are they, and is it on the frameworks the buyer uses? A supplier with 19 contracts from one buyer is a different fight from one with a single award.

**Find the buyers who keep awarding your kind of work.** A competitor's top buyers are a shortlist of organisations that already buy what you sell. Their framework places tell you which frameworks you need to be on to reach that work.

**Build a re-tender pipeline.** Every contract carries its end date. Contracts ending in the next 12 to 24 months are work that may come back to market, often before a tender notice appears.

**Benchmark your price.** Award values show what buyers expected to pay for comparable work (published estimates, not payments), so you can test your numbers against real outcomes instead of guesses.

**Back up win themes and case studies.** Run your own company number to get a clean, linked list of your public wins by buyer and value, ready for a capability statement or bid evidence.

**Plan accounts if you sell to suppliers.** Subcontractors, software vendors and consultancies can see where a target contractor is winning, which buyers and regions it works for, and when its big jobs start and finish.

**Check a supplier or partner.** The same profile flags whether the company is active, has overdue accounts or confirmation statement, insolvency history or outstanding charges, and who its corporate parent is.

## Worked example: Kier Construction Limited (02099533)

From a profile run on 19 October 2026, covering award notices from 17 October 2025 to 19 October 2026:

- **32 direct contracts and call-offs worth £490.7m, from 11 buyers.** 19 of the 32 came from the Department for Education.
- **What the work is worth.** Among the 25 newest contracts listed, DfE main works for four schools ranged from £44.9m (Wellfield Academy) to £64.1m (Polam Hall School). Twelve DfE pre-construction agreements (PCSAs) ranged from about £0.2m to £4.8m.
- **What's coming up.** Eight listed contracts end within 12 months of 2 November 2026, including five DfE PCSAs. A PCSA is usually the first stage of a two-stage build, so ending PCSAs can point to main works awards to come.
- **Where the frameworks are.** Kier holds 7 framework places, including DfE's Construction Framework 2025 (to January 2032), LHC's Public Buildings Construction and Infrastructure (to October 2030) and YORbuild Major Works 2 (to July 2030). Their ceilings add up to £18.9bn, but that is shared by every supplier on each framework and is not spend, so it is kept out of the £490.7m.

For a contractor competing with Kier on schools, that is a checklist of the buyers and frameworks that lead to this work, a price range for both stages, and a list of jobs to watch. The full profile is in [`examples/kier-construction-02099533.json`](examples/kier-construction-02099533.json), and you can browse it at [crawlwren.com/demo](https://crawlwren.com/demo/).

## Why not just ask Grok, ChatGPT or Claude Code?

You can, and for a single notice or a headline award that's fine. For a reliable answer to "what has this company won?", a general agent runs into the same problems every time:

- **The portals can't be searched by supplier.** Neither Find a Tender nor Contracts Finder lets you filter awards by the winning company. To answer properly, something has to read every award notice. Our index covers a year in about 1,600 feed pages of up to 100 notices each. An agent either spends a lot of time and tokens paging through that, or falls back on web search, which finds news stories and a handful of notices.
- **Feeds rate-limit and have silent gaps.** In one of our 17-minute runs, Find a Tender rate-limited us five times. Contracts Finder's paging stopped early for 4 to 11 September 2026 without an error, and re-scanning that week in smaller windows recovered 159 notices. An agent doing a one-off crawl has no way to know what it missed.
- **Names are not identities.** Group companies have similar names, and notices spell names differently. Crawlwren matches each award on the Companies House number in the notice, never on name alone. If you search by name, it only resolves when one company matches clearly, and otherwise returns a free list of candidates to choose from.
- **Totals are easy to get badly wrong.** Framework notices publish ceilings shared by every supplier, and multi-lot notices repeat the same value on every lot. Adding them up for Kier would mix £18.9bn of framework ceilings into £490.7m of direct contracts. Crawlwren counts each notice once at its largest lot value, keeps frameworks separate with the reason each was classed as one, and merges contracts published on both portals.
- **Answers should be repeatable.** The profile has the same structure every time, states its coverage window, and links every contract to its official notice, so you can check it and cite it. An agent's free-form answer can change from one run to the next.
- **The cost is small and fixed.** $0.03 per resolved company, with a spending cap you set per run.

You don't have to choose between them. Grok, ChatGPT, Claude Code and other agents can call the actor directly (see "Use it from an AI agent" below) and spend their effort on the analysis instead of the crawl.

## Quickstart

```bash
git clone https://github.com/crawlwren/uk-supplier-check
cd uk-supplier-check
pip install -r requirements.txt
```

**Try it free on the saved Kier profile** (no account or token needed):

```bash
python check_supplier.py --from-file examples/kier-construction-02099533.json --as-of 2026-11-02 --months 12
```

**Run it live** on any UK company numbers:

```bash
export APIFY_TOKEN=...        # from console.apify.com, never commit it
python check_supplier.py 02099533 02174990
```

Output for the Kier example (shortened):

```text
KIER CONSTRUCTION LIMITED (02099533)
  Health: active=True, accounts overdue=False, insolvency history=False, outstanding charges=False
  Coverage: award notices 2025-10-17 to 2026-10-19
  Direct contracts and call-offs: 32, £490.7m, from 11 buyers (frameworks excluded)
  Top buyers: Department for Education (19), Defence Science and Technology Laboratory (3), ESSEX COUNTY COUNCIL (2), ...
  Award values in the 25 newest contracts listed: £49,575 to £85.6m
  Ending within 12 months of 2026-11-02 (possible re-tender or follow-on work):
    2026-12-01  Department for Education: Matford Brook Academy - PCSA (con_29544) (contract, £727,427)
    2026-12-02  Department for Education: Brit School North - PCSA (con_30758) (contract, £3.5m)
    ...
    2027-08-05  ESSEX COUNTY COUNCIL: Cressing Primary School (contract, £3.8m)
  Framework places: 7 (ceilings total £18.9bn, shared by every supplier on them, not spend)
    Department for Education: Construction Framework 2025 (ends 2032-01-04)
    LHC Procurement Group: Public Buildings Construction and Infrastructure (ends 2030-10-15)
    Leeds City Council: YORbuild Major Works 2 (ends 2030-07-05)
    ...
```

Options: `--months` sets how far ahead to look for contracts ending (default 24), `--as-of` sets the date to count from (default today), and `--max-charge` caps a live run's spend in USD (default 0.50). Live runs list up to 100 contracts per company, newest first, and totals always count every matched award.

## Use it from an AI agent

The actor is available through [Apify's MCP server](https://docs.apify.com/platform/integrations/mcp), so any MCP client (Claude Code, Claude Desktop, Cursor, VS Code and others) can call it as a tool. Add this to your client's MCP config, and sign in to Apify when prompted:

```json
{
  "mcpServers": {
    "crawlwren-uk-company-profile": {
      "url": "https://mcp.apify.com?tools=crawlwren/uk-company-profile"
    }
  }
}
```

Then ask something like: "Profile company 02099533 and tell me which of its contracts end in the next year." Agents without MCP can call the same actor through the [Apify API](https://docs.apify.com/api/v2) or the Python client used in `check_supplier.py`.

## What it costs

Pay per event on Apify: **$0.0005 per run plus $0.03 per resolved company profile**. Profiling 100 companies costs about $3. Unknown company numbers and unresolved names are free. `--max-charge` sets a hard cap on each run. Apify bills your account; this repo never touches payment.

## How the contract numbers are built, and their limits

Because the portals can't be filtered by supplier, the actor keeps an index of award notices from both feeds, keyed by the supplier's Companies House number, and refreshes it from the official APIs once a day. On 26 October 2026 it held 80,496 distinct award entries across 26,180 companies, going back to 17 October 2025.

- **It is a floor, not a full count.** Only awards whose notice gives the supplier a Companies House number can be matched. In a sample of notices published 3 to 17 October 2026, that was 57% of Find a Tender supplier records and 42% of Contracts Finder records. Suppliers listed only by PPON, charity number or name are missed.
- **One value per notice.** Lots of one notice count once, at the largest lot value.
- **Frameworks are not spend.** Framework and DPS values are listed separately, each with the reason it was classed as a framework.
- **Values are as published** by the buyer. A few look wrong for the work described, so open the notice before quoting one.
- **Coverage is stated on every profile** (`ukPublicContracts.coverage`).

A whole-market view built the same way is on [UK government contract awards 2026](https://crawlwren.com/uk-government-contract-awards-2026/).

## Sources and licences

| Data | Source | Licence |
|---|---|---|
| Contract awards | Find a Tender and Contracts Finder (OCDS APIs) | Open Government Licence v3.0 |
| Company status, filings, charges, corporate owners | Companies House public data API | Open Government Licence v3.0 |
| LEI and parent companies | GLEIF API | CC0 1.0 |

Contains public sector information licensed under the Open Government Licence v3.0. Not affiliated with or endorsed by Companies House or the Cabinet Office.

## Personal data

Company-level data only. The actor never outputs directors, secretaries or individual people with significant control, and this script doesn't either. This is a first-pass check, not credit scoring, legal advice or a substitute for proper due diligence.

## Code licence

MIT. See [`LICENSE`](LICENSE). Fork it, change it and run it with your own token.

Questions or a field you need? Open an issue or email hello@crawlwren.com.

---
Crawlwren is operated by Chordio, Inc.
