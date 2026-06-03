---
name: markitdown
description: |
  Convert documents to clean Markdown before LLM processing using Microsoft MarkItDown.
  Saves tokens, preserves structure, and improves LLM comprehension.

  USE FOR:
  - PDF, DOCX, PPTX, XLSX, HTML, EPub, CSV, JSON, XML files
  - Images with OCR extraction
  - ZIP file contents
  - Any situation where a user attaches or references a document

  Must be pre-installed. Run `markitdown --version` to check.
allowed-tools:
  - Bash(markitdown *)
  - Bash(mdp *)
---

# MarkItDown Document Converter

Convert any document to clean, token-efficient Markdown before analysis. Markdown is LLM-native — it eliminates layout noise (page numbers, headers/footers, fonts) while preserving structure (headings, lists, tables).

## When to use

- User references a file ending in .pdf, .docx, .pptx, .xlsx, .html, .epub, .csv, .json, .xml
- User says "read this document", "analyze this file", "summarize this PDF"
- You need to extract text from an image or scan
- Any situation where raw binary or garbled text would be sent to the model

## Command reference

```bash
# Core tool — convert any file to stdout
markitdown path/to/file.pdf

# Save to file
markitdown file.pdf > output.md

# Batch multiple files
mdp-all file1.pdf file2.docx file3.pptx > combined.md
```

## Workflow

1. **Identify** — when user provides a document path or mentions a file
2. **Convert** — run `markitdown` (or `markitdown` piped to analysis)
3. **Analyze** — pass the clean Markdown to reasoning instead of raw file content
4. **Never** send binary content directly to the model

## Cost savings

Markdown reduces tokens by 30–50% vs raw extraction. No page breaks, encoding artifacts, or layout garbage. LLMs are trained on Markdown — comprehension is native.

## Prerequisites

```bash
pipx install 'markitdown[all]'   # or: pip install --user 'markitdown[all]'
markitdown --version               # verify
```

Also installed: `mdp` at `~/.local/bin/mdp` — standalone wrapper for piping to any tool.
