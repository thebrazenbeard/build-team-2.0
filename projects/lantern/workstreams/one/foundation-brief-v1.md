# Project Lantern Foundation Brief v2

Status: `DRAFT_FOR_TWO_RECHALLENGE`
Owner: One
Project key: `lantern`
Supersedes: Foundation Brief v1 at `aecc8a6b30b41afa8379fb63a4f3c4820608e42d`
Challenge basis: Supabase event `76`

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

Lantern earns the right to exist only if it makes those answers materially easier or more accurate than a disciplined Git-and-Markdown control workflow after entry cost is included.

## Intended user and first use cases

The primary v1 user is one technical operator, researcher, investigator, or project lead managing a complicated project over time.

The first use cases are:

- observe a source without promoting its contents into truth;
- distinguish a source identity from the exact bytes or state observed at a particular time;
- record immutable claims;
- record actor-and-scope-specific assessments of claims;
- link support, opposition, assumptions, constraints, and dependencies explicitly;
- preserve contradiction without manufacturing compromise;
- record decisions with evidence, assumptions, alternatives, authority, and status;
- mark directly affected claims and decisions `REVIEW_REQUIRED` when their basis changes, without automatically declaring them false;
- export and re-import a portable, inspectable project capsule without overwriting divergent records.

Multi-user collaboration, semantic extraction, model assistance, and cloud synchronization are not required to prove the core value.

## Smallest falsifiable vertical slice

The first usable version is a local command-line application operating on one portable project directory.

The seeded test project contains:

- two observed versions of one source;
- three claims, including one explicit contradiction;
- scoped assessments for one operator and project context;
- one decision that depends on a claim supported by the superseded source observation.

The minimum operations are:

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
3. display the contradiction without resolving it automatically;
4. mark the directly dependent decision `REVIEW_REQUIRED` with an attributable reason;
5. export the project;
6. import it into a clean directory;
7. reproduce the same record identities, links, lifecycle states, and query answers.

No model call, network access, background worker, scheduler, or autonomous external action is required.

## Six core concepts

Lantern v1 uses only these top-level concepts unless a required query cannot be expressed cleanly:

1. **ProjectManifest**
   - project identity;
   - schema and interchange versions;
   - creation metadata;
   - declared custody and export policy.

2. **SourceSnapshot**
   - source identity and locator;
   - observation time and retrieval route;
   - digest and media type when available;
   - custody mode: `REFERENCE_ONLY`, `CAPTURED`, `EMBEDDED`, `REDACTED`, or `UNAVAILABLE`;
   - optional content-addressed retained bytes;
   - explicit omission reason when bytes are not exported.

3. **Claim**
   - immutable attributable statement;
   - epistemic class and subject scope;
   - no global truth or current-belief field.

4. **Assessment**
   - assessor;
   - project, decision, or inquiry scope;
   - disposition: `ACCEPTED`, `DISPUTED`, `REJECTED`, or `UNVERIFIED`;
   - basis links;
   - effective bounds and supersession.

5. **Decision**
   - chosen action or conclusion;
   - actor and authority;
   - evidence, assumptions, alternatives, and dependencies;
   - lifecycle including `ACTIVE`, `REVIEW_REQUIRED`, `REVISED`, and `SUPERSEDED`.

6. **LinkEvent**
   - typed relationship or event connecting records;
   - initial link vocabulary: `SUPPORTS`, `OPPOSES`, `CONTEXTUALIZES`, `ASSUMES`, `CONSTRAINS`, `DEPENDS_ON`, `CONTRADICTS`, and `SUPERSEDES`;
   - verification receipts and lifecycle transitions are event subtypes rather than new top-level entities.

Temporal fields belong to the canonical record envelope. Contradiction and supersession are typed links or events, not separate systems demanding their own miniature governments.

## Canonical record envelope

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
- lifecycle;
- `supersedes` when applicable;
- `payload_sha256`.

Before Three builds, Lantern must freeze:

- canonical UTF-8 JSON serialization with sorted keys;
- normalized UTC timestamps;
- duplicate-key rejection;
- finite JSON values only;
- normalized repository-relative paths where paths appear;
- deterministic record-ID derivation or generation rules;
- import results: `VERIFIED`, `CREATED`, `CONFLICT`, or `SKIPPED`;
- no overwrite of divergent records.

SQLite file bytes are not the portability contract. Canonical records and the manifest are.

## Source observation and custody

A source locator identifies where material may be found. A source snapshot records what was actually observed.

Every observation records:

- locator and source identity;
- observation time;
- retrieval route;
- digest where bytes are available;
- media type;
- custody mode;
- retention or omission status.

Captured source bytes are stored content-addressably under the project directory when policy permits. Exports must identify every absent, redacted, or unavailable source and why it is missing. Lantern must not silently imply reproducibility when the underlying evidence was never retained.

## Review-required propagation

Changed evidence does not automatically make a conclusion false.

When an active SourceSnapshot, Claim, Assessment, or Decision is superseded or contradicted:

