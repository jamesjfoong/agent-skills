---
name: skill-creator
description: Create, update, validate, package, and improve Agent Skills. Use when the user wants to create a skill, build a new skill, scaffold a skill, update an existing skill, combine skills, validate SKILL.md structure, design skill resources, test skill behavior, improve skill triggering, or learn effective skill design patterns.
compatibility: Agent Skills-style directories with SKILL.md frontmatter and optional bundled resources; no specific agent runtime or CLI is required.
---

# Skill Creator

Use this skill to create or improve reusable Agent Skills without assuming a specific runtime, CLI, path convention, browser, subagent system, package manager, or model provider. Detect the target environment from the repository, user instructions, and available tools. If the environment is unclear, create a portable skill directory and tell the user what still needs runtime-specific installation.

## Core Workflow

1. Capture the skill's intent and target users.
2. Design the reusable skill contents: instructions, scripts, references, and assets.
3. Scaffold or update the skill directory.
4. Write a lean `SKILL.md` using progressive disclosure.
5. Validate structure and metadata.
6. Test on realistic prompts.
7. Iterate from evidence and user feedback.
8. Package or present the skill in whatever format the target environment supports.

Be flexible. If the user only wants a quick draft, skip formal evals. If the skill will automate a fragile workflow, invest in scripts, validation, and test prompts.

## Communicating With The User

Users vary widely in technical background. Prefer plain language by default. Briefly define jargon such as "frontmatter", "assertion", "baseline", or "eval" when the user has not signaled familiarity.

Avoid asking a long questionnaire up front. Extract what you can from the conversation and ask the smallest number of questions needed to proceed.

## Capture Intent

Start by understanding the reusable behavior the user wants to capture. If the current conversation already demonstrates the workflow, mine it first: tools used, step order, corrections from the user, examples, output formats, files touched, and any decisions that should become guidance.

Answer these questions before drafting unless they are already clear:

- What should the skill enable an agent to do?
- When should the skill trigger? Include phrases, file types, workflows, and near-miss cases.
- What should the output look like?
- What knowledge, examples, templates, or scripts would save repeated work?
- How can the skill be tested well enough for the risk involved?

For an existing skill, preserve the skill name unless the user explicitly wants a rename. If the installed copy is read-only, copy it to a writable working directory, edit the copy, and package or return the result.

## Skill Anatomy

A portable skill is a directory with a required `SKILL.md` and optional bundled resources:

```text
skill-name/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

`SKILL.md` contains YAML frontmatter followed by markdown instructions.

Required frontmatter:

- `name`: lowercase letters, digits, and single hyphens; max 64 characters; match the directory name unless the target runtime says otherwise.
- `description`: what the skill does and when to use it; max 1024 characters for broad compatibility.

Optional frontmatter, only when useful and supported by the target runtime:

- `license`
- `compatibility`
- `allowed-tools`
- `metadata`

Do not add runtime-specific fields unless the target environment requires them.

## Progressive Disclosure

Skills should spend context carefully. Put only essential workflow guidance in `SKILL.md`; move detailed material into resources that the agent reads only when needed.

Use the three-level model:

1. Metadata: `name` and `description`, always visible to the agent.
2. `SKILL.md` body: loaded after the skill triggers.
3. Bundled resources: read or executed only when the task needs them.

Keep `SKILL.md` under 500 lines when practical. If it is growing large, split details into one-level references from `SKILL.md`.

Good resource choices:

- `scripts/`: deterministic or repeatedly rewritten code, such as converters, validators, report builders, or API wrappers.
- `references/`: domain knowledge, schemas, policies, API docs, detailed examples, and long workflows.
- `assets/`: files copied into outputs, such as templates, starter projects, fonts, images, or sample data.

Avoid auxiliary clutter such as `README.md`, installation guides, changelogs, and quick-reference docs unless the user specifically needs them. A skill is for the agent using it, not a general documentation site.

## Set Degrees Of Freedom

Match specificity to the task's fragility.

- High freedom: use concise principles and examples when many valid approaches exist.
- Medium freedom: use pseudocode, templates, or configurable scripts when there is a preferred pattern with room for variation.
- Low freedom: provide exact scripts or checklists when the work is fragile, repetitive, or error-prone.

Prefer explaining why guidance matters over piling on rigid rules. If you find yourself writing many absolute requirements, reconsider whether a script, template, or clearer principle would work better.

## Writing `SKILL.md`

Write for a capable agent. Include information that is non-obvious, domain-specific, or easy to forget.

Use imperative instructions:

```markdown
## Invoice Reconciliation

When reconciling invoices:

1. Read the vendor mapping from `references/vendors.md`.
2. Normalize dates to ISO format.
3. Run `scripts/check_totals.py` before returning results.
```

Use concrete examples when they teach better than prose:

```markdown
## Commit Message Format

Example:

