with open(r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\stem_lab_module.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    # Find any createElement with "input" and value prop
    if '"input"' in line and 'value' in line:
        print(f'{i+1}: {line.strip()[:180]}')
    # Also find inputs via JSX-like patterns
    if "'input'" in line and 'value' in line:
        print(f'{i+1}: {line.strip()[:180]}')
