"""
STEM Lab Enhancement Script - adds Snapshot buttons and subtitles.
Uses string interpolation instead of f-strings to avoid brace escaping issues.
"""
import re

FILE = r"c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\stem_lab_module.js"
with open(FILE, 'r', encoding='utf-8', errors='replace') as f:
    c = f.read()

print("Original: %d chars, %d lines" % (len(c), c.count('\n')+1))

# ═══════════════════════════════════════════════════
# FIX 1: Add Snapshot buttons to tools missing them
# ═══════════════════════════════════════════════════
print("\n=== Adding Snapshot buttons ===")

# Snapshot button template
def make_snapshot(snap_id, tool_name, label_expr, indent='            '):
    return (indent + 'React.createElement("button", { onClick: () => { '
            'setToolSnapshots(prev => [...prev, { '
            "id: '" + snap_id + "-' + Date.now(), "
            "tool: '" + tool_name + "', "
            "label: " + label_expr + ", "
            "data: { ...d }, timestamp: Date.now() "
            "}]); addToast('\\uD83D\\uDCF8 Snapshot saved!', 'success'); "
            '}, className: "mt-3 ml-auto px-4 py-2 text-xs font-bold text-white '
            'bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full '
            'hover:from-indigo-600 hover:to-purple-600 shadow-md hover:shadow-lg '
            'transition-all" }, "\\uD83D\\uDCF8 Snapshot")')

tools_needing_snapshot = [
    ('waterCycle', 'wc', "sel ? sel.label : 'Water Cycle'"),
    ('rockCycle', 'rc', "sel ? sel.label : 'Rock Cycle'"),
    ('fractionViz', 'fv', "d.num1 + '/' + d.den1 + ' vs ' + d.num2 + '/' + d.den2"),
    ('unitConvert', 'uc', "d.value + ' ' + d.fromUnit + ' to ' + d.toUnit"),
    ('decomposer', 'dc', "d.material || 'Material'"),
]

for tool_id, snap_id, label_expr in tools_needing_snapshot:
    # Find the tool's block
    pattern = "stemLabTool === '" + tool_id + "'"
    idx = c.find(pattern)
    if idx < 0:
        print("  SKIP: '%s' not found" % tool_id)
        continue
    
    # Find the next tool or module close
    next_tool_idx = len(c)
    for m in re.finditer(r"stemLabTool === '(\w+)'", c[idx+len(pattern):]):
        next_tool_idx = idx + len(pattern) + m.start()
        break
    
    tool_block = c[idx:next_tool_idx]
    if 'Snapshot' in tool_block:
        print("  SKIP: '%s' already has Snapshot" % tool_id)
        continue
    
    # Find the })() that closes this tool's IIFE
    close_pattern = '})(),'
    close_idx = tool_block.rfind(close_pattern)
    if close_idx < 0:
        close_pattern = '})();'
        close_idx = tool_block.rfind(close_pattern)
    if close_idx < 0:
        close_pattern = '})()'
        close_idx = tool_block.rfind(close_pattern)
    
    if close_idx < 0:
        print("  WARNING: Can't find close for '%s'" % tool_id)
        continue
    
    # The })() is at idx + close_idx
    # We need to insert the snapshot button BEFORE the closing of the return statement
    # The return pattern is: return React.createElement("div", {...}, ...children...);
    # The closing is:  ); \n        })()
    
    # Find the ); that precedes })()
    abs_close = idx + close_idx
    
    # Look backwards for the ); 
    region = c[idx:abs_close]
    # Find last ); before })()
    close_paren = region.rfind(');')
    if close_paren < 0:
        close_paren = region.rfind(')')
    
    if close_paren < 0:
        print("  WARNING: Can't find return close for '%s'" % tool_id)
        continue
    
    insert_pos = idx + close_paren
    
    # Insert snapshot button before the closing );
    snapshot_btn = ',\n' + make_snapshot(snap_id, tool_id, label_expr) + '\n'
    c = c[:insert_pos] + snapshot_btn + c[insert_pos:]
    print("  OK: Added Snapshot to '%s'" % tool_id)

