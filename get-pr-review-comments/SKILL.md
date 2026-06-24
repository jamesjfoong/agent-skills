---
name: get-pr-review-comments
description: Use when fetching all PR review comments, line-level feedback, or review summaries from GitHub pull requests. Covers hitting correct API endpoints and verifying completeness. Don't use for creating PRs, managing issues, or general gh CLI tasks.
license: MIT
compatibility: gh CLI authenticated, jq available
metadata:
  author: jamesjfoong
---

## Quick start

3 endpoints, not 1. Hit all, merge results. Count first before reporting.

## Workflow

Copy checklist, check off:

- [ ] Fetch **line-level comments**: `pulls/{number}/comments`
- [ ] Fetch **review summaries**: `pulls/{number}/reviews`
- [ ] Fetch **thread comments**: `issues/{number}/comments`
- [ ] Verify **total count** before reporting — never trust truncated output

## Common commands

```bash
# All line-level comments for a specific user
gh api repos/{owner}/{repo}/pulls/{number}/comments \
  --jq '[.[] | select(.user.login == "username")] | {count: length, items: .}'

# All reviews with state and body
gh api repos/{owner}/{repo}/pulls/{number}/reviews \
  --jq '.[] | {user: .user.login, state: .state, body: .body}'

# All thread comments (START/END REVIEW, general notes)
gh api repos/{owner}/{repo}/issues/{number}/comments \
  --jq '.[] | {user: .user.login, body: .body}'

# Get total comment count for a user
gh api repos/GDP-ADMIN/CATAPA-WEB/pulls/12482/comments \
  --jq '[.[] | select(.user.login == "felix-adhinata")] | length'
```

## Pitfalls to avoid

| Mistake | Fix |
|---------|------|
| Using `pulls/{n}/reviews` for line feedback | Reviews endpoint returns summary envelopes (body often empty). Real line feedback in `pulls/{n}/comments` |
| Trusting truncated ctx_search output after ctx_execute | Always `--jq 'length'` first to verify total count |
| Missing thread-only messages | Also hit `issues/{n}/comments` (START/END REVIEW, bot messages) |
| Using only `gh pr view --json comments` on enterprise repos | Falls back to API directly for full control |

## Verification

After all fetches, assert: sum of line-level + review bodies + thread comments matches PR conversation tab count.
