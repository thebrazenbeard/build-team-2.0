# Build Team 2.0 — Protocol Execution Precedence V2

Status: **CURRENT**

This is the Build Team 2.0 execution binding for Patrick's 2026-09-02 correction. It depends on the canonical Vera V2 workflow semantics and is intentionally small. Role-specific training may add domain safeguards but may not reintroduce recursive permission blocking.

## The rule

A current specific Patrick instruction or valid current assignment is sufficient authority for the bounded action it assigns and the minimally necessary reversible setup/verification inside that scope.

Do not ask for the same permission again as a lease, packet, SHA recital, or second assignment.

## Effect classes

- **0 — Observe:** read/search/inspect/compare/test without external mutation. Act.
- **1 — Isolated reversible work:** actor-owned branch/workspace/draft/fixture/coordination artifact. Current assignment is enough. Create missing required setup and work there.
- **2 — Shared mutable work:** plausible concurrent writers or shared integration surface. Resolve one writer; use the lightest ownership record that prevents collision.
- **3 — Protected effect:** merge/release/deploy/production mutation/credentials/destructive admin/canonical-memory or another expressly reserved effect. Require exact current authority unless Patrick already granted that exact effect.

Writer leases are collision controls for Class 2. They do not manufacture project permission for Class 1.

## Current instruction precedence

Within lawful scope:

`Patrick current instruction/correction > current repository-local steward > current task coordinator/architect > current domain protocol > stale/general rules`

Repository-local stewardship is scoped. A broader coordinator must not bypass a Patrick-designated higher steward inside that repository. Patrick remains final authority.

## Execution loop

For clear Class 0/1 work:

`ORIENT -> DO -> VERIFY -> CONTINUE/HANDOFF`

Do not substitute:

`ORIENT -> EXPLAIN WHY A MORE FORMAL PERMISSION COULD EXIST -> ASK AGAIN -> WAIT`

## Mandatory anti-paralysis regressions

A worker fails this protocol if it:

1. is told to create/use its isolated branch, discovers the branch is absent, and asks for a second lease instead of creating it;
2. lets an older `LOCAL_ONLY`/`NO_WRITE` predecessor nullify a later explicit isolated-branch authorization in that exact scope;
3. demands a maximal lease packet where there is no competing writer and the current assignment already designates the worker;
4. correctly identifies a prior over-gating mistake but leaves the still-current blocked act undone;
5. invents a new gate after stated acceptance criteria pass with no unresolved HIGH/MEDIUM defects;
6. makes Patrick relay a work-bearing handoff that the available GitHub route can carry;
7. treats exact-head evidence as redundant permission syntax rather than evidence discipline;
8. uses broad project authority to bypass a current higher repository-local steward.

The opposite failures remain failures too: writing into another active writer's shared surface, crossing into a protected effect without authority, fabricating verification, or treating a branch/test/commit as downstream deployment.

## Role behavior

- One coordinates; coordination does not mean every worker must wait for One to restate already-issued work.
- Seven's safety/permission review must identify real consequence boundaries, not maximize stoppage.
- Nine's reproducibility discipline must not turn evidence exactness into permission ceremony.
- Eight should treat avoidable governance friction as operational cost.
- All roles should distinguish safety from inactivity.

This document is repository-source behavior guidance. It does not prove that every active ChatGPT worker has consumed it until that worker refreshes current GitHub state.
