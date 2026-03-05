---
description: Sync AlloFlowANTI.txt to App.jsx, build, and deploy to Firebase
---

// turbo-all

## Steps

> **⚠️ IMPORTANT — Hash-based CDN deployment:**
> The app loads `stem_lab_module.js` and `word_sounds_module.js` via jsDelivr CDN using **pinned commit hashes** (e.g. `@c1a9644`).
> After pushing module changes to GitHub, you **must** update the hash in `AlloFlowANTI.txt` so the live app loads the new code.
> The hash is the **short SHA** of the commit that contains the module changes.

1. Push the module files to GitHub and capture the commit hash:
```
git add ui_strings.js stem_lab_module.js word_sounds_module.js AlloFlowANTI.txt; git commit -m "Deploy: sync files"; git push origin main 2>&1 | Select-String -Pattern '[a-f0-9]+\.\.' | ForEach-Object { $_.Line }
```
Working directory: `C:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated`

2. Get the short hash of the commit you just pushed:
```
git rev-parse --short HEAD
```
Working directory: `C:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated`

3. Update the CDN URLs in `AlloFlowANTI.txt` with the new commit hash. Replace the old hash in **both** `loadModule` calls (around line 25381-25382):
```
(Get-Content AlloFlowANTI.txt) -replace '@[a-f0-9]{7,40}/', '@NEW_HASH/' | Set-Content AlloFlowANTI.txt
```
Working directory: `C:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated`

> Replace `NEW_HASH` with the actual hash from step 2. Verify the replacement hit the two `loadModule` lines:
> - `loadModule('StemLab', 'https://cdn.jsdelivr.net/gh/Apomera/AlloFlow@NEW_HASH/stem_lab_module.js')`
> - `loadModule('WordSoundsModal', 'https://cdn.jsdelivr.net/gh/Apomera/AlloFlow@NEW_HASH/word_sounds_module.js')`

4. Copy the updated `AlloFlowANTI.txt` to the deploy directory as `App.jsx`:
```
Copy-Item -Path "AlloFlowANTI.txt" -Destination "prismflow-deploy\src\App.jsx" -Force
```
Working directory: `C:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated`

5. Also update the deploy `AlloFlowANTI.txt` backup:
```
Copy-Item -Path "AlloFlowANTI.txt" -Destination "prismflow-deploy\src\AlloFlowANTI.txt" -Force
```
Working directory: `C:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated`

6. Build the production bundle:
```
npm run build
```
Working directory: `C:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\prismflow-deploy`

7. Deploy to Firebase hosting:
```
npx firebase deploy --only hosting
```
Working directory: `C:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\prismflow-deploy`

8. Confirm deploy succeeded — check that the output shows `Deploy complete!` and the hosting URL.

9. Commit and push the updated `AlloFlowANTI.txt` (with new hash) so the repo stays in sync:
```
git add AlloFlowANTI.txt; git commit -m "Deploy: update CDN hash"; git push origin main
```
Working directory: `C:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated`

> **Note:** No CDN cache purge is needed with hash-based URLs. Each new commit hash is a unique, never-cached URL.
> The fallback mechanism in `loadModule` will try `raw.githubusercontent.com` if the jsDelivr CDN fails.
