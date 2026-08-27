---
name: open-payments-launch
description: >
  This skill should be used when the user asks about "Open Payments", "Sunshine Act",
  "manufacturer spend on physicians", "speaker programme spend", "launch spend
  signal", "KOL engagement", or wants a leading read on how hard a company is pushing
  a specific product before revenue shows up.
metadata:
  version: "0.1.0"
  layer: "Commercial"
---

# Open Payments launch signal

Read manufacturer payment behaviour as a leading indicator of commercial intent,
launch ramp and KOL engagement — then be disciplined about what it cannot say.

## Workflow

1. Pull general payments for the manufacturer, filtered to the product name, by
   program year (`scripts/open_payments.py`). Products are named in the record, so a
   product-level series is available inside a multi-product company.
2. Split by payment nature. The categories carry different meaning:
   - **Compensation for services other than consulting (speaker programmes)** —
     the promotional push. Scales with sales-force deployment.
   - **Consulting fee** — advisory-board work. Rises ahead of launch and ahead of
     label expansions, often two to four quarters before promotional spend.
   - **Food and beverage** — detailing intensity, a rep-activity proxy.
   - **Travel, education, grants** — mixed; grants can be medical-affairs rather
     than commercial and should not be read as promotional.
3. Count **distinct covered recipients**, not just dollars. Recipient breadth tracks
   sales-force reach; dollars alone can be one large speaker contract.
4. Benchmark against the same company's prior launches and against a named competitor
   launch in the same class and year. Absolute dollars are meaningless without an
   analogue; the ratio to a known launch is the usable number.
5. Overlay the timeline: approval date, guideline inclusion, competitor entry.
6. Emit the brief.

## Interpretation

- Consulting spend rising while promotional spend is flat, two quarters before an
  expected approval, is a preparation signal — commercial is building the KOL bench.
- Promotional spend falling year over year on a product still in its first three
  years is a de-prioritisation signal, and it usually shows up before management
  language changes on calls.
- Spend per recipient rising while recipient count falls means the programme has
  narrowed to a core group — consistent with a launch that is deepening rather than
  broadening. Cross-check with `partd-prescriber-share`.
- After a safety signal, watch for speaker-programme spend to stop. Companies pull
  promotional programmes fast; the data lag means you see it a year later, so this is
  a confirmatory rather than a timely signal.

## Caveats that cap this skill's confidence

Annual publication (full prior program year by 30 June, refreshed each January). That
cadence makes this a *structural* signal, not a tradeable one — do not build a
catalyst trade on it. Payments are reported by manufacturer with dispute windows.
Product attribution is imperfect for combination and device-drug products.

## Not-automatic

Spend is not sales, and spend intensity is not efficacy. High promotional spend on a
struggling launch is evidence of effort, not of traction.

Chains to a catalyst engine and a provider-adoption engine.
Contract: `../../references/evidence-brief.md`.
