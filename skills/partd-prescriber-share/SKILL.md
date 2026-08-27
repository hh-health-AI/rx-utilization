---
name: partd-prescriber-share
description: >
  This skill should be used when the user asks about "Part D prescribers", "who is
  writing the drug", "prescriber concentration", "share shift among writers",
  "decile analysis", "is uptake broadening", or wants NPI-level Medicare prescribing
  evidence for a brand or class.
metadata:
  version: "0.1.0"
  layer: "Commercial"
---

# Part D prescriber share

Measure who prescribes a drug in Medicare, how concentrated that base is, and whether
uptake is broadening or stalling inside a fixed group of early adopters.

## Workflow

1. Pull the Medicare Part D Prescribers by Provider and Drug file for the brand and
   for two or three named competitors in the same class (`scripts/partd_prescribers.py`).
2. Build the writer distribution: prescriber count, total claims, claims per writer,
   and the share of claims held by the top decile of writers.
3. Compute the year-over-year delta in **prescriber count** and in **claims per
   writer** separately. These answer different questions and moving them together in
   one "growth" number destroys the signal.
4. Join to specialty. A drug crossing from its launch specialty into primary care is
   the single most reliable open-data marker of a category becoming mainstream.
5. Join to geography and, where the thesis needs it, to trial investigators via
   a provider-adoption engine.
6. Emit the brief.

## Interpretation

- **Broadening** (writer count up, claims per writer flat) is durable growth. It
  usually precedes a consensus upgrade to peak-sales assumptions.
- **Deepening** (writer count flat, claims per writer up) is fragile. It means a fixed
  KOL base is titrating existing patients. It caps peak sales and is vulnerable to a
  single competitor readout.
- **Top-decile share above roughly 60%** means the franchise is hostage to a small
  group of academic centres — a concentration risk to name in position sizing.
- **A writer base that overlaps heavily with trial investigators** two years post
  launch means the drug never escaped its trial network. Check this explicitly.

## Caveats

Annual file, roughly five-month lag (2024 data published May 2026). Medicare-only.
Counts under 11 are suppressed. Prescriber NPI attribution reflects the writer, not
the treating institution, so hospital-employed prescribing is noisy.

## Not-automatic

Prescriber breadth in Medicare does not license a commercial-channel conclusion, and
claims are not revenue — Part D claim counts say nothing about net price.

Contract: `../../references/evidence-brief.md`.
