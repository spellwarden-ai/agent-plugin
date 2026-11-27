#!/bin/sh
# Checks plugins/spellwarden-install-guard/hooks/ask-before-install.sh against tool calls that must and must not ask.
hook="$(dirname "$0")/../plugins/spellwarden-install-guard/hooks/ask-before-install.sh"
fail=0
check() { # expected (ask|none), stdin JSON
  out=$(printf '%s' "$2" | sh "$hook")
  case "$out" in *'"permissionDecision":"ask"'*) got=ask ;; '') got=none ;; *) got=bad ;; esac
  if [ "$got" != "$1" ]; then echo "FAIL want $1 got $got: $2"; fail=1; fi
}
b() { printf '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"%s"}}' "$1"; }
f() { printf '{"hook_event_name":"PreToolUse","tool_name":"%s","tool_input":{"file_path": "%s","content":"x"}}' "$1" "$2"; }
check ask "$(b 'claude plugin install spellwarden@spellwarden')"
check ask "$(b 'claude plugin marketplace add spellwarden-ai/agent-plugin')"
check ask "$(b 'claude mcp add --transport http x https://example.com/mcp')"
check ask "$(b 'claude mcp add-json x {}')"
check ask "$(b 'D=$(mktemp -d) && npx -y skills add owner/repo')"
check ask "$(b 'npx skills@1.2.0 add owner/repo')"
check ask "$(b 'gemini extensions install https://github.com/x/y')"
check ask "$(f Write /home/u/project/.mcp.json)"
check ask "$(f Edit .mcp.json)"
check none "$(b 'which uvx pipx; echo; D=$(mktemp -d /tmp/sw-scan.XXXXXX); echo $D')"
check none "$(b 'git clone --depth 1 https://github.com/anthropics/skills \"$D/repo\"')"
check none "$(b 'uvx spellwarden==1.25.0 scan \"$D\"')"
check none "$(b 'cat \".mcp.json\"')"
check none "$(b 'claude plugin list')"
check none "$(f Write /home/u/project/notes.md)"
check none "$(f Write /tmp/spellwarden-scan-a1B2c3/.mcp.json)"
check ask "$(f Write /tmp/spellwarden-scan-a1B2c3/sub/.mcp.json)"
check ask "$(f Write /home/u/spellwarden-scan-x/../project/.mcp.json)"
[ "$fail" = 0 ] && echo "hook tests passed"
exit "$fail"
