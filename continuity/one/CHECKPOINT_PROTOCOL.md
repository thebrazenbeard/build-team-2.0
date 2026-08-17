# One Operational Checkpoint Protocol

Schema: `ONE_OPERATIONAL_CHECKPOINT_V1`

The checkpoint store is operational continuity, not canonical memory and not permanent training.

## Write rule

A checkpoint is append-only. Every successor names exactly one predecessor. The store rejects a second successor to the same predecessor and rejects a second root for the same role. The checkpoint JSON is accompanied by a caller-computed SHA-256 of its canonical UTF-8 bytes. A checkpoint may record `qualification_id = null`, but such a row cannot establish `BASE_READY`.

Before writing a successor:
1. Read the complete One checkpoint chain.
2. Resolve exactly one current leaf.
3. Re-read current governance and mutable provider/authority facts needed for the checkpoint.
4. Create the successor against that exact leaf.
5. Read the inserted row back and verify predecessor, digest, training binding, and payload.
6. Never update an old checkpoint to make history look cleaner.

## Read rule

A working One chat resolves its exact training package, proves a PASS qualification binding for the exact version/digest or trains first, reads the full checkpoint chain, requires exactly one valid leaf, then freshly verifies current Working Laws, role map, assignments, Warden/lease state, provider objects, blockers, and direct addresses before acting.

No checkpoint grants service-write authority.

## Failure states

- `NO_BASE_QUALIFICATION`: train/qualify before work.
- `CHECKPOINT_ABSENT`: rebuild operational state from current sources.
- `CHECKPOINT_FORK_OR_AMBIGUITY`: fail closed and reconcile.
- `CHECKPOINT_DIGEST_MISMATCH`: reject the row.
- `TRAINING_BINDING_MISMATCH`: reject the checkpoint for this base.
- `CURRENTNESS_REFRESH_FAILED`: preserve the checkpoint as history and stop at the unsupported claim ceiling.
