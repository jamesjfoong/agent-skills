# Agent Skills

Central repository for AI agent skills shared across all agents.

## Supported Agents

| Agent | Load Method |
|-------|-------------|
| **Hermes** | `hermes skills install URL` or symlink to `~/.hermes/skills/` |
| **Claude Code** | Skills auto-load from `~/.claude/skills/` (symlinked) |
| **Codex** | Skills auto-load from `~/.codex/skills/` |
| **Custom `.agent`** | Skills auto-load from `~/.agent/skills/` (symlinked) |

## Install a Skill

```bash
# Hermes: install directly from GitHub
hermes skills install https://github.com/jamesjfoong/agent-skills/blob/master/markitdown/SKILL.md --name markitdown

# Or: clone and symlink
gh repo clone jamesjfoong/agent-skills ~/.agents/skills
cd ~/.claude/skills && ln -s ~/.agents/skills/markitdown .
cd ~/.agent/skills && ln -s ~/.agents/skills/markitdown .
```

## Adding a New Skill

1. Create a new folder: `mkdir my-skill/`
2. Add `SKILL.md` with agent-agnostic instructions
3. Add optional: `rules/`, `references/`, `scripts/`, `templates/`
4. Commit: `git add . && git commit -m "feat: add my-skill" && git push`

## Existing Skills

| Skill | Description |
|-------|-------------|
| `markitdown` | Convert documents to Markdown before LLM processing |
| `firecrawl` | Web scraping and browser automation |
| `paseo` | Multi-agent orchestration |
| `gogcli` | Google Workspace CLI tools |
| `canvas-design` | Design system and typography |
| `pdf` | PDF manipulation and form filling |
| `imagegen` | AI image generation |
| `video` | AI video prompting |
| `youtube-transcript` | YouTube transcript extraction |
