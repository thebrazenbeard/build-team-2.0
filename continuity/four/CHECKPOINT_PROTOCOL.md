# Four Operational Checkpoint Protocol

Schema: `FOUR_OPERATIONAL_RESUME_CHECKPOINT_V1`

The checkpoint store is operational continuity, not canonical memory and not permanent training.

## Training binding

A Four checkpoint is usable only when bound to role `four`, numerical identity `4`, the same package version, and the same source-set digest as a verified PASS qualification. A checkpoint may reference a null qualification ID, but that cannot establish `BASE_READY`.

## Append-only write rule

Before writing a successor:

1. Read the complete Four checkpoint chain.
2. Resolve exactly one valid current leaf.
3. Refresh current governance, role map, assignments, direct Slack addresses, provider heads, blockers, and authority/lease observations material to the checkpoint.
4. Serialize one `FOUR_OPERATIONAL_RESUME_CHECKPOINT_V1` payload and hash the exact UTF-8 bytes.
5. Insert exactly one successor against the exact leaf and training binding.
6. Read the inserted row back and verify predecessor, binding, digest, schema, and payload bytes.
7. Never update/delete history to make the chain cleaner.

## Read rule

A fresh Four chat first proves PASS qualification for the exact training source or trains. Then it resolves the unique checkpoint leaf. Checkpoint observations are historical evidence until refreshed.

## Four-specific preservation

Preserve:

- exact immutable reconstruction subjects;
- current versus superseded specifications/reconstructions;
- pre-byte versus exact-byte status;
- manifests/pathset consequences;
- actual external effects and readback separately from intended effects;
- authority/lease observations;
- unresolved evidence gaps and conflicts;
- handoffs and downstream recipients.

## Failure states

- `NO_BASE_QUALIFICATION`
- `CHECKPOINT_ABSENT`
- `CHECKPOINT_FORK_OR_AMBIGUITY`
- `CHECKPOINT_DIGEST_MISMATCH`
- `TRAINING_BINDING_MISMATCH`
- `CHECKPOINT_SCHEMA_INVALID`
- `CURRENTNESS_REFRESH_FAILED`

No checkpoint, role title, repository access, or tool capability grants service-write authority.
