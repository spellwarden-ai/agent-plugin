# Spellwarden scanner for Cursor

Check an agent skill, plugin, marketplace, extension or MCP server before you install it. This plugin gives Cursor's agent a skill that runs the open-source [Spellwarden scanner](https://github.com/spellwarden-ai/spellwarden) (Apache-2.0) on the content first, on your own machine, and tells you what it found so you can decide.

The scanner checks skills, plugins and marketplaces, hooks, MCP client configurations (including Cursor's `mcp.json`), instruction files such as `AGENTS.md`, and A2A agent cards against its published rules, each mapped to the OWASP lists for agents and MCP. It reads files and never runs what it reads. A passed scan means that no rule found a problem; it does not prove the content is safe.

## Install

From the Cursor Marketplace: open **Customize**, search for **Spellwarden** and select **Install**.

Before the listing is live, or to test a change, copy this folder into Cursor's local plugin folder and reload the window (**Developer: Reload Window**):

```
git clone --depth 1 https://github.com/spellwarden-ai/agent-plugin
mkdir -p ~/.cursor/plugins/local
cp -r agent-plugin/plugins/spellwarden-cursor ~/.cursor/plugins/local/spellwarden
```

You also need [uv](https://docs.astral.sh/uv/) or [pipx](https://pipx.pypa.io/) on your machine. The plugin uses whichever is installed to run the scanner.

## Use it

Ask the agent before an install, for example "Check the skill in github.com/example/skills before I install it", "Scan this MCP server entry before you add it to mcp.json" or "Check the agent setup of this machine". The agent reports the result (passed, failed or incomplete), each critical and high finding with its file and line, and a link to each rule's page. When a scan fails or is incomplete, it asks you before it installs anything.

## What it runs, sends and fetches

- **The scanner.** `uvx spellwarden==1.26.0`, or `pipx run --spec spellwarden==1.26.0 spellwarden`. The first run downloads the `spellwarden` package and its dependencies from PyPI (`pypi.org` and `files.pythonhosted.org`). Run on your machine, the scanner sends nothing anywhere: its usage ping runs only in CI.
- **The content you asked to check.** For a repository, the agent runs `git clone --depth 1` of the address you gave into a temporary directory and deletes it afterwards.
- **A probe, only if you agree.** For a remote MCP server, the agent offers `--probe`, which connects to that server's address without credentials to read its tool list and sign-in metadata.
- **Never by default:** `--analyze`, which sends content to a model endpoint you name, and `--upload`, which sends results to a Spellwarden organisation.

The plugin holds one skill and no script, stores no data and has no account.

## Support

Report a problem in [the repository's issues](https://github.com/spellwarden-ai/agent-plugin/issues). Documentation: [spellwarden.ai/docs/agent-plugin](https://spellwarden.ai/docs/agent-plugin?utm_source=github&utm_medium=readme&utm_campaign=agent-plugin-2026-11).

## License

Apache-2.0. See [LICENSE](LICENSE).
