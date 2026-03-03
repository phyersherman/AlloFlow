"""
STEM Lab Round 2 Enhancement Script
Adds pedagogical depth to Punnett, Probability, Calculus, WaterCycle, RockCycle.
Also fixes the Wave tool comma/paren issues from round 1.
"""

FILE = r"c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\stem_lab_module.js"
with open(FILE, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

print("Original: %d lines" % len(lines))

def find_line(lines, needle, start=0):
    for i in range(start, len(lines)):
        if needle in lines[i]:
            return i
    return -1

def insert_after(lines, line_idx, code_block):
    new_lines = code_block.split('\n')
    for j, nl in enumerate(new_lines):
        lines.insert(line_idx + 1 + j, nl + '\n')
    return len(new_lines)

# ═══════════════════════════════════════════════════
# 1. FIX: Wave tool — the stats line is missing a comma/closing paren
# ═══════════════════════════════════════════════════
print("\n=== Fix: Wave tool syntax ===")

# The issue is around the line with lambda/T/A stats — it needs ), after the text
# Find the problematic pattern
wave_stats_line = find_line(lines, "= ${(2 * Math.PI")
if wave_stats_line >= 0:
    line_content = lines[wave_stats_line].rstrip()
    # Check if it's missing the closing ), 
    if line_content.endswith('`') and not '),' in line_content:
        lines[wave_stats_line] = line_content + '),\n'
        print("  OK: Fixed Wave stats missing ),")
    elif '),' not in line_content and not line_content.endswith('),'):
        # Add ), after the backtick
        lines[wave_stats_line] = line_content + '),\n'
        print("  OK: Fixed Wave stats line")
    else:
        print("  SKIP: Wave stats looks OK")
else:
    print("  SKIP: Wave stats not found")

# Also check for double ), at the end of the wave presets section
wave_double = find_line(lines, "            ),", wave_stats_line + 10 if wave_stats_line >= 0 else 0)
if wave_double >= 0:
    # Check if next line is also ),
    next_line = lines[wave_double + 1].strip() if wave_double + 1 < len(lines) else ''
    if next_line == '),':
        lines.pop(wave_double + 1)
        print("  OK: Removed duplicate ), in Wave")
    else:
        print("  SKIP: No duplicate ), found")

# ═══════════════════════════════════════════════════
# 2. PUNNETT SQUARE — Phenotype Bar Chart + Trait Presets + Educational Tips
# ═══════════════════════════════════════════════════
print("\n=== 2. Punnett: Phenotype chart + trait presets ===")

punnett_tool = find_line(lines, "stemLabTool === 'punnett'")
if punnett_tool >= 0:
    # Find the Snapshot button line
    punnett_snap = find_line(lines, "Punnett snapshot", punnett_tool)
    if punnett_snap >= 0:
        # Insert before the Snapshot line (find the comma + React.createElement above it)
        insert_idx = punnett_snap - 1
        
        punnett_code = """            // ── Trait Presets ──
            React.createElement("div", { className: "mt-3 border-t border-slate-200 pt-3" },
              React.createElement("p", { className: "text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-2" }, "\\uD83E\\uDDEC Quick Crosses"),
              React.createElement("div", { className: "flex flex-wrap gap-1.5" },
                [
                  { label: '\\uD83D\\uDFE4 Heterozygous x Hetero (Bb \\u00D7 Bb)', p1: ['B','b'], p2: ['B','b'], tip: 'Classic 3:1 ratio \\u2014 the Mendelian monohybrid cross' },
                  { label: '\\uD83D\\uDFE4 Hetero x Recessive (Bb \\u00D7 bb)', p1: ['B','b'], p2: ['b','b'], tip: 'Test cross: 1:1 ratio reveals heterozygosity' },
                  { label: '\\uD83D\\uDCA0 Homozygous x Homo (BB \\u00D7 bb)', p1: ['B','B'], p2: ['b','b'], tip: 'All offspring are heterozygous (Bb) \\u2014 100% dominant' },
                  { label: '\\uD83C\\uDF39 Flower Color (Rr \\u00D7 Rr)', p1: ['R','r'], p2: ['R','r'], tip: 'Red flowers (RR, Rr) vs white flowers (rr)' },
                  { label: '\\uD83E\\uDDB7 Tongue Rolling (Tt \\u00D7 Tt)', p1: ['T','t'], p2: ['T','t'], tip: 'Tongue rolling is a dominant trait!' },
                ].map(function(preset) {
                  return React.createElement("button", { key: preset.label, onClick: function() {
                    upd('parent1', preset.p1); upd('parent2', preset.p2);
                    addToast('\\uD83E\\uDDEC ' + preset.tip, 'success');
                  }, className: "px-2 py-1 rounded-lg text-[10px] font-bold bg-violet-50 text-violet-700 border border-violet-200 hover:bg-violet-100 transition-all" }, preset.label);
                })
              ),
              // ── Phenotype Ratio Bar Chart ──
              React.createElement("div", { className: "mt-3 bg-white rounded-lg border p-3" },
                React.createElement("p", { className: "text-[10px] font-bold text-slate-500 mb-2" }, "\\uD83D\\uDCCA Phenotype Distribution"),
                (function() {
                  var domCount = grid.flat().filter(function(g) { return phenotype(g) === 'Dominant'; }).length;
                  var recCount = 4 - domCount;
                  return React.createElement("div", { className: "flex items-end gap-4 justify-center h-20" },
                    React.createElement("div", { className: "flex flex-col items-center" },
                      React.createElement("div", { className: "w-16 bg-emerald-400 rounded-t-lg transition-all", style: { height: (domCount / 4 * 60) + 'px' } }),
                      React.createElement("span", { className: "text-xs font-bold text-emerald-700 mt-1" }, "Dom " + (domCount * 25) + "%")
                    ),
                    React.createElement("div", { className: "flex flex-col items-center" },
                      React.createElement("div", { className: "w-16 bg-amber-400 rounded-t-lg transition-all", style: { height: (recCount / 4 * 60) + 'px' } }),
                      React.createElement("span", { className: "text-xs font-bold text-amber-700 mt-1" }, "Rec " + (recCount * 25) + "%")
                    )
                  );
                })()
              ),
              // ── Educational Callout ──
              React.createElement("p", { className: "mt-2 text-xs text-slate-400 italic" },
                (function() {
                  var domC = grid.flat().filter(function(g) { return phenotype(g) === 'Dominant'; }).length;
                  if (domC === 4) return '\\uD83D\\uDCA1 100% dominant phenotype. At least one parent must be homozygous dominant (BB).';
                  if (domC === 3) return '\\uD83D\\uDCA1 Classic 3:1 ratio! Both parents are heterozygous (Bb) \\u2014 this is Mendel\\u2019s foundational ratio.';
                  if (domC === 2) return '\\uD83D\\uDCA1 1:1 ratio. This is a test cross \\u2014 one parent is heterozygous, the other recessive.';
                  if (domC === 1) return '\\uD83D\\uDCA1 Only 25% dominant. This is unusual \\u2014 check your allele assignments!';
                  return '\\uD83D\\uDCA1 100% recessive. Both parents must be homozygous recessive (bb).';
                })()
              )
            ),"""
        
        inserted = insert_after(lines, insert_idx, punnett_code)
        print("  OK: Inserted %d lines of Punnett enhancements" % inserted)
    else:
        print("  WARNING: Can't find Punnett snapshot")
else:
    print("  WARNING: Can't find Punnett tool")

# ═══════════════════════════════════════════════════
# 3. PROBABILITY — Law of Large Numbers Insight + Expected vs Observed
# ═══════════════════════════════════════════════════
print("\n=== 3. Probability: LLN insight ===")

prob_tool = find_line(lines, "stemLabTool === 'probability'")
if prob_tool >= 0:
    # Find "Law of Large Numbers" text
    lln_line = find_line(lines, "Law of Large Numbers", prob_tool)
    if lln_line >= 0:
        # Insert after the paragraph about LLN
        prob_code = """            d.trials >= 10 && React.createElement("div", { className: "mt-3 bg-violet-50 rounded-xl border border-violet-200 p-3" },
              React.createElement("p", { className: "text-[10px] font-bold text-violet-700 uppercase tracking-wider mb-2" }, "\\uD83D\\uDCCA Statistical Analysis"),
              React.createElement("div", { className: "grid grid-cols-3 gap-2 text-center" },
                React.createElement("div", { className: "p-1.5 bg-white rounded-lg border" },
                  React.createElement("p", { className: "text-[9px] font-bold text-violet-500" }, "Total Trials"),
                  React.createElement("p", { className: "text-lg font-black text-violet-800" }, d.trials)
                ),
                React.createElement("div", { className: "p-1.5 bg-white rounded-lg border" },
                  React.createElement("p", { className: "text-[9px] font-bold text-violet-500" }, "Max Deviation"),
                  React.createElement("p", { className: "text-lg font-black text-violet-800" }, (function() {
                    var maxDev = 0;
                    Object.keys(expected).forEach(function(k) {
                      var observed = (counts[k] || 0) / d.trials;
                      var dev = Math.abs(observed - expected[k]);
                      if (dev > maxDev) maxDev = dev;
                    });
                    return (maxDev * 100).toFixed(1) + '%';
                  })())
                ),
                React.createElement("div", { className: "p-1.5 bg-white rounded-lg border" },
                  React.createElement("p", { className: "text-[9px] font-bold text-violet-500" }, "Fairness"),
                  React.createElement("p", { className: "text-lg font-black " + (function() {
                    var maxDev = 0;
                    Object.keys(expected).forEach(function(k) { var dev = Math.abs((counts[k] || 0) / d.trials - expected[k]); if (dev > maxDev) maxDev = dev; });
                    return maxDev < 0.05 ? 'text-emerald-600' : maxDev < 0.15 ? 'text-yellow-600' : 'text-red-600';
                  })() }, (function() {
                    var maxDev = 0;
                    Object.keys(expected).forEach(function(k) { var dev = Math.abs((counts[k] || 0) / d.trials - expected[k]); if (dev > maxDev) maxDev = dev; });
                    return maxDev < 0.05 ? '\\u2705 Fair' : maxDev < 0.15 ? '\\u26A0 Skewing' : '\\u274C Unfair';
                  })())
                )
              ),
              React.createElement("p", { className: "mt-2 text-xs text-violet-500 italic" },
                d.trials < 30 ? '\\uD83D\\uDCA1 Need more trials! With only ' + d.trials + ' trials, randomness dominates. Try 100+ for reliable patterns.'
                : d.trials < 100 ? '\\uD83D\\uDCA1 Getting better! At ' + d.trials + ' trials, patterns are emerging but may still deviate significantly.'
                : '\\uD83D\\uDCA1 Great sample size! At ' + d.trials + ' trials, the Law of Large Numbers is clearly visible \\u2014 observed frequencies converge toward expected values.'
              )
            ),"""
        inserted = insert_after(lines, lln_line, prob_code)
        print("  OK: Inserted %d lines of Probability analysis" % inserted)
    else:
        print("  WARNING: Can't find LLN text")
else:
    print("  WARNING: Can't find Probability tool")

# ═══════════════════════════════════════════════════
# 4. CALCULUS — Derivative Overlay + Function Presets + Exact Integral Comparison
# ═══════════════════════════════════════════════════
print("\n=== 4. Calculus: Derivative + presets ===")

calc_tool = find_line(lines, "stemLabTool === 'calculus'")
if calc_tool >= 0:
    # Find the sliders section
    calc_sliders = find_line(lines, "Coeff a", calc_tool)
    if calc_sliders >= 0:
        # Find the closing ), of the slider grid
        slider_close = find_line(lines, "),", calc_sliders + 3)
        if slider_close >= 0:
            calc_code = """            React.createElement("div", { className: "mt-3 flex flex-wrap gap-1.5" },
              React.createElement("span", { className: "text-[10px] font-bold text-slate-400 self-center" }, "Presets:"),
              [
                { label: '\\u222B x\\u00B2 [0,1]', a: 1, b: 0, c: 0, xMin: 0, xMax: 1, n: 20, tip: 'Exact answer: 1/3 \\u2248 0.333' },
                { label: '\\u222B x\\u00B2 [0,3]', a: 1, b: 0, c: 0, xMin: 0, xMax: 3, n: 20, tip: 'Exact answer: 9' },
                { label: '\\u222B (x\\u00B2+2x+1) [0,2]', a: 1, b: 2, c: 1, xMin: 0, xMax: 2, n: 20, tip: 'Try increasing n to see convergence!' },
                { label: '\\u222B 2x [0,5]', a: 0, b: 2, c: 0, xMin: 0, xMax: 5, n: 10, tip: 'Linear function \\u2014 exact even with few rectangles' },
                { label: '\\u222B -x\\u00B2+4 [0,2]', a: -1, b: 0, c: 4, xMin: 0, xMax: 2, n: 25, tip: 'A downward parabola \\u2014 find the area under the arch' },
              ].map(function(p) {
                return React.createElement("button", { key: p.label, onClick: function() {
                  upd('a', p.a); upd('b', p.b); upd('c', p.c); upd('xMin', p.xMin); upd('xMax', p.xMax); upd('n', p.n);
                  addToast(p.tip, 'success');
                }, className: "px-2 py-1 rounded-lg text-[10px] font-bold bg-red-50 text-red-700 border border-red-200 hover:bg-red-100 transition-all" }, p.label);
              })
            ),
            React.createElement("div", { className: "mt-2 bg-red-50 rounded-xl border border-red-200 p-3" },
              React.createElement("p", { className: "text-[10px] font-bold text-red-700 uppercase tracking-wider mb-2" }, "\\uD83D\\uDCCA Analysis"),
              React.createElement("div", { className: "grid grid-cols-3 gap-2 text-center" },
                React.createElement("div", { className: "p-1.5 bg-white rounded-lg border" },
                  React.createElement("p", { className: "text-[9px] font-bold text-red-500" }, "Riemann Sum"),
                  React.createElement("p", { className: "text-sm font-bold text-red-800" }, area.toFixed(4))
                ),
                React.createElement("div", { className: "p-1.5 bg-white rounded-lg border" },
                  React.createElement("p", { className: "text-[9px] font-bold text-red-500" }, "Exact (\\u222B)"),
                  React.createElement("p", { className: "text-sm font-bold text-red-800" }, (function() {
                    var exact = (d.a/3)*(Math.pow(d.xMax,3)-Math.pow(d.xMin,3)) + (d.b/2)*(Math.pow(d.xMax,2)-Math.pow(d.xMin,2)) + d.c*(d.xMax-d.xMin);
                    return exact.toFixed(4);
                  })())
                ),
                React.createElement("div", { className: "p-1.5 bg-white rounded-lg border" },
                  React.createElement("p", { className: "text-[9px] font-bold text-red-500" }, "Error"),
                  React.createElement("p", { className: "text-sm font-bold " + (function() {
                    var exact = (d.a/3)*(Math.pow(d.xMax,3)-Math.pow(d.xMin,3)) + (d.b/2)*(Math.pow(d.xMax,2)-Math.pow(d.xMin,2)) + d.c*(d.xMax-d.xMin);
                    var err = Math.abs(area - exact);
                    return err < 0.01 ? 'text-emerald-600' : err < 0.1 ? 'text-yellow-600' : 'text-red-600';
                  })() }, (function() {
                    var exact = (d.a/3)*(Math.pow(d.xMax,3)-Math.pow(d.xMin,3)) + (d.b/2)*(Math.pow(d.xMax,2)-Math.pow(d.xMin,2)) + d.c*(d.xMax-d.xMin);
                    return Math.abs(area - exact).toFixed(4);
                  })())
                )
              ),
              React.createElement("p", { className: "mt-2 text-xs text-red-500 italic" },
                d.n <= 5 ? '\\uD83D\\uDCA1 Very few rectangles! The approximation is rough. Try increasing n.'
                : d.n <= 15 ? '\\uD83D\\uDCA1 Getting closer! More rectangles = better approximation. This is the fundamental idea of integration.'
                : d.n <= 30 ? '\\uD83D\\uDCA1 Good approximation! The error shrinks as n increases (proportional to 1/n\\u00B2 for midpoint).'
                : '\\uD83D\\uDCA1 Excellent! At n=' + d.n + ' rectangles, the Riemann sum closely matches the exact integral. The limit as n\\u2192\\u221E gives the true area.'
              )
            ),"""
            inserted = insert_after(lines, slider_close, calc_code)
            print("  OK: Inserted %d lines of Calculus enhancements" % inserted)
        else:
            print("  WARNING: Can't find slider close")
    else:
        print("  WARNING: Can't find Calculus sliders")
else:
    print("  WARNING: Can't find Calculus tool")

# ═══════════════════════════════════════════════════
# 5. WATER CYCLE — Quiz Mode
# ═══════════════════════════════════════════════════
print("\n=== 5. Water Cycle: Quiz Mode ===")

water_tool = find_line(lines, "stemLabTool === 'waterCycle'")
if water_tool >= 0:
    # Find the Snapshot button
    water_snap = find_line(lines, "tool: 'waterCycle'", water_tool)
    if water_snap >= 0:
        water_snap_line = find_line(lines, "Snapshot", water_snap)
        insert_idx = water_snap_line - 1
        
        water_quiz = """            // ── Water Cycle Quiz ──
            React.createElement("div", { className: "mt-3 border-t border-slate-200 pt-3" },
              React.createElement("button", { onClick: function() {
                var WC_QS = [
                  { q: 'What process turns liquid water into vapor?', a: 'evaporation', opts: ['evaporation', 'condensation', 'precipitation', 'collection'] },
                  { q: 'What forms when water vapor cools in the atmosphere?', a: 'condensation', opts: ['precipitation', 'evaporation', 'condensation', 'transpiration'] },
                  { q: 'Rain, snow, sleet, and hail are all forms of...', a: 'precipitation', opts: ['evaporation', 'transpiration', 'collection', 'precipitation'] },
                  { q: 'Which process involves plants releasing water?', a: 'transpiration', opts: ['transpiration', 'evaporation', 'condensation', 'collection'] },
                  { q: 'Where does water collect after precipitation?', a: 'collection', opts: ['evaporation', 'condensation', 'collection', 'transpiration'] },
                  { q: 'What is the main energy source for the water cycle?', a: 'The Sun', opts: ['Wind', 'The Moon', 'The Sun', 'Gravity'] },
                  { q: 'What percentage of Earth is covered by water?', a: '71%', opts: ['50%', '60%', '71%', '85%'] },
                ];
                var q = WC_QS[Math.floor(Math.random() * WC_QS.length)];
                upd('wcQuiz', { q: q.q, a: q.a, opts: q.opts, answered: false, score: (d.wcQuiz && d.wcQuiz.score) || 0 });
              }, className: "px-3 py-1.5 rounded-lg text-xs font-bold " + (d.wcQuiz ? 'bg-sky-100 text-sky-700' : 'bg-sky-600 text-white') + " transition-all" }, d.wcQuiz ? "\\uD83D\\uDD04 Next Question" : "\\uD83E\\uDDE0 Quiz Mode"),
              d.wcQuiz && d.wcQuiz.score > 0 && React.createElement("span", { className: "ml-2 text-xs font-bold text-emerald-600" }, "\\u2B50 " + d.wcQuiz.score + " correct"),
              d.wcQuiz && React.createElement("div", { className: "mt-2 bg-sky-50 rounded-lg p-3 border border-sky-200" },
                React.createElement("p", { className: "text-sm font-bold text-sky-800 mb-2" }, d.wcQuiz.q),
                React.createElement("div", { className: "grid grid-cols-2 gap-2" },
                  d.wcQuiz.opts.map(function(opt) {
                    var isCorrect = opt === d.wcQuiz.a;
                    var wasChosen = d.wcQuiz.chosen === opt;
                    var cls = !d.wcQuiz.answered ? 'bg-white border-slate-200 hover:border-sky-400' : isCorrect ? 'bg-emerald-100 border-emerald-300' : wasChosen ? 'bg-red-100 border-red-300' : 'bg-slate-50 border-slate-200 opacity-50';
                    return React.createElement("button", { key: opt, disabled: d.wcQuiz.answered, onClick: function() {
                      var correct = opt === d.wcQuiz.a;
                      upd('wcQuiz', Object.assign({}, d.wcQuiz, { answered: true, chosen: opt, score: d.wcQuiz.score + (correct ? 1 : 0) }));
                      addToast(correct ? '\\u2705 Correct!' : '\\u274C The answer is ' + d.wcQuiz.a, correct ? 'success' : 'error');
                    }, className: "px-3 py-2 rounded-lg text-sm font-bold border-2 transition-all capitalize " + cls }, typeof opt === 'string' ? opt.charAt(0).toUpperCase() + opt.slice(1) : opt);
                  })
                )
              )
            ),"""
        
        inserted = insert_after(lines, insert_idx, water_quiz)
        print("  OK: Inserted %d lines of Water Cycle quiz" % inserted)
    else:
        print("  WARNING: Can't find Water Cycle snapshot")
else:
    print("  WARNING: Can't find Water Cycle tool")

# ═══════════════════════════════════════════════════
# 6. ROCK CYCLE — Quiz Mode
# ═══════════════════════════════════════════════════
print("\n=== 6. Rock Cycle: Quiz Mode ===")

rock_tool = find_line(lines, "stemLabTool === 'rockCycle'")
if rock_tool >= 0:
    rock_snap = find_line(lines, "tool: 'rockCycle'", rock_tool)
    if rock_snap >= 0:
        rock_snap_line = find_line(lines, "Snapshot", rock_snap)
        insert_idx = rock_snap_line - 1
        
        rock_quiz = """            // ── Rock Cycle Quiz ──
            React.createElement("div", { className: "mt-3 border-t border-slate-200 pt-3" },
              React.createElement("button", { onClick: function() {
                var RC_QS = [
                  { q: 'Which rock type forms from cooled magma/lava?', a: 'Igneous', opts: ['Igneous', 'Sedimentary', 'Metamorphic'] },
                  { q: 'Which rock type often contains fossils?', a: 'Sedimentary', opts: ['Igneous', 'Sedimentary', 'Metamorphic'] },
                  { q: 'Which rock type forms under heat and pressure?', a: 'Metamorphic', opts: ['Igneous', 'Sedimentary', 'Metamorphic'] },
                  { q: 'Granite is an example of which rock type?', a: 'Igneous', opts: ['Igneous', 'Sedimentary', 'Metamorphic'] },
                  { q: 'Marble forms from which rock?', a: 'Limestone (sedimentary)', opts: ['Granite (igneous)', 'Limestone (sedimentary)', 'Basalt (igneous)'] },
                  { q: 'What breaks rocks into sediment?', a: 'Weathering & erosion', opts: ['Heat & pressure', 'Weathering & erosion', 'Melting'] },
                  { q: 'What must happen for metamorphic rock to become igneous?', a: 'It must melt, then cool', opts: ['It must be weathered', 'It must be compressed', 'It must melt, then cool'] },
                ];
                var q = RC_QS[Math.floor(Math.random() * RC_QS.length)];
                upd('rcQuiz', { q: q.q, a: q.a, opts: q.opts, answered: false, score: (d.rcQuiz && d.rcQuiz.score) || 0 });
              }, className: "px-3 py-1.5 rounded-lg text-xs font-bold " + (d.rcQuiz ? 'bg-orange-100 text-orange-700' : 'bg-orange-600 text-white') + " transition-all" }, d.rcQuiz ? "\\uD83D\\uDD04 Next Question" : "\\uD83E\\uDDE0 Quiz Mode"),
              d.rcQuiz && d.rcQuiz.score > 0 && React.createElement("span", { className: "ml-2 text-xs font-bold text-emerald-600" }, "\\u2B50 " + d.rcQuiz.score + " correct"),
              d.rcQuiz && React.createElement("div", { className: "mt-2 bg-orange-50 rounded-lg p-3 border border-orange-200" },
                React.createElement("p", { className: "text-sm font-bold text-orange-800 mb-2" }, d.rcQuiz.q),
                React.createElement("div", { className: "grid grid-cols-1 gap-2" },
                  d.rcQuiz.opts.map(function(opt) {
                    var isCorrect = opt === d.rcQuiz.a;
                    var wasChosen = d.rcQuiz.chosen === opt;
                    var cls = !d.rcQuiz.answered ? 'bg-white border-slate-200 hover:border-orange-400' : isCorrect ? 'bg-emerald-100 border-emerald-300' : wasChosen ? 'bg-red-100 border-red-300' : 'bg-slate-50 border-slate-200 opacity-50';
                    return React.createElement("button", { key: opt, disabled: d.rcQuiz.answered, onClick: function() {
                      var correct = opt === d.rcQuiz.a;
                      upd('rcQuiz', Object.assign({}, d.rcQuiz, { answered: true, chosen: opt, score: d.rcQuiz.score + (correct ? 1 : 0) }));
                      addToast(correct ? '\\u2705 Correct!' : '\\u274C The answer is ' + d.rcQuiz.a, correct ? 'success' : 'error');
                    }, className: "px-3 py-2 rounded-lg text-sm font-bold border-2 transition-all " + cls }, opt);
                  })
                )
              )
            ),"""
        
        inserted = insert_after(lines, insert_idx, rock_quiz)
        print("  OK: Inserted %d lines of Rock Cycle quiz" % inserted)
    else:
        print("  WARNING: Can't find Rock Cycle snapshot")
else:
    print("  WARNING: Can't find Rock Cycle tool")

# ═══════════════════════════════════════════════════
# 7. CELL DIAGRAM — Additional educational depth (organelle function quiz is already there!)
# ═══════════════════════════════════════════════════
print("\n=== 7. Cell Diagram: Adding function matching ===")

cell_tool = find_line(lines, "stemLabTool === 'cell'")
if cell_tool >= 0:
    # Cell already has quiz mode — add an educational "Organelle Functions" reference card
    cell_snap = find_line(lines, "Cell snapshot", cell_tool)
    if cell_snap >= 0:
        insert_idx = cell_snap - 1
        
        cell_code = """            // ── Organelle Quick Reference ──
            React.createElement("div", { className: "mt-3 bg-green-50 rounded-xl border border-green-200 p-3" },
              React.createElement("p", { className: "text-[10px] font-bold text-green-700 uppercase tracking-wider mb-2" }, "\\uD83D\\uDCD6 Organelle Functions"),
              React.createElement("div", { className: "grid grid-cols-2 gap-1" },
                [
                  ['\\uD83E\\uDDEC Nucleus', 'Control center \\u2014 houses DNA'],
                  ['\\u26A1 Mitochondria', 'Energy production (ATP)'],
                  ['\\uD83C\\uDFED Ribosomes', 'Protein synthesis'],
                  ['\\uD83C\\uDF0A ER', 'Protein & lipid transport'],
                  ['\\uD83D\\uDCE6 Golgi', 'Package & ship proteins'],
                  ['\\u267B Lysosomes', 'Waste disposal'],
                  ['\\uD83D\\uDEE1 Membrane', 'Controls entry/exit'],
                  ['\\uD83D\\uDCA7 Cytoplasm', 'Internal cell fluid'],
                ].concat(d.type === 'plant' ? [
                  ['\\uD83C\\uDF31 Chloroplast', 'Photosynthesis'],
                  ['\\uD83E\\uDDF1 Cell Wall', 'Rigid protection'],
                  ['\\uD83D\\uDCA7 Vacuole', 'Water storage'],
                ] : []).map(function(item) {
                  return React.createElement("div", { key: item[0], className: "flex items-center gap-1 text-[10px] py-0.5" },
                    React.createElement("span", { className: "font-bold text-green-800 w-1/2" }, item[0]),
                    React.createElement("span", { className: "text-slate-500" }, item[1])
                  );
                })
              ),
              d.type === 'plant' && React.createElement("p", { className: "mt-1 text-[10px] text-green-600 italic" }, "\\uD83C\\uDF3F Plant cells have cell walls, chloroplasts, and a large central vacuole that animal cells lack.")
            ),"""
        
        inserted = insert_after(lines, insert_idx, cell_code)
        print("  OK: Inserted %d lines of Cell reference card" % inserted)
    else:
        print("  WARNING: Can't find Cell snapshot")
else:
    print("  WARNING: Can't find Cell tool")

# ═══════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════
print("\n=== Final Validation ===")
content = ''.join(lines)
print("  Total lines: %d" % len(lines))
print("  Total chars: %d" % len(content))

with open(FILE, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\nDone!")
