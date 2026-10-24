---
id: "REQ-SMS-002"
title: "Patient Cancellation via SMS Reply to Free Slot"
category: "Functional"
status: "Pending_Review"
confidence: 0.9
source: "evidence/interviews/receptionist.md"
lines: "43-44"
evidence_quote: "We should text them or something. Early enough that they can cancel and I can give the slot away."
assumptions:
  - "The SMS gateway supports two-way messaging and inbound reply processing."
  - "A single keyword reply is a valid cancellation mechanism."
  - "The 30-second processing target is a technical design assumption not stated in the evidence."
---

## Requirement Statement

WHEN a patient replies to the appointment reminder SMS with the keyword "CANCEL", the system shall mark the corresponding appointment as cancelled and release the time slot for rebooking within 30 seconds of receiving the reply.

## Rationale

The receptionist requested a mechanism to let patients cancel via text so she can reassign the vacant slots and recover wasted capacity (L43–L44). Enabling direct text replies removes friction and automates this process.

## Acceptance Criteria

1. The system shall accept the reply keyword "CANCEL" (case-insensitive) as a valid cancellation command.
2. The system shall update the appointment status to "Cancelled" within 30 seconds of receiving a valid reply.
3. The system shall return the freed slot to the pool of bookable time slots within 30 seconds.
4. The system shall send a confirmation SMS to the patient acknowledging the cancellation.
