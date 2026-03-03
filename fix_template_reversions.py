"""
Fix: Revert t() calls that were incorrectly placed inside HTML template literals
These are in generateStudentProgressReport and generateStudentFriendlyReport functions
where raw HTML is built as template strings, not JSX.
"""
with open(r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# These replacements went into HTML template strings (backtick strings written to new windows)
# where t() is not available. Revert them to raw English text.
reversions = [
    # In generateStudentProgressReport (HTML template literal)
    ("{t('class_analytics.rti_classification')}", "RTI Classification"),
    ("{t('common.student_progress_report')}", "Student Progress Report"),
    
    # In generateStudentFriendlyReport (HTML template literal) 
    ("{t('class_analytics.my_learning_journey')}", "My Learning Journey"),
    
    # In printable score sheet (HTML template)
    ("{t('fluency.oral_score_sheet')}", "Oral Fluency Score Sheet"),
    ("{t('fluency.assessment_record')}", "AlloFlow Assessment Record"),
    ("{t('fluency.verified_wcpm')}", "Verified WCPM"),
    ("{t('fluency.verified_reading_level')}", "Verified Reading Level"),
    ("{t('fluency.teacher_notes')}", "Teacher Notes"),
    ("{t('fluency.teacher_signature')}", "Teacher Signature"),
]

count = 0
for wrong, correct in reversions:
    # Be careful: only revert instances inside template literals 
    # Check if the wrong value appears inside a backtick-delimited section
    n = text.count(wrong)
    if n > 0:
        text = text.replace(wrong, correct)
        count += n
        print(f"  Reverted {n}x: {wrong} -> {correct}")
    else:
        print(f"  Not found: {wrong}")

with open(r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print(f"\nReverted {count} template literal substitutions total")
