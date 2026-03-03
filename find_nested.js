const fs = require('fs');
const content = fs.readFileSync('AlloFlowANTI.txt', 'utf8');
const lines = content.split('\n');

const lineStarts = [0];
for (let i = 0; i < content.length; i++) {
    if (content[i] === '\n') lineStarts.push(i + 1);
}
function getLine(pos) {
    let lo = 0, hi = lineStarts.length - 1;
    while (lo < hi) {
        const mid = (lo + hi + 1) >> 1;
        if (lineStarts[mid] <= pos) lo = mid; else hi = mid - 1;
    }
    return lo + 1;
}

const buttonOpenRe = /<button[\s>]/g;
let match;
const events = [];

while ((match = buttonOpenRe.exec(content)) !== null) {
    const pos = match.index;
    let braceDepth = 0;
    let isSelfClosing = false;
    let tagEnd = -1;

    for (let i = pos + 1; i < content.length; i++) {
        const ch = content[i];
        if (ch === '{') braceDepth++;
        else if (ch === '}') braceDepth--;
        else if (braceDepth === 0 && ch === '>') {
            let j = i - 1;
            while (j >= pos && /\s/.test(content[j])) j--;
            if (j >= pos && content[j] === '/') isSelfClosing = true;
            tagEnd = i;
            break;
        }
    }

    if (!isSelfClosing && tagEnd > 0) {
        events.push({ pos, line: getLine(pos), type: 'open' });
    }
}

const closeRe = /<\/button>/g;
while ((match = closeRe.exec(content)) !== null) {
    events.push({ pos: match.index, line: getLine(match.index), type: 'close' });
}

events.sort((a, b) => a.pos - b.pos);

let depth = 0;
const stack = [];

for (const ev of events) {
    if (ev.type === 'open') {
        depth++;
        stack.push(ev.line);
        if (depth >= 2) {
            const parentLine = stack[stack.length - 2];
            console.log(`NESTED at line ${ev.line}, parent at line ${parentLine}`);
            console.log(`  Parent: ${lines[parentLine - 1].trim().substring(0, 100)}`);
            console.log(`  Child:  ${lines[ev.line - 1].trim().substring(0, 100)}`);
        }
    } else {
        depth = Math.max(0, depth - 1);
        if (stack.length > 0) stack.pop();
    }
}

console.log(`\nBalance: ${events.filter(e => e.type === 'open').length} opens, ${events.filter(e => e.type === 'close').length} closes, final depth=${depth}`);
