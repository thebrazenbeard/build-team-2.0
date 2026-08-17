# Masa Checkpoint Support Contract v1

This support layer sits beside immutable training source `v1.0.0`; it does not alter that version's training semantics.

## Evidence classes

- Training source: `training/roles/masa/v1.0.0/`
- Frozen base: a fresh chat that passed one exact training-source version.
- Operational checkpoint: mutable current-work evidence used for branch resumption.
- Support tool: optional helper only; repository presence does not execute it.

## Commands

`verify-package PACKAGE_DIR` verifies manifest role/version, exact M01-M09 order, module presence, and all `SHA256SUMS` entries.

`new-checkpoint --manifest MANIFEST --output FILE` emits an empty operational checkpoint bound to the exact manifest SHA-256. It deliberately does not guess mutable current state.

`validate-checkpoint FILE` checks checkpoint structure, role/version, allowed claim classes, and the continuity disclaimer.

## Operational fill

Populate mutable state only from fresh governed evidence: Working Laws/role map, roster, coordination high-water, assignments, exact subjects, provider observations and observation times, leases or explicit absence, HIGH/MEDIUM findings, dependencies, and handoff receipts.

A checkpoint proves neither uninterrupted runtime nor subjective continuity. It does not grant current authority or make stale provider observations current.
