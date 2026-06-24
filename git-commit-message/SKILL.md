---
name: git-commit-message
description: Use when generating, reviewing, or amending Git commit messages. Enforces change-describing subjects, imperative mood, type(scope), and bullet bodies. Do not use for PR descriptions, changelog entries, or branch names.
license: MIT
metadata:
  author: James Jeremy Foong
---

# Git Commit Message Skill

## Goal

Produce commit messages that describe the code change, not the review process.

## Rules

1. **Subject describes the change**
   - Format: `<type>(<scope>): <imperative summary>`
   - Good: `fix(attendance): strong type, signal inputs, and shared machine access table in employee mapping edit`
   - Bad: `fix(attendance): address PR review feedback` / `refactor per felix's comments`

2. **Allowed types**: `feat`, `fix`, `refactor`, `test`, `chore`, `docs`, `style`, `perf`, `build`, `ci`

3. **Imperative mood**, lowercase after colon, no trailing period
   - Good: `add explicit typing to employee mapping specs`
   - Bad: `Added explicit typing to employee mapping specs.`

4. **No meta/process words** in the subject or body bullets:
   - Avoid: `address`, `fix review`, `per review`, `feedback`, `requested changes`, `CR comments`, `resolve thread`
   - Allowed only when the change itself is a review workflow feature.

5. **Body bullets list concrete changes**
   - Start with a verb.
   - One bullet per logical change.
   - Keep under 72 chars per line.

6. **Max subject length**: 72 characters. Hard truncate if needed.

## Workflow

1. Read the staged diff (`git diff --cached --stat` and key hunks).
2. Identify the single most accurate type and scope.
3. Draft a subject that says what the code now does.
4. Draft 2–7 body bullets, each describing a concrete change.
5. Run the validation checklist below.
6. If validation fails, rewrite; do not commit with a bad message.

## Validation checklist

- [ ] Subject starts with `type(scope): `.
- [ ] Subject is in imperative mood.
- [ ] Subject does not contain `review`, `feedback`, `address`, `per`, `requested`, `CR`, or `thread`.
- [ ] Subject is 72 chars or fewer.
- [ ] Body bullets start with a verb and describe actual code changes.
- [ ] No body bullet says "address review feedback" or similar.

## Examples

Good:

```text
fix(attendance): strong type, signal inputs, and shared machine access table

- Use PathConstant.BACK for back navigation
- Convert EmployeeMachineAccessTableComponent to input signal
- Extend machine-access table with ObservableComponent for lifecycle
- Convert EmployeeMappingFormSectionComponent inputs to signals
- Remove redundant fetchFailAction loading:false reducer
- Add explicit typing in form-page and machine-access specs
- Apply prettier and empty-line fixes
- Use shared app-employee-machine-access-table in form-section and modal
- Replace list-page edit click handler with routerLink
```

Bad:

```text
fix(attendance): address PR review feedback on employee mapping edit

- Fixed felix's comments
- Resolved review threads
```
