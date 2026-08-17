# Five Operational Checkpoint Protocol

Schema: `FIVE_OPERATIONAL_RESUME_CHECKPOINT_V1`

The checkpoint store is operational continuity, not permanent training, canonical memory, or current provider truth.

## Training binding

A Five checkpoint is usable only when role key `five`, package version, source-set digest, and (when BASE_READY has been established) qualification ID agree with the frozen base. A checkpoint with `qualification_id = null` may preserve work history but cannot establish BASE_READY or substitute for qualification.

## Write rule

Checkpoints are append-only. Before writing a root or successor:

1. Resolve exactly one current Five checkpoint leaf, or verify no Five checkpoint exists.
2. Refresh current Working Laws, permanent role map, direct `#five` addresses across visible BT2 channels, current assignments, Service Warden/lease state, and provider/target facts material to the next claim.
3. Preserve immutable source/candidate/artifact identities separately from mutable refs, environment configuration, deployment state, target observations, and release claims.
4. Serialize exactly one `FIVE_OPERATIONAL_RESUME_CHECKPOINT_V1` payload with `checkpoint_tool.py canonicalize`; hash those exact UTF-8 bytes.
5. Insert using exact role/training binding and predecessor.
6. Read back the row and verify predecessor, qualification/training binding, payload bytes/digest, schema, role key, timestamps, source surface, and source ref.
7. Never update/delete old checkpoints to make history cleaner.

## Read rule

A working Five chat first resolves the current GitHub training registry, verifies the exact registered package source, and proves PASS qualification for that version/digest or trains first. It then resolves the checkpoint leaf. Checkpoint values are historical orientation evidence until independently refreshed against mutable governing/provider surfaces.

No checkpoint, training package, BASE_READY result, role title, repository permission, or tool capability grants a service write.

## Five-specific preservation rules

- Preserve source identity, provider custody, artifact custody, target observation, deployment effect, and release authorization as separate layers.
- Record repository numeric identity, immutable commit/tree/blob identities, mutable ref observations, exact pathsets/modes, raw digests when required, and opening/closing currentness.
- Preserve registry discovery state separately from qualification-admission state. GitHub discovery without the corresponding Supabase package tuple is not end-to-end training usability.
- Preserve ambiguous non-idempotent effects as unresolved until independent readback; never retry merely to obtain green state.
- Preserve superseded findings and historical FAIL/BLOCKED evidence without applying old verdicts to successor bytes.
- Preserve claim ceilings and unknowns explicitly.
- Record direct identity-addressed Slack messages relevant to active work; Slack routing is assignment evidence, not proof of provider/device effects.

## Failure states

- `NO_BASE_QUALIFICATION`: train/qualify before ordinary operational work.
- `TRAINING_REGISTRY_MISMATCH`: discovery and qualification-admission surfaces do not cross-bind the same package tuple.
- `CHECKPOINT_ABSENT`: rebuild current state from authoritative sources; do not invent a predecessor.
- `CHECKPOINT_FORK_OR_AMBIGUITY`: fail closed and reconcile.
- `CHECKPOINT_DIGEST_MISMATCH`: reject the row.
- `TRAINING_BINDING_MISMATCH`: reject checkpoint for this base.
- `CHECKPOINT_SCHEMA_INVALID`: reject payload.
- `CURRENTNESS_REFRESH_FAILED`: preserve checkpoint as history and stop at supported claim ceiling.
- `WRITE_AUTHORITY_UNRESOLVED`: do not perform the service effect.
