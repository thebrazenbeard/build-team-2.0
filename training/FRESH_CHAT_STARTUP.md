# BT2 Fresh-Chat Training Startup

Status: REQUIRED BOOTSTRAP CONTRACT

This file is a declarative loader. It does not execute itself and repository access grants no mutation authority.

## Fresh role startup

Before a fresh chat performs operational work as any registered BT2 role:

1. Read `training/ROLE_TRAINING_REGISTRY.json` from the repository's current authoritative ref.
2. Resolve the **assigned role key** and fetch the exact manifest/bootstrap identified by that registry entry.
3. Bind the training source to the registry-listed immutable source commit and source-set digest. Verify the package's bound file hashes and current-governance compatibility exactly as required by its loader.
4. Establish whether this chat has a verifiable base binding to a `PASS` qualification receipt for that exact role, package version, and source-set digest.
   - A chat title, role label, prior conversation resemblance, checkpoint, memory, historical assignment, or self-assertion is not a base binding.
   - If no valid binding is available, execute the listed training package in strict manifest order and undergo its final qualification process.
5. Do not begin operational work while training is `IN_PROGRESS`, `BLOCKED`, `FAILED`, `PENDING`, `SUPERSEDED_OR_INCOMPATIBLE`, or otherwise unresolved under the role package.
6. `BASE_READY` means only that permanent role competence was qualified for the exact package. It grants no service-write authority and supplies no current assignments, leases, provider state, or device state.
7. After `BASE_READY`, resolve that role's operational checkpoint chain from the registry-listed checkpoint store and role-specific checkpoint protocol/schema. Accept only one unambiguous valid current leaf.
8. Treat checkpoint observations as saved continuity evidence, not automatically current truth. Refresh current Working Laws, permanent role map, assignments/supersession, Service Warden/lease state, provider heads/objects, blockers, and direct coordination before action.
9. If the checkpoint chain is absent, forked, digest-invalid, qualification-mismatched, training-binding-mismatched, or otherwise ambiguous, stop with `OPERATIONAL_REORIENTATION_UNRESOLVED` rather than inventing continuity.
10. Preserve the separation:
   `VERSIONED TRAINING SOURCE -> QUALIFIED FROZEN BASE -> VERIFIED OPERATIONAL CHECKPOINT -> FRESH CURRENTNESS REFRESH -> WORK`.

## Native Project startup hook

For automatic enforcement in every newly opened BT2 chat, the native Build Team Two Project Instructions must contain a startup rule that invokes this contract before role work. Repository files cannot cause ChatGPT to execute themselves.

Recommended minimal hook:

`On a fresh role chat, before operational work, resolve training/ROLE_TRAINING_REGISTRY.json from the current BT2 training repository; resolve the assigned role; prove an exact BASE_READY binding for that registry-listed package or run and qualify it; then load the role's unique valid operational checkpoint and freshly revalidate current governance/provider/authority state. Training source, frozen base, and operational state are distinct. Repository/tool access never grants write authority.`

If that native hook is absent, the repository and Supabase machinery remain available but automatic fresh-chat invocation is not proven.
