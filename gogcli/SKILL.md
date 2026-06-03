---
name: gogcli
description: "Use gogcli to read and edit Google Drive, Docs, Sheets, Slides, Gmail, Calendar, and more from the terminal. Supports multiple Google accounts via OAuth. Trigger when the user mentions Google Drive, Docs, Sheets, Gmail, Calendar, or Google Workspace from the terminal."
---

# gogcli — Google Workspace CLI

[gogcli](https://github.com/steipete/gogcli) is a comprehensive CLI for Google Workspace. It supports reading, editing, creating, deleting, and managing files across Drive, Docs, Sheets, Slides, Gmail, Calendar, Contacts, and more.

## Official Docs

- Quickstart: https://gogcli.sh/quickstart.html
- Full command reference: run `gog schema --json` or visit https://gogcli.sh
- Agent safety profiles: https://gogcli.sh/safety.html

## Install

```bash
brew install gogcli
# or: go install github.com/steipete/gogcli/cmd/gog@latest
```

## One-Time Setup

1. Create a Google Cloud project → enable APIs (Drive, Docs, Sheets, Gmail, Calendar, etc.)
2. Configure [OAuth consent screen](https://console.cloud.google.com/auth/branding) → add test users
3. Create [Desktop OAuth client](https://console.cloud.google.com/apis/credentials) → download JSON
4. Store credentials: `gog auth credentials /path/to/client_secret_*.json`
5. On Linux/WSL (D-Bus unavailable): `gog auth keyring file`
6. Set keyring password: `export GOG_KEYRING_PASSWORD='your-password'` → add to `~/.zshrc`
7. Authorize accounts: `gog auth add <email> --services drive,sheets,docs,gmail,calendar`

## Multi-Account Setup

Same OAuth client authorizes any number of Google accounts. Switch between them:

```bash
gog auth add personal@gmail.com --services drive,sheets,docs
gog auth add work@company.com  --services drive,sheets,docs,gmail,calendar
gog drive ls --account personal@gmail.com
gog drive ls --account work@company.com
export GOG_ACCOUNT=personal@gmail.com  # default; omit --account
```

## Google Drive (Read + Write)

```bash
# Read
gog drive ls --account <email> --max 20
gog drive search "query" --account <email>
gog drive download <fileId> --out ./path

# Write
gog drive upload ./file.pdf --account <email>
gog drive mkdir "New Folder" --parent <folderId>
gog drive copy <fileId> "Copy Name"
gog drive rename <fileId> "New Name"
gog drive delete <fileId>              # move to trash
gog drive delete <fileId> --permanent   # delete forever
gog drive share <fileId> --email friend@gmail.com --role writer
gog drive move <fileId> --parent <newFolderId>
```

## Google Docs (Read + Write)

```bash
# Read
gog docs export <docId> --format md --out ./doc.md
gog docs cat <docId>
gog docs info <docId>

# Create & write
gog docs create "My New Doc"
gog docs write <docId> --text "Hello world"
gog docs insert <docId> "inserted text" --index 10
gog docs edit <docId> "old text" "new text"          # find/replace
gog docs sed <docId> 's/pattern/replacement/g'       # regex replace
gog docs delete --start 0 --end 100 <docId>
gog docs clear <docId>                                # wipe entire doc
gog docs insert-table <docId> --rows 3 --cols 4
gog docs insert-page-break <docId> --at-end
gog docs format <docId> --bold --start 0 --end 50
gog docs copy <docId> "Duplicate Title"
```

## Google Sheets (Read + Write)

```bash
# Read
gog sheets get <spreadsheetId> 'Sheet1!A1:D20' --json

# Create & write
gog sheets create "My Spreadsheet"
gog sheets update <id> 'Sheet1!A1:B2' "A" "B" "C" "D"
gog sheets append <id> 'Sheet1!A:A' "new row value"
gog sheets batch-update --data-json '{"A1":"hello","B1":"world"}' <id>
gog sheets clear <id> 'Sheet1!A1:D10'
gog sheets add-tab <id> "New Tab"
gog sheets rename-tab <id> "Old Name" "New Name"
gog sheets delete-tab <id> "Tab Name" --force
gog sheets copy <id> "Duplicate Sheet"
```

## Gmail

```bash
# Read
gog gmail search 'newer_than:7d subject:meeting'
gog gmail get <messageId> --sanitize-content --json

gog gmail send --to recipient@gmail.com --subject "Hello" --body "Message body"
gog gmail forward <messageId> --to recipient@gmail.com
gog gmail archive <messageId>
gog gmail trash <messageId>
gog gmail mark-read <messageId>
gog gmail unread <messageId>
gog gmail labels create "My Label"
```

## Calendar

```bash
gog calendar events --today
gog calendar create --summary "Review" --from "2026-06-01T10:00:00+07:00" --to "2026-06-01T11:00:00+07:00"
```

## Safety & Agent Guardrails

For AI agents, consider locking gogcli to prevent destructive actions:

```bash
# Block Gmail sends
gog --gmail-no-send <command>

# Only allow specific commands
gog --enable-commands "drive.ls,drive.search,drive.download,docs.export,sheets.get" <command>

# Disable destructive commands
gog --disable-commands "drive.delete,gmail.send,admin" <command>
```

## Keyring (Critical)

- **macOS**: D-Bus SecretService not needed — uses Keychain automatically
- **Linux/WSL**: Must use file keyring: `gog auth keyring file`
- **GOG_KEYRING_PASSWORD** must be exported before every session or added to shell profile
- **Never change the password** after accounts are stored — it corrupts the keyring (`integrity check failed`)
- If corrupted: re-set the correct password, then re-auth with `gog auth add <email> --force-consent`

## Verification

```bash
gog auth list --check          # verify all accounts valid
gog auth doctor --check        # diagnose issues
gog --version                  # should show 0.20.0+
```

## Tips & Tricks

### `--json` for scripting (all commands)

```bash
# Stable JSON envelope — pipes clean into scripts/LLMs
gog drive ls --json --max 5
gog sheets get <id> 'Sheet1!A1:D20' --json
```

### `--results-only` + `--select` for clean LLM output

```bash
# Drop envelope, get only results
gog drive ls --json --results-only --max 3

# Pick specific fields
gog drive ls --json --select "id,name,mimeType" --max 10
gog sheets get <id> 'Sheet1!A1:C5' --json --results-only
```

### `--plain` for TSV (pipe to awk)

```bash
gog drive ls --plain | awk '$2 == "folder" {print $1}'  # list folder IDs
```

### Gmail: `--sanitize-content` strips HTML/URLs for agents

```bash
gog gmail get <messageId> --sanitize-content --json
```

### Offline URL generation

```bash
# No API call needed — works offline
gog open <driveFileId>           # → https://drive.google.com/open?id=...
gog open <docId> --type docs     # → https://docs.google.com/...
gog open <threadId> --type gmail-thread
```

### Drive tree view

```bash
gog drive tree --parent <folderId> --depth 3 --account <email>
gog drive du --parent <folderId> --json       # disk usage per folder
gog drive inventory --account <email> > backup.csv
```

### Audit sharing permissions

```bash
# Find publicly shared files
gog drive audit sharing --account <email>
# Find all files shared with a specific person
gog drive audit user friend@gmail.com
```

### `--dry-run` before mutating

```bash
gog drive delete <id> --dry-run              # preview what would happen
gog drive share <id> --email x@y.com --dry-run
gog docs clear <id> --dry-run                # "Would delete 1,234 chars"
```

### `--no-input` for CI/scripts

```bash
gog drive delete <id> --no-input -y          # fail instead of prompt
gog docs write <id> --text "hi" --no-input   # never interact
```

### Quick access (short aliases)

```bash
gog ls                               # = gog drive ls
gog search "query"                   # = gog drive search
gog dl <id>                          # = gog drive download
gog up ./file.pdf                    # = gog drive upload
gog cat <docId>                      # = gog docs cat
gog me                               # = gog people me (profile)
```
