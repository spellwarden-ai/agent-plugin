# Spellwarden install guard for Claude Code

An optional companion to the `spellwarden` plugin. When Claude itself is about to run `claude plugin install`, `claude plugin marketplace add`, `claude mcp add`, `claude mcp add-json`, `npx skills add` or `gemini extensions install`, or to edit or write a `.mcp.json` file, a `PreToolUse` hook asks you to confirm and suggests a Spellwarden scan first.

```
/plugin marketplace add spellwarden-ai/agent-plugin
/plugin install spellwarden-guard@spellwarden
```

The hook is a shell script (`hooks/ask-before-install.sh`, run with `sh`). It reads the tool call Claude Code passes it, runs nothing from it, sends nothing, and prints one fixed answer when the call is one of these. It stays quiet for the `spellwarden` skill's own scan copy, a `.mcp.json` inside a temporary directory named `spellwarden-scan-*`. Installs you type yourself, such as `/plugin install`, are not tool calls, so the hook does not see them. To turn the hook off, disable this plugin.

Apache-2.0. See [LICENSE](LICENSE). Report a problem in [the repository's issues](https://github.com/spellwarden-ai/agent-plugin/issues).
