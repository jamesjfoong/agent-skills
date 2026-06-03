---
name: google-chat-to-issue
description: Turn a Google Chat thread or space into a structured issue or bug report draft. Trigger this skill whenever the user shares a Google Chat URL (chat.google.com/room/...) and wants it converted into a GitHub issue, Jira ticket, bug report, or any structured issue draft — even if they just say "make an issue from this", "write up a bug report from our chat", "can you draft a ticket from this thread", or "turn this conversation into an issue". Also trigger when the user pastes a Chat URL alongside words like "issue", "bug", "ticket", "report", or "track". Do NOT trigger for general chat summarization with no issue intent, autonomous filing in a tracker, or code-level patch proposals.
---

# Google Chat → Issue Draft

This skill reads a Google Chat thread or space, extracts the relevant technical discussion, and produces a polished issue or bug report draft ready for human review. It never files the issue automatically.

## Step 1: Check required tools

Before anything else, verify that Google Chat MCP tools are available in the current session. Look for tool names that contain `Google_Chat` or `GoogleChat` or `google_chat` (e.g., `mcp__*__Google_Chat__*` or similar patterns).

If no Google Chat tools are found, stop immediately and tell the user:

> This skill requires Google Chat MCP tools to read conversations. Please add a Google Chat MCP server to your agent/client configuration and try again. Without it, I can't access the thread content.

## Step 2: Parse the URL and time window

Classify the URL the user provided:

| URL pattern | Type | Action |
|---|---|---|
| `.../room/<roomId>/<threadId>/...` | Thread | Read entire thread |
| `.../room/<roomId>` (no thread segment) | Space | Use time window (see below) |
| Unrecognizable pattern | Unknown | Ask user to confirm which type |

**Thread URL** — two or more path segments after `/room/`:
```
https://chat.google.com/room/AAAA7zZtnOg/Lrb548iAGiU/Lrb548iAGiU?cls=10
                              ^roomId^     ^threadId^
```
Read all messages in that thread.

**Space URL** — only one path segment after `/room/`, no thread segment:
```
https://chat.google.com/room/AAAA7zZtnOg?cls=7
                              ^roomId only^
```
Determine the time window in this order:
1. If the user already stated a time range in their message (e.g., "1pm–3pm today", "last 2 hours"), use it.
2. If no time range was given, ask: *"What time range should I pull? (e.g., '1pm–3pm today', 'last 2 hours') — I'll default to today if you skip this."*
3. If the user declines to specify, default to today (midnight → now).

## Step 3: Ask clarifying questions (max 2–3, only if needed)

Only ask if critical information is genuinely missing. Bundle all questions into one message rather than asking one at a time.

Useful questions:
- **Time range** — only for space URLs, as above.
- **Issue template** — *"Do you have an issue template URL or format you'd like me to follow? I'll use the default if not."*
- **Scope** — *"Should I create one issue or multiple if I spot distinct problems?"* — only ask if the conversation is clearly multi-topic and the right answer isn't obvious.

