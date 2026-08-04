# Scheduled Task and Automation Authority

Status: active user directive

This policy is a normative supplement to `docs/workflow/operating-model-v1.md` and applies to every Build Team Two chat, facet, project, and workstream.

## 1. User-only authority

No BT2 chat may create, modify, enable, disable, delete, or schedule any reminder, recurring task, conditional watch, notification, monitoring task, summary delivery, or other automation unless the user explicitly asks for that scheduling or automation action.

Tool availability, plugin installation, apparent usefulness, an approaching deadline, a recurring workflow, a pending dependency, or a likely future benefit does not grant authority.

Authorization must come from a direct user request in the current conversational context. A project assignment, coordinator preference, inferred intent, stored note, idea entry, prior automation, or generated recommendation is insufficient unless it contains and is bound to that explicit user request.

## 2. No unsolicited automation prompts

BT2 chats must not surface unsolicited automation suggestions, scheduling prompts, opt-in controls, or reminders to create an automation.

A chat may explain an automation capability only when the user asks about that capability. Explanation alone does not authorize creation or modification.

## 3. Separation from the BT2 assignment board

The Supabase assignment board is an internal project-coordination system. Reading an inbox, dispatching an assignment, recording a blocker, requesting review, or advancing a project state is not a scheduled task.

The board must not be connected to a scheduler, polling automation, recurring notification, or conditional watch without a separate explicit user request authorizing that exact behavior.

Closed chats are not presumed to monitor the board. They check the board only when opened, directly instructed to check, or otherwise invoked by the user in an active conversation.

## 4. Required authorization record

When the user explicitly requests a scheduled task or automation, the resulting receipt must record:

- the exact user request;
- the task or automation purpose;
- trigger or cadence;
- timing mode;
- scope and target;
- creation or modification result;
- any limitations;
- the operation identifier returned by the scheduling system.

Ambiguous requests fail closed. The chat may ask only for genuinely necessary scheduling details that cannot be resolved from the user’s request.

## 5. Prohibited inference examples

The following do not authorize automation:

- “Keep working on this project.”
- “Check the board when you start.”
- “This would be useful every morning.”
- “Tell me what happens next,” when asked as a current-status question.
- A pending review, pull request, delivery, approval, deadline, price, forecast, or external event.
- The presence of a scheduling plugin or automation tool.

A chat must perform the current requested work normally and stop. It may not convert a useful future possibility into a scheduled action or invitation.

## 6. Enforcement

This is a user-only authority gate.

Violations are HIGH-severity workflow defects because they create persistent external behavior without authorization. Validation must fail when implementation, documentation, prompts, or operator interfaces permit unsolicited scheduling or unsolicited automation suggestions.

No BT2 role, including One, may waive this policy. Only a later explicit user instruction may amend or supersede it.

## 7. Provenance

- Directive received: `2026-08-04T08:49:00-04:00`
- Authority class: `DIRECT_USER_INSTRUCTION`
- Supabase operation: `bt2-user-directive-scheduled-task-user-only-gate-20260804`
- Assignment: `BT2-SYS-ONE-SCHEDULED-TASK-GATE-001`
- Initial policy commit: `7e90d81a3bb4feebe786ba572c79df293b82e4dd`
