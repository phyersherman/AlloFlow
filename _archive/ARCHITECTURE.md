# AlloFlow Architecture Guide

> **For AI Assistants:** Read this at the start of every conversation. It will save you significant ramp-up time.
>
> **Last Updated:** 2026-02-27

## Overview

**AlloFlow** (Adaptive Levels, Layers, & Outputs) is a **single-file React monolith** for K-12 literacy education and Universal Design for Learning (UDL). Created by **Aaron Pomeranz, PsyD**. Licensed AGPL-3.0. The monolith also hosts two separate projects — the **Digital Kinship Parenting Tool** and the **Report Writing App** — which are independent applications colocated for deployment convenience (see *Separate Projects* section below).

- **Primary file:** `AlloFlowANTI.txt` (~4.27 MB, ~66,900 lines) — the core app
- **Externalized modules:** `word_sounds_module.js` (~909 KB), `stem_lab_module.js` (~350 KB) — loaded at runtime from GitHub CDN
- **Target platforms:** Google Gemini Canvas (via `@mode react`) + Firebase Hosting
- **Firebase project:** `prismflow-911fe` → `https://prismflow-911fe.web.app`
- **GitHub repo:** `Apomera/AlloFlow` (externalized content + CDN modules)
- **53 React.memo components**, no router — state-driven panel switching

---

## Source of Truth

| What | Source of Truth | Notes |
|---|---|---|
| **Application code** | `AlloFlowANTI.txt` (local) | This file IS the codebase. Everything else derives from it. |
| **Word Sounds Studio** | `word_sounds_module.js` (GitHub) | Externalized module, loaded at runtime via CDN. Local copy exists. |
| **STEM Lab** | `stem_lab_module.js` (GitHub) | Externalized module, loaded at runtime via CDN. Local copy exists. |
| **English UI strings** | `ui_strings.js` (GitHub) | Async-fetched on startup → cached in `localStorage`. |
| **Help tooltips** | `help_strings.js` (GitHub) | Lazy-fetched on first help activation → cached in `localStorage`. |
| **Language packs** | `lang/{language}.js` (GitHub) | Generated via in-app Gemini translation + export. `lang/` directory needs creation. |
| **Psychometric probes** | `psychometric_*.json` (GitHub) | Literacy, math, and combined probe banks. Loaded on demand. |
| **Audio banks** | `word_audio_bank_part1-4.json` (GitHub) | Pre-recorded word audio for phonics (~63 MB total across 4 files). |
| **Firebase build** | `prismflow-deploy/src/App.jsx` | Copy of `AlloFlowANTI.txt` at deploy time. Not independently edited. |
| **Canvas version** | Gemini Canvas paste | Copy of `AlloFlowANTI.txt` pasted into Canvas. Not independently edited. |

> **Key rule:** Always edit `AlloFlowANTI.txt`. Never edit `App.jsx` or Canvas directly. They are copies.

---

## GitHub Repository (`Apomera/AlloFlow`)

Files hosted on GitHub serve as a free CDN via `raw.githubusercontent.com`:

### Runtime Modules (Loaded via `loadModule()`)

| File | Size | Purpose | How It's Loaded |
|---|---|---|---|
| `word_sounds_module.js` | ~461 KB (on GH) | Complete Word Sounds Studio — 13+ phonics activities | `loadModule()` on first access → `new Function()` eval |
| `stem_lab_module.js` | ~129 KB (on GH) | STEM Lab — experiments, simulations, lab tools | `loadModule()` on first access → `new Function()` eval |

### Localization & UI

| File | Size | Purpose | How It's Loaded |
|---|---|---|---|
| `ui_strings.js` | ~285 KB | English UI labels, buttons, menus, tour text | Async on app startup → cached in `localStorage` |
| `help_strings.js` | ~1,104 KB | Context-sensitive help tooltips (621+ entries) | Lazy on first help activation → cached in `localStorage` |
| `lang/{language}.js` | ~250 KB each | Pre-translated language packs | On language switch → cached in IndexedDB |

### Assessment Data

| File | Size | Purpose |
|---|---|---|
| `psychometric_probes.json` | ~243 KB | Combined assessment probe bank |
| `psychometric_literacy_probes.json` | ~19 KB | Literacy-specific probes |
| `psychometric_math_probes.json` | ~107 KB | Math-specific probes |

### Audio Banks

| File | Size | Purpose |
|---|---|---|
| `audio_bank.json` | ~16 MB | Phoneme-level audio (base64) |
| `word_audio_bank_part1-4.json` | ~63 MB total | Pre-recorded word audio for TTS fallback |

### Other Assets

| File | Purpose |
|---|---|
| `shared.css` | Shared stylesheet |
| `calculator.html` | Embedded calculator tool |
| `features.html` | Feature showcase page |
| `index.html` | Landing page |
| `library.html` | Resource library page |
| `allobot.png` / `allobot.svg` | AlloBot mascot assets |
| `profile-image.jpg` / `rainbow-book.jpg` | Static images |

**Files NOT yet on GitHub (need to be pushed):**
- `lang/` directory — needs creation, language packs generated via in-app export

