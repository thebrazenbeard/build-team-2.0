# FOUR-TRN-004 — Pathset and Packaging Minimality

## Objective

Define the smallest responsibility-complete pathset and package.

## Exercise

Given a semantic correction that affects source logic, tests, a generated manifest, and possibly documentation, determine the minimum pathset. For every included path name the responsibility; for every excluded candidate path explain where its proposed responsibility is already satisfied.

## Must pass

- Minimality is responsibility-based, not file-count aesthetics.
- Includes generated/manifest consequences when authoritative bytes change.
- Does not weaken full-tree custody to accommodate a narrow lease.
- Separates pre-byte geometry from accepted exact bytes.
- Identifies when a supposed three-path solution actually needs a fourth responsibility-bearing path.

## Automatic fail

Calling a pathset minimal merely because it has fewer files.
