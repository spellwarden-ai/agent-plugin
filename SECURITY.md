# Security

To report a security problem, write privately to hello@spellwarden.ai. Please do not open a public issue for it.

Say what you found, where, and how to reproduce it. We read every report and answer it.

The plugin holds one script that runs: `claude/ask-before-install.sh`, the Claude Code hook, which prints a fixed answer. The skill and the commands are text files that an agent reads. The scanner itself is reported to the [scanner repository](https://github.com/spellwarden-ai/spellwarden/blob/main/SECURITY.md).
