# Six Operational Checkpoint Protocol

Schema: `SIX_OPERATIONAL_RESUME_CHECKPOINT_V1`

The checkpoint store is operational continuity, not canonical memory and not permanent training.

## Training binding and durable-store envelope

A Six checkpoint is usable for resumed work only when it is bound to role key `six`, the same package version, and the same source-set digest as the qualifying frozen base.

The shared Supabase checkpoint store mechanically requires the serialized JSON payload to contain:
- top-level `schema` equal to the row's `checkpoint_schema`;
- top-level `role_key` equal to the row's `role_key`;
- `training_binding.version` equal to the row's `training_package_version`;
- `training_binding.source_set_digest_sha256` equal to the row's `training_source_set_digest_sha256`.

Six v1.0.0 additionally binds `numerical_identity = 6`. A later training version must use its own registered package/digest. A checkpoint for one version cannot silently qualify another.

A checkpoint may record `training_binding.qualification_id = null` and the row may have `qualification_id = null`, but that cannot establish `BASE_READY` or substitute for qualification.

## Write rule

Checkpoints are append-only. Every successor names exactly one predecessor. The shared store rejects a second root for the same role and a second successor to the same predecessor.

Before writing a successor:

1. Read the complete Six checkpoint chain and resolve exactly one valid current leaf, or establish that no checkpoint exists yet.
2. Re-read current governance, role map, direct `#six` assignments/mentions, target/provider observations, blockers, and authority/lease state material to the checkpoint.
3. Preserve immutable subject identity separately from mutable observations.
4. Serialize one `SIX_OPERATIONAL_RESUME_CHECKPOINT_V1` payload using `checkpoint_tool.py canonicalize`; compute SHA-256 over those exact stored UTF-8 bytes.
5. Insert the root or successor with exact role key, predecessor, training version/source-set digest, and when available the exact qualifying `qualification_id`.
6. Read the inserted row back and verify predecessor, qualification/training binding, payload digest, schema, payload bytes, role key, and timestamps.
7. Never update or delete an old checkpoint to make history look cleaner.

## Read rule

A working Six chat resolves the current registry entry, verifies the exact training source, proves a `PASS` qualification binding for the exact package version/source-set digest or trains first, reads the complete checkpoint chain, and requires exactly one valid leaf.

Checkpoint values are saved evidence, not automatically current truth. Before acting, refresh current Working Laws, permanent role map, assignments/direct mentions, Service Warden/lease state, target/provider objects, blockers, operator-visible state, and any evidence material to the next claim or action.

No checkpoint, qualification, role title, repository access, tool capability, or Warden status grants service-write authority.

## Six-specific preservation rules

- Preserve operator-visible observations separately from package/lifecycle/manager/responder/product-semantic claims.
- Preserve exact target identity/currentness and the authority basis for any target-runtime effect.
- Preserve ambiguous non-idempotent effects as unresolved until readback; never retry merely to obtain green state.
- Preserve `UNKNOWN`, claim ceilings, contradictory observations, and historical failures after later success.
- Preserve target-runtime lease state and verification/closure evidence separately from the actor's report.
- Preserve direct `#six` routing relevant to current work without treating Slack text alone as durable effect evidence.
- Record `do_not_rerun` only when replay would be invalid, destructive, provenance-breaking, already terminal, or prohibited by current authority.

## Failure states

- `NO_BASE_QUALIFICATION`: train/qualify before operational work.
- `CHECKPOINT_ABSENT`: rebuild operational state from current authoritative sources; absence is not permission to invent a predecessor.
- `CHECKPOINT_FORK_OR_AMBIGUITY`: fail closed and reconcile.
- `CHECKPOINT_DIGEST_MISMATCH`: reject the row.
- `TRAINING_BINDING_MISMATCH`: reject the checkpoint for this base.
- `CHECKPOINT_SCHEMA_INVALID`: reject the payload.
- `CURRENTNESS_REFRESH_FAILED`: preserve checkpoint as history and stop at the supported claim ceiling.
- `TARGET_AUTHORITY_UNRESOLVED`: do not perform the target effect.
