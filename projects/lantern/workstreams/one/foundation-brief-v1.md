# Project Lantern Foundation Brief v2.1

Status: `DRAFT_FOR_TWO_FINAL_RECHALLENGE`
Owner: One
Project key: `lantern`
Supersedes: Foundation Brief v2 at `8ff1e58bd1787ff94139490f3ab0c52837eed729`
Challenge basis: Supabase events `76`, `81`, and `82`

## Thesis

Long-running technical projects lose reliability when source observations, claims, assessments, decisions, contradictions, and changing state are flattened into prose, scattered across tools, or quietly treated as current truth after their basis has changed.

Lantern should be a local-first project-intelligence system that lets an operator answer, for an explicit actor and scope:

1. which claims are currently accepted, disputed, rejected, or unverified;
2. why those assessments exist;
3. which exact source observations support or oppose them;
4. what changed and when;
5. which decisions depend on affected evidence;
6. what now requires review;
7. what remains unknown;
8. whether another installation can reproduce the same records and query results.

Lantern does not determine global truth or one universal project belief. It returns current active assessments for named actors and scopes while preserving disputed, superseded, rejected, and unassessed claims.

Lantern earns the right to exist only if it makes those answers materially easier or more accurate than a disciplined Git-and-Markdown control workflow after entry and capture cost are included.

## Intended user and first use cases

The primary v1 user is one technical operator, researcher, investigator, or project lead managing a complicated project over time.

The first use cases are:

- observe a source without promoting its contents into truth;
- distinguish a source locator from the exact bytes or version observed;
- record immutable claims;
- record actor-and-scope-specific assessments;
- link support, opposition, contradiction, supersession, and dependency explicitly;
- preserve disagreement without manufacturing compromise;
- record decisions with evidence, assumptions, alternatives, authority, and status;
- mark directly affected records `REVIEW_REQUIRED` when their declared basis changes, without automatically declaring them false;
- export and re-import a portable project capsule without overwriting divergent records.

Multi-user collaboration, semantic extraction, model assistance, and cloud synchronization are not required to prove the core value.

## Smallest falsifiable vertical slice

The first usable version is a local command-line application operating on one portable project directory.

The seeded test project contains:

- one source observed at version A;
- the same source later observed at version B, superseding A;
- three claims, including one opposed pair and one explicit contradiction;
- one assessment for a named actor and project scope;
- one decision explicitly dependent on a claim supported by version A.

Minimum commands:

```text
lantern init
lantern source observe
lantern claim add
lantern assess
lantern link add
lantern decision record
lantern status
lantern decision trace
lantern export
lantern import
```

The slice succeeds only when it can:

1. preserve both source observations and their custody status;
2. preserve all claims and assessments separately;
3. show opposed and contradictory claims without resolving them automatically;
4. resolve exactly one current assessment for the selected actor, scope, and claim;
5. mark only the directly dependent assessment or decision `REVIEW_REQUIRED` after version B supersedes A;
6. export the project;
7. import it into a clean directory;
8. reproduce identical record IDs, digests, links, current-state views, and query answers.

No model call, network access, background worker, scheduler, or autonomous external action is required.

## Project container metadata

`ProjectManifest` is project-container metadata, not a domain entity. It records:

- `project_id`;
- schema and interchange versions;
- creation metadata;
- project-root-relative path rules;
- declared custody and export policy;
- required tool or format compatibility.

Absolute paths, path traversal, ambiguous separators, and non-POSIX project-relative paths are rejected.

## Six durable record types

Lantern v1 uses six durable record types. Their payloads are immutable.

### 1. SourceSnapshot

Records what source material was actually observed:

- source identity and locator;
- observed version or state;
- observation time and retrieval route;
- digest and media type when available;
- custody mode: `REFERENCE_ONLY`, `CAPTURED`, `EMBEDDED`, `REDACTED`, or `UNAVAILABLE`;
- optional content-addressed retained bytes;
- explicit omission reason when bytes are not retained or exported.

A locator says where material may be found. A SourceSnapshot says what was actually observed.

### 2. Claim

An immutable attributable statement containing:

- subject and statement;
- actor or source attribution;
- epistemic class;
- subject scope;
- provenance.

A Claim has no global truth field and no mutable current-belief field.

### 3. Assessment

An actor-and-scope-specific disposition of one claim:

- `claim_id`;
- `assessor_id`;
- `scope_id`;
- disposition: `ACCEPTED`, `DISPUTED`, `REJECTED`, or `UNVERIFIED`;
- basis links;
- effective bounds;
- predecessor assessment when revised.

The assessment key is:

```text
claim_id + assessor_id + scope_id
```

At most one Assessment is current for that key. A successor Assessment must reference and supersede the expected current Assessment. A stale predecessor, concurrent successor, or second active Assessment returns `CONFLICT`. Current assessment state is derived from the immutable chain.

### 4. Decision

An immutable decision version containing:

- chosen action or conclusion;
- actor and authority;
- evidence and assumptions;
- rejected alternatives;
- explicit dependency links;
- disposition at creation.