Input: Added login endpoint and token validation middleware
Output: `feat(auth): implement token-based login`
```

For output formats, give a template:

```markdown
## Report Structure

Use this structure:

# [Title]
## Summary
## Findings
## Recommendations
```

For multiple domains or variants, keep selection guidance in `SKILL.md` and split details:

```text
cloud-deploy/
├── SKILL.md
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

Tell the agent when to read each reference. Avoid references that only point to deeper references.

## Description Writing

The description is the primary trigger. Put all "when to use this skill" information in the frontmatter description because the body is only loaded after triggering.

Good descriptions include:

- What the skill does.
- Specific trigger scenarios, task types, file types, or user phrases.
- Adjacent cases where this skill should be used even if the user does not name it.

Avoid vague descriptions such as "helps with documents". Prefer a direct description such as:

```yaml
description: Create, edit, inspect, and validate professional documents with templates, tracked changes, comments, and formatting preservation. Use when working with document files, drafting reports, applying company templates, extracting document text, or modifying document structure.
```

## Scaffold A Skill

If creating a new skill, choose the output directory from the user's instructions or the repository's conventions. Do not assume a global user path or runtime-specific project path.

Use the bundled initializer to scaffold a skill directory:

```bash
python scripts/init_skill.py my-skill --path path/to/skills
```

For a minimal skill with only `SKILL.md`, pass `--minimal`:

```bash
python scripts/init_skill.py my-skill --path path/to/skills --minimal
```

Delete placeholder files and unused resource directories before finalizing.

## Validate

Run the bundled validator when Python is available:

```bash
python scripts/quick_validate.py path/to/my-skill
```

Fix validation failures before packaging or handing off. Also review qualitatively:

- The description is specific and trigger-oriented.
- `SKILL.md` is concise and uses consistent terminology.
- Resource references are one level deep and clearly tell the agent when to read or run them.
- Scripts have been run on representative inputs.
- The skill does not include malicious, misleading, surprising, or unauthorized behavior.

## Test And Evaluate

Use evidence proportional to risk.

For low-risk writing or guidance skills, a few human-reviewed examples may be enough. For file transforms, code generation, data extraction, or fragile workflows, create realistic test prompts and reusable checks.

Testing workflow:

1. Write 2-3 realistic prompts the user or a future user would actually ask.
2. Ask the user to confirm or edit them.
3. Run the skill in the available environment.
4. If possible, compare against a baseline: no skill for a new skill, or the prior version for an existing skill.
5. Capture outputs, errors, timing, and repeated mistakes.
6. Use programmatic checks for objective requirements and human review for subjective quality.
7. Improve the skill, then rerun the same prompts.

If independent runners or subagents are available, use them for cleaner comparisons. If not, run the prompts yourself as a sanity check and be transparent that the test is less independent. If there is no browser or review UI, present outputs directly in the conversation or save review artifacts as files.

Good assertions are objective and readable:

```json
[
  {
    "name": "creates-csv-output",
    "description": "The run produces a CSV file with the requested columns."
  }
]
```

Do not force quantitative checks onto subjective work. For subjective skills, collect specific user feedback and generalize from it rather than overfitting to one prompt.

## Improve A Skill

When feedback arrives, improve the reusable mechanism, not just the one example.

Look for:

- Missing domain knowledge that belongs in `references/`.
- Repeated code that should become a script.
- Confusing instructions that caused wasted work.
- Overly broad or narrow trigger descriptions.
- Output format guidance that needs an example or template.
- Resource files that are unused or hard to discover.

Read transcripts or intermediate work when available, not only final outputs. If several runs independently recreate the same helper, add that helper to `scripts/`.

Repeat until the user is satisfied, feedback is empty or minor, or another iteration is no longer improving the skill.

## Optimize Triggering

After the skill works, improve the description.

1. Create 16-20 realistic trigger-eval queries: roughly half should trigger, half should not.
2. Include tricky near-misses, adjacent domains, casual phrasing, file names, and incomplete user context.
3. Ask the user to review the eval set.
4. Test whether the target agent would select the skill, using whatever inspection or evaluation method the environment supports.
5. Rewrite the description based on missed triggers and false positives.
6. Prefer held-out examples or fresh prompts before declaring the description improved.

Avoid obviously irrelevant negative examples. They do not reveal whether the description is well-targeted.

## Package Or Hand Off

Package only in a format supported by the target environment. If `.skill` archives are useful, use:

```bash
python scripts/package_skill.py path/to/my-skill dist
```

If the environment installs skills by copying directories, provide the directory path instead. If the runtime-specific install step is unknown, leave the skill as a portable directory and explain what the user needs to decide.

## Reference Helpers

- `scripts/init_skill.py`: create a portable skill directory with optional example resources.
- `scripts/quick_validate.py`: validate required frontmatter and common portability constraints.
- `scripts/package_skill.py`: create a `.skill` zip archive after validation.