**Format:** `ui_strings.js` and `help_strings.js` are plain JavaScript object literals (not JSON, not modules). They are evaluated via `new Function('return ' + text)()` after fetch. Runtime modules (`word_sounds_module.js`, `stem_lab_module.js`) follow the same pattern.

---

## Monolith Structure

| Region | Line Range | Contents |
|---|---|---|
| **Imports** | L1–66 | React, Lucide icons, Firebase SDK |
| **Config & Setup** | L67–8514 | Constants, API keys, data banks (audio bank URL, Firebase config) |
| **Localization** | L8515–8576 | `UI_STRINGS` async loader (from GitHub CDN) |
| **Helpers & Utilities** | L8577–9395 | Grade helpers, `useTranslation` hook, `t()` function |
| **Contexts & Providers** | L9396–9436 | `LanguageContext`, `LanguageProvider`, RTL support |
| **UI Components** | L9437–23986 | All major panels/features (~14,500 lines) |
| **Main Application** | L23987–67964 | `AlloFlowApp` component, state, API calls |
| **App Export** | L67965+ | `ReactDOM.render` call |

> **Note:** Word Sounds Studio and STEM Lab code have been externalized to GitHub modules. The monolith contains stubs and `loadModule()` calls for these features.

### Key Data Banks (Config Region)

| Constant | Purpose |
|---|---|
| `BENCHMARK_PROBE_BANKS` | Standardized literacy assessment items |
| `LETTER_SVG_PATHS` | SVG path data for letter tracing |
| `DOM_TO_TOOL_ID_MAP` | Help system — DOM element → tool ID mapping |

> **Previously in-file, now on GitHub:** `WORD_SOUNDS_STRINGS`, `WORD_FAMILY_PRESETS`, `INSTRUCTION_AUDIO`, `SOUND_MATCH_POOL`, `PHONEME_AUDIO_BANK`, `IPA_TO_AUDIO`, `PHONEME_GUIDE` (all moved into `word_sounds_module.js`)

---

## Translation / Localization Architecture

### The `t()` Function Resolution Chain
```
t("tour.glossary_title") checks:
  1. languagePack["tour"]["glossary_title"]  → translated string
  2. UI_STRINGS["tour"]["glossary_title"]    → English fallback
  3. WORD_SOUNDS_STRINGS[key]                → activity fallback
  4. Return the key itself                   → "tour.glossary_title"
```

### Language Pack Loading (`loadLanguage()`)
1. **IndexedDB cache** → instant if previously loaded
2. **GitHub fetch** → `raw.githubusercontent.com/Apomera/AlloFlow/main/lang/{lang_slug}.js`
3. **Gemini on-the-fly** → translates UI_STRINGS + HELP_STRINGS in 50-string chunks, caches result
4. **Manual JSON import** → always available via import button

### Help String Translation
When generating a language pack via Gemini, help strings are automatically fetched from GitHub and merged under the `help_mode.*` namespace. The help resolver checks `t('help_mode.' + key)` before falling back to English `HELP_STRINGS[key]`.

---

## API Integrations

| API | Used For | Key Pattern |
|---|---|---|
| **Gemini** | Text generation, translation, analysis | `callGemini(prompt, options)` |
| **Imagen** | Image generation (glossary, activities) | `callImagen(prompt)` — max 5 concurrent |
| **TTS** | Text-to-speech for phonics | `handleAudio(text)` via Gemini TTS |

- **Canvas:** API key auto-injected by sandbox
- **Firebase:** API key from user input, stored in state

---

## Key Feature Systems

| System | Description |
|---|---|
| **Word Sounds Studio** | 13+ phonics activities (isolation, blending, segmentation, rhyming, tracing, etc.) — externalized to `word_sounds_module.js` |
| **STEM Lab** | Science experiments, simulations, virtual instruments, data tables, quizzes — externalized to `stem_lab_module.js` |
| **Screening Dashboard** | Universal literacy screener, composite scoring, RTI/MTSS monitoring |
| **Bridge Mode** | Gemini conversational interface for student engagement |
| **Adventure Mode** | Gamified learning (XP, shop, narrative progression) |
| **Glossary/Vocabulary** | AI definitions, images, 8+ games (Memory, Crossword, Bingo, etc.) |
| **Escape Room** | Puzzle-based gamification with XP, streaks, and team play |
| **Help System** | Context-sensitive tooltips via `HELP_STRINGS` + `DOM_TO_TOOL_ID_MAP` |
| **Lesson Plan** | AI-generated differentiated lesson plans |
| **AlloBot** | Contextual, dynamic tips system triggered by user actions (context-aware suggestions based on current activity) |
| **ORF / Fluency** | Oral Reading Fluency assessment with prosody scoring |
| **Live Session** | Real-time teacher-student sync |
| **Report Writer** | User report profiles, blueprint mode, adaptation studio, multilingual generation |

---

## Separate Projects (Colocated, NOT Part of AlloFlow)

The following are **independent applications** that share the same monolith file for deployment convenience only. They are **not features of AlloFlow** and have distinct user bases, purposes, and design goals:

