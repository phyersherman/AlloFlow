"""
STEM Lab Cleanup Script
1. Remove duplicate render blocks (L4410-4775) 
2. Remove broken grid entries (L610-616)
3. Remove duplicate 'fractions' grid entry (L614)

Strategy: Work from bottom to top so line numbers don't shift.
"""
import re

FILE = r"c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\stem_lab_module.js"
with open(FILE, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

print(f"Original: {len(lines)} lines, {sum(len(l) for l in lines)} chars")

# === FIX 1: Remove duplicate render blocks (bottom of file) ===
# Find the SECOND occurrence of each duplicated tool
# They start around L4410 and go to end of file (minus closing braces)
# We need to find the exact start of the duplicate block

# Find second solarSystem render (the start of the dup block)
dup_start = None
dup_end = None
solar_count = 0
for i, line in enumerate(lines):
    if "stemLabTool === 'solarSystem'" in line:
        solar_count += 1
        if solar_count == 2:
            # Back up to find the section comment or start
            dup_start = i
            # Check if there's a comment block before
            for j in range(i-1, max(i-5, 0), -1):
                if '═══' in lines[j] or lines[j].strip() == '':
                    dup_start = j
                else:
                    break
            break

if dup_start is None:
    print("ERROR: Could not find second solarSystem render block")
else:
    # Find the end: look for the closing of the IIFE (the last })() before the module closing)
    # The duplicate block goes to end of the render function
    # Find the last probability render block's closing
    prob_count = 0
    for i in range(len(lines)-1, dup_start, -1):
        if "stemLabTool === 'probability'" in lines[i]:
            prob_count += 1
            if prob_count == 1:
                # Find the closing })() after this
                depth = 0
                for j in range(i, len(lines)):
                    for ch in lines[j]:
                        if ch == '(':
                            depth += 1
                        elif ch == ')':
                            depth -= 1
                    if depth <= 0 and j > i + 5:
                        dup_end = j + 1
                        break
                break
    
    if dup_end is None:
        # Fallback: find the closing pattern
        # Look for lines that are part of the module close
        # The duplicates end before the module's closing braces
        # Find the last line with stemLabTool in the dup region
        for i in range(len(lines)-1, dup_start, -1):
            if 'stemLabTool' in lines[i]:
                # Find the })() or }); after this
                for j in range(i, min(i+100, len(lines))):
                    stripped = lines[j].strip()
                    if stripped.startswith('})()') or stripped == '})(),':
                        dup_end = j + 1
                        break
                break
    
    if dup_end:
        removed = lines[dup_start:dup_end]
        print(f"\n=== FIX 1: Removing duplicate render blocks ===")
        print(f"  Removing L{dup_start+1} to L{dup_end} ({dup_end - dup_start} lines)")
        print(f"  First line: {lines[dup_start].strip()[:80]}")
        print(f"  Last line:  {lines[dup_end-1].strip()[:80]}")
        
        # Verify all 7 expected tools are in the removed block
        dup_content = ''.join(removed)
        expected_dups = ['solarSystem', 'waterCycle', 'rockCycle', 'ecosystem', 'fractionViz', 'unitConvert', 'probability']
        for tool in expected_dups:
            if f"stemLabTool === '{tool}'" in dup_content:
                print(f"  ✓ Found duplicate: {tool}")
            else:
                print(f"  ✗ MISSING duplicate: {tool}")
        
        del lines[dup_start:dup_end]
        print(f"  After fix 1: {len(lines)} lines")
    else:
        print("ERROR: Could not find end of duplicate block")

# === FIX 2 & 3: Remove broken grid entries (L610-616 area) ===
# These are the entries without desc/color/ready
# Find them by looking for the pattern of entries with just id/icon/label and no desc
# They come after the 'decomposer' entry

grid_remove_start = None
grid_remove_end = None
for i, line in enumerate(lines):
    if "'decomposer'" in line and "'Decomposer'" in line:
        # The broken entries start on the next line
        grid_remove_start = i + 1
        # Find how many lines the broken entries span
        for j in range(i+1, min(i+20, len(lines))):
            # The broken entries end before the calculus entry (which has desc/color/ready)
            if "'calculus'" in lines[j] and 'ready' in lines[j]:
                grid_remove_end = j
                break
        break

if grid_remove_start and grid_remove_end:
    removed_grid = lines[grid_remove_start:grid_remove_end]
    print(f"\n=== FIX 2 & 3: Removing broken grid entries ===")
    print(f"  Removing L{grid_remove_start+1} to L{grid_remove_end} ({grid_remove_end - grid_remove_start} lines)")
    for line in removed_grid:
        stripped = line.strip()
        if stripped:
            print(f"  - {stripped[:100]}")
    
    del lines[grid_remove_start:grid_remove_end]
    print(f"  After fix 2/3: {len(lines)} lines")
else:
    print(f"WARNING: Could not find broken grid entries (start={grid_remove_start}, end={grid_remove_end})")

# Write the cleaned file
with open(FILE, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"\nFinal: {len(lines)} lines, {sum(len(l) for l in lines)} chars")

# Verify: count remaining stemLabTool conditionals
content = ''.join(lines)
tools_remaining = re.findall(r"stemLabTool === '(\w+)'", content)
from collections import Counter
counts = Counter(tools_remaining)
print(f"\n=== Tool render counts (should all be 1) ===")
for tool, count in sorted(counts.items()):
    flag = "✓" if count == 1 else f"⚠ ({count}x)"
    print(f"  {tool}: {flag}")
