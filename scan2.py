with open(r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\stem_lab_module.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    low = line.lower()
    if ('input' in low or 'textarea' in low) and 'value' in line:
        if 'createelement' in low or 'createElement' in line:
            print(f'{i+1}: {line.strip()[:180]}')
