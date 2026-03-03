const fs = require('fs');
const content = fs.readFileSync('AlloFlowANTI.txt', 'utf8');

function findButtonTags(content) {
    const tags = [];
    let i = 0;

    while (i < content.length) {
        if (content[i] === '<' && (content.substring(i, i + 7) === '<button' || content.substring(i, i + 8) === '</button')) {
            const isClose = content[i + 1] === '/';
            const tagStart = i;

            let lineNum = 1;
            for (let j = 0; j < tagStart; j++) {
                if (content[j] === '\n') lineNum++;
            }

            if (isClose) {
                const closeIdx = content.indexOf('>', i);
                if (closeIdx !== -1) {
                    tags.push({ type: 'close', line: lineNum, start: tagStart, end: closeIdx });
                    i = closeIdx + 1;
                    continue;
                }
            } else {
                i += 7;

                let braceDepth = 0;
                let inString = false;
                let stringChar = '';
                let inTemplate = false;
                let foundClose = false;

                while (i < content.length) {
                    const ch = content[i];

                    if (inString) {
                        if (ch === '\\' && i + 1 < content.length) { i += 2; continue; }
                        if (ch === stringChar) inString = false;
                        i++;
                        continue;
                    }

                    if (inTemplate) {
                        if (ch === '\\' && i + 1 < content.length) { i += 2; continue; }
                        if (ch === '`') inTemplate = false;
                        i++;
                        continue;
                    }

                    if (ch === '`') { inTemplate = true; i++; continue; }
                    if (ch === '"' || ch === "'") { inString = true; stringChar = ch; i++; continue; }
                    if (ch === '{') { braceDepth++; i++; continue; }
                    if (ch === '}') { braceDepth--; i++; continue; }

                    if (braceDepth === 0 && ch === '>') {
                        const isSelfClose = content[i - 1] === '/';
                        tags.push({ type: isSelfClose ? 'selfclose' : 'open', line: lineNum, start: tagStart, end: i });
                        foundClose = true;
                        i++;
                        break;
                    }
                    i++;
                }
                if (!foundClose) console.log('WARNING: Unclosed tag at line ' + lineNum);
                continue;
            }
        }
        i++;
    }
    return tags;
}

const tags = findButtonTags(content);
const lines = content.split('\n');

const result = [];
result.push('Open: ' + tags.filter(t => t.type === 'open').length);
result.push('SelfClose: ' + tags.filter(t => t.type === 'selfclose').length);
result.push('Close: ' + tags.filter(t => t.type === 'close').length);
result.push('Total: ' + tags.length);

const stack = [];
const nested = [];

for (const tok of tags) {
    if (tok.type === 'selfclose') {
        if (stack.length > 0) nested.push({ childLine: tok.line, parentLine: stack[stack.length - 1].line });
    } else if (tok.type === 'open') {
        if (stack.length > 0) nested.push({ childLine: tok.line, parentLine: stack[stack.length - 1].line });
        stack.push(tok);
    } else if (tok.type === 'close') {
        if (stack.length > 0) stack.pop();
    }
}

result.push('');
result.push('NESTED BUTTONS: ' + nested.length);
for (const n of nested) {
    result.push('');
    result.push('CHILD L' + n.childLine + ': ' + lines[n.childLine - 1].trim().substring(0, 120));
    result.push('PARENT L' + n.parentLine + ': ' + lines[n.parentLine - 1].trim().substring(0, 120));
}

fs.writeFileSync('nested_result2.txt', result.join('\n'), 'utf8');
console.log('Done. Nested count: ' + nested.length);
