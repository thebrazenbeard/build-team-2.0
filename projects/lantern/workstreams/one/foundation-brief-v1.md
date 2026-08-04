# Project Lantern Foundation Brief v2.2

Status: `DRAFT_FOR_TWO_FINAL_RECHALLENGE`
Owner: One
Project key: `lantern`
Supersedes: Foundation Brief v2.1 at `383853b803dc91b20bc7ed1426cf31713bc9caef`
Challenge basis: Supabase events `76`, `81`, `82`, and `87`

## Goal and falsifiable value proposition

Long-running technical projects lose reliability when source observations, claims, assessments, decisions, contradictions, and changing state are flattened into prose, scattered across tools, or silently treated as current truth after their basis changes.

Lantern should be a local-first project-intelligence system that lets one operator answer, for an explicit actor and scope:

1. which claims are currently accepted, disputed, rejected, or unverified;
2. why those assessments exist;
3. which exact source observations support or oppose them;
4. what contradicts them;
5. what changed and when;
6. which decisions depend on affected evidence;
7. what now requires review;
8. whether another installation can reproduce the same records and answers.

Lantern does not determine global truth or one universal project belief. It returns current active assessments for named actors and scopes while preserving disputed, rejected, superseded, and unassessed claims.

Lantern earns the right to continue only if it outperforms a disciplined Git-and-Markdown control after both capture cost and reconstruction cost are counted.

## V1 scope

The primary v1 user is one technical operator, researcher, investigator, or project lead managing a complicated project over time.

V1 must support:

- observing a source without promoting its contents into truth;
- separating a source locator from the exact bytes or version observed;
- recording immutable claims;
- recording actor-and-scope-specific assessments;
- linking support, opposition, contradiction, dependency, and supersession explicitly;
- preserving disagreement without manufacturing compromise;
- recording decisions with evidence, assumptions, alternatives, authority, and dependencies;
- marking directly affected records `REVIEW_REQUIRED` when their declared basis changes;
- deterministic export and clean import without overwriting divergent records.

V1 does not include:

- a chatbot, persona, or autonomous agent;
- semantic search or natural-language extraction;
- cloud synchronization or multi-user collaboration;
- monitoring, background workers, or scheduled automation;
- a dashboard, plugin system, crawler, archive service, or general-purpose knowledge graph;
- replacement of GitHub, Supabase, Drive, or document storage;
- a BT2-only coordination framework.

## Smallest falsifiable vertical slice

The first usable version is a local command-line application operating on one portable project directory.

The fixed seeded case contains:

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

1. preserve both source observations and custody status;
2. preserve all claims and assessments separately;
3. show opposed and contradictory claims without resolving them automatically;
4. resolve exactly one current assessment for the selected claim, actor, and scope;
5. mark only the directly dependent assessment or decision `REVIEW_REQUIRED` after version B supersedes A;
6. export the project;
7. import it into a clean directory;
8. reproduce identical record IDs, record digests, links, current-state views, and query answers;
9. reject a divergent record with `CONFLICT` and preserve the existing record.

No model call, network access, credential, worker, scheduler, or autonomous external action is required.

## Project container metadata

`ProjectManifest` is container metadata, not a domain entity. It records:

- `project_id`;
- schema and interchange versions;
- creation metadata;
- project-root-relative path rules;
- custody and export policy;
- required compatibility information.

Paths are project-root-relative POSIX paths. Absolute paths, path traversal, backslash ambiguity, empty segments, and non-normalized segments are rejected.

## Six durable record types

Lantern v1 uses six durable record types. All durable record payloads are immutable.

### SourceSnapshot

Records what source material was actually observed:

- source identity and locator;
- observed version or state;
- observation time and retrieval route;
- digest and media type when available;
- custody mode: `REFERENCE_ONLY`, `CAPTURED`, `EMBEDDED`, `REDACTED`, or `UNAVAILABLE`;
- optional content-addressed retained bytes;
- omission reason when bytes are not retained or exported.

A locator says where material may be found. A SourceSnapshot says what was actually observed.

### Claim

An immutable attributable statement containing:

- subject and statement;
- actor or source attribution;
- epistemic class;
- subject scope;
- provenance.

A Claim has no global truth field and no mutable current-belief field.

### Assessment

An actor-and-scope-specific disposition of one Claim:

- `claim_id`;
- `assessor_id`;
- `scope_id`;
- disposition: `ACCEPTED`, `DISPUTED`, `REJECTED`, or `UNVERIFIED`;
- basis Links;
- effective bounds;
- predecessor Assessment when revised.

The Assessment key is:

```text
claim_id + assessor_id + scope_id
```

