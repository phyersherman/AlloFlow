"""
Add window.__ALLO_* exposures after the audio Proxy definitions.
Finds the last Proxy definition line and inserts all three exposures.
"""
import re

FILE = r"c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt"
with open(FILE, 'r', encoding='utf-8') as f:
    c = f.read()

print(f"File: {len(c)} chars")

# Find all Proxy definitions for audio constants
proxy_positions = {}
for name in ['PHONEME_AUDIO_BANK', 'INSTRUCTION_AUDIO', 'ISOLATION_AUDIO']:
    # Find the Proxy definition: NAME = new Proxy(
    pattern = name + r'\s*=\s*new\s+Proxy\('
    m = re.search(pattern, c)
    if m:
        line = c[:m.start()].count('\n') + 1
        print(f"  Found {name} Proxy at L{line}")
        proxy_positions[name] = m.start()
    else:
        print(f"  WARNING: {name} Proxy NOT found!")

if not proxy_positions:
    print("ERROR: No Proxy definitions found!")
    exit(1)

# Find the LAST Proxy definition to insert window exposures after
# We need to find the END of the last Proxy definition
last_name = max(proxy_positions, key=proxy_positions.get)
last_pos = proxy_positions[last_name]
last_line = c[:last_pos].count('\n') + 1
print(f"\nLast Proxy: {last_name} at L{last_line}")

# Find the closing of this Proxy: look for the matching }); pattern
# Walk forward from the Proxy start, tracking depth
depth = 0
in_string = False
string_char = None
i = last_pos
found_end = -1

# Skip to the first ( after "new Proxy"
proxy_start = c.find('(', last_pos + len(last_name))
if proxy_start < 0:
    print("ERROR: Can't find Proxy opening paren")
    exit(1)

depth = 0
i = proxy_start
while i < len(c):
    ch = c[i]
    if in_string:
        if ch == '\\' and i + 1 < len(c):
            i += 2
            continue
        if ch == string_char:
            in_string = False
    else:
        if ch in ('"', "'", '`'):
            in_string = True
            string_char = ch
        elif ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                found_end = i + 1
                break
    i += 1

if found_end < 0:
    print("ERROR: Can't find end of last Proxy")
    exit(1)

# Find the end of the statement (next ; after the closing ))
stmt_end = c.find(';', found_end)
if stmt_end < 0:
    stmt_end = found_end

end_line = c[:stmt_end].count('\n') + 1
print(f"Last Proxy ends at L{end_line}")

# Insert the window exposures AFTER the last Proxy definition
EXPOSURE = """
// Expose audio Proxy objects on window for CDN modules
window.__ALLO_INSTRUCTION_AUDIO = INSTRUCTION_AUDIO;
window.__ALLO_ISOLATION_AUDIO = ISOLATION_AUDIO;
window.__ALLO_PHONEME_AUDIO_BANK = PHONEME_AUDIO_BANK;
"""

# Insert after the semicolon
insert_at = stmt_end + 1
c = c[:insert_at] + EXPOSURE + c[insert_at:]

# Verify the exposures are now present
for name in ['__ALLO_PHONEME_AUDIO_BANK', '__ALLO_INSTRUCTION_AUDIO', '__ALLO_ISOLATION_AUDIO']:
    count = c.count('window.' + name)
    print(f"  window.{name}: {count} refs")

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print(f"\n✅ Window exposures added after L{end_line}")
print(f"New file size: {len(c)} chars")
