#!/bin/bash
# PreToolUse hook: Run outside the LLM. It blocks actions deterministically.

# Read the file path the AI is trying to modify from standard input
input=$(cat)
path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

# Block edits to the raw evidence directory
if [[ "$path" == *"evidence/"* ]]; then
  echo "❌ Access Denied: 'evidence/' contains your immutable audit trail." >&2
  echo "Editing transcripts silently invalidates the citation index." >&2
  exit 2 # Exit code 2 strictly blocks the tool call
fi

exit 0 # Allow other file edits
