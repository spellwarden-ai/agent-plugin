"""Checks that the plugin's versions and its scanner pin agree everywhere.

Run: python3 tools/check.py (Python 3.11 or newer, standard library only).
"""
import json
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parent.parent
problems = []

plugin = json.loads((root / ".claude-plugin/plugin.json").read_text())
gemini = json.loads((root / "gemini-extension.json").read_text())
market = json.loads((root / ".claude-plugin/marketplace.json").read_text())
skill = (root / "skills/scan-before-install/SKILL.md").read_text()
readme = (root / "README.md").read_text()
changelog = (root / "CHANGELOG.md").read_text()

version = plugin["version"]
skill_version = re.search(r"^  version: (\S+)$", skill, re.M)
first_entry = re.search(r"^## (\S+) ", changelog, re.M)
for where, value in [
    ("gemini-extension.json version", gemini["version"]),
    ("SKILL.md metadata.version", skill_version and skill_version.group(1)),
    ("CHANGELOG.md first entry", first_entry and first_entry.group(1)),
]:
    if value != version:
        problems.append(f"{where} is {value}, plugin.json says {version}")

if plugin["name"] != gemini["name"] or [p["name"] for p in market["plugins"]] != [plugin["name"]]:
    problems.append("plugin, extension and marketplace names differ")

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

hooks = (root / "claude/hooks.json").read_text()
if plugin.get("hooks") != "./claude/hooks.json" or (root / "hooks/hooks.json").exists():
    problems.append("Claude hooks must live only in claude/hooks.json (Gemini CLI reads hooks/hooks.json)")
json.loads(hooks)

for problem in problems:
    print("FAIL", problem)
print("check passed" if not problems else f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
