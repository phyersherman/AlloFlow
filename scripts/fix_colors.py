"""
Fix color consistency in generator panel.
Change pink/red/fuchsia to indigo in the sidebar/generator panel elements.
"""

FILE = r"c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt"

with open(FILE, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

count = 0

# Define targeted replacements for known sidebar elements
# We need to be surgical - only change colors in the sidebar panel, not everywhere
replacements = [
    # pink-500 -> indigo-500 (focus rings, borders)
    ('pink-500', 'indigo-500'),
    # pink-600 -> indigo-600 (checkbox text color, icons)
    ('pink-600', 'indigo-600'),
    # pink-800 -> indigo-800 (label text)
    ('pink-800', 'indigo-800'),
    # pink-50 -> indigo-50 (background hover states)
    ('pink-50', 'indigo-50'),
    # pink-100 -> indigo-100 (light backgrounds)
    ('pink-100', 'indigo-100'),
    # red-500 -> indigo-500 (lock settings)
    ('red-500', 'indigo-500'),
    # red-600 -> indigo-600
    ('red-600', 'indigo-600'),
    # red-800 -> indigo-800 (lock label)
    ('red-800', 'indigo-800'),  
    # red-50 -> indigo-50
    ('red-50', 'indigo-50'),
    # fuchsia-500 -> indigo-500
    ('fuchsia-500', 'indigo-500'),
    # fuchsia-600 -> indigo-600
    ('fuchsia-600', 'indigo-600'),
]

for old, new in replacements:
    occurrences = content.count(old)
    if occurrences > 0:
        content = content.replace(old, new)
        count += occurrences
        print("  %s -> %s (%d occurrences)" % (old, new, occurrences))

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nTotal replacements: %d" % count)
print("File saved!")