At most one Assessment is current for that key. A successor Assessment must name the current Assessment it supersedes and provide that expected current ID. A stale expected ID, concurrent successor, or second active Assessment returns `CONFLICT`. Current assessment state is derived from the immutable successor chain.

Lantern does not add consensus voting, confidence aggregation, or global project-truth semantics.

### Decision

An immutable decision version containing:

- chosen action or conclusion;
- actor and authority;
- evidence and assumptions;
- rejected alternatives;
- explicit dependency Links;
- disposition at creation.

A substantive revision creates a successor Decision. Operational lifecycle changes use Events. The prior Decision is never updated in place.

### Link

A durable typed relationship between compatible records.

The closed v1 vocabulary is:

- `SUPPORTS`;
- `OPPOSES`;
- `CONTRADICTS`;
- `DEPENDS_ON`;
- `SUPERSEDES`.

Constraints:

- `CONTRADICTS` connects Claim to Claim;
- `DEPENDS_ON` is directed, endpoint-validated, and cycle-checked;
- `SUPERSEDES` connects compatible records in one semantic lineage and rejects cycles;
- unsupported source-target combinations fail validation.

Other relation types remain deferred unless the seeded slice proves they are required.

### Event

An immutable occurrence, transition, verification, or receipt record, separate from Link.

Event types include:

- lifecycle transition;
- `REVIEW_REQUIRED` trigger;
- source observation result;
- import or export receipt;
- verification result;
- conflict result.

An Event references:

- affected record;
- actor;
- cause and evidence;
- expected predecessor Event or expected revision when applicable;
- resulting operational state.

## Immutable history and current state

SourceSnapshot, Claim, Assessment, Decision, Link, and Event records are immutable.

No durable domain record is updated in place. Every substantive reassessment or Decision revision creates a successor record naming what it supersedes. Operational lifecycle changes, including `REVIEW_REQUIRED`, create append-only Events bound to an affected record and expected predecessor Event or revision.

A stale predecessor, stale expected revision, invalid transition, or competing successor fails as `CONFLICT`.

Current state is a deterministic derived view over immutable records and Events.

A transactional current-head index or projection may be updated for query performance, but it must be fully rebuildable from immutable records and is never authoritative history.

## Canonical envelope and record identity

Every durable record uses a versioned canonical envelope containing:

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
- `record_sha256`.

Identity and serialization rules:

- `project_id` and `record_id` are UUIDv7 values assigned once at creation;
- IDs are preserved unchanged across export and import;
- UUID ordering bits are not temporal authority;
- `record_sha256` is SHA-256 over the complete canonical immutable record envelope excluding the `record_sha256` field;
- canonical bytes use UTF-8 JSON with sorted keys, normalized UTC timestamps, duplicate-key rejection, finite JSON values only, and normalized project-root-relative POSIX paths;
- same `record_id` plus same digest is `VERIFIED`;
- same `record_id` plus different canonical bytes or digest is `CONFLICT`;
- unsupported schema versions fail closed;
- divergent records are never overwritten.

Import outcomes are exactly:

- `VERIFIED`;
- `CREATED`;
- `CONFLICT`;
- `SKIPPED`.

## Source custody and export boundary

Captured source bytes are stored content-addressably under `sources/` when policy permits. Reference-only, private, licensed, prohibited, redacted, or unavailable material is not copied merely to make the archive look complete.

Every export declares:

- included SourceSnapshots;
- retained content digests;
- omitted, redacted, unavailable, and reference-only content;
- the reason for each omission;
- whether exact evidence reconstruction is possible.

Lantern must not claim reproducibility when the underlying evidence was never retained.

## Review-required semantics

Changed evidence does not automatically make a conclusion false.

When a SourceSnapshot, Claim, Assessment, or Decision is superseded or materially contradicted:

1. only explicitly linked active dependents are considered;
2. each directly affected dependent receives an immutable `REVIEW_REQUIRED` Event naming the triggering record and Link;
3. no durable dependent record is modified in place;
4. recursive dependency traversal is available as a query;
5. no recursive automatic rejection or truth revision occurs;
6. only an explicit successor Assessment or Decision changes substantive disposition.

## V1 architecture

Lantern v1 targets:

- one local Python process;
- SQLite as the default operational implementation;
- immutable append-preserved record rows;
- explicit transactions, foreign-key validation, and crash-safe commits;
- deterministic derived views;
- schema migration support;
- canonical JSON or NDJSON plus a manifest as the portability contract;
- a content-addressed `sources/` directory;
- a stable machine-readable CLI response envelope with human-readable rendering above it.

