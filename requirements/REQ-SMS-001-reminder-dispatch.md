---
id: "REQ-SMS-001"
title: "Automated SMS Appointment Reminder Dispatch"
category: "Functional"
status: "Pending_Review"
confidence: 0.95
source: "evidence/interviews/receptionist.md"
lines: "42-42"
evidence_quote: "Half our no-shows are people who just forgot."
assumptions:
  - "The clinic has access to an outbound SMS gateway service."
  - "Patient records include a verified mobile phone number."
  - "The SMS dispatch deadline of 18:00 local time is derived from the stakeholder's statement 'by the evening' (L46) and is subject to clinic confirmation."
---

## Requirement Statement

WHEN a patient has a confirmed appointment scheduled for the following calendar day, the system shall send one SMS reminder to the patient's registered mobile phone number no later than 18:00 local time on the day before the appointment.

## Rationale

The receptionist reported that approximately half of all no-shows are patients who forgot their appointment (L42). The timing of 18:00 is derived from her statement that knowing by that time allows her to fill the slot (L46).

## Acceptance Criteria

1. The system shall send exactly one SMS reminder per confirmed appointment.
2. The SMS shall be dispatched no later than 18:00 local time on the calendar day preceding the appointment.
3. The SMS shall contain the appointment date, time, and clinic location.
4. The system shall log the delivery status (sent, delivered, failed) for each dispatched SMS.
