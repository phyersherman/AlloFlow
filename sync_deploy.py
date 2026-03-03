"""Sync to App.jsx, update CDN URLs, build, and deploy"""
import subprocess, re, shutil

sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()
print(f"Current commit: {sha[:8]}")

with open('AlloFlowANTI.txt', 'r', encoding='utf-8') as f:
    text = f.read()

text, n1 = re.subn(r'(https://cdn\.jsdelivr\.net/gh/Apomera/AlloFlow@)[^/]+(/word_sounds_module\.js)', r'\g<1>' + sha + r'\g<2>', text)
print(f'Updated {n1} word_sounds_module.js URL(s)')

text, n2 = re.subn(r'(https://cdn\.jsdelivr\.net/gh/Apomera/AlloFlow@)[^/]+(/stem_lab_module\.js)', r'\g<1>' + sha + r'\g<2>', text)
print(f'Updated {n2} stem_lab_module.js URL(s)')

with open('AlloFlowANTI.txt', 'w', encoding='utf-8') as f:
    f.write(text)

shutil.copyfile('AlloFlowANTI.txt', 'prismflow-deploy/src/App.jsx')
print('Synced to App.jsx')
