"""Verify localization patch results - output to utf8 file"""
with open(r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt', 'r', encoding='utf-8') as f:
    text = f.read()

results = []
checks = [
    ('RTI Classification', 'class_analytics.rti_classification'),
    ('No Student Data Yet', 'class_analytics.no_student_data'),
    ('Benchmark Probe Battery', 'probes.benchmark_battery'),
    ('Total XP', 'learner.total_xp'),
    ('Perceived Usefulness', 'research.perceived_usefulness'),
    ('Focus Reader', 'adventure.focus_reader'),
    ('Daily Streak', 'learner.daily_streak'),
    ('Nonsense Word Fluency', 'probes.nwf'),
    ('Live Sync', 'class_analytics.live_sync'),
]
results.append('=== Monolith Verification ===')
all_pass = True
for raw, key in checks:
    raw_count = text.count('>' + raw + '<')
    t_count = text.count("t('" + key + "')")
    status = 'PASS' if t_count > 0 and raw_count == 0 else ('PARTIAL' if t_count > 0 else 'FAIL')
    if status != 'PASS':
        all_pass = False
    results.append(f'  {key}: raw={raw_count}, t()={t_count} -> {status}')

with open(r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\ui_strings.js', 'r', encoding='utf-8') as f:
    uis = f.read()
results.append('\n=== ui_strings.js Sections ===')
for section in ['class_analytics', 'rti', 'probes', 'learner', 'research', 'adventure', 'stem', 'glossary_health']:
    found = '"' + section + '"' in uis
    if not found:
        all_pass = False
    results.append(f'  {section}: {"FOUND" if found else "MISSING"}')

results.append(f'\nOverall: {"ALL PASS" if all_pass else "SOME FAILURES"}')

with open(r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\verify_out.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))
print('\n'.join(results))
