"""
Localization Patch Script — High Priority
Adds new UI_STRINGS keys to ui_strings.js and replaces raw English strings
in AlloFlowANTI.txt with t() calls.
"""
import json, re

UI_STRINGS_FILE = r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\ui_strings.js'
MONOLITH_FILE = r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt'

# ── Step 1: Add new sections/keys to ui_strings.js ──

NEW_KEYS = {
    "class_analytics": {
        "rti_classification": "RTI Classification",
        "word_sounds": "Word Sounds",
        "quiz_avg": "Quiz Avg",
        "activities": "Activities",
        "my_learning_journey": "My Learning Journey",
        "leave_empty_hint": "Leave empty to include all sessions",
        "live_sync": "Live Sync",
        "accuracy": "Accuracy",
        "words_completed": "Words Completed",
        "best_streak": "Best Streak",
        "phonemes_practiced": "Phonemes Practiced",
        "growth": "Growth",
        "average": "Average",
        "best_score": "Best Score",
        "attempts": "Attempts",
        "no_student_data": "No Student Data Yet",
        "last_session": "Last Session",
        "minutes_session": "Minutes/Session"
    },
    "rti": {
        "progress_monitor": "RTI Progress Monitor",
        "baseline": "Baseline",
        "target_wcpm": "Target WCPM",
        "target_date": "Target Date",
        "trend_line_comparison": "Trend Line Comparison",
        "ncii_recommended": "NCII recommended",
        "frequency": "Frequency",
        "weekly": "Weekly",
        "group_size": "Group Size",
        "start_date": "Start Date",
        "download_report_title": "Download a growth-focused report suitable for sharing with the family"
    },
    "probes": {
        "benchmark_battery": "Benchmark Probe Battery",
        "standardized": "Standardized",
        "grade_k": "Grade K",
        "math_fluency": "Math Fluency Probe",
        "literacy_fluency": "Literacy Fluency Probes",
        "nwf": "Nonsense Word Fluency",
        "lnf": "Letter Naming Fluency",
        "ran": "Rapid Automatized Naming",
        "missing_number": "Missing Number Probe",
        "correct": "Correct",
        "attempted": "Attempted",
        "accuracy": "Accuracy",
        "qd": "Quantity Discrimination Probe",
        "probe_results": "Probe Results"
    },
    "learner": {
        "total_xp": "Total XP",
        "current_run": "Current Run",
        "daily_streak": "Daily Streak",
        "ws_accuracy": "Word Sounds Accuracy",
        "coming_up": "Coming Up",
        "xp_earned": "XP Earned",
        "words_today": "Words Today",
        "xp_this_week": "XP This Week",
        "activities_week": "Activities",
        "words_this_week": "Words This Week",
        "words_correct": "Words Correct",
        "phonemes_touched": "Phonemes Touched",
        "sessions": "Sessions",
        "label_challenges": "Label Challenges",
        "recent_activity": "Recent Activity",
        "progress_report": "Learning Progress Report"
    },
    "research": {
        "construct": "Construct",
        "perceived_usefulness": "Perceived Usefulness",
        "perceived_ease": "Perceived Ease of Use",
        "behavioral_intention": "Behavioral Intention",
        "measure": "Measure",
        "metric": "Metric",
        "total_students": "Total Students",
        "total_sessions": "Total Sessions",
        "avg_sessions": "Avg Sessions Per Student",
        "fidelity_records": "Fidelity Records",
        "total_probes": "Total Probes Administered",
        "sessions_completed": "Sessions Completed",
        "quiz_responses": "Quiz Responses",
        "probes_administered": "Probes Administered",
        "survey_responses": "Survey Responses",
        "explore_challenges": "Explore Challenges",
        "intervention_logs": "Intervention Logs",
        "recent_probe_results": "Recent Probe Results",
        "external_cbm_scores": "External CBM Scores",
        "export_apa_title": "Export Research Report (APA-formatted)"
    },
    "adventure": {
        "focus_reader": "Focus Reader",
        "tap_pause": "Tap to Pause",
        "tap_play": "Tap or Space to Play",
        "add_character": "Add Character",
        "create_cast_member": "Create a new cast member",
        "remove_character": "Remove character",
        "edit_name": "Click to edit name",
        "edit_role": "Click to edit role",
        "edit_appearance": "Click to edit appearance",
        "regen_portrait": "Regenerate using current description",
        "edit_portrait_placeholder": "e.g. Add green glasses",
        "edit_nanobanana": "Edit portrait with NanoBanana",
        "char_name_placeholder": "Character name",
        "role_placeholder": "Role (e.g. Wise Mentor)",
        "appearance_placeholder": "Appearance (e.g. tall, silver hair, blue robe)"
    },
    "fluency": {
        "oral_score_sheet": "Oral Fluency Score Sheet",
        "assessment_record": "AlloFlow Assessment Record",
        "student": "Student",
        "substitutions": "Substitutions",
        "omissions": "Omissions",
        "insertions": "Insertions",
        "error_rate": "Error Rate",
        "reading_level": "Reading Level",
        "total_errors": "Total Errors",
        "sc_rate": "SC Rate",
        "total_words": "Total Words",
        "verified_wcpm": "Verified WCPM",
        "verified_reading_level": "Verified Reading Level",
        "teacher_notes": "Teacher Notes",
        "teacher_signature": "Teacher Signature",
        "hesitation": "Hesitation"
    },
    "stem": {
        "explore": "Explore",
        "operation": "Operation",
        "difficulty": "Difficulty",
        "volume": "Volume",
        "surface_area": "Surface Area",
        "enter_volume": "Enter volume..."
    },
    "glossary_health": {
        "composite_accuracy": "Composite Accuracy",
        "grade_level": "Grade Level",
        "vocabulary_tiers": "Vocabulary Tiers",
        "suggested_terms": "Suggested Additional Terms",
        "concept_web": "Concept Web"
    }
}

