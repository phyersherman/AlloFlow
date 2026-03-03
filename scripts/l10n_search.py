"""Search AlloFlowANTI.txt for localization keys using Python."""
import re

FILE = r"c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt"
with open(FILE, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

print("Total lines: %d" % len(lines))

# Search for the specific raw keys
targets = [
    'advanced_settings', 'art_style_label', 'art_auto',
    'consistent_characters', 'style_placeholder',
    'toggle_consistent'
]

for t in targets:
    for i, line in enumerate(lines):
        if t in line:
            print("L%d: ...%s..." % (i+1, line.strip()[:200]))

# Also find the t() function definition
print("\n=== t() function ===")
for i, line in enumerate(lines):
    if 'const t =' in line or 'function t(' in line:
        if 'UI_STRINGS' in line or 'translate' in line.lower() or 'split' in line:
            print("L%d: %s" % (i+1, line.strip()[:200]))

# Find adventure section in UI_STRINGS
print("\n=== UI_STRINGS adventure section ===")
for i, line in enumerate(lines):
    if 'adventure:' in line and (i < 10000):  # UI_STRINGS is near the top
        print("L%d: %s" % (i+1, line.strip()[:200]))
        # Print next 30 lines
        for j in range(1, 30):
            if i+j < len(lines):
                print("L%d: %s" % (i+1+j, lines[i+j].strip()[:200]))
        break
