---
id: "REQ-AUTH-001"
title: "Reduced Re-Authentication Frequency for Receptionist Workstation"
category: "Non-Functional"
status: "Pending_Review"
confidence: 0.8
source: "evidence/interviews/receptionist.md"
lines: "47-48"
evidence_quote: "And please don't make me log in every single time."
assumptions:
  - "The clinic security policy defines the maximum allowable session duration and idle timeout thresholds."
  - "The workstation is in a physically secured reception area."
  - "The 60-minute session window is a design assumption balancing usability against security; the exact value must be agreed with the clinic security officer."
---

## Requirement Statement

WHILE a receptionist workstation has an active authenticated session, the system shall maintain that authenticated state without requiring re-entry of credentials for a maximum of 60 continuous minutes, unless an idle timeout event occurs.

## Rationale

The receptionist reported navigating the scheduling screen approximately forty times per hour (L48) and explicitly objected to logging in every time (L47). This requirement reduces authentication friction while deferring the specific mechanism and idle timeout policy to the clinic security architecture to balance usability against patient data protection obligations.

## Acceptance Criteria

1. The system shall not prompt the receptionist for credentials more than once during any 60-minute window of continuous workstation activity.
2. IF the workstation has been idle for a duration exceeding the clinic's defined idle timeout threshold, THEN the system shall require re-authentication before granting access.
3. Each authentication event shall be recorded in the security audit log with a timestamp and workstation identifier.
