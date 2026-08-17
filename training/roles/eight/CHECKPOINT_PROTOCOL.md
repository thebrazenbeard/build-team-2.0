# Eight Training Checkpoint Protocol

This role-level protocol supports resumable training and BASE_READY verification without changing the semantic contents of an already-versioned training package.

## Create a checkpoint skeleton

Run `checkpoint_tool.py init --version <training-version> --source-commit <immutable-commit-or-source-id> --output <checkpoint.json>` only after resolving the exact versioned manifest path. The generated checkpoint begins as `TRAINING_IN_PROGRESS` and is deliberately nonauthorizing.

During training, record module outcomes in order. A completed BASE_READY checkpoint must list exactly M01 through M09, with M01-M08 `PASS`, M09 `QUALIFIED`, zero automatic failures, zero unresolved required criteria, and a nonempty evidence summary. Change `status` to `BASE_READY` only after those conditions are actually met.

Validate with `checkpoint_tool.py validate <checkpoint.json>`. Exit 0 means only that the checkpoint satisfies the role-training structural criteria. It does not prove current governance, assignments, leases, provider state, repository state, Google Drive state, deployment state, uninterrupted runtime, or subjective continuity.

## Operational reorientation

A branch created from a BASE_READY chat must treat the checkpoint as training continuity evidence only. Before current work, reread current governed role/Working Laws, assignments, authority/leases, and relevant provider/service state. Fresh governed evidence overrides saved operational history.

## Version discipline

The tools live outside version directories intentionally. They may validate multiple immutable training versions. Material changes to training semantics belong in a new version directory. Do not silently rewrite a version that may already have qualified a frozen base.
