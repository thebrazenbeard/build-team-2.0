# Eight Operational Checkpoint Protocol

Schema: `EIGHT_OPERATIONAL_CHECKPOINT_V1`

Status: **CONTINUITY SCAFFOLD / TRAINING BINDING NOT YET REGISTERED**

Eight is the economical, pragmatic, maintainability-focused facet. Its continuity record preserves cost/delay/complexity tradeoffs, operational burden, maintainability risks, implementation alternatives, evidence sufficiency, and the exact source/authority state needed to resume pragmatic review.

The checkpoint store is operational continuity, not canonical memory and not permanent training.

## Qualification rule

`training/ROLE_TRAINING_REGISTRY.json` currently has no registered Eight package. Until an exact Eight training package/version/digest and PASS qualification are registered, an Eight checkpoint cannot establish `BASE_READY` by itself.

## Write rule

A checkpoint is append-only. Every successor names exactly one predecessor. Before writing a successor:

1. Read the complete Eight checkpoint chain and resolve exactly one current leaf.
2. Refresh current Build Team governance and `docs/PROTOCOL_EXECUTION_PRECEDENCE_V2.md`.
3. Refresh the exact source/target, implementation alternatives, current blockers, resource/cost evidence, and mutation authority relevant to the review.
4. Separate measured cost/resource evidence from estimates and assumptions.
5. Record maintainability/operational debt and alternatives without converting preference into fact.
6. Create the successor against the exact leaf and verify readback.

## Read rule

A working Eight chat reads the exact current training registry first. If Eight is not registered/qualified, it may reconstruct current pragmatic/operational context from authoritative sources but must report `BASE_READY = NOT_ESTABLISHED` and cannot treat this scaffold as training or authority.

After a valid training binding exists, resolve the unique valid checkpoint leaf and independently refresh mutable currentness before any cost, feasibility, maintainability, or effect claim.

## Role-specific claim discipline

Eight should preserve:
- measured versus estimated cost/resource evidence;
- complexity and maintenance burden;
- delay and operational friction;
- simpler viable alternatives;
- portability and long-term support concerns;
- evidence/provenance sufficiency for tradeoff claims;
- exact source/target cut reviewed.

A checkpoint never grants spending, purchase, provider mutation, merge, deploy, or production authority.

## Failure states

- `NO_REGISTERED_TRAINING_BINDING`
- `CHECKPOINT_ABSENT`
- `CHECKPOINT_FORK_OR_AMBIGUITY`
- `TRAINING_BINDING_MISMATCH`
- `EVIDENCE_INSUFFICIENT`
- `CURRENTNESS_REFRESH_FAILED`
