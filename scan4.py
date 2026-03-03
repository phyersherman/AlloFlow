with open(r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\stem_lab_module.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find ALL instances of input in the stem lab
for i, line in enumerate(lines):
    if '"input"' in line:
        print(f'{i+1}: {line.strip()[:200]}')
print("---")
# Also find textareas  
for i, line in enumerate(lines):
    if '"textarea"' in line:
        print(f'{i+1}: {line.strip()[:200]}')
print("---")
# Find 'checkbox'
for i, line in enumerate(lines):
    if 'checkbox' in line:
        print(f'{i+1}: {line.strip()[:200]}')
