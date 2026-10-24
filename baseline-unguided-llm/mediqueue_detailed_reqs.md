# MediQueue — Detailed Requirements Specification

> **Project**: MediQueue Clinic Booking System
> **Source**: Stakeholder interview — R. Malik, Senior Receptionist
> **Date**: 2026-09-03
> **Scope**: This document specifies four requirements derived **strictly** from the interview transcript (L38–L48).

---

## REQ-SMS-001: Automated SMS Appointment Reminder Dispatch

### Requirement Statement

The system shall automatically send an SMS reminder to each patient **24 hours before** their scheduled appointment time. The reminder shall include the patient's name, appointment date, appointment time, and the name of the assigned practitioner. Reminders shall be dispatched without any manual action by the receptionist.

### Rationale

> **L42–L43**: *"Half our no-shows are people who just forgot. We should text them or something."*
> **L43–L44**: *"Early enough that they can cancel and I can give the slot away."*
> **L45–L46**: *"Day before. If I know by the evening I can fill it."*

R. Malik identifies forgetfulness as the root cause of approximately 50% of no-shows. She explicitly requests SMS ("text them") as the reminder channel and specifies "day before" as the required lead time, because knowing about a cancellation by the evening gives her enough time to reassign the slot.

### Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| AC-1 | Given a patient has an appointment at time **T**, the system sends an SMS reminder at **T − 24 hours** (± 15 minutes tolerance). | Schedule an appointment for 10:00 AM tomorrow. Verify SMS is delivered between 9:45 AM and 10:15 AM today. |
| AC-2 | The SMS body contains: (a) patient's first name, (b) appointment date, (c) appointment time, and (d) practitioner name. | Inspect the delivered SMS content against the appointment record. All four fields must be present and accurate. |
| AC-3 | Reminders are sent automatically — no receptionist interaction is required to trigger dispatch. | Create an appointment and take no further action. Verify the reminder is sent at the scheduled time without manual intervention. |
| AC-4 | If the appointment is cancelled **before** the reminder is due, the reminder is **not** sent. | Create an appointment, cancel it, then wait past the reminder time. Verify no SMS is delivered. |
| AC-5 | If SMS delivery fails (invalid number, carrier error), the failure is logged with the appointment ID, patient phone number, error reason, and timestamp. | Use an invalid phone number. Verify a failure entry appears in the system log within 5 minutes of the failed attempt. |
| AC-6 | The SMS must not contain sensitive medical information (e.g., reason for visit, diagnosis, or treatment details) to protect patient privacy. | Review the SMS template. Verify it contains only the four fields listed in AC-2 and a cancellation instruction — nothing else. |

---

## REQ-SMS-002: Patient Cancellation via SMS Reply to Free Slot

### Requirement Statement

The system shall allow a patient to cancel their appointment by replying to the reminder SMS with the keyword **CANCEL**. Upon receiving a valid cancellation reply, the system shall: (a) update the appointment status to "Cancelled by Patient", (b) immediately release the time slot back into the available schedule, and (c) send a confirmation SMS to the patient acknowledging the cancellation.

### Rationale

> **L43–L44**: *"Early enough that they can cancel and I can give the slot away."*
> **L42**: *"Half our no-shows are people who just forgot."*

R. Malik's core need is a **low-friction cancellation path** for patients who know they won't attend. The slot must be freed immediately so she can reassign it — she explicitly says "give the slot away." SMS reply is the lowest-friction channel since the patient already has the reminder on their phone.

### Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| AC-1 | Given a patient replies **CANCEL** (case-insensitive: `cancel`, `Cancel`, `CANCEL`) to the reminder SMS, the appointment status changes to **"Cancelled by Patient"** within 60 seconds of receipt. | Send a reminder, reply with "cancel" (lowercase). Query the appointment record and verify the status field reads "Cancelled by Patient" within 60 seconds. |
| AC-2 | Upon cancellation, the time slot is immediately released and appears as **available** on the receptionist's scheduling screen. | After the cancellation in AC-1, open the scheduling view. Verify the slot shows as available (not booked or blocked). |
| AC-3 | The system sends a **confirmation SMS** to the patient containing: the appointment date, time, and a statement that the appointment has been cancelled. | After the cancellation in AC-1, verify the patient receives an SMS confirming the cancellation with the correct date and time. |
| AC-4 | Given a patient replies with **unrecognized text** (anything other than "CANCEL"), the system replies with a fallback message instructing the patient to reply CANCEL or call the clinic, and the appointment status remains **unchanged**. | Reply to the reminder with "Maybe". Verify (a) a fallback SMS is received and (b) the appointment status is still "Booked". |
| AC-5 | A cancellation reply received for an **already-cancelled or past** appointment does not alter any records. The system replies with a message informing the patient that no active appointment was found. | Cancel an appointment, then reply CANCEL again. Verify no duplicate cancellation is recorded and an informational SMS is sent. |
| AC-6 | Each cancellation is logged with: appointment ID, patient ID, timestamp of reply, and the source ("SMS Reply"). | After a successful cancellation, query the audit log. Verify all four fields are recorded. |

---

## REQ-SMS-004: Receptionist Notification When Appointment Slot Is Freed

### Requirement Statement

