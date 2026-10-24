# MediQueue — Requirements

## Functional Requirements

### FR-1 — Appointment Scheduling

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1.1 | The system shall allow receptionists to create, view, update, and cancel appointments on a calendar grid | Must |
| FR-1.2 | The system shall display real-time slot availability, updating within ≤ 2 seconds of any change | Must |
| FR-1.3 | The system shall support searching for the next available slot by practitioner, date range, or appointment type | Should |
| FR-1.4 | The system shall prevent double-booking a practitioner in the same time slot unless explicitly overridden | Must |
| FR-1.5 | When a slot is freed (cancellation or no-show), it shall immediately appear as available for rebooking | Must |

### FR-2 — Automated Appointment Reminders

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-2.1 | The system shall send an SMS reminder to the patient 24 hours before the appointment by default | Must |
| FR-2.2 | The reminder message shall include: patient name, appointment date/time, practitioner name, and a reply-to-cancel option | Must |
| FR-2.3 | The system shall support a configurable reminder window (e.g., 24 h, 48 h) per clinic policy | Should |
| FR-2.4 | If a patient replies with a cancellation keyword (e.g., "CANCEL"), the system shall automatically cancel the appointment and free the slot | Must |
| FR-2.5 | Upon auto-cancellation, the system shall send a confirmation SMS to the patient | Must |
| FR-2.6 | Upon auto-cancellation, the system shall notify the receptionist via an in-app alert/badge | Must |
| FR-2.7 | The system shall log all sent reminders and patient responses with timestamps | Must |
| FR-2.8 | The system should support email reminders as a secondary channel | Could |

### FR-3 — Waitlist & Slot Backfill

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-3.1 | The system shall maintain a waitlist of patients who want earlier appointments | Should |
| FR-3.2 | When a slot is freed, the system should automatically notify the next eligible waitlisted patient via SMS | Should |
| FR-3.3 | If the waitlisted patient does not confirm within a configurable window (default: 2 hours), the system shall move to the next patient on the list | Should |

### FR-4 — Authentication & Session Management

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-4.1 | The system shall support long-lived receptionist sessions (minimum 8-hour validity without re-authentication) | Must |
| FR-4.2 | The system shall use a sliding session expiry — activity resets the timeout clock | Must |
| FR-4.3 | The system shall provide a manual "Lock Screen" option (quick PIN re-entry, not full login) for when the receptionist steps away | Should |
| FR-4.4 | Sessions shall be bound to the originating device/browser; concurrent sessions on different devices require separate login | Must |
| FR-4.5 | The system shall enforce role-based access control (Receptionist, Admin, Practitioner) | Must |

### FR-5 — No-Show Tracking & Reporting

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-5.1 | The system shall allow marking a patient as "No-Show" for a given appointment | Must |
| FR-5.2 | The system shall maintain a no-show counter per patient profile | Should |
| FR-5.3 | The system shall generate reports: daily no-show rate, weekly trend, and per-practitioner breakdown | Should |
| FR-5.4 | The system should flag patients with ≥ 3 no-shows in the last 90 days when booking | Could |

---

## Non-Functional Requirements

### NFR — Performance

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Page load time (scheduling screen) | ≤ 2 seconds |
| NFR-2 | Slot availability refresh after change | ≤ 2 seconds |
| NFR-3 | SMS delivery (reminder dispatch to carrier handoff) | ≤ 30 seconds |
| NFR-4 | Concurrent receptionist sessions supported | ≥ 20 simultaneous |
| NFR-5 | Inbound SMS processing (cancel reply → status update) | ≤ 60 seconds |

### NFR — Reliability & Availability

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-6 | System uptime | ≥ 99.5% (Mon–Sat, 07:00–20:00) |
| NFR-7 | Reminder job failure recovery | Auto-retry up to 3× with exponential backoff |
| NFR-8 | Data backup frequency | Daily, with 30-day retention |

### NFR — Security

| ID | Requirement |
|----|-------------|
| NFR-9 | All patient data must be encrypted at rest (AES-256) and in transit (TLS 1.2+) |
| NFR-10 | Authentication tokens must be stored securely (HttpOnly, Secure, SameSite cookies) |
| NFR-11 | Audit log of all appointment changes (who, what, when) retained for 1 year |
| NFR-12 | Compliance with applicable healthcare data regulations (e.g., local data protection laws) |

### NFR — Usability

| ID | Requirement |
|----|-------------|
| NFR-13 | Booking a new appointment must require ≤ 4 interactions from the main screen |
| NFR-14 | The UI must be operable with keyboard-only navigation (for speed) |
| NFR-15 | Colour-coded slot statuses: Available = green, Booked = blue, No-Show = red, Cancelled = grey |
