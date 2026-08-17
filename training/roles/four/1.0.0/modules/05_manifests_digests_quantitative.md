# FOUR-TRN-005 — Manifests, Digests, and Quantitative Verification

## Objective

Mechanically verify exact inventories and hard quantitative constraints.

## Exercise

Build a manifest for a sample package, compute byte counts and SHA-256 values, compute an ordered source-set digest, and verify a stated character-budget limit.

## Must pass

- Uses exact bytes and declared encoding.
- Defines ordering and serialization for aggregate digest computation.
- Mechanically verifies file count, byte count, hash, and character count.
- Detects duplicate paths, case drift, and stale generated manifests.
- Never reports an exact count from visual estimation.

## Automatic fail

Claiming an exact hash/count/character budget without a mechanical calculation.
