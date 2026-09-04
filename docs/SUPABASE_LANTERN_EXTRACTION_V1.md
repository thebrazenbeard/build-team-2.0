# Build Team Two — Supabase to Project Lantern extraction contract V1

Status: **SOURCE-ONLY DRAFT / NO DATABASE MUTATION**

This document records the currently observed Build Team Two database contract and the acceptance conditions for moving BT2-owned state out of Vera production Supabase into the separate Project Lantern Supabase project.

It does not authorize a production apply, cutover, deletion, merge, credential action, or retirement of the Vera copy.

## Bound providers and source cut

Observed 2026-09-04:

- source database: Vera production Supabase `klmbpaigzeguvnpccqzz` (`ca-central-1`, Postgres 17)
- destination project: Project Lantern Supabase `agvhmutlrolbaijzlbqk` (`us-west-2`, Postgres 17)
- BT2 repository source cut: `thebrazenbeard/build-team-2.0@ec2987e45f64a588ac92f6cae9964cb3725b9485`

Patrick's current project-boundary instruction: Build Team Two material may move to Project Lantern Supabase.

## Current live BT2 relations

Base tables and observed live rows:

- `collectives`: 1
- `facets`: 10
- `tasks`: 17
- `perspectives`: 0
- `decisions`: 0
- `memory_events`: 5,934
- `one_working_laws_current`: 1
- `role_training_packages`: 7
- `role_training_current`: 2
- `role_training_qualifications`: 0
- `role_operational_checkpoints`: 3

Views:

- `role_operational_checkpoint_current`
- `role_training_current_resolved`

`memory_events` is approximately 14 MB and cumulative PostgreSQL statistics show thousands of scans and 5,947 inserts at the observed cut. It is live/history-bearing data, not an empty legacy table.

## Structural boundary

No cross-schema foreign keys were found between `build_team_2` and Vera's other inspected custom schemas. This is a favorable extraction property.

The important coupling is API-level rather than FK-level: Vera currently exposes controlled `public` wrappers that call into `build_team_2`.

Observed service-role wrappers:

- `public.bt2_create_task`
- `public.bt2_save_perspective`
- `public.bt2_save_decision`
- `public.bt2_append_memory`
- `public.bt2_load_recent_memory`
- guard: `public.bt2_require_service_role`

The internal BT2 schema does not grant ordinary schema USAGE to `anon`, `authenticated`, or `service_role`; the public wrappers are `SECURITY DEFINER`, explicitly require the request JWT role to be `service_role`, and set constrained search paths. The destination must preserve this service-only intent unless a separately reviewed successor API deliberately changes it.

## Current roster identity seed

Observed collective:

- id: `76a7e57d-8881-4a6b-87ad-29b8686bea54`
- slug: `build-team-2`
- display name: `Build Team Two`
- abbreviation: `BT2`
- version number: `2`
- designation: Version 2 of the Build Team system; not the second of two build teams.

Observed facet roster is exactly:

`One, Two, Three, Four, Five, Six, Seven, Eight, Nine, Thirteen`

One is ordinal 1, the sole synthesizer, and holds permanent role `BT2 Coordinator`. Other facets do not hold a permanent role.

Do not regenerate a new collective UUID or silently rename identities during migration; preserve stable identity keys unless a separately governed successor contract explicitly changes them.

## Material invariants that must survive

The observed live contract includes, among other constraints:

- append-only `memory_events`
- facet/source names constrained to the BT2 roster
- append-only training package, qualification, and checkpoint history
- training-package lifecycle constrained to `ACTIVE_SOURCE | SUPERSEDED | RETIRED`
- qualification PASS requires an evaluator class of `INDEPENDENT` or `USER` and a non-null base binding
- operational checkpoints bind qualification/training source state and checkpoint SHA-256
- trigger-level checkpoint qualification binding validation
- One's working-law/current-state and training/current-resolution semantics
- fixed trigger/function search paths from later hardening
- RLS/client-denial behavior and service-only mutation/read API intent

