"""
Comprehensive localization fix script.
1. Find all raw key-path values in ui_strings.js
2. Find all t('adventure.xxx') calls in AlloFlowANTI.txt
3. Add missing keys to ui_strings.js
"""
import re, json

# === 1. Find all raw key-path values in ui_strings.js ===
with open('ui_strings.js', 'r', encoding='utf-8', errors='replace') as f:
    ui_content = f.read()

print("=== Raw key-path VALUES in ui_strings.js ===")
# Find patterns like "key": "some.dotted.path"
raw_values = re.findall(r'"(\w+)":\s*"(\w+\.\w+)"', ui_content)
for key, val in raw_values:
    print("  %s: \"%s\"" % (key, val))

# === 2. Find all t('adventure.xxx') calls in AlloFlowANTI.txt ===
with open('AlloFlowANTI.txt', 'r', encoding='utf-8', errors='replace') as f:
    app_content = f.read()

print("\n=== t('adventure.xxx') calls in AlloFlowANTI.txt ===")
adv_calls = set(re.findall(r"t\(['\"]adventure\.(\w+)['\"]\)", app_content))
for k in sorted(adv_calls):
    print("  adventure.%s" % k)

print("\n=== t('glossary.xxx') calls in AlloFlowANTI.txt ===")
glos_calls = set(re.findall(r"t\(['\"]glossary\.(\w+)['\"]\)", app_content))
for k in sorted(glos_calls):
    print("  glossary.%s" % k)

print("\n=== t('common.xxx') calls not in UI_STRINGS common section ===")
common_calls = set(re.findall(r"t\(['\"]common\.(\w+)['\"]\)", app_content))
# Check which are in ui_strings
for k in sorted(common_calls):
    if '"' + k + '"' not in ui_content:
        print("  MISSING common.%s" % k)

# === 3. Find the t() function ===
print("\n=== Main t() function candidates ===")
lines = app_content.split('\n')
for i, line in enumerate(lines):
    if 'const t' in line and ('split' in line or 'UI_STRINGS' in line or 'reduce' in line):
        print("  L%d: %s" % (i+1, line.strip()[:300]))
    if 'function t(' in line and ('split' in line or 'key' in line):
        print("  L%d: %s" % (i+1, line.strip()[:300]))

# Also search for the actual translation function
for i, line in enumerate(lines):
    s = line.strip()
    if s.startswith('const t =') and len(s) > 30:
        print("  L%d: %s" % (i+1, s[:300]))
