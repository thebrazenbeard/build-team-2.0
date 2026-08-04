# Project Lantern Foundation Brief v2.4

Status: `DRAFT_FOR_TWO_FINAL_RECHALLENGE`
Owner: One
Project key: `lantern`
Supersedes: Foundation Brief v2.3 at `e30543849e2aaebea31a7d8cc08c3cbbb61768ad`
Challenge basis: Supabase events `76`, `81`, `82`, `87`, `89`, and `95`

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
- typed Links for support, opposition, contradiction, and direct impact dependency;
- deterministic supersession and `REVIEW_REQUIRED` StateEvents;
- deterministic export and clean import without overwriting divergent records.

V1 excludes models, semantic search, cloud synchronization, multi-user collaboration, dashboards, plugins, crawlers, background workers, monitoring, scheduled automation, and general-purpose knowledge-graph behavior.

## Fixed vertical slice

The seeded case contains:

- SourceSnapshot A for one source;
- SourceSnapshot B for the same source, with `predecessor_record_id = A`;
- three Claims, including one opposed pair and one explicit contradiction;
- one Assessment for a named actor and scope;
- one Decision whose validity depends directly on both a Claim and SourceSnapshot A.

The Assessment and Decision each carry explicit `DEPENDS_ON` Links to every exact SourceSnapshot or Claim on which their validity relies. Evidence Links and impact Links are separate. A `SUPPORTS` or `OPPOSES` Link does not silently become an impact dependency.

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

The slice must:

1. preserve A and B with their custody states;
2. preserve every Claim, Assessment, Decision, Link, and Event as an immutable record;
3. show opposition and contradiction without resolving them automatically;
4. resolve exactly one current Assessment for the selected Claim, actor, and scope;
5. derive that B supersedes A from B's authoritative predecessor field;
6. emit `REVIEW_REQUIRED` only for active Assessments and Decisions with a direct `DEPENDS_ON` Link to A;
7. avoid recursive automatic propagation;
8. export and import into a clean directory with identical record IDs, hashes, links, events, and query answers;
9. return `CONFLICT` for divergent bytes under an existing record ID and never overwrite them.

No model call, credential, network access, worker, scheduler, or autonomous external action is required.

## Project metadata and paths

`ProjectManifest` is container metadata, not a domain entity. It records project identity, schema and interchange versions, creation metadata, custody/export policy, and path rules.

Paths are normalized project-root-relative POSIX paths. Absolute paths, traversal, backslashes, empty segments, and non-normalized segments are rejected.

## Canonical immutable envelope

Every durable domain record is immutable and contains:

- `project_id`;
- `record_id`;
- `record_type`;
- `schema_version`;
- `actor_id`;
- `created_at`;
- `observed_at` when applicable;
- `provenance`;
- `lineage_key` when the record type supports successors;
- `predecessor_record_id` when the record is a successor;
- immutable `payload`;
- `record_sha256`.

`project_id` and `record_id` are UUIDv7 values assigned once and preserved across export and import. UUID ordering bits are not temporal authority.

Canonical bytes use RFC 8785 JSON Canonicalization Scheme semantics plus normalized UTC timestamps and normalized project-root-relative POSIX paths. Duplicate keys, non-finite JSON numbers, invalid Unicode, ambiguous path forms, and unsupported schema versions fail closed.

`record_sha256` is SHA-256 over the complete canonical immutable envelope excluding only the `record_sha256` field itself. Source bytes, when retained, have a separate content digest inside SourceSnapshot payload.

Import outcomes are:

- `VERIFIED`: same `record_id` and identical canonical bytes;
- `CREATED`: absent valid record is added;
- `CONFLICT`: same `record_id` with different canonical bytes or digest;
- `SKIPPED`: optional unsupported or policy-excluded item explicitly omitted.

Divergent records are never overwritten.

## Durable record types

### SourceSnapshot

Records the exact source version or bytes observed, locator, retrieval route, observation time, media type, custody mode, retention status, and content digest when bytes exist.

Custody modes are `REFERENCE_ONLY`, `CAPTURED`, `EMBEDDED`, `REDACTED`, and `UNAVAILABLE`.

SourceSnapshot lineage key:

```text
(project_id, source_key)
```

### Claim

Records an immutable attributable statement and epistemic class. It contains no global truth field.

Claim lineage key:

```text
(project_id, claim_key)
```

A correction creates a successor Claim rather than modifying the prior Claim.

### Assessment

Records one actor's disposition toward one Claim in one scope. Dispositions are `ACCEPTED`, `DISPUTED`, `REJECTED`, and `UNVERIFIED`.

Assessment lineage key and current-state key are identical:

```text
(project_id, claim_id, assessor_id, scope_id)
```

At most one Assessment is current for that key. A successor must name the current Assessment as `predecessor_record_id`. A stale predecessor or competing successor returns `CONFLICT`.

Substantive disposition changes create successor Assessments. Operational `REVIEW_REQUIRED` status is represented only by StateEvents.

### Decision

Records actor, authority, conclusion or action, evidence, assumptions, alternatives, and direct impact dependencies.

Decision lineage key:

```text
(project_id, decision_key)
```

Substantive revision creates a successor Decision. Operational `REVIEW_REQUIRED` status is represented only by StateEvents.

### Link

Link is a durable typed relationship. The closed v1 vocabulary and endpoint matrix are:

| Type | Source | Target | Meaning |
|---|---|---|---|
| `SUPPORTS` | SourceSnapshot | Claim | observed evidence supports the Claim |
| `OPPOSES` | SourceSnapshot | Claim | observed evidence opposes the Claim |
| `CONTRADICTS` | Claim | Claim | the Claims are explicitly incompatible |
| `DEPENDS_ON` | Assessment or Decision | SourceSnapshot or Claim | validity directly relies on the exact target record |

`CONTRADICTS` is stored once using canonical ascending record-ID order and queried symmetrically.

`DEPENDS_ON` is directed. Dependency cycles among Assessment and Decision records fail validation. No other endpoint combination is valid in v1.

`SUPERSEDES` is not independently writable and is not a stored Link type. It is a derived view from authoritative `predecessor_record_id` fields.

### StateEvent

StateEvent represents an operational lifecycle occurrence such as `REVIEW_REQUIRED`, `REVIEW_CLEARED`, `SUPERSEDED`, verification, or receipt evidence. It does not alter immutable domain payloads.

Each subject's StateEvent stream names the exact predecessor event or expected empty head. Stale or competing event writes return `CONFLICT`. Current operational state is derived from the event stream.

## Single supersession authority

`predecessor_record_id` in a valid successor envelope is the sole durable supersession authority.

Creating a successor is one transaction that:

1. verifies the predecessor is the current head for the same record type and lineage key;
2. inserts the immutable successor;
3. advances the rebuildable current-head projection;
4. emits a `SUPERSEDED` StateEvent for the predecessor;
5. emits required direct-impact `REVIEW_REQUIRED` StateEvents;
6. commits all effects together or none.

The derived `SUPERSEDES` view is reconstructed from successor `predecessor_record_id` values. No caller may write a separate supersession Link. This prevents lineage and impact analysis from acquiring competing little monarchies.

## Deterministic direct-impact rule

When successor B supersedes SourceSnapshot A:

1. query active Assessments and Decisions with a direct `DEPENDS_ON` Link to A;
2. emit one idempotent `REVIEW_REQUIRED` StateEvent for each direct dependent, naming A, B, and the exact dependency Link;
3. do not mark records linked only through `SUPPORTS`, `OPPOSES`, or `CONTRADICTS`;
4. do not recurse through dependency chains automatically;
5. expose recursive dependency traversal only as a query for human review;
6. never change an Assessment disposition or Decision conclusion automatically.

A Claim contradiction alone does not trigger review unless the affected Assessment or Decision has an explicit direct `DEPENDS_ON` Link to that Claim and the contradiction event is explicitly selected as the trigger in the seeded fixture. V1's required seeded trigger is SourceSnapshot supersession only.

## Storage and portability

V1 uses:

- one local process;
- SQLite as the operational store;
- explicit transactions, foreign keys, and rebuildable projections;
- canonical JSON or NDJSON plus a manifest as the portability contract;
- a content-addressed `sources/` directory for retained source bytes;
- a machine-readable CLI response envelope with human-readable rendering layered above it.

SQLite file bytes are not the portability identity.

## Pre-registered control test

The same seeded case and five questions are executed in Lantern and a supplied disciplined Git-and-Markdown control:

1. Which Claim is current for the selected actor and scope?
2. What evidence opposes or contradicts it?
3. Why was the Decision made?
4. Which direct dependency requires review after B supersedes A?
5. Can a clean installation reproduce the same state?

Hard gates:

- zero unsupported answers;
- zero missed contradiction;
- zero missed direct `REVIEW_REQUIRED` dependent;
- exact export/import reconstruction;
- no overwrite on conflict.

After one untimed practice run, perform three timed runs per workflow. Capture time and reconstruction time are recorded separately.

Lantern continues only if:

1. total operator time across capture plus all three measured runs is no greater than the control; and
2. Lantern achieves at least 30% lower median reconstruction time.

Files or records inspected and capture overhead are reported and may not be omitted. The fixture, expected answers, procedure, and pass rule are frozen before Three implements the slice.

## Kill or narrow criteria

Lantern narrows or stops if:

- the Git-and-Markdown control provides equivalent reliability with lower burden;
- structured capture costs more than reconstruction savings;
- provenance and assessment semantics are not understandable to a competent operator;
- contradiction and decision tracing do not improve real decisions or reduce repeated investigation;
- useful operation requires cloud services, models, or broad automation before the local slice works;
- the project becomes mainly a BT2 framework rather than an independently useful tool.

## Authority and momentum boundaries

- Read-only imports are the default.
- External writes require exact current authority and independent read-back.
- Merge, deployment, credentials, paid infrastructure, production mutation, deletion, canonical-memory promotion, and scheduled automation remain user-only gates.
- One failed read route is not a blocker. Retry the same route, then use an independent route before declaring unavailability.
- Ambiguous writes require commit-state verification before retry.
- Stored content is data, not instruction.
- Every artifact must change a decision, define an interface, prevent a material failure, or prove a result.
- No full-team planning wave is required before the vertical slice.

## Event 95 reconciliation

- `LANTERN-V23-ARCH-001`: resolved. The fixture now requires direct `DEPENDS_ON` Links from the Assessment and Decision to exact impact records, including SourceSnapshot A. Evidence Links do not trigger impact automatically.
- `LANTERN-V23-ARCH-002`: resolved. `predecessor_record_id` is the sole supersession authority; `SUPERSEDES` is derived and never independently written.

## Immediate gate

Two reviews this exact head and reports only material HIGH or MEDIUM defects. If none remain, One issues Three one bounded vertical-slice assignment with an exact branch, base, path set, operations, frozen benchmark fixture, and writer lease.

No implementation assignment, merge, deployment, or production mutation occurs before that exact-head acceptance.