# ═══════════════════════════════════════════════════
# FIX 2: Add subtitles/tips to tools  
# ═══════════════════════════════════════════════════
print("\n=== Adding subtitles ===")

subtitles = [
    ('solarSystem', 'Solar System Explorer', 'Click each planet to explore facts, size, temperature, and more.'),
    ('rockCycle', 'Rock Cycle', 'See how igneous, sedimentary, and metamorphic rocks transform.'),
    ('fractionViz', 'Fraction Visualizer', 'Compare fractions visually. Try bar and pie modes!'),
    ('unitConvert', 'Unit Converter', 'Convert between length, weight, temperature, and speed units.'),
]

for tool_id, title, subtitle in subtitles:
    pattern = "stemLabTool === '" + tool_id + "'"
    idx = c.find(pattern)
    if idx < 0:
        print("  SKIP: '%s' not found" % tool_id)
        continue
    
    # Check if subtitle already exists (look for italic text in next 800 chars)
    next_800 = c[idx:idx+800]
    if 'text-xs text-slate-500 mb-2' in next_800 or 'text-xs text-slate-400 italic' in next_800:
        print("  SKIP: '%s' already has subtitle" % tool_id)
        continue
    
    # Find the title h3 element: "h3", { className: "text-lg font-bold..."
    h3_idx = next_800.find('"h3"')
    if h3_idx < 0:
        print("  WARNING: Can't find h3 for '%s'" % tool_id)
        continue
    
    # Find the closing of the header div (first ), after the h3)
    # The header is: React.createElement("div", {flex items-center gap-3...},
    #   button(back), h3(title))
    # We want to add the subtitle AFTER the header div closes
    
    # Find the header div close: look for the ), that closes the header
    # After the h3, there's the title string, then ), closes the h3
    # Then ), closes the header div, then , starts the next child
    
    # Find two consecutive ) after h3
    pos = h3_idx
    depth = 0
    found_header_close = -1
    
    # Find the closing of the entire header div
    # Start from the "flex items-center" div
    flex_idx = next_800.rfind('flex items-center gap-3', 0, h3_idx)
    if flex_idx < 0:
        print("  WARNING: Can't find flex div for '%s'" % tool_id)
        continue
    
    # Find the createElement("div" that contains the flex
    div_idx = next_800.rfind('React.createElement("div"', 0, flex_idx)
    if div_idx < 0:
        print("  WARNING: Can't find header div for '%s'" % tool_id)
        continue
    
    # Now count depth from this div to find where it closes
    region = next_800[div_idx:]
    depth = 0
    in_str = False
    str_char = None
    for i, ch in enumerate(region):
        if in_str:
            if ch == '\\' and i+1 < len(region):
                continue
            if ch == str_char:
                in_str = False
            continue
        if ch in ('"', "'"):
            in_str = True
            str_char = ch
        elif ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                found_header_close = div_idx + i + 1
                break
    
    if found_header_close < 0:
        print("  WARNING: Can't find header close for '%s'" % tool_id)
        continue
    
    abs_pos = idx + found_header_close
    subtitle_el = (',\n            React.createElement("p", { className: "text-xs text-slate-500 mb-2 -mt-1" }, '
                   '"' + subtitle + '")')
    c = c[:abs_pos] + subtitle_el + c[abs_pos:]
    print("  OK: Added subtitle to '%s'" % tool_id)

# ═══════════════════════════════════════════════════
# FIX 3: Categorize tool grid with section headers
# ═══════════════════════════════════════════════════
print("\n=== Categorizing tool grid ===")

# Find the tool grid array
grid_marker = "grid grid-cols-2 gap-4 max-w-3xl"
grid_idx = c.find(grid_marker)
if grid_idx < 0:
    print("  WARNING: Can't find tool grid")
