"""Targeted manual color substitutions for Text Adaptation Panel"""
FILE = r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt'

with open(FILE, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

count = 0

for i in range(22800, 23300):
    line = lines[i]
    original = line
    
    # 1. "(Optional)" -> text-slate-400
    if '(Optional)' in line:
        line = line.replace('text-pink-600', 'text-slate-400')
        line = line.replace('text-pink-500', 'text-slate-400')
        line = line.replace('text-indigo-600', 'text-slate-400')
        line = line.replace('text-indigo-500', 'text-slate-400')
        
    # 2. Student Interests Heart -> text-red-500
    if '<Heart' in line and (i < len(lines)-2 and 'Student Interests' in lines[i+1] or 'Student Interests' in lines[i]):
        line = line.replace('text-pink-500', 'text-red-500')
        line = line.replace('text-pink-600', 'text-red-500')
        line = line.replace('text-indigo-500', 'text-red-500')
        line = line.replace('text-fuchsia-500', 'text-red-500')
    if 'Student Interests' in line and '<Heart' in line:
        line = line.replace('text-pink-500', 'text-red-500')
        line = line.replace('text-pink-600', 'text-red-500')
        
    # 3. Everything else that is pink -> fuchsia (except if it has text-slate-400 or text-red-500)
    if 'text-red-500' not in line and 'text-slate-400' not in line:
        line = line.replace('pink-500', 'fuchsia-500')
        line = line.replace('pink-600', 'fuchsia-600')
        line = line.replace('pink-50', 'fuchsia-50')
        line = line.replace('pink-100', 'fuchsia-100')
        line = line.replace('pink-800', 'fuchsia-800')

    # 4. Buttons with 'bg-indigo-600 hover:bg-indigo-700' 
    # Let's target lines with bg-indigo-600 near Rewrite Text
    if 'className="bg-indigo-600 hover:bg-indigo-700' in line:
        line = line.replace('bg-indigo-600', 'bg-fuchsia-600')
        line = line.replace('hover:bg-indigo-700', 'hover:bg-fuchsia-700')
        
    if 'className="bg-indigo-50 text-indigo-700' in line:
        line = line.replace('bg-indigo-50', 'bg-fuchsia-50')
        line = line.replace('text-indigo-700', 'text-fuchsia-700')
        line = line.replace('border-indigo-200', 'border-fuchsia-200')
        line = line.replace('hover:bg-indigo-100', 'hover:bg-fuchsia-100')
        
    if line != original:
        lines[i] = line
        count += 1
        print(f"L{i}: Modified")

with open(FILE, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Total lines modified: {count}")
