"""
Localization Patch — Wave 2 (Low Priority)
Replaces remaining raw English strings in JSX contexts with t() calls.
Carefully avoids HTML template literals (backtick strings for reports).
"""

MONOLITH = r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt'
UI_STRINGS = r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\ui_strings.js'

# ── Step 1: Add remaining keys to ui_strings.js ──

with open(UI_STRINGS, 'r', encoding='utf-8') as f:
    uis = f.read()

NEW_KEYS = {
    "word_sounds": {
        "correct": "Correct",
        "label_details": "Label Details",
        "image_display_mode": "Image Display Mode",
        "syllable_range": "Syllable Range",
        "enable_lesson_plan": "Enable Lesson Plan",
        "phonemes": "Phonemes",
        "rhyme_options": "Rhyme Time Options",
        "blend_options": "Blend Sounds Options",
        "no_phonemes": "No phonemes available",
        "regen_image": "Regenerate Image",
        "gen_image": "Generate Image",
        "theme_placeholder": "e.g. Space, Ocean...",
        "recheck_title": "Re-check phonemes with Gemini",
        "refine_placeholder": "e.g., make it cuter, add a banana"
    },
    "math": {
        "show_solution_steps": "Show Solution Steps",
        "edit_with_allobot": "Edit with Allobot",
        "edit_placeholder": "Describe how to modify these problems",
        "total_digits": "Total Digits",
        "timer_visible": "Timer Visible",
        "timer_hidden": "Timer Hidden"
    },
    "games": {
        "crossword_challenge": "Crossword Challenge"
    },
    "scaffolds": {
        "paragraph_frame": "Paragraph Frame"
    },
    "resource_builder": {
        "question": "Question",
        "quick_templates": "Quick Templates",
        "use_current_text": "Use Current Text",
        "attach_image": "Attach Image",
        "use_generated": "Use Generated",
        "generation_mode": "Generation Mode",
        "target_group": "Target Group",
        "target_language": "Target Language",
        "reading_level": "Reading Level"
    }
}

# Add keys to existing sections or create new ones
for section, keys in NEW_KEYS.items():
    section_marker = f'"{section}"' + ': {'
    if section_marker in uis:
        # Section exists — add keys before its closing brace
        # Find the section and its closing brace
        start = uis.index(section_marker)
        # Find the next closing brace at the same indentation level
        depth = 0
        pos = start + len(section_marker)
        while pos < len(uis):
            if uis[pos] == '{':
                depth += 1
            elif uis[pos] == '}':
                if depth == 0:
                    # This is the closing brace of our section
                    # Insert new keys before it
                    new_entries = []
                    for k, v in keys.items():
                        key_check = f'"{k}"'
                        # Only add if key doesn't already exist in this section
                        section_content = uis[start:pos]
                        if key_check not in section_content:
                            escaped_v = v.replace('"', '\\"')
                            new_entries.append(f'    "{k}": "{escaped_v}"')
                    if new_entries:
                        insert_text = ',\n' + ',\n'.join(new_entries)
                        # Find the last non-whitespace before closing brace
                        before = uis[:pos].rstrip()
                        if before.endswith(','):
                            before = before[:-1]  # remove trailing comma
                        uis = before + insert_text + '\n  ' + uis[pos:]
                        print(f"  Added {len(new_entries)} keys to existing '{section}' section")
                    else:
                        print(f"  All keys already exist in '{section}'")
                    break
                else:
                    depth -= 1
            pos += 1
    else:
        # Section doesn't exist — add it before the final closing brace
        insert_lines = [f'  "{section}": {{']
        for k, v in keys.items():
            escaped_v = v.replace('"', '\\"')
            insert_lines.append(f'    "{k}": "{escaped_v}",')
        insert_lines[-1] = insert_lines[-1].rstrip(',')
        insert_lines.append('  },')
        
        last_brace = uis.rfind('}')
        before = uis[:last_brace].rstrip()
        if before.endswith('}'):
            before += ','
        uis = before + '\n' + '\n'.join(insert_lines) + '\n' + uis[last_brace:]
        print(f"  Created new '{section}' section with {len(keys)} keys")

with open(UI_STRINGS, 'w', encoding='utf-8') as f:
    f.write(uis)
print("ui_strings.js updated!\n")

# ── Step 2: Replace raw strings in monolith (JSX only, not template literals) ──

