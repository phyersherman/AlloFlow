"""
Fix all localization issues in ui_strings.js:
1. Add missing 'adventure' section
2. Fix raw key-path values in 'common' section
3. Push to GitHub
"""
import json

FILE = 'ui_strings.js'

with open(FILE, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Parse the JSON
data = json.loads(content)

# === 1. Add 'adventure' section ===
if 'adventure' not in data:
    data['adventure'] = {}

adventure_keys = {
    'advanced_settings': 'Advanced Settings',
    'art_style_label': 'Art Style',
    'art_auto': 'Auto (default)',
    'art_storybook': 'Storybook',
    'art_pixel': 'Pixel Art',
    'art_cinematic': 'Cinematic',
    'art_anime': 'Anime',
    'art_crayon': 'Hand-drawn',
    'art_custom': 'Custom...',
    'consistent_characters_label': 'Consistent Characters',
    'consistent_characters_desc': 'Keep the same character appearances across scenes',
    'story_mode_label': 'Story Mode',
    'story_mode_desc': 'Narrative-focused adventure with rich descriptions',
    'social_story_focus_placeholder': 'e.g., Making friends, Handling frustration...',
    'custom_art_placeholder': 'Describe your preferred art style...',
    'maximize': 'Maximize',
    'low_quality': 'Low Quality Visuals',
}

for k, v in adventure_keys.items():
    if k not in data['adventure']:
        data['adventure'][k] = v
        print("  Added adventure.%s = '%s'" % (k, v))

# === 2. Fix raw key-path values in 'common' section ===
# These entries have their value set to a raw dot-notation key path
raw_fixes = {
    'adventure_social_story_focus_placeholder': 'e.g., Making friends, Handling frustration...',
    'common_placeholder_item_trans': 'Item Translation...',
    'common_placeholder_title_trans': 'Title Translation...',
    'common_placeholder_translation': 'Translation...',
    'common_standards_region_placeholder': 'Region or Framework (e.g. CASEL, CCSS)...',
    'common_url_placeholder': 'https://example.com/article',
    'escape_room_enter_answer': 'Enter your answer...',
    'escape_room_unscramble_placeholder': 'Unscramble the letters...',
    'glossary_custom_edit_placeholder': 'Edit definition...',
    'glossary_style_placeholder': 'e.g., cartoon, realistic, watercolor...',
    'groups_new_group_placeholder': 'New group name...',
    'modals_save_project_placeholder': 'My Lesson Plan...',
    'session_default_placeholder': 'Enter session name...',
    'standards_region_framework_placeholder': 'Region or Framework...',
    'standards_region_optional': 'Region (optional)',
    'timeline_revise_placeholder': 'Revise instructions...',
    'visuals_refiner_placeholder': 'e.g., make it cuter, add a banana...',
    'toggle_consistent_characters': 'Toggle consistent characters',
}

if 'common' in data:
    for k, v in raw_fixes.items():
        old_val = data['common'].get(k)
        if old_val and '.' in old_val and old_val.count('.') == 1:
            # This is a raw key-path value, fix it
            data['common'][k] = v
            print("  Fixed common.%s: '%s' -> '%s'" % (k, old_val, v))
        elif k not in data['common']:
            data['common'][k] = v
            print("  Added common.%s = '%s'" % (k, v))

# === 3. Add glossary section if needed ===
if 'glossary' not in data:
    data['glossary'] = {}
    
glossary_keys = {
    'style_placeholder': 'e.g., cartoon, realistic, watercolor...',
}

for k, v in glossary_keys.items():
    if k not in data['glossary']:
        data['glossary'][k] = v
        print("  Added glossary.%s = '%s'" % (k, v))

# === 4. Write back ===
with open(FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nDone! File updated.")
print("Total keys: %d sections" % len(data))
for section in sorted(data.keys()):
    print("  %s: %d keys" % (section, len(data[section])))
