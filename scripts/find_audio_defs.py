"""
Add window.__ALLO_* exposures for PHONEME_AUDIO_BANK, INSTRUCTION_AUDIO,
and ISOLATION_AUDIO in AlloFlowANTI.txt.

These need to be set AFTER the Proxy definitions so the CDN module can
access them at runtime.
"""
import re

FILE = r"c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt"
with open(FILE, 'r', encoding='utf-8') as f:
    c = f.read()

print(f"File size: {len(c)} chars")

# Find the last definition of each audio constant 
# The Proxy pattern is: const NAME = new Proxy({}, { get: ... })
# OR could be defined with createAudioProxy() etc

for name in ['PHONEME_AUDIO_BANK', 'INSTRUCTION_AUDIO', 'ISOLATION_AUDIO']:
    # Find ALL occurrences to understand the pattern
    refs = list(re.finditer(r'\b' + name + r'\b', c))
    print(f"\n{name}: {len(refs)} refs")
    for ref in refs[:3]:
        line = c[:ref.start()].count('\n') + 1
        before = c[max(0,ref.start()-40):ref.start()].replace('\n', '|')
        after = c[ref.end():ref.end()+60].replace('\n', '|')
        print(f"  L{line}: ...{before.strip()[-30:]}{name}{after.strip()[:40]}...")

# Also check what's around audio_bank_loaded
print("\n\n=== audio_bank_loaded context ===")
for m in re.finditer(r'audio_bank_loaded', c):
    line = c[:m.start()].count('\n') + 1
    ctx = c[max(0,m.start()-60):m.start()+120].replace('\n', ' | ')
    print(f"L{line}: {ctx.strip()[:150]}")

# Check: is there a spot where window.__ALLO_ is assigned to anything?
print("\n\n=== Existing window.__ALLO_ assignments ===")
for m in re.finditer(r'window\.__ALLO_\w+\s*=', c):
    line = c[:m.start()].count('\n') + 1
    ctx = c[m.start():m.start()+80].replace('\n', ' ')
    print(f"L{line}: {ctx.strip()[:70]}")

print("\n\n=== Looking for Proxy pattern ===")
for m in re.finditer(r'Proxy\s*\(\s*\{', c):
    line = c[:m.start()].count('\n') + 1
    before = c[max(0,m.start()-60):m.start()].replace('\n', ' ')
    print(f"L{line}: ...{before.strip()[-50:]}Proxy({{...")
