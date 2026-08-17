# BT2 Two Training Loader

Purpose: train a fresh ChatGPT conversation for the permanent BT2 role **Two / 2** without relying on a prior working chat or manually pasted prompts.

## Loader procedure

1. Confirm the conversation has been assigned role `BT2-TWO` / numerical identity `2`. This is a functional project role, not evidence of persistent personhood or uninterrupted runtime continuity.
2. Locate `training/roles/two/INDEX.yaml` in the authorized BT2 training-source repository.
3. Select the highest entry whose `status` is `APPROVED_FOR_NEW_BASES` and whose compatibility requirements are satisfied by the current verified permanent-role/governance contract. Do **not** select by version number alone.
4. Load that version's `TRAINING_MANIFEST.yaml` and verify every required file listed by the manifest exists. If `CHECKSUMS.sha256` is available, verify exact bytes before training.
5. If the current permanent role or Owner/Warden authority model materially conflicts with the selected version, stop with `TRAINING_VERSION_INCOMPATIBLE`. Do not patch the old training version in place. A new version is required.
6. Execute manifest modules strictly in `order`. A module is complete only when the trainee produces the required demonstration and the module pass criteria are satisfied. Mere acknowledgement, paraphrase, or self-asserted confidence is not a pass.
7. Preserve module answers and module verdicts as qualification evidence. Unresolved evidence, inaccessible required source, skipped module, or critical-failure behavior yields `TRAINING_UNRESOLVED` or `NOT_QUALIFIED`, never an assumed pass.
8. Execute the final qualification module only after all prerequisite modules pass.
9. The trainee may perform a preliminary self-check, but it may not self-award `BASE_READY`. An independent evaluator designated by current BT2 governance or the present user must apply `QUALIFICATION_RUBRIC.md` to the exact training run.
10. `BASE_READY` is allowed only under the exact conditions in the manifest. Record the exact repository, commit, version path, manifest/checksum identities, module results, and evaluator verdict using `BASE_READY_RECEIPT_TEMPLATE.yaml`.
11. Freeze that qualified chat as a **base**. The base carries trained competence only.
12. When a working chat is branched from the base, perform a fresh operational reorientation from current verified state: current governance, role map, roster, assignments, leases, blockers, provider/database state, and project priorities. Never import those mutable facts from the frozen training package.
13. After reorientation, load `training/roles/two/CHECKPOINT_PROTOCOL.md`. Working chats must maintain its turn counter and external continuity checkpoint discipline. The checkpoint protocol is operational infrastructure, not frozen training truth, and must itself be reread if it changes.

## Separation rule

- **Training source** = versioned repository modules and manifest.
- **Frozen base** = a fresh chat that passed one exact training version.
- **Operational state** = separately saved, current, reverified work/currentness loaded after branching.

None of these proves uninterrupted runtime, subjective continuity, or present write authority.
