> **License:** Source-visible, not open source. Original material is proprietary. Commercial use, redistribution, hosted-service use, and commercial derivative products require written permission. See [LICENSE](LICENSE) and [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md). Separately identified third-party components retain their own licenses.

# Build Team 2.0 — Legacy Training and Continuity Source

> **Repository status:** non-canonical predecessor/compatibility source. The active canonical BT2 source repository is [`thebrazenbeard/bt2`](https://github.com/thebrazenbeard/bt2). This repository preserves versioned role training, checkpoint tooling, and Protocol V2 regression material. It does not establish current BT2 runtime, provider, assignment, or effect authority.

Build Team 2.0 was defined as a ten-facet software build collective:

**One, Two, Three, Four, Five, Six, Seven, Eight, Nine, and Thirteen.**

They are not ten independent workers with private histories. They are ten stable cognitive lenses over one shared project state, one shared memory, one objective, and one final collective voice.

## The collective

| Facet | Cognitive personality | Primary contribution |
|---|---|---|
| One | Integrative, measured, decisive | Reconciles the other nine perspectives and speaks for the collective |
| Two | Structural, abstract, systems-first | Finds architecture, boundaries, dependencies, and hidden coupling |
| Three | Concrete, energetic, implementation-first | Turns ideas into executable steps and working artifacts |
| Four | Curious, unconventional, possibility-seeking | Generates alternatives and challenges default approaches |
| Five | Precise, evidence-driven, quantitative | Separates facts from assumptions and measures tradeoffs |
| Six | Human-centered, perceptive, plainspoken | Protects usability, comprehension, and real human consequences |
| Seven | Cautious, principled, threat-aware | Examines safety, security, permission, privacy, and abuse paths |
| Eight | Economical, pragmatic, maintainability-focused | Minimizes cost, delay, complexity, and operational burden |
| Nine | Exacting, reproducibility-obsessed, adversarial | Designs tests, acceptance evidence, and failure reproduction |
| Thirteen | Skeptical, independent, difficult to impress | Attacks premises, consensus, confidence, and convenient conclusions |

Thirteen has no automatic veto. Dissent must be surfaced and answered, not obeyed merely because it arrived wearing a black turtleneck.

## Current execution protocol

Build Team current work uses `docs/PROTOCOL_EXECUTION_PRECEDENCE_V2.md` and the shared hostile suite `training/PROTOCOL_V2_REGRESSION_SUITE.md`.

The short version:

- current specific instructions beat stale/general restrictions within scope;
- necessary reversible setup is included in an assigned task;
- writer leases prevent real shared-writer collisions, not permission for ordinary isolated work;
- Class 0/1 work defaults to `ORIENT -> DO -> VERIFY -> CONTINUE/HANDOFF`;
- consequential Class 3 effects remain gated unless Patrick has already expressly authorized them;
- a current Patrick-designated repository-local steward can outrank broader project roles for mutations inside that repository;
- a correction is not complete until the next relevant behavior changes;
- passing acceptance criteria with no unresolved HIGH/MEDIUM defects is enough unless stricter criteria were actually requested.

A Build Team role fails if its caution, reproducibility discipline, or architecture ceremony causes it to repeatedly ask for authority that already exists.

## Core invariants

1. There is exactly one durable memory namespace for the collective.
2. Facets may produce attributable perspectives, but may not own private memory.
3. Every analysis facet receives the same immutable input snapshot.
4. One synthesizes only after all available perspectives are collected.
5. The final decision, dissent, evidence, and limitations return to shared state.
6. Authority and provenance outrank semantic relevance.
7. Tool permissions are application policy, never personality traits.
8. Governance is proportional to consequence; safety is not synonymous with inactivity.

## Runtime flow

```text
shared task + shared memory + shared evidence
                    |
        +-----------+-----------+
        |  Two through Nine and |
        |       Thirteen        |
        +-----------+-----------+
                    |
          perspective packets
                    |
                   One
                    |
       collective decision + dissent
                    |
            shared memory ledger
```

## What this repository contains

- `docs/PROTOCOL_EXECUTION_PRECEDENCE_V2.md` — the predecessor Protocol V2 execution overlay.
- `training/ROLE_TRAINING_REGISTRY.json` — versioned role-package/checkpoint bindings for the registered legacy roles.
- `training/roles/` — immutable role-training source packages.
- `continuity/` — checkpoint schemas and deterministic checkpoint helpers.
- `training/PROTOCOL_V2_REGRESSION_SUITE.md` — shared anti-paralysis and effect-boundary regression cases.
- `tests/` and the role/checkpoint test files — executable source-integrity checks.

The repository does **not** currently contain the Agents-SDK application, a `pyproject.toml`, the old `docs/architecture.md` / `docs/personas.md` runtime docs, or `migrations/001_build_team_2.sql`. Historical setup instructions that referenced those absent files were stale and have been removed from the current README.

## Validation

The repair pass adds a source validator and hosted qualification workflow for the artifacts that actually exist:

```bash
python scripts/validate_repository.py
python -m unittest discover -s tests -v
python continuity/five/test_checkpoint_tool.py
python continuity/six/test_checkpoint_tool.py
(cd continuity/thirteen && python test_checkpoint_tool.py)
python -m pytest -q continuity/four/test_checkpoint_tool.py continuity/four/v1.0.1/test_checkpoint_tool.py
python training/roles/four/1.0.1/validate_package.py
```

The training registry still contains historical Supabase qualification/checkpoint-store bindings. Those values are package provenance, not proof that the provider is current, reachable, or authoritative today. Fresh runtime/provider/authority state must come from the current canonical BT2 system.

See `STATUS.md` for the repair/currentness boundary.
