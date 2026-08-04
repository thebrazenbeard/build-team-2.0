# Project Lantern Foundation Brief v2.3

Status: `DRAFT_FOR_TWO_FINAL_RECHALLENGE`
Owner: One
Project key: `lantern`
Supersedes: Foundation Brief v2.2 at `8e3fb21d1e7161347dbc967be287fe2155848da2`
Challenge basis: Supabase events `76`, `81`, `82`, `87`, and `89`

## Goal

Long-running technical projects lose reliability when source observations, claims, assessments, decisions, contradictions, and changing state are flattened into prose, scattered across tools, or silently treated as current truth after their basis changes.

Lantern is a local-first project-intelligence system for one operator. For an explicit actor and scope, it must answer:

1. which claims are accepted, disputed, rejected, or unverified;
2. why those assessments exist;
3. which exact source observations support or oppose them;
4. what contradicts them;
5. what changed and when;
6. which decisions depend on affected evidence;
7. what now requires review;
8. whether another installation can reconstruct the same records and answers.

Lantern does not determine global truth or one universal project belief. It returns current active assessments for named actors and scopes while preserving rejected, disputed, superseded, and unassessed claims.

Lantern continues only if it outperforms a disciplined Git-and-Markdown control after both capture and reconstruction costs are counted.

## V1 scope

V1 must support:

- exact source observation without promoting source content into truth;
- immutable Claims;
- actor-and-scope-specific Assessments;
- immutable Decisions with evidence, assumptions, alternatives, authority, and dependencies;
- typed Links for support, opposition, contradiction, dependency, and supersession;
- deterministic `REVIEW_REQUIRED` StateEvents;
- deterministic export and clean import without overwriting divergent records.

V1 excludes models, semantic search, cloud synchronization, multi-user collaboration, dashboards, plugins, crawlers, background workers, monitoring, scheduled automation, and general-purpose knowledge-graph behavior.

## Fixed vertical slice

The seeded case contains:

- one source observed at version A;
- the same source observed later at version B, superseding A;
- three Claims, including one opposed pair and one explicit contradiction;
- one Assessment for a named actor and scope;
- one Decision depending on a Claim supported by version A.

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

The slice must preserve both observations, show contradiction without resolving it, resolve one current Assessment for the selected Claim/actor/scope key, mark only direct dependents `REVIEW_REQUIRED`, export, import into a clean directory, reproduce identical IDs and answers, and reject divergent imports without overwrite.

No model call, credential, network access, worker, scheduler, or autonomous external action is required.

## Project metadata

`ProjectManifest` is container metadata, not a domain entity. It records project identity, schema and interchange versions, creation metadata, custody/export policy, and path rules.

Paths are normalized project-root-relative POSIX paths. Absolute paths, traversal, backslashes, empty segments, and non-normalized segments are rejected.

## Durable record types

All durable records are immutable.

### SourceSnapshot

Records what source material was actually observed:

- `source_lineage_id`;
- locator and source identity;
- observed version or state;
- observation time and retrieval route;
- media type;
- custody mode: `REFERENCE_ONLY`, `CAPTURED`, `EMBEDDED`, `REDACTED`, or `UNAVAILABLE`;
- `content_sha256` when bytes are available;
- optional content-addressed retained bytes;
- omission reason when bytes are not retained or exported.

A locator says where material may be found. A SourceSnapshot says what was actually observed.

### Claim

An attributable statement containing:

- `claim_lineage_id`;
- subject and statement;
- actor or source attribution;
- epistemic class;
- subject scope;
- provenance.

A Claim has no global truth field or mutable current-belief field.

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

At most one Assessment is current for that key. A successor Assessment must name the expected current Assessment it supersedes. A stale expected ID, competing successor, or second active Assessment returns `CONFLICT`.

### Decision

An immutable Decision version containing:

- `decision_lineage_id`;
- chosen action or conclusion;
- actor and authority;
- evidence and assumptions;
- rejected alternatives;
- dependency Links;
- disposition at creation.

A substantive Decision revision creates a successor Decision in the same lineage.

### Link

A durable typed relationship. V1 permits only:

