---
name: sdud-trx-proxy
description: >
  This skill should be used when the user asks for an "open TRx proxy", "SDUD",
  "Medicaid utilisation", "script trend without IQVIA", "is the launch tracking",
  "prescription volume for [brand]", or wants to validate or invalidate a launch
  trajectory, biosimilar erosion, or share shift using free CMS data. Also triggers
  on prompt-library IDs SUB-PHA-03, SUB-PHA-04, SUB-PHA-05.
metadata:
  version: "0.1.0"
  layer: "Commercial"
---

# SDUD TRx proxy

Build an open prescription-volume series for a brand or molecule from Medicaid State
Drug Utilization Data, then state honestly what it can and cannot support.

## Workflow

1. **Resolve the product to NDCs.** A brand maps to many NDC-11s (strengths, pack
   sizes, authorised generics). Pull the NDC set from openFDA `/drug/ndc.json` by
   brand name and labeller, or from the FDA NDC Directory. Record the labeller code —
   an authorised generic under a different labeller is a *different* commercial event
   and must be tracked as its own series, not folded into the brand.
2. **Pull the series.** Run `scripts/sdud_query.py` for each NDC across the quarters
   in scope. Aggregate prescriptions, units and total reimbursed by quarter, keeping
   state granularity in the working table.
3. **Handle suppression before computing anything.** Count state-quarter cells
   returned as suppressed. If suppression exceeds ~20% of contributing states in the
   earliest quarter of the window, do not report a growth rate off the national sum —
   compute the trend on a balanced panel of states with continuous non-suppressed
   history and report it as such.
4. **Separate price from volume.** Total reimbursed ÷ units gives a Medicaid $/unit
   that reflects pre-rebate reimbursement. It is not net price. Track units for volume
   and treat dollars as a separate, weaker series.
5. **Test the payer-mix assumption.** Estimate the brand's Medicaid share from the
   label's indication and the disease's payer skew. Where the company discloses a
   channel split in filings or at conferences, use it and cite it. Where it does not,
   say the assumption is unanchored and cap confidence at 0.5.
6. **Cross-read against Part D.** If the drug has meaningful Medicare exposure, run
   `partd-prescriber-share` and reconcile direction. Two proxies agreeing on direction
   is materially stronger evidence than either alone; disagreeing is a finding in itself.
7. **Emit the brief.**

## Reading the series

- **Launch curves.** Medicaid uptake typically lags commercial by one to two quarters
  because of state formulary and PA processes. A flat Medicaid series in launch
  quarter two is weak evidence of a failing launch; a flat series in quarter six is
  strong evidence.
- **Biosimilar and generic entry.** Watch the units split between the reference
  labeller and entrants, not the aggregate. Medicaid erosion tends to run *faster*
  than commercial because state preferred-drug lists switch mechanically.
- **Divergence between prescriptions and units** usually means a pack-size or dosing
  change, not a demand change. Check the NDC set before writing it up as volume.
- **A step change confined to one or two states** is a formulary or PDL event, not a
  demand event. Name the state.

## Not-automatic (carry into the brief)

A SDUD move does not license a national TRx conclusion, a net-revenue conclusion, or
a share conclusion against competitors with different payer mixes.

## Chaining

a procedure-exposure engine for the denominator · a reimbursement engine where an MFP date sits in the window · your view layer →
model-valuation for the revenue line.

Reference: `references/sdud-mechanics.md`. Contract: `../../references/evidence-brief.md`.
