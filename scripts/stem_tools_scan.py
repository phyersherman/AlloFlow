"""
Deep scan of stem_lab_module.js to find:
1. The full tool grid (all tools available in Explore)
2. Each stemLabTool === 'X' conditional rendering
3. Any bugs, skeleton logic, or missing implementations
"""
import re

FILE = r"c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\stem_lab_module.js"
OUT = r"c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\scripts\stem_tools_detail.txt"

with open(FILE, 'r', encoding='utf-8', errors='replace') as f:
    c = f.read()

out = []

# Find all stemLabTool references
out.append("=== stemLabTool references ===")
for m in re.finditer(r'stemLabTool', c):
    line = c[:m.start()].count('\n') + 1
    ctx = c[max(0,m.start()-20):m.start()+80].replace('\n', ' ')
    out.append(f"  L{line}: {ctx.strip()[:90]}")

out.append("\n=== stemLabTab references ===")
for m in re.finditer(r'stemLabTab', c):
    line = c[:m.start()].count('\n') + 1
    ctx = c[max(0,m.start()-20):m.start()+80].replace('\n', ' ')
    out.append(f"  L{line}: {ctx.strip()[:90]}")

# Find tool definitions inside Explore grid
# Pattern: id: 'toolname', label: 'Label', icon: '...'  
out.append("\n=== Tool definitions (id: '...') ===")
for m in re.finditer(r"id:\s*'(\w+)'", c):
    tool_id = m.group(1)
    line = c[:m.start()].count('\n') + 1
    ctx = c[m.start():m.start()+150].replace('\n', ' ')
    out.append(f"  L{line}: {tool_id} :: {ctx.strip()[:120]}")

# Find all tool view rendering: stemLabTool === 'xxx'
out.append("\n=== Tool view conditionals ===")
for m in re.finditer(r"stemLabTool === '(\w+)'", c):
    tool = m.group(1)
    line = c[:m.start()].count('\n') + 1
    ctx = c[max(0,m.start()-30):m.start()+100].replace('\n', ' ')
    out.append(f"  L{line}: {tool} :: {ctx.strip()[:100]}")

result = '\n'.join(out)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(result)

print(f"Saved to {OUT}")
print(f"Lines: {len(out)}")
