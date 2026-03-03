"""
STEM Lab Pedagogical Depth Enhancement Script
Adds quiz modes, challenge problems, presets, and enriched educational content
to 6 STEM Lab tools using targeted line-based insertion.

Strategy: For each tool, find its render block and insert new JSX elements
at specific anchor points. Uses line-based search for safety.
"""

FILE = r"c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\stem_lab_module.js"
with open(FILE, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

print("Original: %d lines" % len(lines))

def find_line(lines, needle, start=0):
    """Find the first line containing needle, starting from line index start."""
    for i in range(start, len(lines)):
        if needle in lines[i]:
            return i
    return -1

def insert_after(lines, line_idx, code_block):
    """Insert a code block after the given line index."""
    new_lines = code_block.split('\n')
    for j, nl in enumerate(new_lines):
        lines.insert(line_idx + 1 + j, nl + '\n')
    return len(new_lines)

# ═══════════════════════════════════════════════════
# 1. SOLAR SYSTEM — Quiz Mode + Planet Comparison
# ═══════════════════════════════════════════════════
print("\n=== 1. Solar System: Quiz + Comparison ===")

# Find the Solar System tool — after the planet info card, before Snapshot button
ss_tool = find_line(lines, "stemLabTool === 'solarSystem'")
if ss_tool >= 0:
    # Find the Snapshot button in the solar system block
    ss_snapshot = find_line(lines, "tool: 'solarSystem'", ss_tool)
    if ss_snapshot >= 0:
        # Find the line with the Snapshot button createElement
        ss_snap_line = find_line(lines, "Snapshot", ss_snapshot)
        # Insert quiz + comparison mode BEFORE the snapshot button
        # Find the comma before the snapshot button line
        insert_idx = ss_snap_line - 1
        
        quiz_code = """            // ── Quiz Mode ──
            React.createElement("div", { className: "mt-4 border-t border-slate-200 pt-3" },
              React.createElement("div", { className: "flex items-center gap-2 mb-2" },
                React.createElement("button", { onClick: () => {
                  const QUIZ_QS = [
                    { q: 'Which planet is the hottest?', a: 'Venus', opts: ['Mercury', 'Venus', 'Mars', 'Jupiter'], tip: 'Venus has a runaway greenhouse effect reaching 462\\u00B0C!' },
                    { q: 'Which planet has the most moons?', a: 'Saturn', opts: ['Jupiter', 'Saturn', 'Uranus', 'Neptune'], tip: 'Saturn has 146 known moons as of 2024!' },
                    { q: 'Which planet rotates on its side?', a: 'Uranus', opts: ['Neptune', 'Uranus', 'Saturn', 'Pluto'], tip: 'Uranus has an axial tilt of 97.77\\u00B0!' },
                    { q: 'Which is the smallest planet?', a: 'Mercury', opts: ['Mercury', 'Mars', 'Pluto', 'Venus'], tip: 'Mercury is only 4,879 km in diameter.' },
                    { q: 'Which planet has the longest year?', a: 'Pluto', opts: ['Neptune', 'Pluto', 'Uranus', 'Saturn'], tip: 'Pluto takes 248 Earth years to orbit the Sun!' },
                    { q: 'Which planet has the shortest day?', a: 'Jupiter', opts: ['Jupiter', 'Saturn', 'Earth', 'Mars'], tip: 'Jupiter rotates in just 10 hours!' },
                    { q: 'Which planet is known as the Red Planet?', a: 'Mars', opts: ['Venus', 'Mars', 'Mercury', 'Jupiter'], tip: 'Iron oxide (rust) gives Mars its red color.' },
                    { q: 'Which planet could float in water?', a: 'Saturn', opts: ['Jupiter', 'Saturn', 'Neptune', 'Uranus'], tip: 'Saturn\\u2019s density is less than water (0.687 g/cm\\u00B3)!' },
                    { q: 'Where is the tallest volcano in the solar system?', a: 'Mars', opts: ['Earth', 'Venus', 'Mars', 'Jupiter'], tip: 'Olympus Mons on Mars is 21.9 km high \\u2014 nearly 3x Everest!' },
                    { q: 'Which planet has the strongest winds?', a: 'Neptune', opts: ['Jupiter', 'Saturn', 'Neptune', 'Uranus'], tip: 'Neptune\\u2019s winds reach 2,100 km/h!' },
                  ];
                  const q = QUIZ_QS[Math.floor(Math.random() * QUIZ_QS.length)];
                  upd('quiz', { ...q, answered: false, correct: null, score: d.quiz?.score || 0, streak: d.quiz?.streak || 0 });
                }, className: "px-3 py-1.5 rounded-lg text-xs font-bold " + (d.quiz ? 'bg-indigo-100 text-indigo-700' : 'bg-indigo-600 text-white') + " hover:opacity-90 transition-all" }, d.quiz ? "\\uD83D\\uDD04 Next Question" : "\\uD83E\\uDDE0 Quiz Mode"),
                d.quiz && d.quiz.score > 0 && React.createElement("span", { className: "text-xs font-bold text-emerald-600" }, "\\u2B50 " + d.quiz.score + " correct | \\uD83D\\uDD25 " + d.quiz.streak + " streak")
              ),
              d.quiz && React.createElement("div", { className: "bg-indigo-50 rounded-xl p-4 border border-indigo-200 animate-in slide-in-from-bottom" },
                React.createElement("p", { className: "text-sm font-bold text-indigo-800 mb-3" }, d.quiz.q),
                React.createElement("div", { className: "grid grid-cols-2 gap-2" },
                  d.quiz.opts.map(function(opt) {
                    var isCorrect = opt === d.quiz.a;
                    var wasChosen = d.quiz.chosen === opt;
                    var cls = !d.quiz.answered ? 'bg-white text-slate-700 border-slate-200 hover:border-indigo-400 hover:bg-indigo-50' : isCorrect ? 'bg-emerald-100 text-emerald-800 border-emerald-300' : wasChosen && !isCorrect ? 'bg-red-100 text-red-800 border-red-300' : 'bg-slate-50 text-slate-400 border-slate-200';
                    return React.createElement("button", { key: opt, disabled: d.quiz.answered, onClick: function() {
                      var correct = opt === d.quiz.a;
                      upd('quiz', Object.assign({}, d.quiz, { answered: true, correct: correct, chosen: opt, score: d.quiz.score + (correct ? 1 : 0), streak: correct ? d.quiz.streak + 1 : 0 }));
                      if (correct) addToast('\\u2705 Correct! ' + d.quiz.tip, 'success');
                      else addToast('\\u274C The answer is ' + d.quiz.a + '. ' + d.quiz.tip, 'error');
                    }, className: "px-3 py-2 rounded-lg text-sm font-bold border-2 transition-all " + cls }, opt);
                  })
                ),
                d.quiz.answered && React.createElement("p", { className: "mt-2 text-xs text-indigo-600 italic" }, "\\uD83D\\uDCA1 " + d.quiz.tip)
              ),
              // ── Planet Comparison ──
              React.createElement("div", { className: "mt-3" },
                React.createElement("p", { className: "text-xs font-bold text-slate-500 mb-1" }, "\\uD83D\\uDD0D Compare Planets"),
                React.createElement("div", { className: "flex gap-2 mb-2" },
                  React.createElement("select", { value: d.compare1 || '', onChange: function(e) { upd('compare1', e.target.value); }, className: "flex-1 px-2 py-1 border rounded text-sm" },
                    React.createElement("option", { value: "" }, "Select..."),
                    PLANETS.map(function(p) { return React.createElement("option", { key: p.name, value: p.name }, p.name); })
                  ),
                  React.createElement("span", { className: "text-slate-400 font-bold self-center" }, "vs"),
                  React.createElement("select", { value: d.compare2 || '', onChange: function(e) { upd('compare2', e.target.value); }, className: "flex-1 px-2 py-1 border rounded text-sm" },
                    React.createElement("option", { value: "" }, "Select..."),
                    PLANETS.map(function(p) { return React.createElement("option", { key: p.name, value: p.name }, p.name); })
                  )
                ),
                d.compare1 && d.compare2 && (function() {
                  var p1 = PLANETS.find(function(p) { return p.name === d.compare1; });
                  var p2 = PLANETS.find(function(p) { return p.name === d.compare2; });
                  if (!p1 || !p2) return null;
                  var GRAVITY = { Mercury: 0.38, Venus: 0.91, Earth: 1.0, Mars: 0.38, Jupiter: 2.34, Saturn: 1.06, Uranus: 0.92, Neptune: 1.19, Pluto: 0.06 };
                  return React.createElement("div", { className: "grid grid-cols-3 gap-1 text-center text-xs" },
                    [['', p1.name, p2.name], ['\\uD83C\\uDF21 Temp', p1.temp, p2.temp], ['\\u2600 Day', p1.dayLen, p2.dayLen], ['\\uD83C\\uDF0D Year', p1.yearLen, p2.yearLen], ['\\uD83D\\uDCCF Size', p1.diameter, p2.diameter], ['\\uD83C\\uDF11 Moons', p1.moons, p2.moons], ['\\u2696 Gravity', (GRAVITY[p1.name] || 1).toFixed(2) + 'g', (GRAVITY[p2.name] || 1).toFixed(2) + 'g'], ['\\uD83E\\uDDD1 70kg on', Math.round(70 * (GRAVITY[p1.name] || 1)) + 'kg', Math.round(70 * (GRAVITY[p2.name] || 1)) + 'kg']].map(function(row, ri) {
                      return React.createElement(React.Fragment, { key: ri },
                        row.map(function(cell, ci) {
                          return React.createElement("div", { key: ci, className: "py-1 " + (ri === 0 ? 'font-black text-slate-700' : ci === 0 ? 'font-bold text-slate-500' : 'font-bold text-slate-700') + (ri > 0 && ri % 2 === 0 ? ' bg-slate-50' : '') }, cell);
                        })
                      );
                    })
                  );
                })()
              )
            ),"""
        
        inserted = insert_after(lines, insert_idx, quiz_code)
        print("  OK: Inserted %d lines of quiz + comparison code" % inserted)
    else:
        print("  WARNING: Can't find Solar System snapshot")
else:
    print("  WARNING: Can't find Solar System tool")

# ═══════════════════════════════════════════════════
# 2. ECOSYSTEM — Presets + Phase Portrait
# ═══════════════════════════════════════════════════
print("\n=== 2. Ecosystem: Presets + Phase Portrait ===")

eco_tool = find_line(lines, "stemLabTool === 'ecosystem'")
if eco_tool >= 0:
    # Insert presets after the description paragraph
    eco_desc = find_line(lines, "Lotka-Volterra", eco_tool)
    if eco_desc >= 0:
        presets_code = """            React.createElement("div", { className: "flex flex-wrap gap-1.5 mb-3" },
              [
                { label: '\\uD83D\\uDC07\\uD83D\\uDC3A Balanced', prey0: 80, pred0: 30, preyBirth: 0.1, preyDeath: 0.01, predBirth: 0.01, predDeath: 0.1 },
                { label: '\\uD83D\\uDCA5 Extinction Spiral', prey0: 30, pred0: 80, preyBirth: 0.05, preyDeath: 0.02, predBirth: 0.01, predDeath: 0.05 },
                { label: '\\uD83D\\uDCC8 Population Boom', prey0: 50, pred0: 10, preyBirth: 0.3, preyDeath: 0.005, predBirth: 0.005, predDeath: 0.15 },
                { label: '\\u2696 Equilibrium', prey0: 100, pred0: 50, preyBirth: 0.1, preyDeath: 0.01, predBirth: 0.005, predDeath: 0.1 },
              ].map(function(preset) {
                return React.createElement("button", { key: preset.label, onClick: function() {
                  upd('prey0', preset.prey0); upd('pred0', preset.pred0);
                  upd('preyBirth', preset.preyBirth); upd('preyDeath', preset.preyDeath);
                  upd('predBirth', preset.predBirth); upd('predDeath', preset.predDeath);
                  upd('data', []); upd('steps', 0);
                }, className: "px-2.5 py-1 rounded-lg text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200 hover:bg-emerald-100 transition-all" }, preset.label);
              })
            ),"""
        inserted = insert_after(lines, eco_desc, presets_code)
        print("  OK: Inserted %d lines of presets" % inserted)
        
        # Find the SVG chart end and add phase portrait after it
        eco_svg_end = find_line(lines, "Predators\")", eco_tool + inserted)
        if eco_svg_end >= 0:
            # Find the closing of the SVG
            eco_svg_close = find_line(lines, "),", eco_svg_end)
            if eco_svg_close >= 0:
                phase_code = """            d.data.length > 0 && React.createElement("div", { className: "mt-3" },
              React.createElement("p", { className: "text-xs font-bold text-slate-500 mb-1" }, "\\uD83D\\uDD04 Phase Portrait (Prey vs Predator)"),
              React.createElement("svg", { viewBox: "0 0 300 300", className: "w-full bg-white rounded-xl border border-emerald-200", style: { maxHeight: "260px" } },
                React.createElement("line", { x1: 30, y1: 270, x2: 270, y2: 270, stroke: "#e2e8f0", strokeWidth: 1 }),
                React.createElement("line", { x1: 30, y1: 30, x2: 30, y2: 270, stroke: "#e2e8f0", strokeWidth: 1 }),
                React.createElement("text", { x: 150, y: 295, textAnchor: "middle", fill: "#22c55e", style: { fontSize: '10px', fontWeight: 'bold' } }, "Prey Population"),
                React.createElement("text", { x: 10, y: 150, textAnchor: "middle", fill: "#ef4444", style: { fontSize: '10px', fontWeight: 'bold' }, transform: "rotate(-90,10,150)" }, "Predator Population"),
                React.createElement("polyline", { points: d.data.map(function(dp) {
                  return (30 + dp.prey / maxVal * 240) + "," + (270 - dp.pred / maxVal * 240);
                }).join(" "), fill: "none", stroke: "#6366f1", strokeWidth: 1.5 }),
                React.createElement("circle", { cx: 30 + d.data[0].prey / maxVal * 240, cy: 270 - d.data[0].pred / maxVal * 240, r: 4, fill: "#22c55e" }),
                React.createElement("circle", { cx: 30 + d.data[d.data.length-1].prey / maxVal * 240, cy: 270 - d.data[d.data.length-1].pred / maxVal * 240, r: 4, fill: "#ef4444" }),
                React.createElement("text", { x: 35 + d.data[0].prey / maxVal * 240, y: 270 - d.data[0].pred / maxVal * 240 - 8, fill: "#22c55e", style: { fontSize: '8px', fontWeight: 'bold' } }, "Start"),
                React.createElement("text", { x: 35 + d.data[d.data.length-1].prey / maxVal * 240, y: 270 - d.data[d.data.length-1].pred / maxVal * 240 - 8, fill: "#ef4444", style: { fontSize: '8px', fontWeight: 'bold' } }, "End")
              ),
              React.createElement("div", { className: "mt-2 grid grid-cols-3 gap-2 text-center" },
                React.createElement("div", { className: "p-1.5 bg-emerald-50 rounded-lg border border-emerald-200" },
                  React.createElement("p", { className: "text-[9px] font-bold text-emerald-600 uppercase" }, "Peak Prey"),
                  React.createElement("p", { className: "text-sm font-bold text-emerald-800" }, Math.max.apply(null, d.data.map(function(dp) { return dp.prey; })))
                ),
                React.createElement("div", { className: "p-1.5 bg-red-50 rounded-lg border border-red-200" },
                  React.createElement("p", { className: "text-[9px] font-bold text-red-600 uppercase" }, "Peak Predators"),
                  React.createElement("p", { className: "text-sm font-bold text-red-800" }, Math.max.apply(null, d.data.map(function(dp) { return dp.pred; })))
                ),
                React.createElement("div", { className: "p-1.5 bg-indigo-50 rounded-lg border border-indigo-200" },
                  React.createElement("p", { className: "text-[9px] font-bold text-indigo-600 uppercase" }, "Cycles"),
                  React.createElement("p", { className: "text-sm font-bold text-indigo-800" }, (function() { var peaks = 0; for (var i = 2; i < d.data.length; i++) { if (d.data[i-1].prey > d.data[i-2].prey && d.data[i-1].prey > d.data[i].prey) peaks++; } return peaks; })())
                )
              ),
              React.createElement("p", { className: "mt-2 text-xs text-slate-400 italic text-center" }, "\\uD83D\\uDCA1 The phase portrait shows the classic Lotka-Volterra orbit. Closed loops indicate stable oscillations.")
            ),"""
                inserted2 = insert_after(lines, eco_svg_close, phase_code)
                print("  OK: Inserted %d lines of phase portrait" % inserted2)
            else:
                print("  WARNING: Can't find SVG close")
        else:
            print("  WARNING: Can't find SVG end")
    else:
        print("  WARNING: Can't find ecosystem description")
else:
    print("  WARNING: Can't find ecosystem tool")

# ═══════════════════════════════════════════════════
# 3. WAVE SIMULATOR — Wavelength Markers + Presets
# ═══════════════════════════════════════════════════
print("\n=== 3. Wave: Presets + Musical Notes ===")

wave_tool = find_line(lines, "stemLabTool === 'wave'")
if wave_tool >= 0:
    # Find the stats line with lambda/T/A
    wave_stats = find_line(lines, "= ${(2 * Math.PI", wave_tool)
    if wave_stats >= 0:
        wave_presets = """            React.createElement("div", { className: "mt-2 flex flex-wrap gap-1.5" },
              React.createElement("span", { className: "text-[10px] font-bold text-slate-400 self-center" }, "Presets:"),
              [
                { label: '\\uD83C\\uDFB5 Concert A (440Hz)', amp: 1, freq: 1, phase: 0, tip: 'The standard tuning pitch for musical instruments' },
                { label: '\\uD83C\\uDF0A Ocean Wave', amp: 1.5, freq: 0.3, phase: 0, tip: 'Long wavelength, low frequency \\u2014 like an ocean swell' },
                { label: '\\u26A1 High Energy', amp: 0.8, freq: 3.5, phase: 0, tip: 'Higher frequency = higher energy (E = hf)' },
                { label: '\\uD83D\\uDCA5 Destructive', amp: 1, freq: 1, phase: 3.14, tip: 'Two waves 180\\u00B0 out of phase cancel out completely!' },
              ].map(function(p) {
                return React.createElement("button", { key: p.label, onClick: function() {
                  upd('amplitude', p.amp); upd('frequency', p.freq); upd('phase', p.phase);
                  if (p.label.includes('Destructive')) { upd('wave2', true); upd('amp2', 1); upd('freq2', 1); }
                  addToast(p.tip, 'success');
                }, className: "px-2 py-1 rounded-lg text-[10px] font-bold bg-cyan-50 text-cyan-700 border border-cyan-200 hover:bg-cyan-100 transition-all" }, p.label);
              })
            ),
            React.createElement("div", { className: "mt-2 grid grid-cols-4 gap-1.5 text-center" },
              [
                ['\\uD83C\\uDFB5', 'Note', (function() { var notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']; var f = d.frequency * 110; var n = Math.round(12 * Math.log2(f / 440) + 69); return n >= 0 && n < 128 ? notes[n % 12] + Math.floor(n / 12 - 1) : '\\u2014'; })()],
                ['\\uD83C\\uDF0A', 'Wavelength', (2 * Math.PI / d.frequency).toFixed(2) + ' units'],
                ['\\u23F1', 'Period', (1 / d.frequency).toFixed(2) + 's'],
                ['\\u26A1', 'Energy', d.amplitude > 1.5 ? 'High' : d.amplitude > 0.8 ? 'Medium' : 'Low'],
              ].map(function(item) {
                return React.createElement("div", { key: item[1], className: "p-1 bg-cyan-50/50 rounded-lg border border-cyan-100" },
                  React.createElement("p", { className: "text-[9px] text-cyan-500 font-bold" }, item[0] + ' ' + item[1]),
                  React.createElement("p", { className: "text-xs font-bold text-cyan-800" }, item[2])
                );
              })
            ),"""
        inserted = insert_after(lines, wave_stats, wave_presets)
        print("  OK: Inserted %d lines of wave presets + notes" % inserted)
    else:
        print("  WARNING: Can't find wave stats")
else:
    print("  WARNING: Can't find wave tool")

# ═══════════════════════════════════════════════════
# 4. DATA PLOTTER — Correlation Strength + Presets
# ═══════════════════════════════════════════════════
print("\n=== 4. Data Plotter: Correlation + Presets ===")

data_tool = find_line(lines, "stemLabTool === 'dataPlot'")
if data_tool >= 0:
    # Find the subtitle line
    data_subtitle = find_line(lines, "Auto-calculates linear regression", data_tool)
    if data_subtitle >= 0:
        data_presets = """            React.createElement("div", { className: "flex flex-wrap gap-1.5 mb-2" },
              React.createElement("span", { className: "text-[10px] font-bold text-slate-400 self-center" }, "Datasets:"),
              [
                { label: '\\uD83D\\uDCCA Height vs Weight', pts: [{x:150,y:50},{x:155,y:52},{x:160,y:58},{x:165,y:62},{x:170,y:68},{x:175,y:72},{x:180,y:78},{x:185,y:82},{x:190,y:88}] },
                { label: '\\uD83D\\uDCDA Study vs Grade', pts: [{x:0,y:55},{x:1,y:62},{x:2,y:68},{x:3,y:72},{x:4,y:78},{x:5,y:85},{x:6,y:88},{x:7,y:92},{x:8,y:95}] },
                { label: '\\uD83C\\uDF21 Temp vs Ice Cream', pts: [{x:15,y:20},{x:18,y:35},{x:22,y:45},{x:25,y:60},{x:28,y:70},{x:30,y:85},{x:33,y:90},{x:35,y:95}] },
                { label: '\\uD83C\\uDFB2 Random (No Corr)', pts: Array.from({length: 12}, function() { return {x: Math.round(Math.random()*10*10)/10, y: Math.round(Math.random()*10*10)/10}; }) },
              ].map(function(ds) {
                return React.createElement("button", { key: ds.label, onClick: function() { upd('points', ds.pts); }, className: "px-2 py-1 rounded-lg text-[10px] font-bold bg-teal-50 text-teal-700 border border-teal-200 hover:bg-teal-100 transition-all" }, ds.label);
              })
            ),"""
        inserted = insert_after(lines, data_subtitle, data_presets)
        print("  OK: Inserted %d lines of data presets" % inserted)
        
        # Add correlation strength indicator after the existing stats
        # Find "r\\u00B2 =" or "r² =" in the data plotter
        corr_line = find_line(lines, "r2.toFixed(3)", data_tool + inserted)
        if corr_line >= 0:
            corr_code = """            d.points.length >= 2 && React.createElement("div", { className: "mt-2 bg-white rounded-lg border p-2" },
              React.createElement("p", { className: "text-[10px] font-bold text-slate-500 mb-1" }, "Correlation Strength"),
              React.createElement("div", { className: "flex items-center gap-2" },
                React.createElement("div", { className: "flex-1 h-3 bg-slate-100 rounded-full overflow-hidden" },
                  React.createElement("div", { style: { width: (Math.abs(r2) * 100) + '%', height: '100%', borderRadius: '9999px', backgroundColor: Math.abs(r2) > 0.8 ? '#22c55e' : Math.abs(r2) > 0.5 ? '#eab308' : Math.abs(r2) > 0.3 ? '#f97316' : '#ef4444', transition: 'all 0.5s' } })
                ),
                React.createElement("span", { className: "text-xs font-bold " + (Math.abs(r2) > 0.8 ? 'text-emerald-600' : Math.abs(r2) > 0.5 ? 'text-yellow-600' : Math.abs(r2) > 0.3 ? 'text-orange-600' : 'text-red-500') }, Math.abs(r2) > 0.9 ? '\\u2B50 Very Strong' : Math.abs(r2) > 0.7 ? 'Strong' : Math.abs(r2) > 0.5 ? 'Moderate' : Math.abs(r2) > 0.3 ? 'Weak' : 'Very Weak'),
                React.createElement("span", { className: "text-[10px] text-slate-400" }, slope > 0 ? '\\u2197 Positive' : slope < 0 ? '\\u2198 Negative' : '\\u2794 None')
              ),
              React.createElement("p", { className: "text-[10px] text-slate-400 mt-1 italic" }, r2 > 0.9 ? '\\uD83D\\uDCA1 Almost a perfect linear relationship!' : r2 > 0.7 ? '\\uD83D\\uDCA1 Strong trend \\u2014 a linear model fits well.' : r2 > 0.4 ? '\\uD83D\\uDCA1 Some relationship, but other factors may be at play.' : '\\uD83D\\uDCA1 Weak or no linear relationship. Try a different model?')
            ),"""
            inserted2 = insert_after(lines, corr_line, corr_code)
            print("  OK: Inserted %d lines of correlation strength" % inserted2)
        else:
            print("  WARNING: Can't find r2 display")
    else:
        print("  WARNING: Can't find data subtitle")
else:
    print("  WARNING: Can't find data plotter tool")

# ═══════════════════════════════════════════════════
# 5. CIRCUIT BUILDER — Per-Component Power Display
# ═══════════════════════════════════════════════════
print("\n=== 5. Circuit: Per-Component Power ===")

circuit_tool = find_line(lines, "stemLabTool === 'circuit'")
if circuit_tool >= 0:
    # Find the existing stats grid (Mode, Resistance, Current, Power)
    circuit_stats = find_line(lines, "'Power'", circuit_tool)
    if circuit_stats >= 0:
        # Find the closing of the stats grid
        stats_close = find_line(lines, "),", circuit_stats)
        if stats_close >= 0:
            circuit_extra = """            d.components.length > 0 && React.createElement("div", { className: "mt-3 bg-yellow-50 rounded-xl border border-yellow-200 p-3" },
              React.createElement("p", { className: "text-[10px] font-bold text-yellow-700 uppercase tracking-wider mb-2" }, "\\u26A1 Per-Component Analysis"),
              React.createElement("div", { className: "space-y-1" },
                d.components.map(function(comp, i) {
                  var compR = comp.value || 1;
                  var compI = mode === 'series' ? current : d.voltage / compR;
                  var compV = mode === 'series' ? current * compR : d.voltage;
                  var compP = compV * compI;
                  return React.createElement("div", { key: comp.id, className: "flex items-center gap-2 text-xs bg-white rounded-lg px-2 py-1 border" },
                    React.createElement("span", { className: "font-bold text-yellow-700 w-16" }, (comp.type === 'resistor' ? '\\u2AE8 R' : '\\uD83D\\uDCA1 B') + (i + 1)),
                    React.createElement("span", { className: "text-slate-500 w-16" }, comp.value + '\\u03A9'),
                    React.createElement("span", { className: "text-blue-600 w-20 font-mono" }, compV.toFixed(2) + 'V'),
                    React.createElement("span", { className: "text-emerald-600 w-20 font-mono" }, compI.toFixed(3) + 'A'),
                    React.createElement("span", { className: "text-red-600 w-20 font-mono font-bold" }, compP.toFixed(2) + 'W'),
                    comp.type === 'bulb' && React.createElement("span", { className: "text-yellow-500" }, compP > 10 ? '\\uD83D\\uDD06' : compP > 3 ? '\\uD83D\\uDCA1' : '\\uD83D\\uDD05')
                  );
                })
              ),
              React.createElement("div", { className: "mt-2 flex items-center gap-2 text-[10px] text-slate-400" },
                React.createElement("span", null, "\\u2696 V = IR"),
                React.createElement("span", null, "\\u2022"),
                React.createElement("span", null, "P = IV"),
                React.createElement("span", null, "\\u2022"),
                React.createElement("span", null, mode === 'series' ? 'Series: same current through all' : 'Parallel: same voltage across all')
              )
            ),
            React.createElement("div", { className: "mt-3 bg-amber-50 rounded-xl border border-amber-200 p-3" },
              React.createElement("p", { className: "text-[10px] font-bold text-amber-700 uppercase tracking-wider mb-2" }, "\\uD83C\\uDFAF Circuit Challenge"),
              React.createElement("div", { className: "flex gap-2" },
                [
                  { label: 'Get 2A current', target: 2, type: 'current' },
                  { label: 'Get 0.5A current', target: 0.5, type: 'current' },
                  { label: 'Total R = 200\\u03A9', target: 200, type: 'resistance' },
                ].map(function(ch) {
                  var actual = ch.type === 'current' ? current : totalR;
                  var close = Math.abs(actual - ch.target) < ch.target * 0.05;
                  return React.createElement("button", { key: ch.label, onClick: function() {
                    if (close) { addToast('\\u2705 Challenge complete! You hit ' + actual.toFixed(3) + ' (target: ' + ch.target + ')', 'success'); }
                    else { addToast('\\uD83C\\uDFAF Target: ' + ch.target + (ch.type === 'current' ? 'A' : '\\u03A9') + ' | Current: ' + actual.toFixed(3) + '. Adjust components!', 'info'); }
                    upd('challenge', ch);
                  }, className: "px-2 py-1 rounded-lg text-[10px] font-bold border transition-all " + (close ? 'bg-emerald-100 text-emerald-700 border-emerald-300' : 'bg-white text-amber-700 border-amber-200 hover:bg-amber-50') }, (close ? '\\u2705 ' : '\\uD83C\\uDFAF ') + ch.label);
                })
              )
            ),"""
            inserted = insert_after(lines, stats_close, circuit_extra)
            print("  OK: Inserted %d lines of per-component + challenges" % inserted)
        else:
            print("  WARNING: Can't find stats close")
    else:
        print("  WARNING: Can't find circuit stats")
else:
    print("  WARNING: Can't find circuit tool")

# ═══════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════
print("\n=== Validation ===")
content = ''.join(lines)

# Check bracket balance (ignoring strings)
paren_d = 0
bracket_d = 0
for ch in content:
    if ch == '(': paren_d += 1
    elif ch == ')': paren_d -= 1
    elif ch == '[': bracket_d += 1
    elif ch == ']': bracket_d -= 1

print("  Paren balance: %d (raw)" % paren_d)
print("  Bracket balance: %d (raw)" % bracket_d)
print("  Total lines: %d" % len(lines))

# Write the enhanced file
with open(FILE, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\nDone! Written %d lines." % len(lines))
