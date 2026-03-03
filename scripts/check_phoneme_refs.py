"""
Check all PHONEME_AUDIO_BANK replacements in the CDN module
to verify no syntax issues from the regex replacement.
"""
import re

FILE = r"c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\word_sounds_module.js"
with open(FILE, 'r', encoding='utf-8', errors='replace') as f:
    c = f.read()

# Find ALL references to __ALLO_PHONEME_AUDIO_BANK and show context
print("=== ALL PHONEME_AUDIO_BANK REFERENCES ===")
for m in re.finditer(r'__ALLO_PHONEME_AUDIO_BANK', c):
    start = max(0, m.start() - 60)
    end = min(len(c), m.end() + 80)
    ctx = c[start:end].replace('\n', ' ')
    line = c[:m.start()].count('\n') + 1
    print(f"\nL{line}: ...{ctx}...")

# Also check: is there any phoneme validation code?
print("\n\n=== PHONEME VALIDATION/SEGMENTATION ===")
for m in re.finditer(r'(estimatePhoneme|splitPhoneme|phonemeMap|phonemeSequence|getPhonemes)', c, re.IGNORECASE):
    ctx = c[max(0,m.start()-20):m.start()+100]
    line = c[:m.start()].count('\n') + 1
    print(f"L{line}: {ctx.strip()[:90]}")

# Check for 'in window.__ALLO_PHONEME_AUDIO_BANK' patterns (need to verify syntax)
print("\n\n=== 'in' OPERATOR PATTERNS ===")
for m in re.finditer(r"in\s+window\.__ALLO_PHONEME_AUDIO_BANK", c):
    ctx = c[max(0,m.start()-30):m.start()+60]
    line = c[:m.start()].count('\n') + 1
    print(f"L{line}: {ctx.strip()[:90]}")

# Check for typeof patterns
print("\n\n=== typeof PATTERNS ===")
for m in re.finditer(r"typeof\s+window\.__ALLO", c):
    ctx = c[max(0,m.start()-10):m.start()+60]
    line = c[:m.start()].count('\n') + 1
    print(f"L{line}: {ctx.strip()[:80]}")

# Check for any potential issues: PHONEME_AUDIO_BANK?. followed by problematic patterns
print("\n\n=== POTENTIAL SYNTAX ISSUES ===")
for m in re.finditer(r'__ALLO_PHONEME_AUDIO_BANK\?\.\[', c):
    ctx = c[m.start()-30:m.end()+40]
    line = c[:m.start()].count('\n') + 1
    print(f"L{line}: {ctx.strip()[:80]}")
