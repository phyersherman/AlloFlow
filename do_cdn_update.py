import urllib.request, json, re

try:
    url = 'https://api.github.com/repos/Apomera/AlloFlow/commits/master'
    req = urllib.request.Request(url, headers={'User-Agent': 'AlloFlow'})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read().decode('utf-8'))
    sha = data['sha']
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
except Exception as e:
    print(f'Failed: {e}')