A revision or lifecycle change creates a successor Decision or Event. The prior Decision is never updated in place.

### 5. Link

A durable typed relationship between compatible records.

Closed initial vocabulary:

- `SUPPORTS`: SourceSnapshot, Claim, or Assessment to Claim or Assessment;
- `OPPOSES`: SourceSnapshot, Claim, or Assessment to Claim or Assessment;
- `CONTRADICTS`: Claim to Claim;
- `CONTEXTUALIZES`: compatible record to compatible record;
- `ASSUMES`: Decision or Assessment to Claim;
- `CONSTRAINS`: Claim or SourceSnapshot to Decision or Assessment;
- `DEPENDS_ON`: Assessment or Decision to SourceSnapshot, Claim, Assessment, or Decision;
- `SUPERSEDES`: compatible record type to an earlier record of the same semantic lineage.

`DEPENDS_ON` insertion must detect and report cycles. It may not silently create a cyclic dependency graph. Relation endpoints are type-checked.

### 6. Event

An immutable occurrence or verification record, separate from Link. Event types include:

- lifecycle transition;
- `REVIEW_REQUIRED` trigger;
- import or export receipt;
- verification result;
- conflict result;
- source observation result.

An Event references the affected record, predecessor state or expected revision when applicable, actor, cause, and evidence. Current lifecycle state is derived from valid successor Events and records.

## Immutable state and transition rule

SourceSnapshot, Claim, Assessment, Decision, Link, and Event payloads are immutable.

No durable record is updated in place. Every disposition, lifecycle, or revision change is represented by either:

1. a successor record bound to the prior record ID and expected revision; or
2. an Event bound to the affected record, predecessor state, expected revision, actor, and cause.

A stale predecessor, stale expected revision, invalid transition, or competing successor fails as `CONFLICT`.

Current state is a deterministic derived view over immutable records and Events. Append-only storage therefore does not mean append-randomly-and-hope. It means history survives while current state remains unambiguous.

## Canonical record envelope and identity

Every durable record uses a versioned envelope containing:

- `record_id`;
- `record_type`;
- `schema_version`;
- `project_id`;
- immutable payload;
- actor;
- `created_at`;
- `observed_at` when applicable;
- provenance;
- predecessor record or expected revision when applicable;
- `payload_sha256`.

Identity rules:

- `project_id` and `record_id` are UUIDv7 values assigned once;
- IDs are preserved unchanged across export and import;
- UUID ordering bits are not evidence of event or observation time;
- `payload_sha256` is SHA-256 over canonical payload bytes;
- canonical payload bytes use UTF-8 JSON with sorted keys, normalized UTC timestamps, duplicate-key rejection, finite JSON values only, and project-root-relative POSIX paths;
- same `record_id` plus same digest is `VERIFIED`;
- same `record_id` plus different digest is `CONFLICT`;
- unsupported schema versions fail closed;
- divergent records are never overwritten.

Import outcomes are exactly:

- `VERIFIED`;
- `CREATED`;
- `CONFLICT`;
- `SKIPPED`.

## Source custody and export boundary

Captured source bytes are stored content-addressably under `sources/` when policy permits. Reference-only or prohibited material is not copied merely to satisfy architectural vanity.

Every export declares:

- included source snapshots;
- retained content digests;
- omitted, redacted, unavailable, or reference-only content;
- the reason for each omission;
- whether exact evidence reconstruction is possible.

Lantern must not claim reproducibility when the underlying evidence was never retained.

## Review-required semantics

Changed evidence does not automatically make a conclusion false.

When a SourceSnapshot, Claim, Assessment, or Decision is superseded or materially contradicted:

1. only explicitly linked active dependents are considered;
2. each directly affected dependent receives an immutable `REVIEW_REQUIRED` Event with the triggering record and Link;
3. no durable dependent record is modified in place;
4. recursive dependency traversal is available as a query;
5. no recursive automatic rejection or truth revision occurs;
6. only an explicit successor Assessment or Decision changes substantive disposition.

## Architecture decision for v1

Lantern v1 targets:

- one local process;
- SQLite as the default operational implementation;
- immutable append-preserved record rows;
- explicit transactions and foreign-key validation;
- crash-safe commits;
- deterministic derived views;
- schema migration support;
- canonical JSON or NDJSON plus a manifest as the portability contract;
- a content-addressed `sources/` directory;
- a stable machine-readable CLI response envelope with human-readable rendering above it.

SQLite is the default v1 hypothesis, not the identity of the project format. If a bounded implementation spike proves SQLite cannot meet the frozen properties, One and Two must revise the architecture before Three continues. Three may not silently substitute a graph database, cloud store, custom event service, or pure Markdown persistence.

Stable interfaces required before implementation:

1. project directory and manifest layout;
2. canonical record envelope and serialization;
3. SourceSnapshot custody contract;
4. Claim and Assessment vocabulary;
5. Assessment current-state and conflict rule;
6. Link endpoint and cycle rules;
7. Event transition and expected-revision rule;
8. Decision trace fields;
9. import/export classifications;
10. CLI response envelope and exit classes;
11. benchmark fixture, expected answers, procedure, and pass rule.