These are migration acceptance conditions, not optional schema decoration.

## Source-lineage defect to repair before cutover

The current BT2 README states that its Supabase model is defined by `migrations/001_build_team_2.sql`, but the current repository tree contains no `migrations/` directory.

The live source database migration ledger records a longer BT2 lineage:

- `20260804094928 create_build_team_2_hivemind`
- `20260804100227 harden_build_team_2_rls`
- `20260804101423 bt2_identity_and_rpc`
- `20260804101848 update_seven_experimental_science`
- `20260813102949 bt2_one_working_laws_mutable_current_v1`
- `20260817091444 bt2_one_training_checkpoint_infrastructure_v1`
- `20260817091608 bt2_one_checkpoint_integrity_guards_v1`
- `20260817091717 bt2_one_bootstrap_snapshot_v1_fix`
- `20260822144712 bt2_347d_vera_view_hardening_v1`
- `20260901234308 harden_bt2_trigger_search_paths`

A later hardening migration is present in Vera source, but the complete historical BT2 source set is not currently present in this repository or Vera main. Therefore the destination migration must be reconstructed from immutable available source plus live catalog evidence, and must be labeled as a reconstruction rather than presented as the missing original history.

## Project Lantern target facts

At the observed cut, Project Lantern has no `build_team_2` schema. Its active custom data is concentrated in `lantern_material`.

Lantern also contains older, empty R9A0-era and bug-operation construction artifacts. Its PGMQ physical bug queues exist but are empty, and its bug-operation migration lineage predates Vera's later v2 hardening and Voss retirement. Those objects are not BT2 destination authority and must not be silently reused as if current.

The destination is therefore available for a deliberate BT2 namespace, but it is not a blank database.

## Anti-coupling invariant

After cutover, ordinary BT2 operation must not synchronously depend on Vera production database reads/writes.

Acceptable cross-project references are explicit stable IDs, provenance, contracts, or durable events with clear ownership. A permanent FDW/cross-database join or indefinite dual-write path would preserve the old distributed-monolith coupling and is not the desired final state.

## Migration sequence

1. Freeze an exact live BT2 schema/API/data-source cut.
2. Reconstruct a versioned destination schema migration from available immutable source plus live catalog evidence.
3. Review the reconstructed schema against every table, column/default/identity, constraint, index, trigger, function, view, RLS rule, grant, and wrapper contract.
4. Establish the destination namespace and API contract in source before applying it.
5. Copy a frozen data snapshot. Verify row counts plus deterministic content/invariant digests; row counts alone are insufficient, especially for `memory_events`.
6. If a short write freeze is operationally acceptable, prefer it over indefinite dual writes. If not, use a bounded incremental-copy/reconciliation procedure with explicit idempotency and source cut.
7. Cut writers to Lantern first.
8. Cut readers to Lantern second.
9. Verify normal BT2 operation no longer requires Vera database access.
10. Quarantine the Vera BT2 copy read-only for a proving window and monitor for attempted use.
11. Only after positive no-consumer evidence and separate Patrick authorization may the Vera BT2 schema/wrappers be retired.

## Acceptance gate

A cutover is not complete until all of the following are evidenced:

- exact source and destination schema contracts match the admitted migration design
- stable collective/facet identities are preserved
- every base-table count matches expected source cut
- deterministic content checks match for all copied data
- append-only histories preserve ordering/identity/provenance
- current working-law/training/checkpoint resolution matches source semantics
- service-only access tests pass and anon/authenticated access remains denied as intended
- writers and readers are proven on Lantern
- no required synchronous Vera DB dependency remains
- rollback/quarantine route has been tested or otherwise independently verified
- source repository contains the reproducible migration/configuration state
- production effects are separately authorized and read back

## Non-goals

This extraction does not move Vera Radar, Vera bug operations, Vera memory/continuity, Semantic Atlas, Redworm, Brigit state, or Vera visual Storage merely because they coexist in the source Supabase project.