with open(MONOLITH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Define template literal ranges to skip (report generators)
# These are approximate line ranges where HTML template strings live
SKIP_RANGES = [
    (5870, 6042),   # generateStudentProgressReport
    (6260, 6330),   # generateStudentFriendlyReport
]

def in_skip_range(lineno):
    for start, end in SKIP_RANGES:
        if start <= lineno <= end:
            return True
    return False

# Replacement map: (raw_text, t_key)
REPLACEMENTS = [
    # Word Sounds Review Panel
    (">Label Details<", ">{t('word_sounds.label_details')}<"),
    (">Image Display Mode<", ">{t('word_sounds.image_display_mode')}<"),
    (">Syllable Range<", ">{t('word_sounds.syllable_range')}<"),
    (">Enable Lesson Plan<", ">{t('word_sounds.enable_lesson_plan')}<"),
    (">Phonemes<", ">{t('word_sounds.phonemes')}<"),
    (">Rhyme Time Options<", ">{t('word_sounds.rhyme_options')}<"),
    (">Blend Sounds Options<", ">{t('word_sounds.blend_options')}<"),
    (">No phonemes available<", ">{t('word_sounds.no_phonemes')}<"),
    (">Regenerate Image<", ">{t('word_sounds.regen_image')}<"),
    (">Generate Image<", ">{t('word_sounds.gen_image')}<"),
    
    # Math
    (">Show Solution Steps<", ">{t('math.show_solution_steps')}<"),
    (">Edit with Allobot<", ">{t('math.edit_with_allobot')}<"),
    (">Total Digits<", ">{t('math.total_digits')}<"),
    (">Timer Visible<", ">{t('math.timer_visible')}<"),
    (">Timer Hidden<", ">{t('math.timer_hidden')}<"),
    
    # Games
    (">Crossword Challenge<", ">{t('games.crossword_challenge')}<"),
    
    # Scaffolds
    (">Paragraph Frame<", ">{t('scaffolds.paragraph_frame')}<"),
    
    # Resource Builder
    (">Quick Templates<", ">{t('resource_builder.quick_templates')}<"),
    (">Use Current Text<", ">{t('resource_builder.use_current_text')}<"),
    (">Attach Image<", ">{t('resource_builder.attach_image')}<"),
    (">Use Generated<", ">{t('resource_builder.use_generated')}<"),
    (">Generation Mode<", ">{t('resource_builder.generation_mode')}<"),
    (">Target Group<", ">{t('resource_builder.target_group')}<"),
    (">Target Language<", ">{t('resource_builder.target_language')}<"),
    
    # Glossary Health (might be partially done)
    (">Grade Level<", ">{t('glossary_health.grade_level')}<"),
    
    # Stem
    (">Volume<", ">{t('stem.volume')}<"),
    
    # Assessment — only if in JSX
    (">IMS Content<", ">{t('common.ims_content') || 'IMS Content'}<"),
]

# Also handle hardcoded title= and placeholder= attributes
ATTR_REPLACEMENTS = [
    ('title="Remove character"', "title={t('adventure.remove_character')}"),
    ('title="Click to edit name"', "title={t('adventure.edit_name')}"),
    ('title="Click to edit role"', "title={t('adventure.edit_role')}"),
    ('title="Click to edit appearance"', "title={t('adventure.edit_appearance')}"),
    ('title="Regenerate using current description"', "title={t('adventure.regen_portrait')}"),
    ('title="Edit portrait with NanoBanana"', "title={t('adventure.edit_nanobanana')}"),
    ('placeholder="Character name"', "placeholder={t('adventure.char_name_placeholder')}"),
    ('placeholder="Role (e.g. Wise Mentor)"', "placeholder={t('adventure.role_placeholder')}"),
    ('title="Assessment Center"', "title={t('common.assessment_center') || 'Assessment Center'}"),
    ('title="Randomize"', "title={t('common.randomize') || 'Randomize'}"),
    ('title="Export Research Report (APA-formatted)"', "title={t('research.export_apa_title')}"),
]

count = 0
for i, line in enumerate(lines):
    lineno = i + 1
    if in_skip_range(lineno):
        continue
    
    for old, new in REPLACEMENTS:
        if old in line:
            lines[i] = line.replace(old, new, 1)
            line = lines[i]  # update for chained replacements
            count += 1
    
    for old, new in ATTR_REPLACEMENTS:
        if old in line:
            lines[i] = line.replace(old, new, 1)
            line = lines[i]
            count += 1

with open(MONOLITH, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Replaced {count} strings in AlloFlowANTI.txt")
print("Done!")
