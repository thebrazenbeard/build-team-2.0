# Three Operational Checkpoint Protocol

Schema: `THREE_OPERATIONAL_CHECKPOINT_V1`

Status: **CONTINUITY SCAFFOLD / TRAINING BINDING NOT YET REGISTERED**

Three is the concrete, energetic, implementation-first facet. Its continuity record preserves executable plans, implementation state, artifact/source bindings, verification evidence, blockers, and the exact authority/currentness needed to resume implementation safely.

The checkpoint store is operational continuity, not canonical memory and not permanent training.

## Qualification rule

`training/ROLE_TRAINING_REGISTRY.json` currently has no registered Three package. Until an exact Three training package/version/digest and PASS qualification are registered, a Three checkpoint cannot establish `BASE_READY` by itself.

## Write rule

A checkpoint is append-only. Every successor names exactly one predecessor. Before writing a successor:

1. Read the complete Three checkpoint chain and resolve exactly one current leaf.
2. Refresh current Build Team governance and `docs/PROTOCOL_EXECUTION_PRECEDENCE_V2.md`.
3. Refresh exact repository/branch/PR/provider/target state relevant to the implementation.
4. Record intended implementation separately from verified execution/effect.
5. Record blockers, failed attempts, retries, and alternative methods without rewriting history.
6. Create the successor against the exact leaf and verify readback.

## Read rule

A working Three chat reads the exact current training registry first. If Three is not registered/qualified, it may reconstruct current implementation context from authoritative sources but must report `BASE_READY = NOT_ESTABLISHED` and cannot treat this scaffold as training or mutation authority.

After a valid training binding exists, resolve the unique valid checkpoint leaf and independently refresh mutable source/provider/target and authority facts before action.

## Role-specific claim discipline

Three should preserve:
- exact source/branch/PR/artifact identities;
- implementation plan and completed steps;
- tests actually run and their results;
- failed attempts and materially different retries;
- remaining executable work;
- source/build/install/runtime/effect as separate states.

A checkpoint never grants merge, deploy, provider mutation, credential, machine-write, or production authority.

## Failure states

- `NO_REGISTERED_TRAINING_BINDING`
- `CHECKPOINT_ABSENT`
- `CHECKPOINT_FORK_OR_AMBIGUITY`
- `TRAINING_BINDING_MISMATCH`
- `SOURCE_OR_TARGET_DIVERGENCE`
- `CURRENTNESS_REFRESH_FAILED`
