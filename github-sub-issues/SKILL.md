---
name: github-sub-issues
description: "Use when creating sub-issues on GitHub via the GraphQL API. Not for linking branches, creating repos, or managing projects."
license: MIT
compatibility: gh CLI v2.40+ with GraphQL API access
metadata:
  source: https://github.com/jamesjfoong
  author: jamesjfoong
---

# GitHub Sub-Issues via GraphQL

Create sub-issues using `gh api graphql` with `addSubIssue` mutation.

## Quick start

```bash
# Get node_id of parent issue
PARENT_ID=$(gh api repos/$OWNER/$REPO/issues/$PARENT_NUM --jq '.node_id')

# Get node_id of child issue
CHILD_ID=$(gh api repos/$OWNER/$REPO/issues/$CHILD_NUM --jq '.node_id')

# Link as sub-issue
gh api graphql -f query='
mutation {
  addSubIssue(input: {
    issueId: "'$PARENT_ID'"
    subIssueId: "'$CHILD_ID'"
  }) { clientMutationId }
}'
```

## Workflow

1. Get node IDs for parent + child issues
2. Run `addSubIssue` mutation
3. Verify with query:
   ```bash
   gh api graphql -f query='
   query {
     node(id: "'$PARENT_ID'") {
       ... on Issue {
         subIssues(first: 20) { nodes { number title } }
       }
     }
   }' --jq '.data.node.subIssues.nodes'
   ```

## Remove sub-issue

```bash
gh api graphql -f query='
mutation {
  removeSubIssue(input: {
    issueId: "'$PARENT_ID'"
    subIssueId: "'$CHILD_ID'"
  }) { clientMutationId }
}'
```

## Notes

- Race condition: running parallel mutations on same parent may fail with "Priority has already been taken". Retry fixes it.
- Sub-issues appear in parent's `subIssues` connection, not in `trackedByIssues`.
- GitHub enforces a limit on sub-issues per parent (varies by plan).
