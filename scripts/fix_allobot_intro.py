"""Fix AlloBot intro - using line numbers directly."""

FILE = r"c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt"

with open(FILE, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

print("Total lines:", len(lines))

# Line 10523 (0-indexed: 10522) should have "canPlayIntro && !hasSeenBotIntro"
line = lines[10522]
print("L10523:", line.strip()[:200])

# Check: does it contain hasSeenBotIntro?
if 'hasSeenBotIntro' in line:
    # Fix 1: Remove !hasSeenBotIntro gate
    lines[10522] = line.replace('!hasSeenBotIntro && ', '')
    print("  -> Removed !hasSeenBotIntro")
else:
    print("  -> hasSeenBotIntro NOT found at this line. Searching...")
    for i in range(10510, 10550):
        if 'hasSeenBotIntro' in lines[i]:
            print("  Found at L%d: %s" % (i+1, lines[i].strip()[:200]))
            lines[i] = lines[i].replace('!hasSeenBotIntro && ', '')
            print("  -> Fixed!")
            break

# Fix 2: Change speak to use welcome message
for i in range(10522, 10545):
    if "bot_events.intro_greeting" in lines[i] and 'speak' in lines[i]:
        indent = '            '
        lines[i] = indent + "const welcomeMsg = t('sidebar.ai_guide_welcome');\r\n"
        lines.insert(i+1, indent + "if (welcomeMsg && welcomeMsg !== 'sidebar.ai_guide_welcome') {\r\n")
        lines.insert(i+2, indent + "    speak(welcomeMsg);\r\n")
        lines.insert(i+3, indent + "}\r\n")
        print("  -> Changed speak to welcome message at L%d" % (i+1))
        break

# Fix 3: fix deps array - remove hasSeenBotIntro
for i in range(10522, 10560):
    if 'hasSeenBotIntro' in lines[i] and 'onBotIntroSeen' in lines[i]:
        lines[i] = lines[i].replace('hasSeenBotIntro, ', '')
        print("  -> Removed hasSeenBotIntro from deps at L%d" % (i+1))
        break

# Fix 4: increase delay from 2000 to 2500
for i in range(10522, 10555):
    if '}, 2000)' in lines[i]:
        lines[i] = lines[i].replace('}, 2000)', '}, 2500)')
        print("  -> Increased delay to 2500ms at L%d" % (i+1))
        break

with open(FILE, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("SUCCESS! File saved.")
