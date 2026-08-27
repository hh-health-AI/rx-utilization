# rx-utilization — standing instructions

**Layer covered:** Commercial (volume, share, launch ramp).
**Position in the stack:** evidence engine. Feeds your valuation and portfolio-view layer. Chains to a procedure-exposure engine,
a provider-adoption engine, a reimbursement engine.

## What this engine is for

Reconstructing drug volume, share and launch trajectory from open CMS administrative
data when the desk does not have — or does not want to wait for — IQVIA scripts.

## The one caveat that governs everything here

**These are population-restricted proxies, not a national panel.**

- **SDUD** covers Medicaid fee-for-service and managed care only. Medicaid share of a
  brand varies enormously by therapy area — near-zero for an oncology drug sold into
  Medicare, dominant for paediatric and behavioural-health products. A SDUD trend is
  only a national trend if the payer mix is stable, and payer mix is exactly what
  moves during a launch, a formulary win, or an IRA negotiation.
- **Part D** covers Medicare beneficiaries only, annual, ~5-month lag.
- **Open Payments** is manufacturer spend, not sales. It is a leading indicator of
  commercial intent and KOL engagement, not of revenue.

Every brief from this engine must state the payer-mix assumption explicitly in
**Not-automatic**. A skill run that reports a SDUD delta as though it were TRx growth
is wrong even when the number is right.

## Suppression and denominators

SDUD suppresses cells with fewer than 11 prescriptions. In a launch quarter that is
most states, so the national sum is biased low and the bias shrinks as the launch
grows — which manufactures a growth rate. Always report the count of suppressed
state-quarter cells alongside any growth figure, and prefer state-level series with
continuous non-suppressed history when computing a trend.

## Anchored prompt-library IDs

SUB-PHA-03 (TRx vs NRx Divergence) · SUB-PHA-04 (Gross-to-Net Erosion) ·
SUB-PHA-05 (Biosimilar Erosion Curve).

## Connector status

No hosted MCP for CMS bulk data as of Aug 2026. Scripts in `scripts/` call the public
DKAN/Socrata endpoints directly with stdlib `urllib`. No key required; be polite about
rate. If a hosted CMS-data connector appears, declare it here and let other engines
reach it by co-install.
## Connector

Declares **`medicare`** (`openpharma-org/medicare-mcp`) — CMS Socrata datasets: Part D
prescribers by provider and drug, hospital utilisation, drug spending. This plugin is
the CMS bulk-data anchor; `provider-economics` consumes the session.

Not covered by the server, and therefore script-only: **SDUD** (`sdud_query.py`),
**Open Payments** (`open_payments.py`) and **HCRIS**. No MCP exists for any of them.

Two joins that look easy and are not. Open Payments carries no NPI, so linking it to
Part D prescriber records has to go through name-and-address string matching, with the
error rate that implies — say so in the brief rather than implying a clean key. And
SDUD's under-11 suppression is per cell: a product whose suppressed cells resolve as
the denominator grows will show growth that is partly an artefact of disclosure
thresholds, not demand.

## Standard of evidence

This engine is built to **institutional investor standards: rigorous and auditable.**
That is a claim about specific mechanisms, and the full list is in
`references/auditability.md`. The load-bearing ones:

- Every finding carries a source, a retrieval date and the **vintage of the underlying
  data** — a different and usually much earlier date.
- Confidence is gated by vintage, not by conviction.
- Scripts fail loudly on empty result sets. Silence is never a negative finding.
- Known limitations travel with the number, in-line, not in a footnote.
- Evidence and view stay separated. This engine does not issue recommendations.

## Desk conventions (all engines)

- **One connector, one plugin — for plugin-level servers only.** A self-hosted
  stdio server is declared in exactly one plugin's `.mcp.json`; co-installed
  plugins share every server session-wide, so a second declaration buys a
  duplicate process, not extra capability. **Account-level hosted connectors are
  different**: CMS Coverage, PopHIVE, ClinicalTrials.gov, PubMed, ChEMBL,
  bioRxiv and Scholar Gateway are connected once in the directory and are visible
  to every plugin. Plugins reference those; they never declare or own them.
  Full map in `references/mcp-setup.md`.
- **MCP for the analyst, scripts for the watcher.** Both paths ship in every
  plugin and they are not redundant. Interactive query refinement goes through
  the server; unattended scheduled evidence goes through the script, because a
  watcher has to be deterministic and re-runnable against the same vintage.
  Where the two disagree, the script wins for anything entering a brief — you
  cannot cite the internals of a third-party server.
- **Engines produce evidence, not views.** An engine skill ends at the brief. The
  your view layer is the only place a position
  is argued. Do not write a recommendation into an engine output.
- **Open data only.** Every input here is free and public. If an analysis needs
  IQVIA, Symphony, Definitive, EvaluatePharma or Citeline, say so and stop — do
  not silently substitute a proxy for the paid panel and present it as equivalent.
- **Cite the vintage every time.** See `references/evidence-brief.md`.
- **Chain, don't duplicate.** These eight engines cross-reference each other by
  name. Anything outside them — valuation models, single-name research, the
  portfolio view layer — is chained into, never reimplemented here. An engine
  that starts doing valuation has stopped being an engine.
- **Scripts are stdlib-only Python 3.** No pip installs. Every script takes
  `--help`, prints JSON or CSV to stdout, and fails loudly on an empty result set
  rather than returning silence that reads like a negative finding.
