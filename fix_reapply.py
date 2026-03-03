"""
Re-apply t() calls only in JSX contexts (not template literals).
Find the specific JSX locations and patch them back.
"""
with open(r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

changes = 0

# 'My Learning Journey' appears as JSX at line ~6319/6340 and 20830
# In JSX, the pattern is either:
# >My Learning Journey<  (inside JSX tags)
# or as part of a JSX expression like 'My Learning Journey'

# RTI Classification appears in JSX at line 6004
# But that was inside a template string, so DON'T re-apply there.

# Let's check what the current state looks like for key strings
for i, line in enumerate(lines):
    lineno = i + 1
    # Skip lines inside template literals (backtick strings)
    # Template literals in this file are used for HTML reports (lines ~5877-6034, 6266-6327)
    if 5870 <= lineno <= 6042:
        continue  # generateStudentProgressReport
    if 6260 <= lineno <= 6330:
        continue  # generateStudentFriendlyReport
    
    # Re-apply My Learning Journey in JSX (should be at line ~20830)
    if '>My Learning Journey<' in line:
        lines[i] = line.replace('>My Learning Journey<', ">{t('class_analytics.my_learning_journey')}<")
        changes += 1
        print(f"  Re-applied at line {lineno}: My Learning Journey")
    
    # Re-apply RTI Classification if it's in JSX context (not template)
    if '>RTI Classification<' in line:
        lines[i] = line.replace('>RTI Classification<', ">{t('class_analytics.rti_classification')}<")
        changes += 1
        print(f"  Re-applied at line {lineno}: RTI Classification")

with open(r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print(f"\nRe-applied {changes} JSX substitutions")
