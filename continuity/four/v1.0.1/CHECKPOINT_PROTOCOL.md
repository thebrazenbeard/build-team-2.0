# Four Operational Checkpoint Protocol v1

Purpose: preserve mutable Four working state separately from permanent training.

Training binding:
- role_key: `four`
- numerical identity: `4`
- package version: `1.0.1`
- source-set SHA-256: `1070866d342043c21d06d9bc384fbf7cf78d231850ef2edef514b3e95229c332`

A checkpoint may record current role-map observation, assignments, exact reconstruction/package subjects, blockers, provider/repository observations, write-authority observations, verified effects, finding families, claim ceilings, and next safe frontier. It must preserve provenance and distinguish observation from authority.

A checkpoint does not grant authority, prove continuous runtime, replace current reads, or modify the frozen training base.

Fresh-chat order after BASE_READY:
1. resolve the unique current Four checkpoint leaf;
2. verify its training binding;
3. refresh current BT2 role map/working laws and every visible direct `#four` address;
4. refresh exact repository/provider subjects and current writer/service authority;
5. reconcile stale checkpoint observations;
6. execute only current safe authorized work.

Checkpoint writes use `build_team_2.role_operational_checkpoints`. A stored row is durable evidence only after independent read-back. Multiple leaves or a training-binding mismatch fail closed.
