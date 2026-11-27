"""Checks that the plugin's versions and its scanner pin agree everywhere.

Run: python3 tools/check.py (Python 3.11 or newer, standard library only).
"""
import json
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parent.parent
problems = []

plugin = json.loads((root / "plugins/spellwarden/.claude-plugin/plugin.json").read_text())
guard = json.loads((root / "plugins/spellwarden-guard/.claude-plugin/plugin.json").read_text())
gemini = json.loads((root / "gemini-extension.json").read_text())
market = json.loads((root / ".claude-plugin/marketplace.json").read_text())
skill = (root / "skills/scan-before-install/SKILL.md").read_text()
readme = (root / "README.md").read_text() + (root / "plugins/spellwarden/README.md").read_text()
changelog = (root / "CHANGELOG.md").read_text()

version = plugin["version"]
skill_version = re.search(r"^  version: (\S+)$", skill, re.M)
first_entry = re.search(r"^## (\S+) ", changelog, re.M)
for where, value in [
    ("gemini-extension.json version", gemini["version"]),
    ("spellwarden-guard plugin.json version", guard["version"]),
    ("SKILL.md metadata.version", skill_version and skill_version.group(1)),
    ("CHANGELOG.md first entry", first_entry and first_entry.group(1)),
]:
    if value != version:
        problems.append(f"{where} is {value}, plugin.json says {version}")

if plugin["name"] != gemini["name"] or [(p["name"], p["source"]) for p in market["plugins"]] != [
    (plugin["name"], "./plugins/spellwarden"), (guard["name"], "./plugins/spellwarden-guard")]:
    problems.append("plugin, extension and marketplace names or sources differ")

# The Claude directory takes the skill plugin as plugins/spellwarden. It accepts no hooks,
# scripts or `network` field from an organisation that isn't Verified, so the skill plugin
# holds only Markdown, its manifest, its icon and the license. Gemini CLI reads skills/ at the root.
if (root / "plugins/spellwarden/skills/scan-before-install/SKILL.md").read_text() != skill:
    problems.append("plugins/spellwarden/skills/scan-before-install/SKILL.md differs from skills/scan-before-install/SKILL.md")
allowed = {".claude-plugin/plugin.json", "README.md", "LICENSE", "assets/icon.png", "skills/scan-before-install/SKILL.md"}
present = {str(f.relative_to(root / "plugins/spellwarden")) for f in (root / "plugins/spellwarden").rglob("*") if f.is_file()}
if present != allowed:
    problems.append(f"plugins/spellwarden holds {sorted(present ^ allowed)} beyond or short of the directory's list")
for field in ("hooks", "network", "mcpServers", "commands", "agents", "lspServers", "monitors"):
    if field in plugin:
        problems.append(f"plugins/spellwarden plugin.json has `{field}`, which the directory refuses")

pin = re.search(r"^  scanner: spellwarden==(\d+\.\d+\.\d+)$", skill, re.M)
if not pin:
    problems.append("SKILL.md metadata.scanner is missing")
else:
    scanner = pin.group(1)
    for name, text in [("SKILL.md", skill), ("README.md", readme), ("CHANGELOG.md", changelog)]:
        found = set(re.findall(r"spellwarden==(\d+\.\d+\.\d+)", text))
        if name == "CHANGELOG.md":
            found = set(re.findall(r"spellwarden==(\d+\.\d+\.\d+)", changelog.split("\n## ", 2)[1]))
        if found != {scanner}:
            problems.append(f"{name} pins {sorted(found)}, SKILL.md metadata says {scanner}")
    if f"version {scanner}" not in skill:
        problems.append(f"SKILL.md text does not name version {scanner}")

json.loads((root / "plugins/spellwarden-guard/hooks/hooks.json").read_text())
if (root / "hooks/hooks.json").exists() or (root / ".claude-plugin/plugin.json").exists():
    problems.append("the root must hold no Claude plugin or hooks/hooks.json (Gemini CLI reads hooks/hooks.json)")

for problem in problems:
    print("FAIL", problem)
print("check passed" if not problems else f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
