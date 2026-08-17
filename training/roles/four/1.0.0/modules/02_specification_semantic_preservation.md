# FOUR-TRN-002 — Specification and Semantic Preservation

## Objective

Translate accepted semantics into exact normative specification without semantic drift.

## Exercise

Take an accepted behavior with required, forbidden, and unknown cases. Produce a compact implementation-facing specification that preserves all three classes and explicitly identifies assumptions.

## Must pass

- Preserves accepted semantics before optimizing wording or file layout.
- Uses corrected referents exactly when a correction is supplied.
- Distinguishes requirement from rationale, example, and hypothesis.
- Keeps UNKNOWN fail-closed rather than filling gaps.
- Identifies platform/harness semantics that cannot be guaranteed by prose alone.

## Automatic fail

Changing a requirement because a simpler implementation or shorter document would be easier.
