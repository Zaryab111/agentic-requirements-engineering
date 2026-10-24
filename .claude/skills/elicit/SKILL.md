---
name: elicit
description: "Extract requirement candidates from raw stakeholder interviews under evidence/. Produces grounded, cite-verified candidate statements ready for the Specifier Agent."
---

# Elicit Skill — Candidate Extraction Pipeline

This skill is invoked whenever the agent needs to extract requirement candidates from raw interview transcripts. Follow every step in order. Do NOT skip steps.

## Step 1: Inventory Evidence Files

Scan `evidence/interviews/` and list every `.md` file found. Each file is one interview transcript.

## Step 2: Parse Transcript Structure

For each transcript file:
1. Read the entire file.
2. Identify every line that starts with a transcript marker `L##` (e.g., `L38`, `L42`).
3. Group consecutive lines into **utterances**: a speaker line (`L## Q:` or `L## A:`) followed by zero or more continuation lines (`L## <text>` with no speaker marker).
4. Record each utterance with:
   - **Speaker**: Q (interviewer) or A (stakeholder)
   - **Transcript lines**: start–end (e.g., `42-44`)
   - **Full text**: the complete utterance with all continuation lines joined

## Step 3: Extract Candidate Pain Points

From the stakeholder (A:) utterances ONLY, identify distinct pain points or feature requests. Rules:
- **One candidate per distinct pain point.** Do not merge unrelated complaints into one candidate.
- **Never extract from interviewer (Q:) lines.** The interviewer's questions are prompts, not requirements.
- **Use the stakeholder's exact words as the evidence quote.** If the quote spans multiple transcript lines, join the continuation text and cite the full range (e.g., `43-44`).
- **If a quote is too long, use the single most specific sentence** that captures the core pain point. Cite only the transcript line(s) containing that sentence.

## Step 4: Classify Each Candidate

For each candidate, determine:
- **Category**: Functional, Non-Functional, Constraint, or DomainRule (per `_schema.json`)
- **Confidence**: 0.0–1.0 based on how explicitly the stakeholder stated the need
  - 0.9–1.0: Stakeholder directly stated a clear need or request
  - 0.7–0.89: Need is implied but not directly stated
  - Below 0.7: Speculative; flag for review

## Step 5: Handoff to Specifier Agent

For each candidate, produce a YAML frontmatter block with ALL required fields from `_schema.json`:
- `id`: Use pattern `REQ-<AREA>-<NNN>` (e.g., `REQ-SMS-001`, `REQ-AUTH-001`)
- `lines`: Use **transcript line markers** (e.g., `"42-42"` or `"43-44"`), NOT file line numbers
- `evidence_quote`: The verbatim stakeholder quote. Must appear in the transcript at the cited lines after stripping the `L## A:` prefix.
- `source`: Relative path to the evidence file (e.g., `evidence/interviews/receptionist.md`)
- `assumptions`: List anything the requirement depends on that is NOT stated in the evidence

## Step 6: Specifier Agent — Translate to EARS

For each candidate, write the requirement statement using EARS grammar (per `.claude/rules/requirements.md` §3):
- **Event-driven**: `WHEN [Trigger], the system shall [Response]`
- **State-driven**: `WHILE [State], the system shall [Response]`
- **Unwanted behavior**: `IF [Trigger], THEN the system shall [Response]`

### Critical Rules for the Statement:
1. The statement MUST contain the word "shall".
2. The statement MUST NOT contain any banned words from `.claude/rules/requirements.md` §1.
3. The statement MUST NOT contain rationale or explanatory "so that" clauses. Rationale goes in the Rationale section only.
4. **Quantified metrics** (timing, counts, durations) that are NOT explicitly stated in the evidence MUST be listed as assumptions. Do NOT silently invent numbers.
5. The EARS state or trigger must use **objective, testable conditions** (e.g., "has an active authenticated session") not subjective descriptions (e.g., "is actively using").

## Step 7: Ambiguity Audit

Before writing each file, scan the full body text (statement + rationale + acceptance criteria) against the banned word list from `.claude/rules/requirements.md` §1. If any banned word is found, rewrite the sentence to use a quantifiable metric.

## Step 8: Write and Lint

1. Write each requirement file to `requirements/`.
2. Run `python scripts/lint-requirements.py`.
3. If ANY file fails, read the error, fix the file, and re-run until all pass.