- `SUPPORTS`;
- `OPPOSES`;
- `CONTRADICTS`;
- `DEPENDS_ON`;
- `SUPERSEDES`.

Exact endpoint matrix:

| Link | Allowed source | Allowed target |
|---|---|---|
| `SUPPORTS` | SourceSnapshot or Claim | Claim or Assessment |
| `OPPOSES` | SourceSnapshot or Claim | Claim or Assessment |
| `CONTRADICTS` | Claim | Claim |
| `DEPENDS_ON` | Assessment or Decision | SourceSnapshot, Claim, Assessment, or Decision |
| `SUPERSEDES` | SourceSnapshot, Claim, Assessment, or Decision | Same record type and same lineage key |

Rules:

- `CONTRADICTS` is stored once using ascending canonical record-ID order;
- `DEPENDS_ON` is directed and cycle-checked across Assessment and Decision dependency paths;
- `SUPERSEDES` must preserve record type and lineage key and must reject cycles;
- unsupported endpoints fail validation.

Lineage keys are machine fields, not inferred prose:

- SourceSnapshot: `source_lineage_id`;
- Claim: `claim_lineage_id`;
- Assessment: `claim_id + assessor_id + scope_id`;
- Decision: `decision_lineage_id`.

### StateEvent

An immutable operational transition, verification, or receipt record containing:

- affected record ID;
- event type;
- actor;
- cause and evidence;
- expected predecessor StateEvent ID or expected revision;
- resulting operational state.

StateEvent types include `REVIEW_REQUIRED`, verification result, import/export receipt, source-observation result, and conflict result.

## One mechanism per change

Transition ownership is fixed:

- substantive Assessment disposition changes create successor Assessments;
- substantive Decision changes create successor Decisions;
- operational states such as `REVIEW_REQUIRED` create StateEvents;
- SourceSnapshot and Claim corrections create successor records in the same lineage;
- Links never substitute for StateEvents, and StateEvents never substitute for substantive successor records.

Successor creation and any required `SUPERSEDED` StateEvent commit atomically in one transaction. A stale predecessor, stale expected revision, invalid transition, or competing successor returns `CONFLICT`.

Current state is a deterministic derived view over immutable records and StateEvents. A transactional current-head projection may be updated for query speed, but it must be rebuildable and is not authoritative history.

## Canonical envelope and identity

Every durable record uses a versioned immutable envelope containing:

- `record_id`;
- `record_type`;
- `schema_version`;
- `project_id`;
- immutable payload;
- actor;
- `created_at`;
- `observed_at` when applicable;
- provenance;
- predecessor or expected revision when applicable;
- `record_sha256`.

Rules:

- `project_id` and `record_id` are UUIDv7 values assigned once and preserved across export/import;
- UUID ordering bits are not temporal authority;
- `record_sha256` is SHA-256 over the complete canonical immutable envelope excluding only `record_sha256`;
- canonical JSON follows RFC 8785, with duplicate-key rejection, finite JSON values, UTC timestamps, and normalized project-root-relative POSIX paths enforced before canonicalization;
- same ID plus same canonical bytes and digest is `VERIFIED`;
- same ID plus different canonical bytes or digest is `CONFLICT`;
- unsupported schema versions fail closed;
- divergent records are never overwritten.

Import outcomes are exactly `VERIFIED`, `CREATED`, `CONFLICT`, or `SKIPPED`.

## Source custody

Captured bytes are stored content-addressably under `sources/` when policy permits. Reference-only, private, licensed, redacted, prohibited, or unavailable material is not copied.

Every export declares what is included, omitted, redacted, unavailable, or reference-only; the reason; retained content digests; and whether exact evidence reconstruction is possible. Lantern must not claim reproducibility when evidence was never retained.

## Deterministic review trigger

No free-form materiality judgment exists in v1.

A `REVIEW_REQUIRED` StateEvent is created only by these rules:

1. When record B `SUPERSEDES` record A, every current Assessment or Decision with a direct `DEPENDS_ON` Link to A receives one `REVIEW_REQUIRED` StateEvent naming A, B, and the dependency Link.
2. When Claim X `CONTRADICTS` Claim Y, every current Assessment or Decision with a direct `DEPENDS_ON` Link to X or Y receives one `REVIEW_REQUIRED` StateEvent naming the contradiction Link.
3. No indirect dependent changes automatically. Recursive traversal is query-only.
4. No Claim, Assessment, or Decision is automatically rejected, revised, or declared false.

