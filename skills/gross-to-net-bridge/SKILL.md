---
name: gross-to-net-bridge
description: >
  This skill should be used when the user asks about "gross to net", "GtN erosion",
  "net price assumption", "rebate pressure", "list vs net", "IRA maximum fair price
  impact", or wants to build or stress a net-revenue bridge for a drug from open data.
  Anchors prompt-library ID SUB-PHA-04.
metadata:
  version: "0.1.0"
  layer: "Commercial"
---

# Gross-to-net bridge

Assemble a defensible net-price path for a drug from open CMS sources, and mark
clearly where the estimate stops being data and starts being assumption.

## Workflow

1. **Anchor list price.** Pull WAC from the company's own disclosures or a public
   price-transparency filing. Record the date of the last list increase — most large
   caps now take one modest increase per January.
2. **Build the observable net floors.**
   - Medicaid: SDUD total reimbursed ÷ units gives a pre-rebate reimbursement level;
     the statutory Medicaid rebate (23.1% of AMP for most brands, plus the CPI
     penalty) sets a hard floor well below it.
   - Medicare: the CMS Medicare Part B and Part D Spending by Drug dashboards publish
     average spending per dosage unit and annual change — the cleanest open series
     for a Medicare-weighted net trend.
   - 340B: HRSA covered-entity growth in the relevant setting is a structural
     GtN headwind. Size it qualitatively; the discount itself is not public per drug.
3. **Layer the policy calendar.** IRA maximum fair price effective dates, Part D
   redesign (manufacturer liability in the catastrophic phase), and any inflation
   rebate exposure where list increases outran CPI. Pull dates from
   a reimbursement engine rather than re-deriving them here.
4. **Bridge it.** Gross → statutory rebates → commercial rebates and PBM fees →
   340B and other mandated discounts → patient assistance and copay support → net.
   Only the statutory and Medicare components are observable. Label the commercial
   rebate line as the assumption it is, and show the net-revenue sensitivity to it
   at ±5 percentage points.
5. **Sanity-check against reported results.** Company-reported net revenue ÷ your
   estimated volume gives an implied net price. If that implies a GtN outside 
   reasonable bounds for the class, your volume estimate is wrong, not the company's.
6. Emit the brief, with the commercial-rebate assumption named in **Not-automatic**.

## Class heuristics

GtN gaps are widest where PBM competition is fiercest — insulins, respiratory
inhalers, TNF inhibitors, and increasingly the GLP-1 class. They are narrowest in
buy-and-bill oncology and single-source rare disease. A model that applies one house
GtN percentage across a diversified pharma's portfolio will misprice the mix shift,
which is usually the actual driver of net-price surprise.

## Not-automatic

An observable Medicaid or Medicare net level does not license a commercial net price.
The commercial book is where the rebate war happens and it is not public.

Framework anchors: your own valuation framework;
Kongstvedt on PBM and rebate mechanics; MedPAC and KFF for policy context.
Contract: `../../references/evidence-brief.md`.
