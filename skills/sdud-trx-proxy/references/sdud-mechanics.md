# SDUD mechanics, caveats and practitioner heuristics

## What the dataset is

State Drug Utilization Data is a by-product of the Medicaid Drug Rebate Program.
States report, per NDC-11 per quarter: number of prescriptions, units reimbursed,
total amount reimbursed, Medicaid amount reimbursed, non-Medicaid amount reimbursed.
Files split into Fee-For-Service and Managed Care Organization series — **pull both
or state which you used**; the FFS-only series has been shrinking for a decade as
states moved to managed care, which produces a spurious downtrend.

## Cadence and lag

CMS requires states to submit within 60 days of the end of the rebate period.
Posting to data.medicaid.gov typically runs one to two quarters behind the quarter
covered. Late and restated state submissions mean the two most recent quarters are
revised upward after first posting — never build a trend whose final point is the
most recently posted quarter without flagging it as provisional.

## Suppression

Cells with fewer than 11 prescriptions are suppressed. Consequences that matter:

- National sums are biased low, and the bias shrinks as volume grows, manufacturing
  growth. This is the single most common error in open-TRx work.
- Small states are suppressed persistently, so a balanced panel is usually the large
  states plus whichever mid-size states cleared the threshold in the first period.
- For a rare-disease drug, most cells are suppressed and the dataset is unusable.
  Say so and stop rather than reporting a series built from three states.

## Heuristics practitioners use

- Index the series to launch quarter rather than calendar quarter when comparing
  analogue launches, and compare against two or three named analogues in the same
  therapeutic area and payer mix.
- Medicaid is disproportionately useful for: behavioural health, HIV, addiction
  medicine, paediatrics, sickle cell, obstetrics, and any product with a large
  duals population. It is close to useless for: oncology sold into Medicare,
  ophthalmology buy-and-bill, and most device-adjacent therapies.
- Authorised generics show up under the AG labeller. If the brand series drops and
  an AG series appears, total molecule volume may be flat — a franchise defence, not
  a demand collapse.
- Unit definitions differ across formulations (mL vs tablets vs units). Never sum
  units across dosage forms; sum prescriptions, or normalise to days of therapy using
  the label's dosing.

## Framework anchors

- Kongstvedt, *Health Insurance and Managed Care* — channel and PDL mechanics that
  determine why a state series steps rather than drifts.
- Your own commercial-metrics reference — the volume and
  share metric definitions this skill must populate.
