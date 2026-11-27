# Changelog

## 1.4.0 (2026-11-27)

- Runs the scanner `spellwarden==1.26.0` (68 rules, the same as 1.25.0), up from 1.25.0. The scan's findings are unchanged; 1.26.0 adds links to the rule pages in its Markdown report, which the skill does not use. The repository's own CI scan uses the Spellwarden action v1.26.0.

## 1.3.0 (2026-11-27)

- Cursor: a Cursor plugin, `spellwarden` (`plugins/spellwarden-cursor`, listed in `.cursor-plugin/marketplace.json`), with the same `scan-before-install` skill. Still runs the scanner `spellwarden==1.25.0`.

## 1.2.0 (2026-11-27)

- Runs the scanner `spellwarden==1.25.0` (68 rules), up from 1.24.0. The repository's own CI scan uses the Spellwarden action v1.25.0.

## 1.1.1 (2026-11-27)

- The optional hook plugin is renamed `spellwarden-install-guard` (`plugins/spellwarden-install-guard`), so it isn't confused with the policy hook `spellwarden_guard.py` from the Spellwarden docs. Install `spellwarden-install-guard@spellwarden`. Still runs the scanner `spellwarden==1.24.0`.

## 1.1.0 (2026-11-27)

- Claude Code: the marketplace now holds two plugins. `spellwarden` (`plugins/spellwarden`) is the scanner skill alone, the version submitted to the Claude plugin directory, which accepts no hooks from organisations it hasn't verified. The confirmation hook moves to the optional `spellwarden-guard` plugin (`plugins/spellwarden-guard`), and its command now names its interpreter (`sh`). Install `spellwarden-guard@spellwarden` to keep the hook. Still runs the scanner `spellwarden==1.24.0`.
- Gemini CLI: no change beyond the version.

## 1.0.1 (2026-11-27)

- The skill makes its temporary directory with the name prefix `spellwarden-scan-`, and the Claude Code hook no longer asks when the skill writes its scan copy of an MCP server entry (`.mcp.json`) there. Still runs the scanner `spellwarden==1.24.0`.
- The README says what the hook reads: the tool call, from which it runs nothing.

## 1.0.0 (2026-11-26)

- First release: the `scan-before-install` skill for Claude Code and Gemini CLI, the Gemini CLI commands `/spellwarden:scan` and `/spellwarden:workstation`, and the Claude Code confirmation hook for installs Claude starts. Runs the scanner `spellwarden==1.24.0`.
