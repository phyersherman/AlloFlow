import sys

with open(r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

results = []
for i, line in enumerate(lines):
    for attr_name in ['title="', 'placeholder="']:
        if attr_name in line:
            idx = line.index(attr_name)
            rest = line[idx+len(attr_name):]
            end = rest.find('"')
            if end > 3:
                val = rest[:end]
                if '{' not in val and '}' not in val and 'http' not in val:
                    if 'bg-' not in val and 'text-' not in val and 'flex' not in val:
                        if any(c.isalpha() for c in val) and len(val) > 3:
                            results.append(f'{i+1} [{attr_name[:-1]}]: {val[:60]}')

with open('attr_gaps.txt', 'w', encoding='utf-8') as out:
    out.write('\n'.join(results))
    out.write(f'\n\nTotal: {len(results)}\n')
print(f'Found {len(results)} hardcoded title/placeholder attrs')