1. directly linked active dependents receive `REVIEW_REQUIRED`;
2. the transition records the triggering record and link;
3. recursive dependency traversal is available as a query;
4. no recursive automatic rejection occurs;
5. only an explicit actor assessment or decision revision changes substantive disposition.

This keeps Lantern from becoming an automated certainty machine, a product category humanity has already overfunded.

## Architecture decision for v1

Lantern v1 uses:

- one local process;
- SQLite as the canonical operational store;
- append-only immutable record rows;
- explicit transactions and foreign-key validation;
- derived views for status and decision tracing;
- canonical JSON or NDJSON plus a manifest as the portable interchange format;
- a content-addressed `sources/` directory for retained source bytes;
- a stable machine-readable CLI response envelope with human-readable rendering layered above it.

Stable interfaces required before implementation:

1. project directory and manifest layout;
2. canonical record envelope and serialization;
3. source custody modes;
4. closed initial record and link vocabulary;
5. import/export classifications and conflict behavior;
6. deterministic `REVIEW_REQUIRED` rules;
7. CLI response envelope and exit classes.

No plugin system, API server, web interface, general knowledge graph, model layer, or cloud service belongs in the first slice.

## Executable control comparison

Lantern must be tested against a supplied disciplined Git-and-Markdown workflow using the same seeded project and the same operator questions:

1. Which claim is currently accepted for the selected actor and scope?
2. What evidence contradicts it?
3. Why was the decision made?
4. Which dependency now requires review?
5. Can another operator reconstruct the same state from the handoff?

Measure:

- completion time;
- unsupported or incorrect answers;
- omitted provenance;
- missed contradiction or stale dependency;
- files or records inspected;
- data-entry and capture overhead;
- successful portable reconstruction.

Lantern advances beyond the prototype only if it produces a material trace-accuracy improvement or a material reconstruction-time improvement without hiding greater capture cost. If the Markdown control delivers essentially the same reliability with materially less burden, Lantern narrows to a schema-and-index tool or stops.

The benchmark protocol and pass rule must be frozen before the prototype is judged. The implementation may not rewrite the test after seeing its score, because even software deserves protection from moving goalposts.

## Non-goals for v1

Lantern v1 is not:

- a chatbot, persona, or autonomous agent;
- a general-purpose knowledge graph;
- a replacement for GitHub, Supabase, Drive, or document storage;
- a cloud collaboration service;
- a desktop or web dashboard;
- a monitoring or scheduled-automation system;
- a semantic-search or natural-language-extraction system;
- a system that treats ingested material as instruction or truth;
- a complete solution for every research, legal, scientific, or compliance domain;
- a BT2-only coordination framework.

## Success criteria

The vertical slice must prove:

1. Every material claim and assessment exposes actor, scope, provenance, and basis.
2. Source identity and exact source observation remain distinct.
3. Contradictory claims remain separately inspectable.
4. Decision trace identifies evidence, assumptions, alternatives, dependencies, and authority.
5. Changed evidence creates attributable review requirements without automatic truth revision.
6. Export and re-import preserve deterministic identities and relationships.
7. Divergent imports fail as `CONFLICT` and never overwrite.
8. The system runs locally without credentials or network access after installation.
9. Ordinary status is understandable without reading raw SQLite rows.
10. The control comparison justifies continuing beyond the prototype.

## Kill or narrow criteria

Lantern must be narrowed, redesigned, or stopped if:

- Git plus structured Markdown and a generated index delivers essentially the same value with materially less burden;
- structured entry costs more effort than later reconstruction saves in representative use;
- the provenance, assessment, and temporal model cannot remain understandable to a competent operator;
- contradiction and decision tracing do not change real decisions or reduce repeated investigation;
- reproducibility depends on retained material that cannot legally, privately, or practically be exported;
- the architecture requires cloud services, broad automation, or model inference before the local slice is useful;
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
- Once Two confirms zero unresolved HIGH or MEDIUM foundation defects, One assigns Three one thin implementation slice.
- Other facets enter only for a concrete unresolved risk or exact validation need.

## Reconciliation of Two's objections

- `LANTERN-TWO-001`: accepted. Claim and scoped Assessment are separated.
- `LANTERN-TWO-002`: accepted. Source identity, observed snapshot, custody, and retained bytes are separated.
- `LANTERN-TWO-003`: accepted. Canonical record envelope and import conflict behavior are now required pre-build interfaces.
- `LANTERN-TWO-004`: accepted. Propagation produces attributable `REVIEW_REQUIRED`, never automatic rejection.
- `LANTERN-TWO-005`: accepted. The Git-and-Markdown comparison is now an executable control test.
- `LANTERN-TWO-006`: accepted. The domain is reduced to six top-level concepts.
- `LANTERN-TWO-007`: accepted. SQLite is selected for v1 operations; canonical JSON or NDJSON remains the interchange contract.

## Immediate next gate

Two re-challenges this exact revision and reports only remaining material HIGH or MEDIUM issues. One resolves any remaining defect directly. Once none remain, Three receives one bounded vertical-slice assignment.

No wider Lantern workflow is authorized before that gate clears.