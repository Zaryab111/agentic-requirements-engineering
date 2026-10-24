---
paths:
  - "requirements/**/*.md"
---

# Requirements Quality & Ambiguity Rules

This rule set is automatically active whenever you read, write, or edit files inside the `requirements/` directory.

## 1. Automated Ambiguity Audit (Subjective Words)
Before saving or modifying any requirement file, you must audit the statement to ensure it contains zero subjective language. Immediately flag, reject, or rewrite if you find any of these "requirement smells":
- **Performance**: *fast, slow, quickly, extremely, robust, responsive, laggy, in a jiffy* (Replace with quantitative metrics, e.g., "within 2.0 seconds").
- **Time**: *morning, evening, afternoon, night, immediately, timely, shortly, twilight* (Replace with explicit local military time windows, e.g., "no later than 18:00 local time").
- **Usability**: *user-friendly, intuitive, simple, easy, appropriate, sufficient, appropriate* (Replace with explicit actions, e.g., "requiring no more than one badge tap").

## 2. The 7 ISO Quality Criteria Check
Every requirement must satisfy these semantic gates:
- **Unambiguous**: Can only be interpreted one single way.
- **Verifiable**: A developer can write a clear, mathematical pass/fail test for it.
- **Feasible**: Technically realistic for our clinic stack.
- **Complete**: All triggers and system actors are fully declared.
- **Consistent**: Must not contradict or fight other requirements in this folder.
- **Traceable**: Contains direct quotes matching `evidence/interviews/receptionist.md` verbatim.
- **Necessary**: Solves a documented pain point from our evidence files.

## 3. Mandatory Grammar (EARS)
All requirements must match one of the following templates using the binding keyword "shall":
- **Event-driven**: WHEN [Trigger], the system shall [Response]
- **State-driven**: WHILE [State], the system shall [Response]
- **Unwanted behavior**: IF [Trigger], THEN the system shall [Response]