else:
    # Find the [ that starts the tool array
    bracket_start = c.find('[', grid_idx)
    # Find the ].map(tool that ends it
    bracket_end = c.find('].map(tool', grid_idx)
    
    if bracket_start > 0 and bracket_end > 0:
        tool_array_content = c[bracket_start+1:bracket_end]
        
        # Parse out individual tool objects
        tools = re.findall(r"\{[^}]+id:\s*'(\w+)'[^}]*\}", tool_array_content)
        print("  Grid tools: %s" % ', '.join(tools))
        
        # Define category order
        cat_order = [
            ('Math Fundamentals', ['volume', 'numberline', 'areamodel', 'fractionViz', 'base10', 'coordinate', 'protractor', 'multtable']),
            ('Advanced Math', ['funcGrapher', 'inequality', 'calculus', 'probability', 'fractions', 'unitConvert']),
            ('Life & Earth Science', ['cell', 'solarSystem', 'waterCycle', 'rockCycle', 'ecosystem', 'decomposer', 'molecule']),
            ('Physics & Chemistry', ['wave', 'circuit', 'chemBalance', 'punnett', 'physics', 'dataPlot']),
        ]
        
        # Extract each tool's full object definition
        tool_objects = {}
        for m in re.finditer(r"(\{[^{}]*?id:\s*'(\w+)'[^{}]*?\})", tool_array_content):
            tool_objects[m.group(2)] = m.group(1)
        
        print("  Parsed %d tool objects" % len(tool_objects))
        
        # Build new array with category dividers
        new_items = []
        for cat_name, cat_tools in cat_order:
            # Add category header (spans full width with col-span-2)
            cat_header = ("{ id: '_cat_" + cat_name.replace(' ', '') + "', "
                         "icon: '', label: '" + cat_name + "', "
                         "desc: '', color: 'slate', category: true }")
            new_items.append(cat_header)
            for tid in cat_tools:
                if tid in tool_objects:
                    new_items.append(tool_objects[tid])
                else:
                    print("  WARNING: Tool '%s' not found in grid" % tid)
        
        # Check for any tools not in categories
        categorized = set()
        for _, cat_tools in cat_order:
            categorized.update(cat_tools)
        uncategorized = [t for t in tools if t not in categorized]
        if uncategorized:
            print("  Uncategorized tools: %s" % ', '.join(uncategorized))
            for tid in uncategorized:
                if tid in tool_objects:
                    new_items.append(tool_objects[tid])
        
        new_array = '[\n      ' + ',\n      '.join(new_items) + '\n      ]'
        
        # Now modify the .map() handler to render category headers differently
        # Find the existing .map(tool => ... handler
        map_handler_start = c.find('].map(tool =>', grid_idx)
        map_handler_end = c.find('tool.desc))))', map_handler_start)
        
        if map_handler_start > 0 and map_handler_end > 0:
            map_handler_end += len('tool.desc))))')
            
            # Build new map handler that handles category headers
            new_map = """].map(tool => tool.category
        ? /*#__PURE__*/React.createElement("div", {
            key: tool.id,
            className: "col-span-2 mt-3 first:mt-0"
          }, /*#__PURE__*/React.createElement("h3", {
            className: "text-sm font-bold text-slate-500 uppercase tracking-wider border-b border-slate-200 pb-1 mb-1"
          }, tool.label))
        : /*#__PURE__*/React.createElement("button", {
        key: tool.id,
        onClick: () => setStemLabTool(tool.id),
        className: `p-5 rounded-2xl border-2 text-left transition-all hover:scale-[1.02] hover:shadow-xl bg-${tool.color}-50 border-${tool.color}-200 hover:border-${tool.color}-400`
      }, /*#__PURE__*/React.createElement("div", {
        className: "text-3xl mb-2"
      }, tool.icon), /*#__PURE__*/React.createElement("h4", {
        className: `font-bold text-sm text-${tool.color}-800 mb-1`
      }, tool.label), /*#__PURE__*/React.createElement("p", {
        className: `text-xs text-${tool.color}-600/70`
      }, tool.desc))))"""
            
            # Replace old array + map with new
            c = c[:bracket_start] + new_array + new_map + c[map_handler_end:]
            print("  OK: Categorized tool grid with section headers")
        else:
            print("  WARNING: Can't find map handler (start=%d, end=%d)" % (map_handler_start, map_handler_end))
    else:
        print("  WARNING: Can't find tool array bounds")

print("\nFinal: %d chars, %d lines" % (len(c), c.count('\n')+1))

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print("\nDone!")
