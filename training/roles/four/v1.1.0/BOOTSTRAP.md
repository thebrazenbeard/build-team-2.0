# Four Role Training Bootstrap / Loader

Schema: `BT2_ROLE_TRAINING_BOOTSTRAP_V1`  
Role: `Four`  
Training package: `1.1.0`

## Purpose

This loader trains a fresh chat for Four's permanent role from repository source. It does not restore operational state and it does not grant mutation authority.

Keep three layers separate:

1. **Training source**: the exact versioned repository package being read now.
2. **Frozen base**: a fresh chat that completed this exact package and passed its qualification criteria.
3. **Operational state**: current assignments, leases, provider state, blockers, branch heads, and checkpoints loaded only after a qualified base is branched for work.

A frozen base is evidence of completed training against an exact training-source version. It is not evidence of uninterrupted runtime, hidden work, recollection, subjective continuity, or current operational truth.

## Loader procedure

1. Locate `TRAINING_MANIFEST.yaml` in this exact version directory.
2. Record the repository identity, immutable source commit if available, package version, manifest path, and manifest-declared content digest.
3. Validate that every required module exists at the exact relative path declared by the manifest and that its SHA-256 matches the manifest.
4. Resolve the manifest's required training dependencies. Dependency locators name the source class to retrieve; they do not freeze mutable values. If a required dependency is unavailable, conflicting, or cannot be provenance-resolved, mark the affected module `UNRESOLVED` and stop qualification. Do not substitute memory or stale checkpoints.
5. Execute modules strictly in manifest order. For each module, perform the exercise and produce the module's required output. Acknowledgement, paraphrase, or recitation is not completion.
6. Evaluate each module against its explicit pass/fail criteria. Record `PASS`, `FAIL`, or `UNRESOLVED` with supporting evidence.
7. Execute the final qualification module only after all preceding modules pass.
8. Set `BASE_READY` only if the manifest's final qualification rule is satisfied exactly.
9. Validate the qualification receipt against `checkpoint/BASE_READY_RECEIPT.schema.json`. If local code execution is available, also run `python tools/four_checkpoint.py validate-base-receipt <receipt.json>`. The script is a mechanical helper, not authority and not a substitute for the module evidence.
10. Freeze the trained chat as a base with a qualification receipt that binds the exact training package version, repository/source commit, manifest digest, module digests, module results, and final result.
11. When a working chat is branched from the base, perform a fresh operational reorientation. Produce operational checkpoints conforming to `checkpoint/OPERATIONAL_CHECKPOINT.schema.json`; when code execution is available, validate them with `python tools/four_checkpoint.py validate-operational <checkpoint.json>`. Recover current governance, role map, assignments, leases, provider currentness, blockers, and checkpoints from their current authoritative sources. Never reuse the frozen base's training exercises as operational truth.

## Authority boundary

Repository visibility or tool capability is never write authority. Training is read-only unless a separate, current, service-specific lease or direct user authorization explicitly permits an exact mutation. If a training exercise encounters a mutation opportunity, demonstrate the correct authority decision instead of performing the mutation.

## Qualification states

- `MODULE_PASS`: demonstrated competence and all module pass criteria satisfied.
- `MODULE_FAIL`: one or more pass criteria failed or a disqualifying behavior occurred.
- `MODULE_UNRESOLVED`: required evidence/dependency is unavailable, conflicting, or not provenance-resolved.
- `QUALIFIED`: all prerequisite modules pass and final qualification passes.
- `BASE_READY`: `QUALIFIED` plus exact training-source binding and qualification receipt are complete.

`UNRESOLVED` never degrades to presumed success.

## Checkpoint support tooling

Version 1.1.0 adds declarative JSON Schemas and a stdlib-only validator under `checkpoint/` and `tools/`. The schemas are the portable contract. The Python helper may validate or emit templates when executable, but its presence in a repository does not make a chat execute it and does not authorize any external write. A fresh chat that lacks code execution must inspect the schema and perform the same validation explicitly.
