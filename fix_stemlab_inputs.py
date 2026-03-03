with open(r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt', 'r', encoding='utf-8') as f:
    text = f.read()

old1 = "dataPlot: { points: [], trendLine: null, equation: '', challenge: null, feedback: null }"
new1 = "dataPlot: { points: [], trendLine: null, equation: '', tableMode: false, challenge: null, feedback: null }"

old2 = "cell: { selectedOrganelle: null, labels: true, type: 'animal', challenge: null, feedback: null }"
new2 = "cell: { selectedOrganelle: null, labels: true, type: 'animal', quizMode: false, quizTarget: null, quizFeedback: null, challenge: null, feedback: null }"

c1 = text.count(old1)
c2 = text.count(old2)
print(f"Found {c1} dataPlot matches, {c2} cell matches")

text = text.replace(old1, new1, 1)
text = text.replace(old2, new2, 1)

with open(r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print('Fixed labToolData initial state for dataPlot.tableMode and cell.quizMode')
