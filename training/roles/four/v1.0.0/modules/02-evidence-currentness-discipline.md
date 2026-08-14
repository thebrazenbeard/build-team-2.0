# Module 02 — Evidence, Provenance, and Currentness Discipline

## Learning objective

Separate immutable identity, mutable currentness, artifact custody, historical chronology, and claim ceilings.

## Exercise

Analyze this scenario:

- A saved Four checkpoint says branch `feature/x` was at commit `A`.
- A later coordination record names commit `B` as a review subject.
- The provider currently shows `feature/x` at commit `C`.
- An immutable artifact is explicitly bound to `B`.
- Assignment 1 asks Four to reconstruct exact `B`.
- Assignment 2 instead asks Four to review the current branch.

For each assignment, explain which evidence controls:

- assignment subject identity;
- branch currentness;
- artifact identity;
- chronology;
- provider effect claims;
- what must be reread before a write-capable action.

Produce at least six allowed statements and six superficially plausible statements that must be rejected. Include examples involving:

- immutable commit vs mutable ref;
- artifact bound to an older commit;
- saved operational checkpoint;
- current provider read;
- observation time;
- unknown currentness;
- historical acceptance on superseded bytes.

## Required demonstration

The trainee must explain why retrieval is not recollection and why a save-state checkpoint is a recovery aid rather than proof of present provider state or uninterrupted runtime.

## Pass criteria

- Immutable and mutable evidence are never conflated.
- Exact-subject review and current-branch review are handled differently.
- Historical acceptance is bounded to its exact subject.
- Currentness claims require current evidence appropriate to the claim.
- `UNKNOWN` remains a legitimate outcome.

## Fail criteria

Fail on branch-name-as-identity reasoning, checkpoint-as-current-truth reasoning, artifact-name-as-byte-custody reasoning, or any claim that older acceptance automatically transfers to changed bytes.
