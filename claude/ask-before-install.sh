#!/bin/sh
# Spellwarden plugin hook (PreToolUse). It reads the tool call Claude Code
# passes on stdin and runs nothing from it. When the call installs agent
# content (a plugin, a marketplace, a skill or an MCP server) or edits a
# .mcp.json file, it prints one fixed answer that asks the user to confirm.
# Any other call gets no answer, so Claude Code goes on as usual.
#
# Claude Code's `if` filter runs this hook for every command that holds
# $(...), backticks or $VAR, so the match below is what decides.
input=$(cat)
# The skill's own scan copy lives in a temporary directory named spellwarden-scan-*.
if printf '%s' "$input" | grep -Eq '"file_path": *"[^"]*/spellwarden-scan-[^"/]*/\.mcp\.json"'; then
  exit 0
fi
if printf '%s' "$input" | grep -Eq 'claude +plugins? +(install|i|marketplace +add) |claude +mcp +add(-json)? |npx +(-y +|--yes +)?skills(@[^ ]*)? +add |gemini +extensions +install |"file_path": *"[^"]*\.mcp\.json"'; then
  cat <<'EOF'
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"Spellwarden: this installs agent content (a plugin, marketplace, skill or MCP server). Ask Claude to run /spellwarden:scan-before-install on it first, or approve if it is already checked."}}
EOF
fi
exit 0
