# Agentic Requirements Engineering Pipeline (MediQueue Case Study)

> An AI-agent-driven requirements engineering system that extracts, specifies, and validates software requirements from raw stakeholder interviews — with zero subjective language, full evidence traceability, and automated quality gates.

## What This Project Demonstrates

Traditional requirements engineering is manual, error-prone, and produces ambiguous specifications. This project builds a **deterministic, auditable pipeline** where AI agents follow codified rules — not improvisation — to produce ISO-quality requirements from raw interview transcripts.

### The Problem It Solves

| Traditional (Manual) RE | This Agentic Pipeline |
|---|---|
| Requirements contain vague words ("fast", "easy", "user-friendly") | Automated banned-word scanner rejects subjective language |
| No traceability to stakeholder statements | Every requirement cites verbatim quotes with transcript line numbers |
| Inconsistent formatting across authors | EARS grammar (WHEN/WHILE/IF + "shall") enforced by linter |
| Invented metrics presented as stakeholder needs | Non-evidence numbers flagged as explicit assumptions |
| Quality review is manual and subjective | Python linter + GitHub Actions CI gate = automated quality control |

## Architecture

```
evidence/interviews/         ← Immutable stakeholder transcripts (write-protected)
     ↓
.claude/skills/elicit/       ← Elicitor Agent skill (extraction rules)
     ↓
.claude/rules/requirements.md ← Quality rules (banned words, EARS grammar, ISO criteria)
     ↓
requirements/                ← Output: EARS-formatted, evidence-grounded .md files
     ↓
scripts/lint-requirements.py ← Automated linter (grounding verification, banned words, EARS check)
     ↓
.github/workflows/           ← CI gate blocks non-compliant requirements from merging
```

### Quality Gates (Defense-in-Depth)

| Layer | File | What It Catches |
|---|---|---|
| **Pre-write** | `.claude/hooks/protect-evidence.sh` | Blocks any edit to `evidence/` — the audit trail is immutable |
| **Pre-write** | `.claude/rules/requirements.md` | Agent auto-audits for banned words, EARS grammar, ISO criteria before writing |
| **Pre-write** | `.claude/skills/elicit/SKILL.md` | Codified 8-step extraction pipeline the agent must follow |
| **Post-write** | `scripts/lint-requirements.py` | Grounding verification, banned word scan, EARS keyword check, duplicate ID detection |
| **CI** | `.github/workflows/requirements-ci.yml` | GitHub Actions blocks non-compliant pushes |

## Case Study: MediQueue Clinic

The demo uses an interview transcript with R. Malik, Senior Receptionist at a medical clinic, who describes:
- **No-show problem**: "Half our no-shows are people who just forgot."
- **SMS reminder request**: "We should text them or something."
- **Cancellation + slot reuse**: "Early enough that they can cancel and I can give the slot away."
- **Login friction**: "Don't make me log in every single time."

The pipeline extracts **4 requirements** from this single transcript:

| ID | Title | EARS Pattern | Evidence |
|---|---|---|---|
| REQ-SMS-001 | Automated SMS Appointment Reminder | WHEN (event) | L42 |
| REQ-SMS-002 | Patient Cancellation via SMS Reply | WHEN (event) | L43–L44 |
| REQ-SMS-003 | Receptionist Notification on Freed Slot | WHEN (event) | L46 |
| REQ-AUTH-001 | Reduced Re-Authentication Frequency | WHILE (state) | L47–L48 |

## How to Run

### Prerequisites
- Python 3.10+
- PyYAML (`pip install pyyaml`)

### Run the Linter
```bash
python scripts/lint-requirements.py
```

Expected output:
```
⚙️ Loaded dynamic banned word list: ['fast', 'slow', 'evening', 'sufficient', ...]
🔍 Auditing requirement file: requirements/REQ-AUTH-001-reduced-reauth.md
✅ Success: Requirement passed all automated checks!
🔍 Auditing requirement file: requirements/REQ-SMS-001-reminder-dispatch.md
✅ Success: Requirement passed all automated checks!
🔍 Auditing requirement file: requirements/REQ-SMS-002-cancellation-reply.md
✅ Success: Requirement passed all automated checks!
🔍 Auditing requirement file: requirements/REQ-SMS-003-slot-freed-alert.md
✅ Success: Requirement passed all automated checks!
```

## Key Technical Features

### Transcript-Aware Grounding Verification
The linter doesn't just check file line numbers — it builds a **transcript marker index** (`L38`, `L42`, etc.) and resolves citations by marker, making verification robust even if the interview file is reformatted.

### Dynamic Banned Word Extraction
Banned words aren't hardcoded in the linter. They're parsed live from `.claude/rules/requirements.md` using regex, so adding a new banned word to the rules file automatically updates the linter — zero code changes needed.

### Evidence Immutability
A pre-tool-use hook (`protect-evidence.sh`) blocks any write to `evidence/` at the system level, ensuring the audit trail can never be silently modified.

## Project Structure

```
.
├── .claude/
│   ├── hooks/
│   │   └── protect-evidence.sh       # Blocks edits to evidence/
│   ├── rules/
│   │   └── requirements.md           # Quality rules (banned words, EARS, ISO)
│   ├── skills/
│   │   └── elicit/
│   │       └── SKILL.md              # 8-step extraction pipeline
│   └── settings.json                 # Hook and rule configuration
├── .github/
│   └── workflows/
│       └── requirements-ci.yml       # CI quality gate
├── evidence/
│   └── interviews/
│       └── receptionist.md           # Raw stakeholder transcript
├── requirements/
│   ├── _schema.json                  # JSON Schema for requirement files
│   ├── REQ-AUTH-001-reduced-reauth.md
│   ├── REQ-SMS-001-reminder-dispatch.md
│   ├── REQ-SMS-002-cancellation-reply.md
│   └── REQ-SMS-003-slot-freed-alert.md
├── scripts/
│   └── lint-requirements.py          # Automated quality linter
├── AGENTS.md                         # Agent role definitions
├── CLAUDE.md                         # Developer rules
└── README.md
```

## Technologies & Concepts

- **Requirements Engineering**: EARS syntax, ISO 29148 quality criteria, stakeholder elicitation
- **AI Agent Orchestration**: Multi-agent pipeline (Elicitor → Specifier), codified skills, rule-driven behavior
- **DevOps / CI**: GitHub Actions quality gate, pre-commit hooks, automated linting
- **Python**: YAML frontmatter parsing, regex-based transcript analysis, grounding verification
- **Software Quality**: Defense-in-depth validation, evidence traceability, ambiguity detection

## License

MIT License — see [LICENSE](LICENSE) for details.
