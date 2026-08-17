# Nine Operational Checkpoint Protocol

Schema: `NINE_OPERATIONAL_RESUME_CHECKPOINT_V1`

The checkpoint store is operational continuity, not canonical memory and not permanent training.

## Training binding

A Nine checkpoint is usable for resumed work only when it is bound to the same role key, package version, and source-set digest as the qualifying frozen base. The Nine v1.0.0 source-set digest is computed from `training_manifest.json.file_inventory` by sorting paths lexicographically and hashing the UTF-8 concatenation of `path + NUL + sha256 + NUL + decimal byte_count + LF` for each manifest-owned file.

A checkpoint may record `qualification_id = null`, but such a row cannot establish `BASE_READY` or substitute for qualification.

## Write rule

Checkpoints are append-only. Every successor names exactly one predecessor. The shared store rejects a second root for the same role and a second successor to the same predecessor.

Before writing a successor:
1. Read the complete Nine checkpoint chain.
2. Resolve exactly one current leaf.
3. Re-read current governance, role map, direct assignments, provider/target facts, and authority observations needed for the checkpoint.
4. Serialize one `NINE_OPERATIONAL_RESUME_CHECKPOINT_V1` payload and compute SHA-256 over the exact stored UTF-8 payload bytes.
5. Insert the successor against that exact leaf and exact training binding.
6. Read the inserted row back and verify predecessor, qualification binding, digest, schema, and payload bytes.
7. Never update or delete an old checkpoint to make history look cleaner.

## Read rule

A working Nine chat resolves the current registry entry, verifies the exact training package, proves a PASS qualification binding for the exact version/source-set digest or trains first, reads the complete checkpoint chain, and requires exactly one valid leaf.

Checkpoint observations are saved evidence, not automatically current truth. Before acting, refresh current Working Laws, role map, assignments, Service Warden/lease state, provider/target objects, blockers, direct identity addresses, and any mutable evidence material to the acceptance proposition.

No checkpoint, qualification, role title, repository access, or tool capability grants service-write authority.

## Nine-specific preservation rules

- Preserve current and superseded verdicts separately.
- Preserve historical incidents after correction.
- Preserve claim ceilings and `UNKNOWN`/`PROVENANCE_BLOCKED` states rather than inflating them after later success.
- Record reviewer-contamination or blind-review loss when it occurred.
- Record `do_not_rerun` only when replay would be invalid, destructive, provenance-breaking, or already terminal under current good-enough rules.

## Failure states

- `NO_BASE_QUALIFICATION`: train/qualify before operational work.
- `CHECKPOINT_ABSENT`: rebuild operational state from current authoritative sources.
- `CHECKPOINT_FORK_OR_AMBIGUITY`: fail closed and reconcile.
- `CHECKPOINT_DIGEST_MISMATCH`: reject the row.
- `TRAINING_BINDING_MISMATCH`: reject the checkpoint for this base.
- `CHECKPOINT_SCHEMA_INVALID`: reject the payload.
- `CURRENTNESS_REFRESH_FAILED`: preserve the checkpoint as history and stop at the unsupported claim ceiling.