SQLite is the default v1 hypothesis, not the identity of the project format. If a bounded implementation spike proves SQLite cannot meet the frozen properties, One and Two must revise the architecture before implementation continues. Three may not silently substitute a graph database, cloud store, custom event service, or pure Markdown persistence.

The following interfaces must be frozen in Three's assignment and tests:

1. project directory and manifest layout;
2. canonical envelope and serialization;
3. SourceSnapshot custody contract;
4. Claim and Assessment vocabulary;
5. Assessment current-state and conflict rule;
6. Link endpoint and cycle rules;
7. Event transition and expected-predecessor rule;
8. Decision trace fields;
9. import and export classifications;
10. CLI response envelope and exit classes;
11. seeded benchmark fixture, expected answers, procedure, and pass rule.

## Pre-registered Git-and-Markdown control

Lantern must be compared with a supplied disciplined Git-and-Markdown workflow using the same seeded case, starting evidence, operator questions, and instructions.

Questions:

1. Which claim is currently accepted for the selected actor and scope?
2. What evidence opposes or contradicts it?
3. Why was the Decision made?
4. Which direct dependency now requires review?
5. Can another operator reconstruct the same state from the handoff?

Hard gates for every timed run:

- zero unsupported answers;
- zero missed contradiction;
- zero missed direct `REVIEW_REQUIRED` dependency;
- zero divergent import reconstruction;
- no overwrite on conflict;
- exact reconstruction of record IDs, digests, Links, and current query answers.

Procedure:

1. freeze the fixture, expected answers, instructions, and scoring receipt before Three receives implementation authority;
2. perform one untimed practice run per workflow;
3. perform three timed runs per workflow under the same conditions;
4. record capture time, reconstruction time, total operator time, inspected artifacts, provenance omissions, and errors;
5. preserve raw measurements and expected answers;
6. report capture overhead separately and include it in total operator time.

Preselected continuation rule:

Lantern passes only when:

1. every hard gate passes;
2. total operator time across capture plus the three timed runs is no greater than the Git-and-Markdown control; and
3. Lantern achieves either:
   - at least 30 percent lower median reconstruction time; or
   - at least 50 percent fewer inspected artifacts.

Failure narrows Lantern to a structured Markdown schema and generated index unless another material benefit was pre-registered before implementation. The pass rule may not be rewritten after results are known.

## Success criteria

The vertical slice must prove:

1. Every material Claim and Assessment exposes actor, scope, provenance, and basis.
2. Source location and exact observation remain distinct.
3. Contradictory Claims remain separately inspectable.
4. Exactly one current Assessment resolves for each Claim, assessor, and scope key.
5. Decision trace identifies evidence, assumptions, alternatives, dependencies, and authority.
6. Changed evidence creates attributable review requirements without mutating history or declaring truth automatically.
7. Export and import preserve deterministic identities and relationships.
8. Divergent imports fail as `CONFLICT` and never overwrite.
9. Cyclic dependencies and supersession cycles are rejected and reported.
10. The system runs locally without credentials or network access after installation.
11. Ordinary status is understandable without reading raw SQLite rows.
12. The pre-registered control comparison passes.

## Kill or narrow criteria

Lantern must be narrowed, redesigned, or stopped if:

- Git plus structured Markdown and a generated index delivers essentially the same value with materially less burden;
- the pre-registered benchmark rule fails;
- structured entry costs more effort than later reconstruction saves;
- the model cannot remain understandable to a competent operator;
- contradiction and Decision tracing do not reduce repeated investigation or change real decisions;
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
- While awaiting a specialist reply, One continues every nondependent definition, reconciliation, and verification task, then checks the ledger again before reporting status.
- Once Two confirms zero unresolved HIGH and MEDIUM foundation defects, One assigns Three one thin implementation slice.
- Other facets enter only for a concrete unresolved risk or exact validation need.

## Reconciliation status

The seven objections in event `76` and five remaining findings in event `82` are accepted or materially narrowed.

Event `87` is incorporated by:

- hashing the full canonical record envelope rather than only the payload;
- separating Link from Event;
- reducing the initial Link vocabulary to five required relations;
- adding cycle checks for dependency and supersession;
- allowing only rebuildable nonauthoritative current-head projections;
- counting capture cost in the benchmark continuation rule;
- adding one untimed practice run and three timed runs per workflow;
- requiring total operator time not to exceed the control.

## Immediate next gate

Two reviews this exact revision and reports only remaining material HIGH or MEDIUM defects. Previous verdicts remain historical and do not transfer automatically.

No implementation assignment is authorized until that exact-head challenge returns zero unresolved HIGH and MEDIUM defects.
