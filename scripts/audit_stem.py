"""
Full audit of STEM Lab tools - output to file to avoid truncation.
"""
import re, json

FILE = r"c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\stem_lab_module.js"
OUT = r"c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\scripts\stem_audit_results.txt"

with open(FILE, 'r', encoding='utf-8', errors='replace') as f:
    c = f.read()

out = []
out.append(f"=== STEM LAB MODULE: {len(c)} chars, {c.count(chr(10))+1} lines ===\n")

# 1. Find tool grid definitions
out.append("=== TOOL DEFINITIONS (key/label/icon) ===")
for m in re.finditer(r"key:\s*['\"](\w+)['\"]", c):
    key = m.group(1)
    ctx = c[max(0,m.start()-200):m.start()+300]
    label_match = re.search(r"label:\s*['\"]([^'\"]+)['\"]", ctx)
    icon_match = re.search(r"icon:\s*['\"]([^'\"]{1,5})['\"]", ctx)
    desc_match = re.search(r"description:\s*['\"]([^'\"]+)['\"]", ctx)
    label = label_match.group(1) if label_match else "?"
    icon = icon_match.group(1) if icon_match else "?"
    desc = desc_match.group(1) if desc_match else ""
    out.append(f"  {key}: {label} ({icon}) - {desc[:60]}")

# 2. Find activeTool cases
out.append("\n=== TOOL RENDER CASES (activeTool === 'X') ===")
tools_found = set()
for m in re.finditer(r"activeTool\s*===?\s*['\"](\w+)['\"]", c):
    tool = m.group(1)
    line = c[:m.start()].count('\n') + 1
    if tool not in tools_found:
        tools_found.add(tool)
        out.append(f"  L{line}: '{tool}'")

# 3. State variables
out.append("\n=== KEY STATE VARIABLES ===")
state_count = 0
for m in re.finditer(r"const\s+\[(\w+),\s*set\w+\]\s*=\s*(?:React\.)?useState", c):
    name = m.group(1)
    line = c[:m.start()].count('\n') + 1
    val_start = c.find('(', m.end())
    if val_start > 0:
        depth = 0
        val_end = val_start
        for i in range(val_start, min(val_start+200, len(c))):
            if c[i] == '(': depth += 1
            elif c[i] == ')':
                depth -= 1
                if depth == 0:
                    val_end = i
                    break
        default_val = c[val_start+1:val_end][:50]
    else:
        default_val = "?"
    out.append(f"  L{line}: {name} = {default_val}")
    state_count += 1

out.append(f"\n  ({state_count} total state variables)")

# 4. Major functions
out.append("\n=== MAJOR FUNCTIONS ===")
for m in re.finditer(r"const\s+(\w+)\s*=\s*(?:React\.use(?:Callback|Memo)|function|\()", c):
    name = m.group(1)
    if len(name) > 4 and name[0].islower():
        line = c[:m.start()].count('\n') + 1
        # Check if useCallback, useMemo, or plain function
        after = c[m.end():m.end()+30]
        kind = "useCallback" if "useCallback" in c[m.start():m.start()+80] else \
               "useMemo" if "useMemo" in c[m.start():m.start()+80] else "function"
        out.append(f"  L{line}: {name} ({kind})")

# 5. Check for specific manipulative features
out.append("\n=== MANIPULATIVE KEYWORDS ===")
keywords = ['ruler', 'protractor', 'thermometer', 'clock', 'fraction', 'balance', 
            'number line', 'numberLine', 'geometry', 'grid', 'coordinate', 'graph',
            'dice', 'spinner', 'base10', 'base-10', 'counters', 'pattern',
            'measuring', 'angle', 'perimeter', 'area', 'volume', 'weight',
            'timer', 'stopwatch', 'calculator', 'money', 'coins', 'tangram',
            'geoboard', 'cube', 'block', 'tile', 'shape']
for kw in keywords:
    count = len(re.findall(kw, c, re.IGNORECASE))
    if count > 0:
        out.append(f"  {kw}: {count} refs")

result = '\n'.join(out)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(result)

print(f"Audit saved to {OUT}")
print(f"\nTool count: {len(tools_found)}")
print(f"Tools: {', '.join(sorted(tools_found))}")
