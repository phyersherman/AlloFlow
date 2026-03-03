"""Targeted color replacements for the Text Adaptation Panel (L22800-23200)"""
import re
FILE = r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt'

with open(FILE, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

count = 0
for i in range(22800, 23300):
    line = lines[i]
    original_line = line
    
    # 1. "(Optional)" labels -> text-slate-400
    if '(Optional)' in line:
        line = re.sub(r'text-(pink|fuchsia|indigo|red|slate)-[0-9]{2,3}', 'text-slate-400', line)
        
    # 2. Student Interests Heart -> text-red-500
    if '<Heart' in line or 'HeartIcon' in line:
        line = re.sub(r'text-(pink|fuchsia|indigo|red)-[0-9]{2,3}', 'text-red-500', line)
        
    # 3. General Checkboxes & Focus Rings: pink-500/600 -> fuchsia-500/600
    # But ONLY if it's not the Student Interests heart we just fixed (which is red-500 now) or Optional (slate-400)
    if 'text-red-500' not in line and 'text-slate-400' not in line:
        line = line.replace('pink-500', 'fuchsia-500')
        line = line.replace('pink-600', 'fuchsia-600')
        line = line.replace('pink-50', 'fuchsia-50')
        line = line.replace('pink-100', 'fuchsia-100')
        line = line.replace('pink-800', 'fuchsia-800')

    # 4. The "Rewrite Text" generate button. 
    # Usually contains: bg-indigo-600 hover:bg-indigo-700
    if 'Rewrite Text' in line or 'bg-indigo-' in line:
        # We only want to change the primary generate button for this tool, not other random indigo things.
        # But this whole section is Text Adaptation, so changing its primary buttons to Fuchsia is correct.
        # Let's target the Rewrite Text button specifically if it spans multiple lines.
        # We'll just replace indigo with fuchsia if the line looks like a button
        if 'hover:bg-indigo-' in line or 'bg-indigo-' in line:
            line = line.replace('indigo-50', 'fuchsia-50')
            line = line.replace('indigo-100', 'fuchsia-100')
            line = line.replace('indigo-300', 'fuchsia-300')
            line = line.replace('indigo-500', 'fuchsia-500')
            line = line.replace('indigo-600', 'fuchsia-600')
            line = line.replace('indigo-700', 'fuchsia-700')
        
    if line != original_line:
        lines[i] = line
        count += 1

with open(FILE, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"\nTotal lines modified: {count}")
print("File saved!")
