# AlloFlow Pilot — Data Collection & Analysis Protocol

**Purpose:** Standardize data collection procedures and analysis methods across all pilot sites.

---

## 1. Data Collection Timeline

| Timepoint | Instrument | Collector | Method |
|-----------|------------|-----------|--------|
| Week 1 (Day 1–2) | Teacher Pre-Survey | PI/RA | Digital form |
| Week 1 (Day 2–3) | Student Pre-Survey | Teacher | Paper or digital in class |
| Week 1 (Day 3–5) | Baseline Classroom Observation | PI/RA | In-person (30 min) |
| Weeks 2–5 (weekly) | Teacher Fidelity Log | Teacher | Digital form (5 min) |
| Weeks 2–5 (weekly) | 15-min Check-In Call | PI/RA | Phone/video |
| Week 5 (Day 1–3) | Post Classroom Observation | PI/RA | In-person (30 min) |
| Week 6 (Day 1–2) | Teacher Post-Survey | PI/RA | Digital form |
| Week 6 (Day 2–3) | Student Post-Survey | Teacher | Paper or digital in class |
| Week 6 (Day 3–5) | Teacher Focus Group/Interview | PI | Recorded (30–45 min) |

---

## 2. Survey Administration Guidelines

### Teacher Surveys
- Send via Google Forms link (or equivalent secure platform)
- Allow 3 business days for completion
- Send one reminder after 2 days if not completed
- De-identify upon receipt: assign Teacher ID codes (T01–T10)

### Student Surveys
- **K–2:** Teacher administers verbally, one question at a time, students circle emoji responses
- **3–5:** Teacher distributes paper copies, reads instructions aloud, students complete independently
- **6–12:** Digital administration or paper, students complete independently
- Allow 5–10 minutes of class time
- De-identify immediately: assign Student ID codes (S001–S250)

### Missing Data Protocol
- If a teacher misses a fidelity log, follow up within 24 hours
- If a student is absent for survey day, allow a 3-day makeup window
- Document all missing data and reasons in the data tracking spreadsheet

---

## 3. Observation Protocol

### Structured Observation Form (30 minutes)

| Dimension | Indicators | Rating (1–5) |
|-----------|-----------|---------------|
| **Differentiation** | Multiple reading levels visible; modified materials for diverse learners | ___ |
| **Technology Integration** | Tech used meaningfully for learning (not just passive consumption) | ___ |
| **Student Engagement** | On-task behavior; active participation; voluntary interaction | ___ |
| **Accessibility** | Students with diverse needs accessing the same content | ___ |
| **Teacher Facilitation** | Teacher circulating, scaffolding, using real-time data | ___ |

### Observation Notes Template
- **Date/Time:** ___
- **Teacher ID:** ___
- **Grade/Subject:** ___
- **Number of students present:** ___
- **AlloFlow features in use:** ___
- **Specific observations (3–5 bullet points):**
  - ___
  - ___
  - ___
- **Notable student interactions:** ___
- **Barriers or technical issues observed:** ___

---

## 4. Platform Usage Data Extraction

AlloFlow stores usage data locally. To collect this:

1. **At end of Week 5**, teacher exports usage data as JSON:
   - Open AlloFlow → Settings → Export Session Data
   - Save file as `T[XX]_usage_data.json`
2. **Data points to extract:**
   - Total sessions
   - Average session duration (minutes)
   - Content types generated (count by type)
   - Features accessed (frequency count)
   - Student XP progression (aggregate, de-identified)
   - Lessons created (count)
3. **Analysis script** will aggregate across teachers using Python/R

---

## 5. Analysis Plan

### 5.1 Quantitative Analysis

| Research Question | Variables | Test | Expected Output |
|------------------|-----------|------|-----------------|
| RQ1: Differentiation quality | Teacher survey B1–B8 (pre vs post) | Paired t-test or Wilcoxon | Mean difference, CI, Cohen's d |
| RQ1: Time savings | B9 pre vs C12 post (hours/week) | Paired t-test | Mean reduction in hours |
| RQ2: Teacher usability | C1–C11 post-survey means | Descriptive | Mean ± SD for each item |
| RQ2: Net Promoter Score | C13 (0–10 scale) | Descriptive | NPS score, distribution |
| RQ2: Student engagement | Student survey items (pre vs post) | Paired t-test | Mean difference, Cohen's d |
| RQ3: Implementation fidelity | Fidelity log composite score | Descriptive | Mean % of target behaviors |
| RQ4: Student outcomes | Student survey engagement/confidence items | Paired t-test | Pre-post differences |

### 5.2 Effect Size Benchmarks

| Cohen's d | Interpretation | Practical Meaning |
|-----------|---------------|-------------------|
| 0.2 | Small | Noticeable to researchers |
| 0.5 | Medium | Noticeable to practitioners |
| 0.8 | Large | Obvious to all stakeholders |

### 5.3 Qualitative Analysis

1. **Transcribe** all interviews and open-ended responses
2. **Initial coding:** Two coders independently identify themes
3. **Code reconciliation:** Discuss and resolve discrepancies (target κ > 0.80)
4. **Thematic grouping:** Organize codes into 4–6 major themes
5. **Member checking:** Share themes with 2–3 participants for validation
6. **Integration:** Triangulate qualitative themes with quantitative findings

---

## 6. Data Management

### File Structure
```
pilot_data/
├── raw/
│   ├── teacher_surveys/      (T01_pre.csv, T01_post.csv, ...)
│   ├── student_surveys/       (S001_pre.csv, S001_post.csv, ...)
│   ├── fidelity_logs/         (T01_week2.csv, ...)
│   ├── observations/          (T01_obs_pre.md, T01_obs_post.md, ...)
│   ├── interviews/            (T01_interview.mp3, T01_transcript.md, ...)
│   └── usage_data/            (T01_usage_data.json, ...)
├── processed/
│   ├── teacher_summary.csv
│   ├── student_summary.csv
│   └── usage_summary.csv
├── analysis/
│   ├── quantitative_results.md
│   └── qualitative_themes.md
└── reports/
    ├── technical_report.md
    └── executive_summary.md
```

### Security
- All files on encrypted, password-protected drive
- Access limited to PI and authorized research staff
- No cloud storage for raw data containing any identifiers
- De-identification completed within 48 hours of collection
