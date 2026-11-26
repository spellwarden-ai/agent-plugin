# Spellwarden scanner for Claude Code and Gemini CLI

Check an agent skill, plugin, marketplace, extension or MCP server before you install it. This plugin teaches your agent to run the open-source [Spellwarden scanner](https://github.com/spellwarden-ai/spellwarden) (Apache-2.0) on the content first, on your own machine, and to tell you what it found so you can decide.

The scanner checks skills, Claude Code plugins and marketplaces, hooks, MCP client configurations, instruction files such as `AGENTS.md`, `CLAUDE.md` and `GEMINI.md`, and A2A agent cards against its published rules, each mapped to the OWASP lists for agents and MCP. It reads files and never runs what it reads. A passed scan means that no rule found a problem; it does not prove the content is safe.

The same repository is a Claude Code plugin and a Gemini CLI extension.

## Install

**Claude Code**

```
/plugin marketplace add spellwarden-ai/agent-plugin
/plugin install spellwarden@spellwarden
```

**Gemini CLI**

```
gemini extensions install https://github.com/spellwarden-ai/agent-plugin
```

You also need [uv](https://docs.astral.sh/uv/) or [pipx](https://pipx.pypa.io/) on your machine. The plugin uses whichever is installed to run the scanner.

## Use it

Ask your agent before an install, for example:

- "Check the skill in github.com/example/skills before I install it."
- "Scan this MCP server entry before you add it to .mcp.json."
- "Check the agent setup of this machine."

Or run the commands directly:

| Agent | Command | What it does |
|---|---|---|
| Claude Code | `/spellwarden:scan-before-install <target>` | Scans a repository, a folder or an MCP server entry |
| Gemini CLI | `/spellwarden:scan <target>` | The same |
| Gemini CLI | `/spellwarden:workstation` | Scans this machine's agent setup (`scan --user`) |

The agent reports the result (passed, failed or incomplete), each critical and high finding with its file and line, and a link to each rule's page, which explains how to fix it. When a scan fails or is incomplete, the agent asks you before it installs anything.

## What it runs, sends and fetches

- **The scanner.** `uvx spellwarden==1.24.0`, or `pipx run --spec spellwarden==1.24.0 spellwarden`. The first run downloads the `spellwarden` package and its dependencies (PyPI, `pypi.org` and `files.pythonhosted.org`). Run on your machine, the scanner sends nothing anywhere: its usage ping runs only in CI.
- **The content you asked to check.** For a repository, the agent runs `git clone --depth 1` of the address you gave into a temporary directory and deletes it afterwards.
- **A probe, only if you agree.** For a remote MCP server, the agent offers `--probe`, which connects to that server's address without credentials to read its tool list and sign-in metadata.
- **Never by default:** `--analyze`, which sends content to a model endpoint you name, and `--upload`, which sends results to a Spellwarden organisation. The agent uses them only when you ask for them by name.

**Claude Code only: a confirmation hook.** When Claude itself is about to run `claude plugin install`, `claude plugin marketplace add`, `claude mcp add`, `claude mcp add-json`, `npx skills add` or `gemini extensions install`, or to edit or write a `.mcp.json` file, a `PreToolUse` hook asks you to confirm and suggests a scan first. The hook is a shell script that prints one fixed answer; it reads nothing and runs nothing else. Installs you type yourself, such as `/plugin install`, are not tool calls, so the hook does not see them. To turn the hook off, disable the plugin.

This plugin stores no data and has no account. The hosted Spellwarden product is separate and is not needed here.

## Support

Report a problem in [this repository's issues](https://github.com/spellwarden-ai/agent-plugin/issues). Report a security issue as [SECURITY.md](SECURITY.md) describes. Documentation: [spellwarden.ai/docs/agent-plugin](https://spellwarden.ai/docs/agent-plugin?utm_source=github&utm_medium=readme&utm_campaign=agent-plugin-2026-11).

## License

Apache-2.0. See [LICENSE](LICENSE).
