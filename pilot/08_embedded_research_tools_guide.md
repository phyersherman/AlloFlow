# AlloFlow Pilot — Embedded Research Tools Guide

**Purpose:** AlloFlow includes a dedicated **Research Mode** with built-in data collection tools. This guide shows pilot teachers how to activate and use these tools during the study.

---

## 1. Overview — What's Built In

AlloFlow's Research Tools panel (accessible from the Teacher Dashboard) includes:

| Tool | Purpose | Output |
|------|---------|--------|
| **🔬 Research Mode** | Start/end a named study with configurable settings | Session tracking, auto-surveys |
| **📄 Export Research CSV** | Download all research data as a spreadsheet | CSV file for analysis |
| **📋 Import CBM Score** | Enter Curriculum-Based Measurement data from external assessments | Linked CBM records |
| **🧒 Student Survey** | Built-in student survey instrument | Local survey responses |
| **👨‍🏫 Teacher Survey** | Built-in teacher self-assessment survey | Local survey responses |
| **👪 Parent/Guardian Survey** | Built-in parent survey for home perspectives | Local survey responses |
| **📊 Fidelity Log** | Automatic session logging (activity, duration, date) | Timestamped activity records |
| **📈 Session Counter** | Auto-counts sessions and triggers survey prompts | Session frequency data |

> **Privacy Note:** All research data is stored locally on the device — no student data is ever transmitted to external servers. Export the CSV when you need to share data with the research team.

---

## 2. Activating Research Mode

### Step-by-Step

1. Open **AlloFlow** and navigate to the **Teacher Dashboard**
2. Look for the **🔬 Research Tools** panel (gradient purple/pink section)
3. Click **🔬 Start Study**
4. Complete the **Research Mode Setup** form:

| Field | What to Enter | Example |
|-------|---------------|---------|
| **Study Name** | Name of your pilot study | `AlloFlow Pilot Study Spring 2026` |
| **Auto-Survey Frequency** | How often to prompt surveys | `Every 5 sessions` (recommended) |
| **IRB Number** | Your IRB approval number (if applicable) | `IRB-2026-0042` |
| **Notes** | Any study-specific notes | `Week 2 of 6-week pilot` |

5. Click **▶️ Start Research Mode**
6. A green **"Active"** badge will appear confirming the study is running

### What Research Mode Does Automatically:
- **Logs every session** — records student name, activity type, duration, date, and weekday
- **Counts sessions** — tracks cumulative session count
- **Triggers surveys** — automatically prompts surveys at your configured frequency (e.g., every 5 sessions)
- **Tags all data** — associates every data point with your study name

---

## 3. Collecting Survey Data

### Built-In Surveys
AlloFlow includes pre-configured surveys accessible from the Research Tools panel:

| Survey | Audience | When to Use |
|--------|----------|-------------|
| **🧒 Student Survey** | Students | Pre-study (Week 1) and Post-study (Week 6) |
| **👨‍🏫 Teacher Survey** | You (the teacher) | Pre-study (Week 1) and Post-study (Week 6) |
| **👪 Parent/Guardian Survey** | Parents | Post-study or as needed |

### How to Administer:
1. Click the corresponding survey button in the Research Tools panel
2. The survey modal opens with age-appropriate questions
3. For student surveys: project or share the screen, or have students take turns
4. Responses are saved locally and included in the CSV export
5. A response counter badge shows how many responses have been collected

### Auto-Survey Prompts
When Research Mode is active, AlloFlow automatically prompts surveys based on your configured frequency. When a student reaches the session threshold (e.g., every 5 sessions), a non-intrusive prompt appears asking them to complete a brief survey.

---

## 4. Importing CBM Scores

If you're conducting Curriculum-Based Measurement (CBM) assessments outside AlloFlow (e.g., DIBELS, AIMSweb, EasyCBM), you can import those scores:

1. Click **📋 Import CBM Score** in the Research Tools panel
2. Enter:
   - Student identifier (codename, not real name)
   - Assessment type (e.g., ORF, MAZE, math computation)
   - Score
   - Date
3. Imported CBM scores are linked with AlloFlow session data in the CSV export

