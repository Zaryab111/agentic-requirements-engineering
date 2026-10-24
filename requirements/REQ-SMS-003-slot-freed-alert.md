---
id: "REQ-SMS-003"
title: "Receptionist Notification When Appointment Slot Is Freed"
category: "Functional"
status: "Pending_Review"
confidence: 0.85
source: "evidence/interviews/receptionist.md"
lines: "46-46"
evidence_quote: "Day before. If I know by the evening I can fill it."
assumptions:
  - "The receptionist workstation runs the clinic scheduling interface."
  - "The notification is delivered within the scheduling application, not via a separate channel."
  - "The 60-second notification target is a technical design assumption not stated in the evidence."
---

## Requirement Statement

WHEN a patient cancels an appointment via SMS reply, the system shall display a notification on the receptionist's scheduling interface within 60 seconds, showing the freed date, time, and slot duration.

## Rationale

The receptionist stated that if she knows about a cancellation in time, she can fill it (L46). She also described wanting to give the slot away (L44). This requires the system to proactively notify her when a slot opens up, rather than requiring her to discover it manually.

## Acceptance Criteria

1. The notification shall appear on the receptionist's active scheduling screen within 60 seconds of a successful SMS cancellation.
2. The notification shall display the freed appointment date, time, and duration.
3. The notification shall persist on screen until the receptionist acknowledges it.
