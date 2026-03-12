---
name: cdn-module-management
description: Safe editing and deployment of the 4 CDN-loaded JavaScript modules (stem_lab, word_sounds, behavior_lens, report_writer)
---

# CDN Module Management Skill

## Context
AlloFlow loads 4 heavy modules via CDN (`cdn.jsdelivr.net`) at runtime. They are **not bundled** into the React build — they run as standalone scripts that register themselves on `window`.

| Module | File | Size | Port |
|--------|------|------|------|
| STEM Lab | `stem_lab_module.js` | ~2.3 MB | `window.__STEM_LAB_MODULE__` |
| Word Sounds | `word_sounds_module.js` | ~935 KB | `window.__WORD_SOUNDS_MODULE__` |
| BehaviorLens | `behavior_lens_module.js` | ~1.3 MB | `window.__BEHAVIOR_LENS_MODULE__` |
| Report Writer | `report_writer_module.js` | ~166 KB | `window.__REPORT_WRITER_MODULE__` |

## CDN URL Format
```
https://cdn.jsdelivr.net/gh/Apomera/AlloFlow@{COMMIT_HASH}/{filename}
```
The commit hash is baked into `AlloFlowANTI.txt` during build via `build.js --mode=prod`.

## Safe Editing Workflow

### 1. Edit the module file directly
```bash
# These files are at repo root — edit them with Python scripts
# (they exceed the 4MB editor limit)
python -c "
with open('stem_lab_module.js', 'r', encoding='utf-8') as f:
    text = f.read()
# ... modifications ...
with open('stem_lab_module.js', 'w', encoding='utf-8') as f:
    f.write(text)
"
```

### 2. Copy to deploy directory
```bash
copy stem_lab_module.js prismflow-deploy\public\stem_lab_module.js
```

### 3. Push to GitHub first (CDN pulls from GitHub)
```bash
git add stem_lab_module.js
git commit -m "fix: description of module change"
git push origin main
```

### 4. Build and deploy (updates the hash in App.jsx)
```bash
node build.js --mode=prod  # Updates CDN hash to latest commit
npm run build              # In prismflow-deploy/
# ... stamp SW and firebase deploy ...
```

## Cache Invalidation
- jsDelivr caches by commit hash, so pushing a new commit automatically busts cache
- If you need to test with a specific hash: `@{hash}` in the URL
- Browser-side: The service worker may cache modules — stamp `sw.js` with new timestamp

## Common Gotchas
- **Never edit `prismflow-deploy/public/*.js` directly** — it gets overwritten by copy step
- **Module registration**: Each module must call `window.__MODULE_NAME__ = { render, ... }` at the end
- **Console markers**: Look for `[CDN] ModuleName script executed. Registration: SUCCESS` to verify loading
