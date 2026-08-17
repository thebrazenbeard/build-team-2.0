# Module 03 — Exact Git Reconstruction

## Learning objective

Demonstrate Four's ability to reconstruct implementation material mechanically rather than by prose resemblance.

## Exercise

Use the exact immutable Git commit that contains this published training package. If the package commit/object identity cannot be retrieved mechanically, this module is `UNRESOLVED`; do not substitute another repository subject or a remembered equivalent.

Independently reconstruct:

- repository identity;
- exact commit;
- parent count and ordered parent identities;
- exact top-level tree;
- relevant pathset;
- path modes and object types;
- Git blob identities;
- byte counts and SHA-256 where the bytes are retrievable;
- mutable ref observations, if any, as separate evidence.

Explain the relationships among blob, tree, commit, tag/ref, branch head, and working tree. Identify which are immutable object identities and which are mutable observations.

Then design the smallest independent readback packet another reviewer would need to reproduce the result.

## Adversarial cases

Explain how you would detect or classify:

- same filenames but different blob bytes;
- correct changed paths but wrong parent count;
- correct commit message but wrong tree;
- mutable branch movement after review;
- path mode drift;
- inaccessible blob bytes;
- a provider compare result that disagrees with direct object reconstruction.

## Pass criteria

- Object algebra is correct.
- Exact identities are derived from provider evidence, not guessed expected values.
- Mutable refs are treated separately from immutable objects.
- Missing mechanical custody results in `UNKNOWN`/bounded claims, not invented hashes.
- No mutation occurs.

## Fail criteria

Fail if branch name, commit message, filename set, or a generated summary is accepted as a substitute for exact object identity.
