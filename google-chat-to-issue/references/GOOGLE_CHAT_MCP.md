# Google Chat MCP — Tool Reference

This reference documents how to call Google Chat MCP tools to fetch thread messages.
It is validated against the **GLConnector** integration but the same parameters apply to any compliant Google Chat MCP server.

---

## Identifying the integration

Tool names vary by MCP server. Common patterns:

| Integration | Tool name pattern |
|---|---|
| GLConnector | `mcp1_google_chat_*` or `mcp__google_chat__*` |
| Generic | any tool containing `Google_Chat`, `google_chat`, or `GoogleChat` |

The tool used in this skill is `messages_list` (namespaced: `mcp1_google_chat_messages_list`).

---

## Parsing a Google Chat URL

```
https://chat.google.com/room/<spaceId>/<threadId>/<messageId>?cls=10
                               ^^^^^^^^   ^^^^^^^^   ^^^^^^^^^
```

| URL segment | Maps to | API resource name |
|---|---|---|
| `<spaceId>` | Space | `spaces/<spaceId>` |
| `<threadId>` | Thread | `spaces/<spaceId>/threads/<threadId>` |
| `<messageId>` | Message | see note below |

> **Thread root vs. reply**: When the URL repeats the same value for both thread and message segments (e.g., `.../gskWxw7_dKU/gskWxw7_dKU`), it links to the thread's root message.
> For replies the message segment contains only the reply's short ID (the part after the dot in the API's `messages.name` field — see below).

---

## Fetching messages from a thread

### Parameters

| Parameter | Value | Notes |
|---|---|---|
| `path.parent` | `spaces/<spaceId>` | Space resource name |
| `query.filter` | `thread.name=spaces/<spaceId>/threads/<threadId>` | Filters to a specific thread |
| `response_fields` | `["messages.name", "messages.create_time", "messages.text", "messages.sender"]` | Minimal useful set |

### Example

Given the URL:
```
https://chat.google.com/room/AAAAse3ABDE/gskWxw7_dKU/gskWxw7_dKU?cls=10
```

Call:
```
messages_list(
  path            = { parent: "spaces/AAAAse3ABDE" },
  query           = { filter: "thread.name=spaces/AAAAse3ABDE/threads/gskWxw7_dKU" },
  response_fields = ["messages.name", "messages.create_time", "messages.text", "messages.sender"]
)
```

### Response shape (validated)

```json
{
  "messages": [
    {
      "name": "spaces/AAAAse3ABDE/messages/gskWxw7_dKU.SrIuItZbwtI",
      "create_time": "2026-04-28T07:58:17.309839Z",
      "text": "...",
      "sender": {
        "name": "users/116971061710484663070",
        "type": "HUMAN"
      }
    }
  ]
}
```

**Key fields:**

| Field | Format | Notes |
|---|---|---|
| `messages.name` | `spaces/<spaceId>/messages/<threadId>.<replyId>` | For the thread root, it is just `<threadId>` with no dot suffix |
| `messages.create_time` | ISO 8601 UTC | e.g. `2026-04-28T07:58:17.309839Z` |
| `messages.text` | plain string | Raw message text |
| `messages.sender.name` | `users/<numericId>` | Google People resource name — **not** a display name (see Known Limitations) |
| `messages.sender.type` | `HUMAN` \| `BOT` | Sender type |

---

## Constructing a Google Chat link

To link to the **thread** (root message):
```
https://chat.google.com/room/<spaceId>/<threadId>/<threadId>?cls=10
```

To link to a **specific reply**:
```
https://chat.google.com/room/<spaceId>/<threadId>/<replyId>?cls=10
```

Where `<replyId>` is the short ID after the dot in `messages.name`:

```
messages.name = "spaces/AAAAse3ABDE/messages/gskWxw7_dKU.SrIuItZbwtI"
                                              ^^^^^^^^^^^  ^^^^^^^^^^^
                                              <threadId>   <replyId>

→ https://chat.google.com/room/AAAAse3ABDE/gskWxw7_dKU/SrIuItZbwtI?cls=10
```

For a root message (no dot in the message name segment), both thread and message segments are the same:
```
messages.name = "spaces/AAAAse3ABDE/messages/gskWxw7_dKU"

→ https://chat.google.com/room/AAAAse3ABDE/gskWxw7_dKU/gskWxw7_dKU?cls=10
```

---

## Known limitations

- **Sender is an opaque ID**: `messages.sender.name` returns a Google People resource name (`users/<numericId>`), not a human-readable display name. Inform the user when sender attribution matters. Resolving display names requires the People/Directory API, which is out of scope for this skill.
- **Pagination**: Large threads require iterating via `pageToken`. Handle automatically and warn the user if results are partial.