### Why This Matters for Research:
Linking external CBM data with AlloFlow usage data allows you to:
- Correlate AlloFlow session frequency with CBM growth
- Track whether students who use more features show greater progress
- Compare pre/post CBM scores alongside AlloFlow engagement metrics

---

## 5. Using the Built-In Probes

AlloFlow includes dedicated assessment probes accessible from the main app:

### Math Fluency Probes
- **Location:** Educator Tools → Math Fluency Probes
- **What it measures:** Computation fluency (digits correct per minute)
- **Operations:** Addition, subtraction, multiplication, division
- **Output:** Timed score with automatic accuracy tracking
- **Research use:** Pre/post measure of computational fluency

### Oral Reading Fluency (ORF)
- **Location:** Word Sounds module → Oral Reading Fluency
- **What it measures:** Words correct per minute (WCPM)
- **Features:** Built-in passage bank, real-time student recording, AI accuracy analysis, color-coded heat map
- **Output:** WCPM score, accuracy percentage, error patterns
- **Research use:** Pre/post measure of reading fluency, RTI/MTSS progress monitoring

### Literacy Fluency Probes
- **Location:** Educator Tools → Literacy Fluency Probes
- **What it measures:** Letter naming, letter sound, phoneme segmentation
- **Research use:** Pre/post measure for early literacy skills

---

## 6. Exporting Research Data

### How to Export
1. Click **📄 Export Research CSV** in the Research Tools panel
2. Save the CSV file to your secure research drive
3. Share with the research team (PI) at weekly check-ins and at study end

### What the Export Includes

| Column | Description |
|--------|-------------|
| `date` | ISO timestamp of the session |
| `weekday` | Day of week |
| `student` | Student codename (never real names) |
| `activity` | Activity type (reading, quiz, adventure, etc.) |
| `duration` | Session length in minutes |
| `researchStudy` | Your study name |
| `surveyResponses` | Linked survey data (if applicable) |
| `cbmScores` | Imported CBM scores (if applicable) |

### Export Schedule for Pilot
| When | Action |
|------|--------|
| End of Week 2 | First export (verify data is collecting properly) |
| End of Week 3 | Mid-study export (check-in with PI) |
| End of Week 5 | Final implementation export |
| Week 6 | Post-study export (complete dataset) |

---

## 7. Additional Data Sources in AlloFlow

Beyond the Research Mode panel, AlloFlow tracks several data streams that are relevant for the pilot:

| Data Source | Location | What It Shows |
|-------------|----------|---------------|
| **XP & Gamification** | Student profiles | Engagement over time, level progression, streaks |
| **Class Analytics** | Teacher Dashboard | Aggregate class performance, RTI tier distributions |
| **Quiz/Exit Ticket Scores** | Assessment results | Content comprehension per lesson |
| **Session History** | Settings → Session Data | Full history of all AlloFlow sessions |
| **Adventure Mode Progress** | Adventure save files | Story completion, XP earned, rooms explored |
| **Probe Results** | Probes section | Math/reading fluency scores with dates |

### BehaviorLens Tools (if applicable)
For special education or behavioral research, BehaviorLens includes:
- **IOA Calculators** — Interobserver agreement for reliability data
- **Frequency/Duration/Latency Records** — Direct observation measures
- **Effect Size Calculators** — Tau-U, NAP, PND for single-case designs
- **Progress Monitoring** — Visual trend analysis for IEP goals

---

## 8. Quick Reference Card

```
🔬 START RESEARCH MODE
  Dashboard → Research Tools → 🔬 Start Study → Fill in details → Start

📊 COLLECT DATA (automatic)
  Sessions auto-logged when Research Mode is active

📋 ADMINISTER SURVEYS
  Research Tools → Student/Teacher/Parent Survey buttons

📄 EXPORT DATA
  Research Tools → Export Research CSV → Save to secure drive

⏹️ END STUDY
  Research Tools → ⏹ End Study (after final data export)
```

---

## 9. Troubleshooting

| Issue | Solution |
|-------|----------|
| Research Mode badge not showing | Click 🔬 Start Study and complete the setup form |
| Survey data not appearing in export | Make sure respondents click "Submit" on each survey |
| CBM import not accepting scores | Ensure score is a number and date is valid |
| Session counter not incrementing | Verify Research Mode shows "Active" badge |
| Need to restart with clean data | End current study → clear localStorage → start new study |
