# Module 05 — Specification-to-Pathset Materialization

## Learning objective

Translate accepted semantics into the smallest sufficient exact implementation/package pathset while preserving generated provenance.

## Exercise

Assume an accepted semantic owner changes behavior in one executable source file. The repository also contains:

- a checked-in generated source manifest;
- a source-path registry;
- focused tests;
- full-package tests;
- a deterministic package builder;
- optional workflow/documentation files.

Determine, with reasons, whether each surface must change.

You must explicitly test these questions:

1. Does an existing-path byte change require source-path-registry mutation?
2. Does the generated manifest require regeneration?
3. Are focused-test changes required to make the new semantic contract executable and falsifiable?
4. Does a workflow belong in the product pathset merely because it runs validation?
5. Is documentation normative, descriptive, or generated?
6. What happens if the semantic requirement is under-specified?

Design a validation order that includes:

- exact predecessor/source snapshot;
- candidate application;
- deterministic generator run;
- pre-test exact diff capture;
- focused and full tests;
- second generator run;
- generated-byte stability check;
- post-test clean-worktree check;
- exact allowed-pathset check;
- deterministic package rebuild/rebuild comparison;
- final source/package crossbind.

## Self-heal hostile

A test invokes the generator in-place before comparing the manifest. A stale checked-in manifest is silently rewritten and the test reports green. Explain why this is not acceptance and how your procedure detects it.

## Pass criteria

- Minimum pathset is justified from dependencies, not aesthetic preference.
- Generated provenance cannot self-heal unnoticed.
- Extra workflow/docs paths are not added without a real material dependency.
- Semantic ambiguity is escalated instead of invented.
- Validation order prevents a green-but-dirty result.

## Fail criteria

Fail if the trainee uses “related file” as sufficient reason to expand scope, accepts self-healing tests, or changes semantics while claiming to perform materialization only.
