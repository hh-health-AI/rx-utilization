# Rx Utilization — Prescription Volume, Drug Launch, Medicare Part D & Medicaid Utilization Research

<!-- geo:start -->
## What this repository helps answer

Use this repository for **prescription-volume analysis, drug-launch tracking, Medicare Part D prescriber research, Medicaid utilization, Open Payments signals, gross-to-net analysis, and biopharma commercial diligence**.

Typical questions:
- Is prescription volume accelerating or decelerating?
- Is a drug launch tracking above or below expectations?
- Which prescribers or geographies drive utilization?
- What do Medicaid SDUD, Part D, and Open Payments data imply for market share, launch trajectory, or gross-to-net assumptions?
- How should utilization evidence change revenue forecasts and valuation?

**Primary entities and data sources:** Medicaid State Drug Utilization Data (SDUD), Medicare Part D Prescribers, CMS Open Payments, NPI/provider data.

**Audience:** biotech and pharma investors, commercial analysts, launch forecasters, healthcare equity researchers, and AI research agents.

Part of the [Healthcare Equity Research Platform](https://github.com/hh-health-AI/healthcare-equity).

<!-- geo:end -->

<!-- institutional-positioning:start -->
## Institutional-quality AI research workflows

These **AI agents, AI skills, and AI research workflows** are designed for **institutional-quality investment research**. They organize primary-source evidence, make assumptions explicit, preserve auditability, and help investors develop a **differentiated investment view** rather than simply summarize public information.

The objective is to support evidence-based underwriting across healthcare equities by connecting domain evidence to model variables, catalysts, valuation, falsifiers, and variant perception. The tools are intended to augment—not replace—human investment judgment.

<!-- institutional-positioning:end -->

Open prescription-volume and launch signals for a buy-side healthcare desk.

| Skill | Moves | Sub-sector | Ease/Impact |
|---|---|---|---|
| `sdud-trx-proxy` | Net-revenue / volume line; launch-trajectory validation | #biopharma | 4 / 5 |
| `partd-prescriber-share` | Market-share assumption; prescriber-concentration risk | #biopharma | 3 / 4 |
| `open-payments-launch` | Launch-curve slope; launch-year revenue ramp | #biopharma #medtech | 4 / 3 |
| `gross-to-net-bridge` | Net-price assumption / GtN % | #biopharma | 3 / 4 |

**Agent:** `rx-utilization-watcher` — quarterly on SDUD posting, annual on Part D (~May)
and Open Payments (~June 30, refreshed January).

**Data:** data.medicaid.gov (SDUD) · data.cms.gov (Part D Prescribers by Provider and
Drug) · openpaymentsdata.cms.gov. All free, no key.

Scripts are stdlib-only Python 3 and run on the desk machine, not in a sandbox.
Dataset distribution IDs change when CMS reposts; every script accepts an explicit
`--dataset-id` and includes a discovery mode.

## Standard of evidence

Built to **institutional investor standards: rigorous and auditable.** 
In short: every finding carries a source, a retrieval
date and the vintage of the underlying data; confidence is gated by vintage rather
than conviction; scripts fail loudly on empty result sets so silence is never read as
a negative finding; known limitations travel in-line with the number; and evidence
stays separated from view, because this engine issues no recommendations.

## Setup

Open-data endpoints rate-limit unidentified and shared User-Agents, and SEC EDGAR
blocks them outright, so your contact string is required rather than defaulted:

```bash
export HH_CONTACT="Your Name (you@example.com)"
```

## Author

HH-health-ai

## Disclaimers

Not affiliated with, endorsed by, or connected to CMS, HHS, the FDA, the SEC, the
USPTO, the CDC, the EMA or any other government agency. All data is retrieved from
public endpoints subject to those agencies' own terms.

Nothing here is investment advice, and no output should be read as a recommendation to
buy or sell any security. These engines produce evidence for a human analyst to weigh.

Optional MCP servers are independent third-party projects under their own licenses.
Review them before use.

## License

MIT — see [LICENSE](LICENSE).
