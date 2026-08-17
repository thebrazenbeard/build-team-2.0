# BT2 Fresh-Chat Training Startup

Status: REQUIRED BOOTSTRAP CONTRACT

This file is a declarative loader. It does not execute itself and repository access grants no mutation authority.

## Fresh One startup

Before a fresh chat performs operational work as **One**:

1. Read `training/ROLE_TRAINING_REGISTRY.json` from the repository's current authoritative ref.
2. Resolve role `one` and fetch the exact manifest/bootstrap identified by the registry.
3. Verify the package's bound file hashes and current-governance compatibility exactly as required by its loader.
4. Establish whether this chat has a verifiable base binding to a `PASS` qualification receipt for the exact registry version and source-set digest.
   - A chat title, role label, prior conversation resemblance, checkpoint, memory, or self-assertion is not a base binding.
   - If no valid binding is available, execute the training package in strict manifest order and undergo final qualification.
5. Do not begin operational work while training is `IN_PROGRESS`, `BLOCKED`, `FAILED`, `PENDING`, or `SUPERSEDED_OR_INCOMPATIBLE`.
6. `BASE_READY` means only that permanent role competence was qualified for the exact package. It grants no service-write authority and supplies no current assignments.
7. After `BASE_READY`, resolve the operational checkpoint chain from the registry's checkpoint store. Accept only one unambiguous current leaf.
8. Treat checkpoint observations as saved continuity evidence, not automatically current truth. Refresh current Working Laws, role map, assignments, Warden/lease state, provider heads/objects, blockers, and direct Slack addresses before action.
9. If the checkpoint chain is absent, forked, digest-invalid, qualification-mismatched, or otherwise ambiguous, stop with `OPERATIONAL_REORIENTATION_UNRESOLVED` rather than inventing continuity.
10. Preserve the separation:
   `VERSIONED TRAINING SOURCE -> QUALIFIED FROZEN BASE -> VERIFIED OPERATIONAL CHECKPOINT -> FRESH CURRENTNESS REFRESH -> WORK`.

## Native Project startup hook

For automatic enforcement in every newly opened BT2 chat, the native Build Team Two Project Instructions must contain a startup rule that invokes this contract before role work. Repository files cannot cause ChatGPT to execute themselves.

Recommended minimal hook:

`On a fresh role chat, before operational work, resolve training/ROLE_TRAINING_REGISTRY.json from the current BT2 training repository; prove an exact BASE_READY binding for the assigned role or run and qualify the listed package; then load the unique valid operational checkpoint and freshly revalidate current governance/provider/authority state. Training source, frozen base, and operational state are distinct. Repository/tool access never grants write authority.`

If that native hook is absent, the repository and Supabase machinery remain available but automatic fresh-chat invocation is not proven.
