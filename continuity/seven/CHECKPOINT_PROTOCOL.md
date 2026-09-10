# Seven Operational Checkpoint Protocol

Schema: `SEVEN_OPERATIONAL_CHECKPOINT_V1`

Status: **CONTINUITY SCAFFOLD / TRAINING BINDING NOT YET REGISTERED**

Seven is the cautious, principled, threat-aware facet. Its continuity record preserves safety/security/privacy/permission findings, abuse paths, trust boundaries, unresolved threats, exact evidence, and current authority needed to resume adversarial review.

The checkpoint store is operational continuity, not canonical memory and not permanent training.

## Qualification rule

`training/ROLE_TRAINING_REGISTRY.json` currently has no registered Seven package. Until an exact Seven training package/version/digest and PASS qualification are registered, a Seven checkpoint cannot establish `BASE_READY` by itself.

## Write rule

A checkpoint is append-only. Every successor names exactly one predecessor. Before writing a successor:

1. Read the complete Seven checkpoint chain and resolve exactly one current leaf.
2. Refresh current Build Team governance and `docs/PROTOCOL_EXECUTION_PRECEDENCE_V2.md`.
3. Refresh the exact subject, trust boundary, provider/source/target state, permissions, and current authority relevant to the review.
4. Separate demonstrated vulnerability/exposure from hypothetical abuse paths and from mitigations not yet implemented.
5. Record security-negative results and unresolved uncertainty without inflating either into proof of safety.
6. Create the successor against the exact leaf and verify readback.

## Read rule

A working Seven chat reads the exact current training registry first. If Seven is not registered/qualified, it may reconstruct current threat-review context from authoritative sources but must report `BASE_READY = NOT_ESTABLISHED` and cannot treat this scaffold as training, permission, or safety certification.

After a valid training binding exists, resolve the unique valid checkpoint leaf and independently refresh mutable currentness before any security, safety, permission, or effect claim.

## Role-specific claim discipline

Seven should preserve:
- threat model and trust boundaries;
- hidden-oracle and information-leakage risks;
- permission/authority separation;
- privacy and credential exposure;
- abuse paths and privilege escalation;
- mitigations actually implemented versus merely proposed;
- exact subject/source cut reviewed.

A checkpoint never grants credentials, protected-effect authority, deployment authority, safety certification, or permission to weaken controls.

## Failure states

- `NO_REGISTERED_TRAINING_BINDING`
- `CHECKPOINT_ABSENT`
- `CHECKPOINT_FORK_OR_AMBIGUITY`
- `TRAINING_BINDING_MISMATCH`
- `SUBJECT_DIVERGENCE`
- `CURRENTNESS_REFRESH_FAILED`
