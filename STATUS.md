# Build Team 2.0 Repository Status

Observed: 2026-09-28

## Role

This repository is a non-canonical predecessor/compatibility source for BT2
training, continuity, and Protocol V2 behavior.

The active canonical BT2 engineering/runtime repository is:

`thebrazenbeard/bt2`

This repository does not override current BT2 Project instructions, provider
state, assignments, runtime state, or protected-effect authority.

## What remains authoritative here

Within this repository's historical/compatibility scope:

- versioned role-training source packages;
- role-training registry bindings;
- checkpoint schemas and deterministic checkpoint helpers;
- Protocol V2 execution-precedence source;
- Protocol V2 regression material.

These artifacts are source/provenance. Runtime qualification records or
provider bindings named inside them are not automatically current.

## Repair findings

The pre-repair README described an application/runtime surface that no longer
exists in this repository: no `pyproject.toml`, no `.env.example`, no
Agents-SDK CLI package, no old runtime architecture docs, and no
`migrations/001_build_team_2.sql`.

The repository is therefore repaired as a training/continuity source corpus,
not reconstructed into the retired application shape.

## Qualification

The repair adds:

- `scripts/validate_repository.py`;
- hosted repository validation;
- Protocol V2 overlay regression execution;
- checkpoint helper tests;
- Four v1.0.1 package validation.

A passing repository qualification proves source integrity for this repository.
It does not prove current BT2 runtime/provider state.
