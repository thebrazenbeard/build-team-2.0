> **License:** Source-visible, not open source. Original material is proprietary. Commercial use, redistribution, hosted-service use, and commercial derivative products require written permission. See [LICENSE](LICENSE) and [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md). Separately identified third-party components retain their own licenses.

# Build Team 2.0

Build Team 2.0 is a ten-facet software build collective:

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

## Local setup

```bash
uv sync --extra dev
cp .env.example .env
# Fill OPENAI_API_KEY and Supabase values.
uv run build-team roster
uv run build-team run "Design a health endpoint for the service"
```

The runtime uses the OpenAI Agents SDK. Supabase is optional for local inspection commands, but required for durable shared task and memory state.

## Storage model

The `build_team_2` Supabase schema contains shared tasks, perspectives, decisions, and an append-only collective memory ledger. There are deliberately no per-facet memory tables or private session identifiers.

See `docs/architecture.md`, `docs/personas.md`, and `migrations/001_build_team_2.sql`.