| Project | Description | Target Audience |
|---|---|---|
| **Digital Kinship Parenting Tool** | Indigenous-centric parenting platform (Hearth Hub, Parent Wellness Studio, Conflict Resolution Lab, Tribal Nations Explorer) | Parents, families, community |

---

## Deployment

```powershell
# Standard deploy (also see .agent/workflows/deploy.md):
Copy-Item AlloFlowANTI.txt prismflow-deploy\src\App.jsx -Force
Copy-Item AlloFlowANTI.txt prismflow-deploy\src\AlloFlowANTI.txt -Force
cd prismflow-deploy
npm run build          # Must exit code 0
npx firebase deploy --only hosting
```

---

## Critical Rules for AI Assistants

1. **File size is critical** — Canvas has share link limits. Track every KB.
2. **The file exceeds 4MB** — `replace_file_content` tool won't work. Use Python scripts.
3. **Never remove `#region` markers** — they're the only structural navigation.
4. **Always build before deploying** — `npm run build` exit code 0 required.
5. **Regex patterns contain `//`** — comment-stripping must track string/regex context.
6. **`UI_STRINGS` loads async** — app must handle the 200ms empty window.
7. **Canvas uses esbuild** (stricter) vs Firebase uses webpack (lenient). Both must work.
8. **Line endings are `\n`** after Python processing, not `\r\n`.
9. **Test in Canvas too** — a webpack pass doesn't guarantee Canvas compilation.
10. **Edit `AlloFlowANTI.txt` only** — `App.jsx` is a derivative copy.
11. **Externalized modules use `new Function()` eval** — syntax errors in `word_sounds_module.js` or `stem_lab_module.js` will silently fail at runtime.

---

## Useful Grep Patterns

```bash
# Find component definitions
grep "React.memo" AlloFlowANTI.txt
# Find state declarations
grep "useState.*variableName" AlloFlowANTI.txt
# Find #region boundaries
grep "#region" AlloFlowANTI.txt
# Find t() usage for a key
grep "t('" AlloFlowANTI.txt | grep "key_name"
# Find help key assignments
grep "data-help-key" AlloFlowANTI.txt
# Find loadModule calls
grep "loadModule" AlloFlowANTI.txt
```

---

## Project Directory Notes

The project directory contains ~92 files + 23 subdirectories. Most `_*.txt` and `analyze_*.txt` files are **temporary artifacts from past debugging sessions** and can be ignored. Key files:

| File/Dir | Purpose |
|---|---|
| `AlloFlowANTI.txt` | **THE app** — source of truth |
| `word_sounds_module.js` | Local copy of externalized Word Sounds module |
| `stem_lab_module.js` | Local copy of externalized STEM Lab module |
| `ui_strings.js` | Externalized English UI strings (also on GitHub) |
| `help_strings.js` | Externalized help tooltips (also on GitHub) |
| `psychometric_*.js/.json` | Probe bank data files |
| `prismflow-deploy/` | Firebase build directory |
| `.agent/workflows/` | Agent workflow definitions |
| `ARCHITECTURE.md` | This file (in `_archive/`) |
| `scripts/` | ~544 utility scripts from past sessions |
| `_archive/` | ~1,104 archived files |
| `AlloFlowANTI.bak*.txt` | Backup snapshots (various stages) |

---

## File Size History

| Date | Size | Lines | Change |
|---|---|---|---|
| Original | 5.29 MB | 80,088 | — |
| Comments removed | 5.11 MB | 77,201 | -177 KB |
| UI_STRINGS externalized | 4.88 MB | 72,012 | -262 KB |
| Inline comments stripped | 4.83 MB | 72,005 | -19 KB |
| HELP_STRINGS externalized | 4.51 MB | 71,417 | -327 KB |
| Word Sounds + STEM Lab externalized, localization patches | 4.27 MB | 66,915 | -240 KB |
| **Current** | **4.27 MB** | **66,915** | **-1,024 KB total (19.4%)** |

---

## Active Task List

> **Instructions:** Update this list as work progresses. Mark `[x]` when done, `[/]` when in progress.

### Completed
- [x] Push `ui_strings.js` to GitHub (`Apomera/AlloFlow`)
- [x] Push `help_strings.js` to GitHub
- [x] Externalize `word_sounds_module.js` to GitHub
- [x] Externalize `stem_lab_module.js` to GitHub
- [x] Push `psychometric_*.json` probe banks to GitHub
- [/] Fix JSX text localization gaps (add keys to `ui_strings.js`, wrap in `t()`) — partially done

### High Priority
- [ ] Create `lang/` directory on GitHub
- [ ] Generate pre-built language packs for top 12 languages
- [ ] Continue fixing remaining JSX text localization gaps

### Medium Priority
- [ ] Fix remaining `aria-label`/`title` attribute localization gaps
- [ ] Fix remaining toast message localization gaps
- [ ] Clean up temp files in project root (move to `_archive/`)

### Low Priority / Future
- [ ] Consider externalizing `BENCHMARK_PROBE_BANKS`
- [ ] Consider externalizing `DOM_TO_TOOL_ID_MAP`
- [ ] Explore further dead code removal for file size reduction