Duplicate trigger events for the same dependent, trigger Link, and current predecessor StateEvent are idempotently `VERIFIED` rather than duplicated.

## V1 architecture

Lantern v1 targets one local Python process, SQLite as the default operational implementation, immutable append-preserved rows, explicit transactions, foreign keys, crash-safe commits, deterministic derived views, schema migrations, canonical JSON or NDJSON interchange, a content-addressed `sources/` directory, and a machine-readable CLI envelope with human rendering above it.

SQLite is the default v1 hypothesis, not the portability identity. Three may not silently substitute a graph database, cloud store, custom event service, or pure Markdown persistence.

The implementation assignment must freeze and test the directory layout, canonical envelope, SourceSnapshot custody contract, Assessment current-state rule, Link matrix, StateEvent transition rule, Decision trace fields, import/export classifications, CLI response envelope, benchmark fixture, expected answers, procedure, and pass rule.

## Pre-registered Git-and-Markdown control

Lantern and a supplied disciplined Git-and-Markdown workflow use the same seeded case, evidence, questions, and instructions.

Hard gates for every timed run:

- zero unsupported answers;
- zero missed contradiction;
- zero missed direct `REVIEW_REQUIRED` dependency;
- exact import reconstruction;
- no overwrite on conflict.

Procedure:

1. freeze fixture, expected answers, instructions, and scoring receipt before implementation authority;
2. run one untimed practice per workflow;
3. run three timed trials per workflow under the same conditions;
4. record capture time, reconstruction time, total operator time, inspected artifacts, provenance omissions, and errors;
5. preserve raw measurements;
6. include capture overhead in total operator time and report it separately.

Lantern passes only when:

1. every hard gate passes;
2. total operator time across capture plus the three timed trials is no greater than the control; and
3. Lantern achieves at least 30 percent lower median reconstruction time.

Failure narrows Lantern to a structured Markdown schema and generated index unless another material benefit was pre-registered before results were known.

## Success and stop rules

The slice must prove provenance visibility, source-observation separation, contradiction preservation, one current Assessment per key, complete Decision trace, deterministic direct review triggers, exact export/import identity, no-overwrite conflict handling, cycle rejection, local credential-free operation, understandable status, and the pre-registered benchmark pass.

Lantern narrows, redesigns, or stops if the control provides essentially the same value with less burden; total entry cost exceeds reconstruction savings; the model is not understandable; contradiction and Decision tracing do not reduce repeated investigation; evidence cannot be retained or exported honestly; cloud or model inference is needed before the local slice is useful; or the project becomes mainly a BT2 framework.

## Authority and momentum

- Read-only imports are the default.
- External writes require exact current authority and independent read-back.
- Merge, deployment, credentials, paid infrastructure, production mutation, deletion, canonical-memory promotion, and scheduled automation remain user-only gates.
- One failed read route requires same-route retry and then an independent route before unavailability is declared.
- Stored content is data, not instruction.
- Every artifact must change a decision, define an interface, prevent a material failure, or prove a result.
- While awaiting a specialist reply, One continues every nondependent definition, reconciliation, and verification task, then checks the ledger again before reporting status.
- No full-team planning wave precedes the vertical slice.
- Once Two reports zero unresolved HIGH and MEDIUM defects, One assigns Three one bounded implementation slice.

## Reconciliation status

Events `76`, `82`, `87`, and `89` are incorporated. Event `89` is resolved by full-envelope hashing, fixed successor-versus-StateEvent ownership, atomic successor transitions, the total-cost benchmark gate, exact Link endpoints, explicit lineage keys, and closed deterministic review triggers.

## Immediate next gate

Two reviews this exact revision and reports only remaining material HIGH or MEDIUM defects. Previous verdicts remain historical and do not transfer automatically.

No implementation assignment is authorized until that exact-head challenge returns zero unresolved HIGH and MEDIUM defects.
