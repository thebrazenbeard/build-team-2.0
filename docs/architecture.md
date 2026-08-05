# Hivemind Architecture

## Purpose

Build Team Two (BT2), version 2 of the Build Team system, implements ten distinct cognitive personalities as one collective system. Personality changes interpretation and emphasis. It does not create isolated identity, private goals, private memory, or independent authority.

## Shared snapshot

Every task is normalized into one immutable `HivemindSnapshot` containing:

- objective;
- constraints;
- relevant shared memory;
- repository and tool evidence;
- current collective state;
- provenance and authority notes.

The snapshot is serialized once and hashed. Two through Nine and Thirteen receive the exact same serialized snapshot. Their instructions differ; their evidence does not.

## Analysis phase

Nine analysis facets run concurrently and return structured `Perspective` packets. A packet contains observations, assumptions, risks, proposals, questions, confidence, and explicit disagreements. These packets are operational contributions to shared state, not personal memories.

## Coordination and synthesis

One permanently serves as **BT2 Coordinator**. One receives:

1. the original shared snapshot;
2. all completed perspective packets;
3. any failed-facet notices;
4. the requirement to preserve material dissent.

One returns a structured `CollectiveDecision`. The decision must state the chosen approach, rejected alternatives, unresolved dissent, evidence, action sequence, approval gates, and limitations.

## Shared memory

Durable memory is append-only and collective. Entries can record source facets for provenance, but no facet can retrieve or write a private namespace. Retrieval filters by collective, task relevance, authority, provenance, lifecycle, and time.

## Failure behavior

- One unavailable analysis facet does not silently disappear; its failure is listed.
- Thirteen's dissent is always included when material.
- One may decide against the majority but must explain why.
- No model output authorizes destructive tools or production changes.
- Ambiguous writes are verified before retry.

## Why manager-style orchestration

The system uses an application-managed fan-out/fan-in loop rather than peer handoffs. Peer handoffs would allow one facet to inherit and reshape conversation history. This design instead guarantees identical evidence input, explicit perspective boundaries, and one final collective voice.
