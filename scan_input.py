with open(r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\stem_lab_module.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'input' in line.lower() and ('value' in line or 'onChange' in line):
        print(f'{i+1}: {line.strip()[:140]}')
