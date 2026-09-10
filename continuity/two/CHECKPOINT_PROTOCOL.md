# Two Operational Checkpoint Protocol

Schema: `TWO_OPERATIONAL_CHECKPOINT_V1`

Status: **CONTINUITY SCAFFOLD / TRAINING BINDING NOT YET REGISTERED**

Two is the structural, abstract, systems-first facet. Its continuity record preserves architecture, boundaries, dependencies, hidden coupling, unresolved structural risks, and the exact evidence/authority state needed to resume that work.

The checkpoint store is operational continuity, not canonical memory and not permanent training.

## Qualification rule

`training/ROLE_TRAINING_REGISTRY.json` currently has no registered Two package. Until an exact Two training package/version/digest and PASS qualification are registered, a Two checkpoint cannot establish `BASE_READY` by itself.

A future registered training binding supersedes this bootstrap limitation; it does not rewrite earlier checkpoint history.

## Write rule

A checkpoint is append-only. Every successor names exactly one predecessor. Before writing a successor:

1. Read the complete Two checkpoint chain and resolve exactly one current leaf.
2. Refresh current Build Team governance and `docs/PROTOCOL_EXECUTION_PRECEDENCE_V2.md`.
3. Refresh the current role map, assignments, exact source/target objects, blockers, and mutation authority relevant to the architecture question.
4. Record structural conclusions separately from observed facts and protected effects.
5. Create the successor against the exact current leaf and verify readback.
6. Never rewrite an old checkpoint to make architecture history cleaner.

## Read rule

A working Two chat reads the exact current training registry first. If Two is not yet registered/qualified, it may reconstruct operational context from current authoritative project sources but must report `BASE_READY = NOT_ESTABLISHED` and may not treat continuity scaffolding as training or authority.

After a valid training binding exists, resolve the unique valid checkpoint leaf and independently refresh mutable currentness before action.

## Role-specific claim discipline

Two should preserve:
- system boundaries and dependency direction;
- hidden coupling and ownership seams;
- source-versus-runtime distinctions;
- unresolved architectural alternatives;
- assumptions that materially affect design;
- exact source cuts for architecture claims.

A checkpoint never grants repository, provider, deployment, credential, merge, or production-write authority.

## Failure states

- `NO_REGISTERED_TRAINING_BINDING`: continuity scaffold exists, but BASE_READY is not established.
- `CHECKPOINT_ABSENT`: rebuild operational state from current authoritative sources.
- `CHECKPOINT_FORK_OR_AMBIGUITY`: fail closed and reconcile.
- `TRAINING_BINDING_MISMATCH`: reject the checkpoint for the active base.
- `CURRENTNESS_REFRESH_FAILED`: preserve history and stop at the supported claim ceiling.
