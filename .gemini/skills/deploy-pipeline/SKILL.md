---
name: deploy-pipeline
description: Full production deployment pipeline for AlloFlow — push, build, stamp, deploy, verify
---

# Deploy Pipeline Skill

## Quick Reference

```bash
# Full deploy from scratch (from repo root):
git push origin main
node build.js --mode=prod
cd prismflow-deploy
npm run build
node -e "const fs=require('fs');const ts=Date.now();const f='build/sw.js';let c=fs.readFileSync(f,'utf-8');c=c.replace('__BUILD_TS__',String(ts));fs.writeFileSync(f,c,'utf-8');console.log('SW stamped:',ts)"
npx firebase deploy --only hosting
```

## Step-by-Step with Verification

### 1. Push source to GitHub
```bash
git add -A
git commit -m "description"
git push origin main
```
**Verify:** `git log --oneline -1` shows your commit on `origin/main`

### 2. Run build.js
```bash
node build.js --mode=prod
```
**What it does:**
- Auto-detects latest git hash
- Reads `AlloFlowANTI.txt` (the source of truth)
- Writes `prismflow-deploy/src/App.jsx` with CDN hash substitutions (`@{HASH}`)
- Logs the hash for verification

**Verify:** Output shows `Auto-detected git hash: {HASH}` matching your latest commit

### 3. Production build
```bash
cd prismflow-deploy
npm run build
```
**Verify:** Exit code 0, no compilation errors

### 4. Stamp service worker
```bash
node -e "const fs=require('fs');const ts=Date.now();const f='build/sw.js';let c=fs.readFileSync(f,'utf-8');c=c.replace('__BUILD_TS__',String(ts));fs.writeFileSync(f,c,'utf-8');console.log('SW stamped:',ts)"
```
**Why:** Forces client browsers to invalidate their SW cache and fetch new assets.

### 5. Deploy to Firebase
```bash
npx firebase deploy --only hosting
```
**Verify:** Output shows `✓ Deploy complete!` with hosting URL

### 6. Post-deploy verification
- **Hard refresh** (Ctrl+Shift+R) the live site
- Check console for: `[AlloFlow] UI_STRINGS loaded: X top-level keys`
- Check console for: `[CDN] ... Registration: SUCCESS` for all 4 modules
- Verify the commit hash in CDN URLs matches your push

## Error Recovery

| Error | Fix |
|-------|-----|
| `build.js` can't find `AlloFlowANTI.txt` | Run from repo root |
| `npm run build` fails with compilation error | Fix the error in `AlloFlowANTI.txt`, re-run build.js |
| Firebase deploy fails with auth error | Run `npx firebase login` |
| SW stamp fails (`__BUILD_TS__` not found) | The build already ran once — rebuild first |
| CDN shows stale content after deploy | jsDelivr caches by hash; ensure `build.js` used latest hash |

## Important Notes
- **Source of truth**: `AlloFlowANTI.txt` → everything flows from this
- **Never edit** `prismflow-deploy/src/App.jsx` directly — it's generated
- **CDN modules** (stem_lab, word_sounds, etc.) update when pushed to `main` — the CDN hash in `App.jsx` pins them
- **GitHub Pages** (website) updates automatically on push to `main`
