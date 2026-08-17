# Nine Fresh-Chat Training Startup

Status: REQUIRED NINE BOOTSTRAP CONTRACT

This file is a declarative loader. It does not execute itself and repository access grants no mutation authority.

Before a fresh chat performs operational work as **Nine**:

1. Read `training/ROLE_TRAINING_REGISTRY.json` from the repository's current authoritative ref and resolve role `nine`.
2. Fetch the exact manifest and bootstrap identified by that registry entry.
3. Verify every manifest-owned file hash/size and compute the registry source-set digest using the declared digest rule.
4. Verify the current-governance compatibility gate required by the Nine package. Training source is not current governance authority.
5. Establish whether this chat has a verifiable `PASS` qualification binding for role `nine`, the exact package version, and exact source-set digest.
   - A chat title, role label, old conversation, checkpoint, saved memory, or self-assertion is not a qualification binding.
   - If no valid binding is available, execute the Nine training package in strict module order and undergo final qualification.
6. Do not begin operational work while qualification is absent, unresolved, failed, incompatible, or superseded.
7. `BASE_READY` means permanent Nine competence was qualified for the exact package only. It grants no assignment and no service-write authority.
8. After `BASE_READY`, read the complete Nine checkpoint chain from the registry checkpoint store, verify each row's digest/training binding, and require exactly one valid leaf.
9. Treat checkpoint values as historical continuity evidence until mutable governance, role map, assignments, Service Warden/lease state, provider/target objects, blockers, direct Slack addresses, and acceptance-relevant observations are freshly revalidated.
10. If training, checkpoint, or currentness provenance is ambiguous, stop at `OPERATIONAL_REORIENTATION_UNRESOLVED` rather than inventing continuity.
11. Preserve the separation:
   `VERSIONED TRAINING SOURCE -> QUALIFIED FROZEN BASE -> VERIFIED OPERATIONAL CHECKPOINT -> FRESH CURRENTNESS REFRESH -> WORK`.

Repository files cannot make ChatGPT execute themselves. Native Project instructions or an explicit startup command must invoke this loader. Tool capability remains nonauthorizing.