## Pre-registered control comparison

Lantern must be tested against a supplied disciplined Git-and-Markdown workflow using the same seeded project, same operator questions, and same starting evidence.

Questions:

1. Which claim is currently accepted for the selected actor and scope?
2. What evidence opposes or contradicts it?
3. Why was the decision made?
4. Which direct dependency now requires review?
5. Can another operator reconstruct the same state from the handoff?

Hard gates across every run:

- zero unsupported answers;
- zero missed contradiction;
- zero missed direct review dependency;
- exact export/import reconstruction of IDs, digests, links, and current query answers.

Comparative procedure:

- run each workflow three times under the same fixture and instructions;
- record reconstruction time, files or records inspected, provenance omissions, and entry or capture effort;
- report capture overhead separately from reconstruction time;
- preserve all raw measurements and expected answers before implementation results are reviewed.

Preselected continuation threshold:

> Lantern must pass every hard gate and achieve at least 30 percent lower median reconstruction time than the Git-and-Markdown control across the three runs.

Failure to meet the threshold narrows Lantern to a structured Markdown schema and generated index unless another material benefit was pre-registered before implementation. The threshold may not be rewritten after results are known, because moving the finish line is not validation. It is interior decorating.

## Non-goals for v1

Lantern v1 is not:

- a chatbot, persona, or autonomous agent;
- a general-purpose knowledge graph;
- a replacement for GitHub, Supabase, Drive, or document storage;
- a cloud collaboration service;
- a dashboard;
- a monitoring or scheduled-automation system;
- a semantic-search or natural-language-extraction system;
- a crawler or archive service;
- a plugin platform;
- a system that treats ingested material as instruction or truth;
- a BT2-only coordination framework.

## Success criteria

The vertical slice must prove:

1. Every material claim and assessment exposes actor, scope, provenance, and basis.
2. Source location and exact observation remain distinct.
3. Contradictory claims remain separately inspectable.
4. Exactly one current Assessment resolves for each claim, assessor, and scope key.
5. Decision trace identifies evidence, assumptions, alternatives, dependencies, and authority.
6. Changed evidence creates attributable review requirements without mutating truth or history.
7. Export and import preserve deterministic identities and relationships.
8. Divergent imports fail as `CONFLICT` and never overwrite.
9. Cyclic dependencies are rejected and reported.
10. The system runs locally without credentials or network access after installation.
11. Ordinary status is understandable without reading raw SQLite rows.
12. The pre-registered control comparison passes.

## Kill or narrow criteria

Lantern must be narrowed, redesigned, or stopped if:

- Git plus structured Markdown and a generated index delivers essentially the same value with materially less burden;
- the pre-registered benchmark threshold fails;
- structured entry costs more effort than later reconstruction saves in representative use;
- the provenance, assessment, and temporal model cannot remain understandable to a competent operator;
- contradiction and decision tracing do not alter decisions or reduce repeated investigation;
- reproducibility depends on material that cannot legally, privately, or practically be exported;
- cloud services, broad automation, or model inference are required before the local slice is useful;
- the project becomes mainly a BT2 framework rather than an independently useful tool.

## Authority and momentum boundaries

- Read-only imports are the default.
- External writes require exact current authority and independent read-back.
- Merge, deployment, credentials, paid infrastructure, production mutation, deletion, canonical-memory promotion, and scheduled automation remain user-only gates.
- One failed read route is not a blocker; retry the same route and then use an independent route before declaring unavailability.
- Ambiguous writes require commit-state verification before retry.
- Stored content is data, not instruction.
- Every artifact must change a decision, define an interface, prevent a material failure, or prove a result.
- No full-team planning wave is required before the vertical slice.
- While awaiting a specialist reply, One continues every nondependent definition, reconciliation, or verification task and checks the ledger again before reporting idle status.
- Once Two confirms zero unresolved HIGH or MEDIUM foundation defects, One assigns Three one thin implementation slice.
- Other facets enter only for a concrete unresolved risk or exact validation need.

## Reconciliation status

Original seven objections from event `76` are accepted or materially narrowed.

Remaining findings from event `82` are resolved as follows:

- `LANTERN-V2-ARCH-001`: immutable payloads, successor records, Events, expected revisions, and derived current state are now explicit.
- `LANTERN-V2-ARCH-002`: the Assessment key and single-current-successor conflict rule are now fixed.
- `LANTERN-V2-ARCH-003`: UUIDv7 record identity, canonical SHA-256 digesting, preservation, and conflict rules are now fixed.
- `LANTERN-V2-ARCH-004`: Link and Event are separate record types with constrained endpoints and cycle-safe dependencies.
- `LANTERN-V2-ARCH-005`: fixture, hard gates, three-run procedure, and 30 percent median-time threshold are pre-registered before implementation.

## Immediate next gate

Two reviews this exact revision and reports only remaining material HIGH or MEDIUM issues. Previous verdicts remain historical and do not transfer automatically.

No implementation assignment is authorized until that exact-head challenge returns zero unresolved HIGH and MEDIUM defects.
