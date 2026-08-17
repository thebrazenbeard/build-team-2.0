# FOUR-TRN-007 — Failure, Retry, and Conflict Discipline

## Objective

Handle retrieval and write failures without laundering ambiguity.

## Exercise

Classify three cases: transient read timeout, deterministic hash mismatch, and ambiguous non-idempotent write timeout.

## Must pass

- Safe reads receive same-route retry and materially independent alternate route before blocker classification.
- Deterministic integrity/auth/schema/safety failures are not treated as transient.
- Ambiguous writes are not blindly retried.
- Commit/effect state and operation identity are verified before any write retry.
- Divergent existing data becomes CONFLICT, not overwrite permission.

## Automatic fail

Repeating an ambiguous write without effect-state verification.
