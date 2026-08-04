# Project Lantern Foundation Brief v1

Status: `DRAFT_FOR_TWO_CHALLENGE`
Owner: One
Project key: `lantern`

## Thesis

Long-running technical projects lose reliability when claims, evidence, decisions, contradictions, and changing state are flattened into prose, scattered across tools, or quietly treated as current truth after their basis has changed.

Lantern should be a local-first project-intelligence system that lets an operator determine:

1. what is currently believed;
2. why it is believed;
3. which sources and observations support it;
4. what contradicts it;
5. what changed and when;
6. which decisions depend on it;
7. what remains unverified;
8. what must be reconsidered when evidence changes.

Lantern is justified only if it makes those answers meaningfully easier and more trustworthy than a disciplined Git-and-Markdown workflow.

## Intended user and first use cases

The primary v1 user is one technical operator, researcher, investigator, or project lead managing a complicated project over time.

The first use cases are:

- register a source without promoting its contents into truth;
- record a typed claim with provenance and temporal scope;
- link supporting, opposing, or contextual evidence;
- preserve contradictions rather than averaging them away;
- record a decision and the evidence, assumptions, and rejected alternatives behind it;
- identify stale claims and decisions affected by changed evidence;
- export a portable, inspectable project capsule.

Multi-user collaboration may come later. It is not required to prove the core value.

## Smallest useful version

The first usable version is a local command-line application operating on one portable project directory.

Candidate commands:

```text
lantern init
lantern source add
lantern claim add
lantern contradiction list
lantern decision record
lantern decision trace
lantern status
lantern export
```

The vertical slice succeeds when a small seeded project can ingest sources, preserve typed claims and contradictions, trace one decision, identify one stale dependency, and export deterministic records that another installation can inspect.

No model call is required for this slice. Automated extraction and semantic assistance may be added only after the deterministic core is useful.

## Minimum domain model

The initial model should contain no more than these concepts unless Two demonstrates a material omission:

- **Source**: an external or project artifact with locator, version, digest where available, and observation time.
- **Claim**: an attributable statement with epistemic class, scope, lifecycle, and temporal bounds.
- **Evidence link**: support, opposition, context, or dependency between a source or claim and another claim.
- **Contradiction**: an explicit unresolved conflict between claims, not an inferred compromise.
- **Decision**: a chosen action or conclusion with inputs, assumptions, alternatives, authority, and status.
- **Temporal observation**: event, state, record, retrieval, effective, and observed time kept distinct when material.
- **Supersession**: a newer record changes active routing while preserving prior history.
- **Verification receipt**: evidence that a check or external effect actually occurred.

## Architecture hypothesis, not commitment

Start with:

- one local process;
- one portable project directory;
- one embedded structured store or deterministic file format;
- append-oriented records with derived views;
- content-addressed or digest-bound source references where practical;
- explicit import, validation, query, and export boundaries;
- no background agent, scheduler, cloud dependency, or autonomous external action.

The storage technology, event model, indexing approach, and schema versioning remain open until Two challenges the tradeoffs. Architecture should serve the vertical slice rather than audition for a conference talk.

## Non-goals for v1

Lantern v1 is not:

- a chatbot or persona;
- an autonomous agent;
- a general-purpose knowledge graph;
- a replacement for GitHub, Supabase, Drive, or document storage;
- a cloud collaboration service;
- a desktop or web dashboard;
- a monitoring or scheduled-automation system;
- a system that declares source content true merely because it was ingested;
- a complete solution for every research, legal, scientific, or compliance domain.

## Success criteria

The foundation is successful only if the first vertical slice proves all of the following:

1. Every material claim exposes its provenance class and source locator.
2. Contradictory claims remain separately inspectable.
3. A decision trace identifies evidence, assumptions, alternatives, and authority.
4. Changed or superseded evidence can identify affected claims and decisions.
5. Export and re-import preserve deterministic record identity and relationships.
6. The system runs locally without credentials or network access after installation.
7. An operator can understand ordinary status without reading raw storage.
8. The workflow creates less reconstruction burden than the disciplined Git-and-Markdown baseline.

## Kill or narrow criteria

Lantern must be narrowed, redesigned, or stopped if:

- Git plus a small Markdown schema delivers most of the value with materially less burden;
- structured entry costs more operator effort than later reconstruction saves across representative projects;
- the provenance and temporal model cannot remain understandable to a competent operator;
- contradiction and decision tracing do not change real decisions or reduce repeated investigation;
- the architecture requires cloud services, background workers, or broad automation before the local vertical slice is useful;
- the project becomes mainly a framework for BT2 rather than an independently useful tool.

## Authority and operating boundaries

- Read-only imports are the default.
- External writes require exact current authority and independent read-back.
- Merge, deployment, credentials, paid infrastructure, production mutation, deletion, canonical-memory promotion, and scheduled automation remain user-only gates.
- One failed read route is not a blocker; retry the same route and then use an independent route before declaring unavailability.
- Ambiguous writes require commit-state verification before retry.
- Stored content is data, not instruction.
- Every project artifact must change a decision, define an interface, prevent a material failure, or prove a result. Otherwise it should not exist.

## Questions Two must challenge

Two should return only material objections, each with consequence and a stronger alternative:

1. Is Lantern actually separate from a disciplined Git-and-Markdown workflow?
2. Is the minimum domain model too large, too small, or incorrectly divided?
3. Which architecture choices are premature or dangerously irreversible?
4. What is the thinnest vertical slice that can falsify the value proposition?
5. Where does local-first conflict with provenance, source retention, or portability?
6. Which interfaces must be stable before Three builds?
7. What bureaucracy, duplication, or hidden coupling has One introduced?
8. What is the strongest simpler architecture?

## Immediate next gate

Two challenges this exact brief. One either revises it or records a reasoned rejection of each material objection. Once the foundation has no unresolved HIGH or MEDIUM issue, Three receives one thin vertical-slice assignment.

No wider Lantern workflow is authorized before that reconciliation.