# Read current ui_strings.js
with open(UI_STRINGS_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the closing brace of the main object and insert new sections before it
# The file ends with "}" so we insert before the last }
insert_lines = []
for section_key, keys in NEW_KEYS.items():
    # Check if section already exists
    if f'"{section_key}"' in content:
        print(f"  Section '{section_key}' already exists, skipping")
        continue
    insert_lines.append(f'  "{section_key}": {{')
    for k, v in keys.items():
        escaped_v = v.replace('"', '\\"')
        insert_lines.append(f'    "{k}": "{escaped_v}",')
    # Remove trailing comma from last key
    if insert_lines:
        insert_lines[-1] = insert_lines[-1].rstrip(',')
    insert_lines.append('  },')

if insert_lines:
    # Remove trailing comma from last section
    insert_lines[-1] = insert_lines[-1].rstrip(',')
    
    # Insert before the final closing brace
    insert_text = '\n'.join(insert_lines)
    # Find the last } and insert before it
    last_brace = content.rfind('}')
    if last_brace > 0:
        # Check if there's a comma needed
        # Find the last non-whitespace before the closing brace
        before = content[:last_brace].rstrip()
        if before.endswith('}'):
            # Need to add a comma after the last section
            content = before + ',\n' + insert_text + '\n' + content[last_brace:]
        else:
            content = content[:last_brace] + insert_text + '\n' + content[last_brace:]
        
        with open(UI_STRINGS_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added {len(NEW_KEYS)} new sections to ui_strings.js")
else:
    print("All sections already exist in ui_strings.js")

# ── Step 2: Replace raw strings in AlloFlowANTI.txt with t() calls ──

print("\nNow patching raw strings in AlloFlowANTI.txt...")

with open(MONOLITH_FILE, 'r', encoding='utf-8') as f:
    mono = f.read()

# Build replacement map: raw string -> t() call
# Only replace exact JSX text between >...< to avoid breaking code
REPLACEMENTS = {
    # class_analytics
    ">RTI Classification<": ">{t('class_analytics.rti_classification')}<",
    ">No Student Data Yet<": ">{t('class_analytics.no_student_data')}<",
    ">Live Sync<": ">{t('class_analytics.live_sync')}<",
    ">Words Completed<": ">{t('class_analytics.words_completed')}<",
    ">Best Streak<": ">{t('class_analytics.best_streak')}<",
    ">Phonemes Practiced<": ">{t('class_analytics.phonemes_practiced')}<",
    ">Best Score<": ">{t('class_analytics.best_score')}<",
    ">My Learning Journey<": ">{t('class_analytics.my_learning_journey')}<",
    # rti
    ">RTI Progress Monitor<": ">{t('rti.progress_monitor')}<",
    ">Trend Line Comparison<": ">{t('rti.trend_line_comparison')}<",
    ">NCII recommended<": ">{t('rti.ncii_recommended')}<",
    # probes
    ">Benchmark Probe Battery<": ">{t('probes.benchmark_battery')}<",
    ">Math Fluency Probe<": ">{t('probes.math_fluency')}<",
    ">Literacy Fluency Probes<": ">{t('probes.literacy_fluency')}<",
    ">Nonsense Word Fluency<": ">{t('probes.nwf')}<",
    ">Letter Naming Fluency<": ">{t('probes.lnf')}<",
    ">Rapid Automatized Naming<": ">{t('probes.ran')}<",
    ">Missing Number Probe<": ">{t('probes.missing_number')}<",
    ">Quantity Discrimination Probe<": ">{t('probes.qd')}<",
    ">Probe Results<": ">{t('probes.probe_results')}<",
    # learner
    ">Total XP<": ">{t('learner.total_xp')}<",
    ">Current Run<": ">{t('learner.current_run')}<",
    ">Daily Streak<": ">{t('learner.daily_streak')}<",
    ">Word Sounds Accuracy<": ">{t('learner.ws_accuracy')}<",
    ">Coming Up<": ">{t('learner.coming_up')}<",
    ">XP Earned<": ">{t('learner.xp_earned')}<",
    ">Words Today<": ">{t('learner.words_today')}<",
    ">XP This Week<": ">{t('learner.xp_this_week')}<",
    ">Words This Week<": ">{t('learner.words_this_week')}<",
    ">Words Correct<": ">{t('learner.words_correct')}<",
    ">Phonemes Touched<": ">{t('learner.phonemes_touched')}<",
    ">Label Challenges<": ">{t('learner.label_challenges')}<",
    ">Recent Activity<": ">{t('learner.recent_activity')}<",
    ">Learning Progress Report<": ">{t('learner.progress_report')}<",
    # research
    ">Perceived Usefulness<": ">{t('research.perceived_usefulness')}<",
    ">Perceived Ease of Use<": ">{t('research.perceived_ease')}<",
    ">Behavioral Intention<": ">{t('research.behavioral_intention')}<",
    ">Total Probes Administered<": ">{t('research.total_probes')}<",
    ">Fidelity Records<": ">{t('research.fidelity_records')}<",
    ">Avg Sessions Per Student<": ">{t('research.avg_sessions')}<",
    ">Sessions Completed<": ">{t('research.sessions_completed')}<",
    ">Quiz Responses<": ">{t('research.quiz_responses')}<",
    ">Probes Administered<": ">{t('research.probes_administered')}<",
    ">Survey Responses<": ">{t('research.survey_responses')}<",
    ">Explore Challenges<": ">{t('research.explore_challenges')}<",
    ">Intervention Logs<": ">{t('research.intervention_logs')}<",
    ">Recent Probe Results<": ">{t('research.recent_probe_results')}<",
    ">External CBM Scores<": ">{t('research.external_cbm_scores')}<",
    # adventure
    ">Focus Reader<": ">{t('adventure.focus_reader')}<",
    ">Tap to Pause<": ">{t('adventure.tap_pause')}<",
    ">Tap or Space to Play<": ">{t('adventure.tap_play')}<",
    ">Add Character<": ">{t('adventure.add_character')}<",
    ">Create a new cast member<": ">{t('adventure.create_cast_member')}<",
    # fluency
    ">Oral Fluency Score Sheet<": ">{t('fluency.oral_score_sheet')}<",
    ">AlloFlow Assessment Record<": ">{t('fluency.assessment_record')}<",
    ">Verified WCPM<": ">{t('fluency.verified_wcpm')}<",
    ">Verified Reading Level<": ">{t('fluency.verified_reading_level')}<",
    ">Teacher Notes<": ">{t('fluency.teacher_notes')}<",
    ">Teacher Signature<": ">{t('fluency.teacher_signature')}<",
    # stem
    ">Surface Area<": ">{t('stem.surface_area')}<",
    # glossary health  
    ">Glossary Health Check<": ">{t('glossary_health.composite_accuracy') || 'Glossary Health Check'}<",
    ">Composite Accuracy<": ">{t('glossary_health.composite_accuracy')}<",
    ">Vocabulary Tiers<": ">{t('glossary_health.vocabulary_tiers')}<",
    ">Suggested Additional Terms<": ">{t('glossary_health.suggested_terms')}<",
    ">Concept Web<": ">{t('glossary_health.concept_web')}<",
    # misc
    ">Assessment Center<": ">{t('common.assessment_center') || 'Assessment Center'}<",
    ">Show Solution Steps<": ">{t('math.show_solution_steps') || 'Show Solution Steps'}<",
    ">Crossword Challenge<": ">{t('games.crossword_challenge') || 'Crossword Challenge'}<",
    ">Paragraph Frame<": ">{t('scaffolds.paragraph_frame') || 'Paragraph Frame'}<",
}

count = 0
for old, new in REPLACEMENTS.items():
    n = mono.count(old)
    if n > 0:
        mono = mono.replace(old, new)
        count += n

with open(MONOLITH_FILE, 'w', encoding='utf-8') as f:
    f.write(mono)

print(f"Replaced {count} raw strings in AlloFlowANTI.txt")
print("Done!")