When an appointment is cancelled via SMS reply (REQ-SMS-002), the system shall immediately display a **real-time notification** on the receptionist's workstation screen. The notification shall include the freed slot's date, time, practitioner name, and the name of the patient who cancelled. The notification shall persist until the receptionist acknowledges it.

### Rationale

> **L46**: *"If I know by the evening I can fill it."*
> **L44**: *"I can give the slot away."*
> **L38–L41**: *"The phone doesn't stop. And half the slots I'm booking in, the slot's already wasted because someone else just didn't turn up."*

R. Malik's ability to backfill a cancelled slot depends entirely on **knowing it is free**. She states that if she knows by the evening, she can fill it. Since cancellations happen asynchronously via SMS, the receptionist must be alerted in real time — she cannot be expected to poll the schedule continuously while handling a high volume of incoming calls during peak hours (8–9 AM).

### Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| AC-1 | When an appointment is cancelled via SMS reply, a notification appears on the receptionist's screen within **10 seconds** of the cancellation being processed. | Trigger a cancellation via SMS. Observe the receptionist's screen. A notification must appear within 10 seconds. |
| AC-2 | The notification displays: (a) freed slot date, (b) freed slot time, (c) practitioner name, and (d) the cancelling patient's name. | Inspect the notification content against the cancelled appointment record. All four fields must be present and accurate. |
| AC-3 | The notification **persists visually** (badge, banner, or panel entry) until the receptionist explicitly dismisses or acknowledges it. | After a notification appears, navigate away from the screen and return. Verify the notification is still visible until manually dismissed. |
| AC-4 | If **multiple cancellations** occur, each generates its own notification. Notifications do not overwrite each other. | Trigger two cancellations in quick succession. Verify both notifications are visible simultaneously. |
| AC-5 | The notification must be visible **without requiring the receptionist to navigate away** from the scheduling screen. | While the receptionist is on the scheduling screen during a booking, trigger a cancellation. Verify the notification appears on the current screen (e.g., as an overlay, toast, or sidebar badge) — not on a separate page. |
| AC-6 | The notification is delivered in real time via a persistent connection (e.g., WebSocket); the receptionist does **not** need to refresh the page. | Trigger a cancellation. Verify the notification appears without any page refresh or manual polling action. |

---

## REQ-AUTH-001: Reduced Re-Authentication Frequency for Receptionist Workstation

### Requirement Statement

The system shall maintain the receptionist's authenticated session for the **duration of a working shift** (minimum 8 continuous hours) without requiring re-entry of full login credentials (username and password), provided there is user activity within a rolling inactivity window. If the session becomes idle beyond the inactivity threshold, the system shall lock the screen and require only a **short PIN** to resume — not a full login.

### Rationale

> **L47–L48**: *"And please don't make me log in every single time. I'm in and out of that screen forty times an hour."*

R. Malik accesses the scheduling screen approximately **40 times per hour**. Any authentication friction — even a 10-second login — multiplied across that frequency would consume approximately 6–7 minutes per hour of pure login overhead. She explicitly requests the elimination of repeated logins. However, the system handles patient data and must still enforce security, so a lightweight re-authentication (PIN) on idle timeout is the appropriate compromise.

### Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| AC-1 | Given the receptionist logs in at the start of a shift, the session remains valid for at least **8 hours** without requiring full re-authentication, as long as there is at least one interaction (click, keystroke, or navigation) within every rolling **30-minute** window. | Log in and interact with the system periodically. Verify the session is still active after 8 hours without any full login prompt. |
| AC-2 | Given the session has been idle for more than **30 minutes**, the system locks the screen and prompts for a **4–6 digit PIN** — not a full username/password login. | Log in, then leave the workstation idle for 31 minutes. Verify the screen is locked and only a PIN prompt is shown. |
| AC-3 | Given the correct PIN is entered, the session resumes to the **last-viewed screen** in under **1 second**. No data or context is lost. | Lock the screen while viewing a specific date on the calendar. Enter the PIN. Verify the same calendar date is displayed immediately. |
| AC-4 | Given **5 consecutive incorrect PIN attempts**, the system terminates the session and requires a full login (username and password). | Enter an incorrect PIN 5 times in a row. Verify the system redirects to the full login screen. |
| AC-5 | The session is bound to the **originating device and browser**. Opening the application on a different device requires a separate, independent login. | Log in on Device A. Open the application URL on Device B. Verify Device B shows a login screen and Device A's session is unaffected. |
| AC-6 | A **manual logout** action is always available. When used, it fully terminates the session and requires a new full login to re-enter. | While logged in, click the logout button. Verify the session is terminated and attempting to access any page redirects to the login screen. |
| AC-7 | The PIN is stored as a **salted, hashed value** — never in plain text. PIN entry is rate-limited to prevent brute-force attacks. | Inspect the database schema: verify the PIN column stores a hash. Attempt 10 rapid PIN entries: verify the system enforces a cooldown or lockout after 5 failures (per AC-4). |

---

## Transcript Traceability Summary

| Requirement | Transcript Lines | Key Quote |
|-------------|-----------------|-----------|
| REQ-SMS-001 | L42–L44, L45–L46 | *"text them or something… Day before"* |
| REQ-SMS-002 | L42–L44 | *"cancel and I can give the slot away"* |
| REQ-SMS-004 | L44, L46 | *"If I know by the evening I can fill it"* |
| REQ-AUTH-001 | L47–L48 | *"don't make me log in every single time… forty times an hour"* |
