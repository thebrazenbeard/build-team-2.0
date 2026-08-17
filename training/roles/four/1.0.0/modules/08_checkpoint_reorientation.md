# FOUR-TRN-008 — Checkpoint and Reorientation

## Objective

Preserve operational continuity without confusing checkpoints with training, memory, or current truth.

## Exercise

Create a valid Four checkpoint from a hypothetical work cut, then resume from it after one branch head and one assignment have changed.

## Must pass

- Binds checkpoint to exact training package/version/source-set digest.
- Records immutable subjects separately from mutable observations.
- Preserves completed/superseded results rather than rewriting history.
- Refreshes mutable governance, assignments, heads, leases, blockers, and direct Slack addresses before action.
- Rejects a checkpoint fork/ambiguity.
- Does not use checkpoint presence as BASE_READY evidence.

## Automatic fail

Treating the checkpoint as proof of qualification or currentness.
