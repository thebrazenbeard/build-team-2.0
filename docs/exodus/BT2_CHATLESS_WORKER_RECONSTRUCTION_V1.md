# Build Team Two Chatless Worker Reconstruction V1

Status: **EXODUS CANDIDATE / STARTING_SNAPSHOT — FRESHNESS REQUIRED BEFORE EFFECT**

This document externalizes the Build Team Two worker model so permanent worker chats are not infrastructure.

## Persistent interface topology

The intended persistent ChatGPT interface for Build Team Two is exactly `BT2 Coordinator`.

`BT2 Coordinator` is the human-facing interface for the durable coordinator role represented by **One**. It is not One's canonical state store and does not require permanent chats for the remaining workers.

Every other BT2 identity may execute inside a temporary ChatGPT context, Work task, API/model runtime, CLI session, subagent, or other terminal. A terminal is not the worker's durable identity, memory, authority, assignment, or qualification.

## Durable reconstruction sources

Fresh runtimes reconstruct BT2 work in this order:

1. current repository `thebrazenbeard/build-team-2.0`;
2. current `training/ROLE_TRAINING_REGISTRY.json` and exact immutable package bindings where a package exists;
3. current provider `build_team_2.one_working_laws_current` and role-training/checkpoint relations when authorized read access is available;
4. current Chat Communication Bus topology and direct durable assignment/handoff evidence;
5. current owning-project source/PR/issue/checkpoint;
6. fresh exact authority before any protected effect.

Historical checkpoint rows, Bus branches, role packages, or chat-origin provenance never prove current assignment or authority by themselves.

## Current active roster and role map evidence

A fresh read of `build_team_2.one_working_laws_current` during the Exodus audit reported revision 10, source event 6064, and this active roster:

- One
- Two
- Three
- Four
- Five
- Six
- Seven
- Eight
- Nine
- Thirteen
- Masa
- Mune
- Hephaestus

The same current row reported this permanent-role allocation:

- One — Sole Governance Authority; Coordinator; Consolidator; Project Architect / Integration Controller; Task Queue Steward; Slack / Coordination Warden.
- Two — Systems Architect; Database Owner; Migration Owner; Repository Change Engineering / Implementation Producer.
- Three — State Machine / Data Model & Schema Steward; Supabase Service Warden; WoWSQL Service Warden.
- Four — Documentation / Specification Owner; Exact Implementation Reconstruction / Packaging.
- Five — Release / Effect Custodian; Source / Registry Owner; GitHub Service Warden; Provider Currentness / Provenance Steward.
- Six — Observability / Operator Experience; DS216 / Target Runtime Warden; Runbook / Target-Evidence Steward.
- Seven — Security Reviewer; Security Test Warden; Hostile Validation / Threat Modeling Lead.
- Eight — Google Drive Service Warden; Minimality / Resource Economy; Storage / Backup / Pathset Economy.
- Nine — Auditor; Test / Validation Owner; Independent Acceptance / Release-Closure Oracle.
- Thirteen — Corrections Lead; Governance / Authority Review; No-False-Authority Challenger.
- Masa — Debugger Lead; Root Cause / Incident / Reliability Engineering.
- Mune — Debugger Verification / Regression Specialist.
- Hephaestus — Debugger Implementation / Repair Specialist; Bounded Correction Implementer.

This is an observed provider snapshot, not a GitHub canonical promotion. Fresh-read current governance before relying on it.

## Immutable role-training coverage

The current GitHub registry contains immutable package bindings for One, Four, Five, Six, Nine, and Thirteen. Those packages define role competence and authority boundaries but do not grant a current assignment or protected-effect authority.

Two, Three, Seven, Eight, Masa, Mune, and Hephaestus do not currently have entries in `training/ROLE_TRAINING_REGISTRY.json`. Their role semantics are therefore recoverable from current governance/role-map evidence, but they do not have the same immutable packaged-training path. That is a **WORKER_RECONSTRUCTION_QUALIFICATION_GAP**, not permission to recover instructions from an archived chat.

## Current Exodus supersession

Patrick's current Exodus instruction supersedes the following pre-Exodus operating assumptions **within this scope**:

- a worker does not need its own permanent ChatGPT conversation to become operational;
- activation is not defined as "a user turn in that identity's permanent conversation";
- Slack is not a required current delivery path or system of record;
- worker-to-worker coordination belongs in durable GitHub/Bus state;
- a temporary runtime may instantiate a worker from durable role + assignment + authority evidence;
- the three persistent ChatGPT interfaces are `Vera`, `Vera Control Plane Coordinator`, and `BT2 Coordinator` only.

This supersession does **not** mutate the provider row. The provider conflict remains explicit until separately reconciled under authority.

## Dispatch requirements

Before BT2 Coordinator dispatches a temporary worker runtime, durable current evidence must establish:

- worker/role;
- project/domain;
- exact assignment/subject;
- repository and current Bus route or supported invocation path;
- relevant training/role contract or explicit bounded role definition;
- dependency and collision state;
- authority ceiling and prohibited effects;
- required independent-review separation;
- durable result destination;
- post-work verification/currentness rules.

If those cannot be established without a retired chat, classify `WORKER_RECONSTRUCTION_GAP` and stop at that frontier.

## Authority

Role ownership, service-warden status, technical access, tool availability, assignment, qualification, successful tests, or a Bus route do not automatically grant a protected external mutation.

The current Owner/Warden lease model and Patrick's exact current instruction remain controlling for protected effects. This Exodus source change grants no merge, provider mutation, deployment, credentials, permission change, training, public release, destructive rewrite, Slack activation, or canonical-memory effect.

## Slack boundary

Slack may later be implemented as a Vera interface/transport only under separate authority. Slack is not worker state, does not replace the Bus, and Slack history must not be required for reconstruction.

## Retirement test

This repository is Exodus-ready only when BT2 Coordinator can instantiate the required worker from GitHub/Bus/current authorized provider evidence, execute a bounded assignment, and persist the result without opening that worker's former permanent chat.
