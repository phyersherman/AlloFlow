"""Check which verification items failed"""
with open(r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt', 'r', encoding='utf-8') as f:
    text = f.read()

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

for raw, key in checks:
    raw_count = text.count('>' + raw + '<')
    t_count = text.count("t('" + key + "')")
    if t_count == 0 and raw_count == 0:
        # Check if the raw string exists at all in the file
        general = text.count(raw)
        print(f"FAIL {key}: raw_jsx=0, t()=0, general_occurrences={general}")
    elif t_count > 0:
        print(f"PASS {key}: t()={t_count}")
    else:
        print(f"PARTIAL {key}: raw_jsx={raw_count}, t()={t_count}")
