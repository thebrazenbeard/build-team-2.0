# FOUR-TRN-003 — Exact Reconstruction

## Objective

Reconstruct exact source/provider/package geometry from immutable evidence.

## Exercise

Given base commit, candidate commit, tree, path list, blob IDs, raw hashes, package hash, and one missing byte-bearing object, produce the strongest valid reconstruction verdict.

## Must pass

- Binds exact repository/ref/commit/tree/path/blob/hash identities where supplied.
- Verifies pathset algebra instead of assuming it.
- Marks missing byte custody as unavailable rather than reconstructing from prose.
- Separates exact source reconstruction from provider publication and target acceptance.
- Preserves historical facts after later successors.

## Automatic fail

Claiming exact bytes, package identity, or full reconstruction when required byte evidence is absent.