Never ask about things you can infer (e.g., don't ask "is this a bug?" when the thread is clearly about a bug).

## Step 4: Gather the conversation

If the conversation looks complex (a sprawling multi-day space thread, many linked threads, or the user mentions multiple distinct topics), consider using the planning tool to map out what needs to be fetched and in what order before starting.

Use the Google Chat MCP tools to fetch:
1. All messages in the thread (or space within the time window), handling pagination automatically.
2. Any Chat thread URLs **linked within** those messages, up to **2 hops deep**: threads linked from the main thread (hop 1), and threads linked from those (hop 2). Stop there — don't follow further. Record every thread URL visited so you don't revisit one already fetched.

Handle errors gracefully:
- **Pagination errors**: continue with what was retrieved; warn the user that results may be partial and how many messages were fetched.
- **Empty results**: report "No messages found in that time window" and offer to widen the range.
- **Access denied / invalid URL**: explain the specific problem and stop — don't guess at content you can't read.
- **Linked thread loop detected** (URL already visited): stop following that branch.

## Step 5: Fetch referenced external resources (opportunistic)

Scan message content for external links. Prioritize: GitHub issues/PRs, Google Drive/Docs, error dashboards, log links. Limit to the 5 most relevant links.

For each:
- **GitHub issues/PRs**: use GitHub MCP tools if available, else `WebFetch` — extract title, status, and description.
- **Google Drive / Docs**: use Google Drive MCP tools if available.
- **Other URLs**: use `WebFetch` if available.

If a fetch fails, note it in "Additional context" and continue — don't let a broken link block the whole draft.

## Step 6: Decide single vs. multi-issue

Read the full conversation and identify distinct problems:

| Situation | Decision |
|---|---|
| One clear problem | One issue |
| Multiple causally-linked problems (A causes B) | One issue describing the chain |
| User explicitly asked for multiple issues | Split into multiple issues |
| Multiple independent problems, obvious and confirmed | Multiple issues with cross-references |
| Ambiguous — could be one or many | Default to one issue; note potential split in "Additional context" |

When producing multiple issues, label relationships explicitly: "blocked by", "related to #2", etc. Each issue must be fully self-contained.

## Step 7: Detect or apply issue template

If the user provided a template URL or file path, fetch or read it and use that structure. Fill all required fields the template defines.

If no template is provided, use the default template below.

## Step 8: Write the draft(s)

### Default template

```markdown
<1–3 sentence summary: what is happening and why it matters, written so someone unfamiliar with the thread grasps it immediately — no jargon without definition>

## What happened
<Observed behavior, drawn directly from the chat. Use the project's own terminology. Describe what a user sees or experiences — avoid file paths, line numbers, or internal implementation details, which rot quickly and make the issue hard to search.>

## Expected behavior
<What should have happened instead.>

## Steps to reproduce
<Numbered steps. If the thread doesn't state reproduction steps explicitly, infer the most likely path and mark inferred steps with "(inferred)".>

## Potential solutions / next actions
<Concrete options or next steps discussed in the thread. If none were discussed, note what reasonable next steps would be based on the nature of the problem.>

## Additional context
<Links to relevant threads followed, external resources fetched, related issues, and anything else that doesn't fit above. Note any pagination gaps, fetch failures, or inferred content here.>
```

### Writing guidelines

- **Use the project's language**: borrow terms directly from the conversation — don't introduce synonyms that could confuse readers.
- **Observable behavior only**: describe what a user sees or experiences, not which function threw or which line failed. Issues outlive the code they're filed against.
- **Self-contained**: each issue must make sense without reading the chat thread.
- **Label inferences**: anything you inferred rather than read explicitly — mark it "(inferred)".
- **Multi-issue titles**: each issue gets a standalone descriptive title and its own full set of sections, plus a "Related issues" note at the top.

## Step 9: Present to user

Render the draft(s) as Markdown in the conversation. After presenting, add:

> Does this look right? I can adjust tone, add detail, split into multiple issues, apply a different template, or restructure any section.

Do **not** offer to file the issue in any tracker — that's out of scope for this skill.

---

## Edge case quick reference

| Situation | Behavior |
|---|---|
| No Google Chat MCP tools available | Stop; tell user to add Google Chat MCP server |
| URL pattern unclear (thread vs. space) | Ask user to confirm |
| Empty time window / no messages found | Report it; offer to widen the range |
| Linked threads form a loop | Stop following at depth 2 |
| No project template provided | Use default; tell user |
| Pagination or fetch error | Continue with partial data; warn user clearly |
| Multiple distinct problems in thread | One issue by default; split only if user asked or it's clearly necessary |
| External link fetch fails | Note in "Additional context"; don't block the draft |
| Conversation is noise with no actionable issue | Tell the user honestly; don't fabricate an issue |

---

## Appendix A: Google Chat MCP Tool Reference

See [`references/GOOGLE_CHAT_MCP.md`](references/GOOGLE_CHAT_MCP.md) for full details on:
- Identifying the correct tool name for your MCP integration (GLConnector or generic)
- Calling `messages_list` with the correct `path`, `query.filter`, and `response_fields`
- Parsing a Google Chat URL to extract `spaceId`, `threadId`, and `replyId`
- Constructing a Google Chat deep-link from API response fields
- Known limitations (sender as opaque ID, pagination)
