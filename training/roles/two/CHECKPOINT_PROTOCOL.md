# BT2 Two Operational Checkpoint Protocol

Purpose: preserve enough externally recoverable operational continuity for a later Two working branch without confusing a checkpoint with training source, current authority, personhood, or uninterrupted runtime continuity.

## Scope

This protocol applies **after** a chat has been trained/qualified as Two and has performed fresh operational reorientation. It is not part of frozen training version semantics. It may be revised separately when current BT2 governance changes checkpoint requirements.

## Turn counter

1. Count user turns in the active working conversation.
2. At the end of every fifth user turn, after completing useful current work, persist one external Two checkpoint and reset the local checkpoint counter to zero.
3. If the fifth-turn checkpoint cannot be persisted, do not pretend it exists. Record the failure in the current response, preserve the intended checkpoint payload locally if possible, and retry only under the current write/retry discipline.
4. A new branch does not inherit a trustworthy counter from prose alone. Recover the newest verified checkpoint and begin a fresh counter from the branch activation/reorientation unless current governance supplies a stronger counter source.

## Required checkpoint payload

Use `CHECKPOINT_TEMPLATE.yaml` as the field contract. At minimum record:

- schema and checkpoint purpose;
- identity `Two` / numerical identity `2`;
- training-source version/commit used by the base when known;
- current verified Working Laws revision/source;
- current verified permanent-role map source;
- canonical coordination-ledger high-water;
- active assignment IDs, states, and exact bounded scopes;
- current service-specific leases held by Two, if any;
- blockers/inaccessible dependencies;
- exact mutable provider/database heads or other currentness observations materially needed to resume work;
- external effects attempted this turn and their verified readback status;
- unresolved High/Medium findings relevant to Two's current work;
- exact next executable action;
- claim boundary stating that the checkpoint is continuity evidence only, not present authority or uninterrupted-runtime/personhood evidence.

Do **not** stuff entire project history into the checkpoint. Preserve the smallest state sufficient to reorient without guessing.

## Persistence surface

Persist to a current BT2-approved external continuity surface that a replacement Two can mechanically retrieve. Prefer Two's designated Slack home channel when Slack coordination writes are available and permitted. If current governance designates another canonical checkpoint surface, use that instead.

Repository presence, tool access, or the ability to write a surface does not itself authorize mutation. Respect the current service/coordination authority model.

## Write and readback discipline

1. Before persistence, resolve the current checkpoint target/surface and authority.
2. Give the checkpoint a unique operation identity when the surface/protocol supports it.
3. Perform one bounded write.
4. Independently read back the persisted checkpoint and verify the material fields.
5. If the write result is ambiguous, inspect the target/effect state before any retry. Never blindly duplicate a checkpoint write.
6. Authentication, authorization, schema, hash, integrity, or safety failures are deterministic stops, not transient retry candidates.

## Recovery procedure

A later working branch must:

1. load its qualified frozen-base competence;
2. retrieve the newest mechanically verified Two checkpoint;
3. treat checkpoint contents as historical/currentness evidence, not automatic present authority;
4. re-resolve current Working Laws, role map, roster, assignments, leases, blockers, and mutable provider/database state;
5. reconcile any disagreement in favor of fresher authoritative evidence;
6. continue only executable current work.

A checkpoint may say what was true when written. It cannot make stale state current by surviving longer than the thing it described.
