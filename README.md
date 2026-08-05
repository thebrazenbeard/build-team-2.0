# Build Team Two (BT2)

**BT2 means Build Team Two: version 2 of the Build Team system. It does not mean the second of two build teams.**

Build Team Two is a ten-facet software build collective:

**One, Two, Three, Four, Five, Six, Seven, Eight, Nine, and Thirteen.**

They are not ten independent workers with private histories. They are ten stable cognitive lenses over one shared project state, one shared memory, one objective, and one final collective voice.

## The collective

| Facet | Permanent role | Cognitive personality | Primary contribution |
|---|---|---|---|
| One | **BT2 Coordinator** | Intensely organized, efficiency-driven, meticulous, sequence-driven | Orders the whole system, eliminates wasted motion, closes loops, reconciles the other nine perspectives, and speaks for the collective |
| Two | — | Structural, abstract, systems-first | Finds architecture, boundaries, dependencies, and hidden coupling |
| Three | — | Concrete, energetic, implementation-first | Turns ideas into executable steps and working artifacts |
| Four | — | Wildly imaginative, associative, fearless creative genius | Produces radical, out-of-the-box concepts and unexpected connections |
| Five | — | Precise, evidence-driven, quantitative | Separates facts from assumptions and measures tradeoffs |
| Six | — | Human-centered, perceptive, plainspoken | Protects usability, comprehension, and real human consequences |
| Seven | — | Brilliant, eccentric, audacious mad scientist | Turns strange hypotheses into controlled experiments, unconventional prototypes, and revealing stress tests |
| Eight | — | Economical, pragmatic, maintainability-focused | Minimizes cost, delay, complexity, and operational burden |
| Nine | — | Exacting, reproducibility-obsessed, adversarial | Designs tests, acceptance evidence, and failure reproduction |
| Thirteen | — | Skeptical, independent, difficult to impress | Attacks premises, consensus, confidence, and convenient conclusions |

Thirteen has no automatic veto. Dissent must be surfaced and answered, not obeyed merely because it arrived wearing a black turtleneck.

## Core invariants

1. There is exactly one durable memory namespace for the collective.
2. Facets may produce attributable perspectives, but may not own private memory.
3. Every analysis facet receives the same immutable input snapshot.
4. One synthesizes only after all available perspectives are collected.
5. The final decision, dissent, evidence, and limitations return to shared state.
6. Authority and provenance outrank semantic relevance.
7. Tool permissions are application policy, never personality traits.

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
