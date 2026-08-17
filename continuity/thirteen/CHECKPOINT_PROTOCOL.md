# Thirteen Operational Checkpoint Protocol

Schema: `THIRTEEN_OPERATIONAL_CHECKPOINT_V1`

The checkpoint store preserves **operational continuity evidence** for Thirteen. It is not permanent training, canonical governance, a frozen base, or mutation authority.

## Training binding

Current training-source identity for this protocol integration:

- role key: `thirteen`
- package version: `1.0.0`
- package path: `training/roles/thirteen/corrections/v1.0.0`
- immutable source commit: `4de273b3d56ec642c7f9ba83e4767029cf054559`
- source-set digest: `89f3da76b9033c9302e2ddb85c68b6bf0b7856383d7bce65f671170d4a8a7bc1`
- digest contract: SHA-256 over the UTF-8 concatenation of sorted records `<relative-path>\0<file-sha256>\0<decimal-byte-count>\n` for all 11 package files.

This binding identifies training source. It does not prove that a chat passed qualification. `qualification_id = null` is permitted for continuity storage but cannot establish `BASE_READY`.

## Write rule

A checkpoint is append-only. Every successor names exactly one predecessor. The shared store rejects a second root for the same role and rejects a second successor to the same predecessor.

Before writing a root or successor:

1. Resolve this role through `training/ROLE_TRAINING_REGISTRY.json` from the current authoritative ref.
2. Verify package version, immutable source identity, and source-set digest.
3. Read the complete Thirteen checkpoint chain and require exactly one current leaf before a successor write.
4. Re-read current governance, role map, assignments/supersession, relevant Warden/lease state, provider objects, blockers, and direct coordination needed for the checkpoint.
5. Build a payload conforming to `THIRTEEN_OPERATIONAL_CHECKPOINT_V1.schema.json`.
6. Canonicalize the payload as sorted-key compact UTF-8 JSON and compute its SHA-256. `checkpoint_tool.py` is an optional standard-library helper for this step.
7. Insert exactly one append-only checkpoint against the resolved predecessor (or one root if none exists).
8. Read the inserted row back and verify predecessor, role, schema, training binding, payload text, and digest.
9. Never update old checkpoint content to make history look cleaner.

An ambiguous non-idempotent checkpoint insert is not blindly retried. Read the store first to determine whether the effect occurred.

## Read / reorientation rule

A working Thirteen chat:

1. Resolves the exact registry-listed training package.
2. Proves a PASS qualification binding for that exact package version/digest, or trains/qualifies before treating itself as `BASE_READY`.
3. Reads the full checkpoint chain and requires exactly one valid leaf.
4. Treats the leaf as saved evidence, not automatically current truth.
5. Freshly verifies current Working Laws, permanent role map, assignment generation/supersession, Warden/lease state, relevant provider/device objects, blockers, and direct coordination before acting.
6. Preserves Thirteen's permanent authority boundary: Corrections Lead / Governance-Authority Review / No-False-Authority Challenger is not itself service-write, task-dispatch, release, or governance authority.

No checkpoint grants service-write authority.

## Failure states

- `NO_BASE_QUALIFICATION`: train/qualify before claiming `BASE_READY`.
- `CHECKPOINT_ABSENT`: rebuild operational state from current authoritative sources.
- `CHECKPOINT_FORK_OR_AMBIGUITY`: fail closed and reconcile.
- `CHECKPOINT_DIGEST_MISMATCH`: reject the row.
- `TRAINING_BINDING_MISMATCH`: reject the checkpoint for this base/package.
- `TRAINING_SOURCE_UNRESOLVED`: exact package source cannot be bound.
- `CURRENTNESS_REFRESH_FAILED`: preserve the checkpoint as history and stop at the unsupported claim ceiling.
- `AUTHORITY_UNRESOLVED`: no mutation until current authority/lease is established.
