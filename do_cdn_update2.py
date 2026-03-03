import re

sha = '89b26d2e8dc5ab0e276388926b7734c640a64f2ed'
print(f'Latest Commit SHA: {sha}')

f = open('AlloFlowANTI.txt', 'r', encoding='utf-8')
content = f.read()
f.close()

old_pattern = r"(https://cdn\.jsdelivr\.net/gh/Apomera/AlloFlow)@([a-zA-Z0-9]+)(/(?:stem_lab|word_sounds)_module(?:_clean)?\.js)(\?v=\d+)?"
new_repl = rf"\1@{sha}\3"

result, count = re.subn(old_pattern, new_repl, content)

print(f'Replaced {count} CDN URLs.')

with open('AlloFlowANTI.txt', 'w', encoding='utf-8') as out:
    out.write(result)
