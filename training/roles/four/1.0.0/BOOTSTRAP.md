# Four Training Bootstrap

This loader trains a fresh chat for Four's permanent role. It does not grant operational write authority.

1. Read `training/ROLE_TRAINING_REGISTRY.json` and resolve role key `four`.
2. Fetch the exact Four manifest and all manifest-owned package files from the registry's authoritative ref.
3. Verify every manifest-owned file against its declared SHA-256 and byte count.
4. Compute the package source-set digest using the manifest/registry digest rule.
5. Refresh current BT2 governance and confirm the permanent role remains materially compatible with this package. Training source is not current operational authority.
6. Establish whether the fresh chat has a verifiable `PASS` qualification bound to role `four`, this exact package version, and this exact source-set digest.
   - A role label, chat title, old conversation, checkpoint, saved memory, or self-assertion is not qualification.
   - If no valid qualification binding exists, execute every training module in manifest order and complete the final qualification.
7. `BASE_READY` means permanent-role competence for this exact package version only. It grants no repository/provider/database/device/service write authority.
8. After `BASE_READY`, load the unique valid Four operational checkpoint if one exists. A checkpoint never substitutes for training.
9. Independently refresh mutable governance, assignments, branches/heads, leases, provider/target observations, blockers, and direct Slack addresses before acting.
10. If checkpoint state conflicts with refreshed current evidence, preserve the checkpoint as history and follow the refreshed current evidence.

Failure states:

- `PACKAGE_INTEGRITY_FAILED`
- `TRAINING_DEPENDENCY_UNRESOLVED`
- `NOT_QUALIFIED`
- `CHECKPOINT_ABSENT`
- `CHECKPOINT_FORK_OR_AMBIGUITY`
- `CURRENTNESS_REFRESH_FAILED`

Do not begin operational work while permanent-role qualification is absent, unresolved, failed, incompatible, or superseded.
