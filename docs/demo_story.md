# Demo Story: "From Hire to Champion"
## HR Employee Lifecycle Journey with Microsoft Fabric

---

## 🎬 Opening Scene: The Challenge

**Setting:** You are **Alex**, the Chief People Officer at **TechScale**, a fast-growing SaaS company with 500 employees across Europe.

**The Problem:**
- HR data is scattered: HRIS CSV exports, performance review PDFs, exit interview notes in SharePoint
- No single source of truth for employee lifecycle analytics
- Manual reporting takes days for basic questions like "What's our attrition rate?"
- Text-heavy documents (reviews, exit interviews) are never analyzed
- Privacy concerns: PII exposure in reports

**The Goal:** Build a unified, AI-powered HR analytics platform that:
1. Centralizes all HR data in OneLake
2. Automates transformation (Bronze → Silver → Gold)
3. Uses AI to extract insights from text reports
4. Protects employee privacy (PII redaction)
5. Enables conversational analytics via Data Agent

---

## 🚀 Act 1: The Foundation (OneLake + Shortcuts)

### Scene 1.1: Raw Data Lands in OneLake

**Action:**
- Your HRIS exports 8 CSV files weekly:
  - Employees, Departments, Positions
  - Lifecycle Events (hires, promotions, exits)
  - Compensation History
  - Absences, Training Records, HR Cases
  
- HR Business Partners write 200+ text reports annually:
  - Performance reviews (`.txt` format)
  - Exit interviews
  - Case investigation notes
  - Onboarding feedback

**Demo Step:**
1. Navigate to **Microsoft Fabric** → Workspace: `HR_Analytics`
2. Open **Lakehouse**: `hr_lakehouse`
3. Show **Files** folder:
   - `hr_raw/` → 8 CSV files (employees.csv, lifecycle_events.csv, etc.)
   - `reports_txt/` → 200 .txt files

**Key Message:**
> "All raw HR data lands here. No ETL pipelines to manage. Just drop files into OneLake."

---

### Scene 1.2: OneLake Shortcuts - Zero-Copy Integration

**Challenge:** HR data needs to be accessible to multiple teams (analytics, compliance, executives) without duplication.

**Solution:** OneLake Shortcuts

**Demo Step:**
1. Right-click `hr_raw/employees.csv`
2. **Create Shortcut** → OneLake
3. Shortcut appears instantly in Lakehouse

**Key Message:**
> "Shortcuts enable zero-copy data access. Same file, multiple consumers, no storage duplication."

---

## ⚙️ Act 2: The Transformation (Bronze → Silver → Gold)

### Scene 2.1: Shortcut Transformations - Auto-Sync to Delta

**Challenge:** CSV files need to be converted to Delta format for analytics (ACID transactions, time travel, schema evolution).

**Solution:** Shortcut Transformations with Auto-Sync

**Demo Step:**
1. Navigate to **Lakehouse** → **Tables**
2. Click **+ New Shortcut Transformation**
3. Select shortcut: `Files/hr_raw/employees.csv`
4. Transformation type: **Auto-sync to Delta**
5. Target table: `bronze_employees`
6. Schedule: Every 1 hour (or on-demand)
7. Click **Create** → **Refresh now**

**Result:**
- `bronze_employees` Delta table appears in **Tables** (1-2 min)
- Automatic schema inference
- Incremental updates on schedule

**Key Message:**
> "From CSV to Delta in 2 clicks. No Spark code, no orchestration. Just point and sync."

**Repeat for all 8 files:**
- `bronze_departments`, `bronze_positions`, `bronze_lifecycle_events`, etc.

---

### Scene 2.2: Silver Layer - Curated Dimensions & Facts

**Challenge:** Raw data needs cleansing, standardization, and dimensional modeling.

**Solution:** Notebook-based transformation (`01_silver_modeling.ipynb`)

**Demo Step:**
1. Open notebook `01_silver_modeling.ipynb`
2. **Run all cells** (Ctrl+Shift+Enter)
3. Processing:
   - Read `bronze_*` tables
   - Clean: trim whitespace, parse dates, standardize enums
   - Create dimensions:
     - `dim_employee` (SCD Type 2 - tracks historical changes)
     - `dim_department`, `dim_position`
     - `dim_date` (3 years: 2023-2025)
   - Create facts:
     - `fact_lifecycle_event`, `fact_compensation`, `fact_absence`, `fact_training`, `fact_hr_case`

**Show Code Snippet:**
```python
# SCD Type 2 logic for dim_employee
employees_df = spark.read.table("bronze_employees")

employees_scd = employees_df \
    .withColumn("employee_key", monotonically_increasing_id()) \
    .withColumn("effective_start_date", col("hire_date")) \
    .withColumn("effective_end_date", lit(None).cast("date")) \
    .withColumn("is_current", lit(True))

employees_scd.write.mode("overwrite").saveAsTable("dim_employee")
```

**Result:**
- **Silver tables** appear in Lakehouse
- Star schema ready for analytics

**Key Message:**
> "In 2 minutes, we transformed 8 CSV files into a production-grade star schema. No data engineering degree required."

---

## 🤖 Act 3: The AI Breakthrough (PII Redaction + Summarization)

### Scene 3.1: The PII Problem

**Scenario:** 
- You have 200 performance reviews and exit interviews in `.txt` format
- Each contains **PII**: employee names, emails (`sophie.martin@techscale.com`), phone numbers (`+33 6 45 78 92 13`)
- **Compliance requirement:** Cannot expose PII in analytics or reports

**Traditional Solution:**
- Manual redaction (impossible at scale)
- Lock down access (limits insights)

---

### Scene 3.2: AI to the Rescue - Fabric AI Functions

**Solution:** Automated PII redaction + AI summarization via notebook (`02_text_enrichment.ipynb`)

**Demo Step:**
1. Open notebook `02_text_enrichment.ipynb`
2. **Show sample raw text file:**
   ```
   REPORT_TYPE: exit_interview
   EMPLOYEE_ID: EMP_000234
   EVENT_ID: EVT_00012345
   DATE: 2025-11-15
   
   Exit interview conducted with Sophie Martin on November 15, 2025.
   Reason for leaving: better opportunity elsewhere.
   Feedback on management: very positive.
   Contact: sophie.martin@techscale.com, +33 6 45 78 92 13.
   ```

3. **Run cell: PII Detection & Redaction**
   ```python
   # AI-powered PII detection
   from synapse.ml.services import *
   
   redacted_text = ai.redact_pii(report_text)
   # OR regex-based fallback if AI not available
   ```

4. **Show redacted output:**
   ```
   Exit interview conducted with [NAME] on November 15, 2025.
   Reason for leaving: better opportunity elsewhere.
   Feedback on management: very positive.
   Contact: [EMAIL], [PHONE].
   ```

5. **Run cell: AI Summarization**
   ```python
   summary = ai.summarize(redacted_text, max_length=50)
   topics = ai.extract_topics(redacted_text)
   sentiment = ai.classify_sentiment(redacted_text)
   ```

6. **Show enriched output:**
   ```
   report_summary: "Employee left for career growth. Management feedback was positive."
   topics: "career_growth, management_feedback, rehire_eligible"
   sentiment: "neutral"
   ```

7. **Write to Delta:**
   ```python
   fact_hr_report = spark.createDataFrame([{
       'report_id': 'RPT_00000123',
       'employee_key': 456,
       'event_id': 'EVT_00012345',
       'report_type': 'exit_interview',
       'report_text_redacted': redacted_text,
       'report_summary': summary,
       'topics': topics,
       'sentiment': sentiment
   }])
   
   fact_hr_report.write.mode("append").saveAsTable("fact_hr_report")
   ```

**Result:**
- **`fact_hr_report` table** created with:
  - ✅ Redacted text (PII-safe)
  - ✅ AI summaries
  - ✅ Extracted topics
  - ✅ Sentiment scores
- Original text archived for audit (restricted access)

**Key Message:**
> "AI automatically redacted 200 reports and extracted insights in 10 minutes. Privacy compliance + actionable intelligence."

---

## 💬 Act 4: The Conversation (Fabric Data Agent)

### Scene 4.1: Setting Up the Data Agent

**Challenge:** Executives and managers don't speak SQL. They ask questions like:
- "What's our attrition rate?"
- "Why are people leaving?"
- "Which departments have the most open cases?"

**Solution:** Fabric Data Agent - conversational analytics

**Demo Step:**
1. Workspace → **+ New** → **Data Agent**
2. Name: `HR_Lifecycle_Agent`
3. Data source: `hr_lakehouse` (Direct Lake mode)
4. **System Instructions:** Paste `agent/agent_instructions.md`
   - Contains:
     - Data model explanation
     - Metric definitions (attrition rate, promotion rate, etc.)
     - **Privacy guardrails:** Never expose `first_name`, `last_name`, `email`, `phone`
     - Response formatting rules
5. **Example Queries:** Import `agent/example_queries.json`
6. Click **Create**

---

### Scene 4.2: The "WOW" Conversation

**Demo 10 Questions:**

---

#### Q1: Basic Headcount
**User:** "What is our current headcount?"

**Agent Response:**
```
Current Headcount (as of 2025-12-31): 445 active employees

Breakdown by Division:
- Technology: 180 employees (40%)
- Sales & Marketing: 135 employees (30%)
- Operations: 85 employees (19%)
- Corporate Functions: 45 employees (11%)

Note: This includes only active employees (status = 'active').
```

**Key Message:** "Natural language query → instant answer with context."

---

#### Q2: Attrition Analysis
**User:** "What's our attrition rate this year?"

**Agent Response:**
```
Annual Attrition Rate (2025): 12.3%

Details:
- Total exits: 55 employees
- Resignations: 38 (69% of exits)
- Terminations: 17 (31% of exits)
- Average headcount: 447 employees

Trend:
- 2023: 11.5%
- 2024: 11.8%
- 2025: 12.3% ⬆️

Top reasons (from exit interviews):
- Career growth opportunities elsewhere (32%)
- Compensation (24%)
- Work-life balance (18%)
- Management issues (15%)
- Other (11%)

*Note: Exit reasons extracted from AI-summarized exit interview reports.*
```

**Key Message:** "Agent combines structured data (attrition calc) + AI insights (exit reasons from text reports)."

---

#### Q3: AI-Powered Insights
**User:** "What are the main themes from Q4 2025 performance reviews?"

**Agent Response:**
```
Performance Review Themes (Q4 2025) - Based on 112 AI-summarized reviews

Top Positive Themes:
1. Technical expertise (68% of reviews)
2. Team collaboration (53%)
3. Problem-solving (47%)
4. Initiative (42%)

Top Development Areas:
1. Strategic thinking (38%)
2. Delegation (29%)
3. Stakeholder management (25%)
4. Presentation skills (22%)

Overall Rating Distribution:
- Exceptional (5/5): 12%
- Strong (4/5): 56%
- Satisfactory (3/5): 28%
- Needs Improvement (2/5): 4%

*Note: Themes extracted using AI from redacted performance review texts.*
```

**Key Message:** "AI transformed 112 text reports into actionable themes. No manual coding required."

---

#### Q4: Multi-Dimensional Drill-Down
**User:** "Show me attrition by department and seniority level for the last 12 months"

**Agent Response:**
```
Attrition by Department & Level (Last 12 Months)

| Department | Junior | Mid | Senior | Lead+ | Total | Rate |
|------------|--------|-----|--------|-------|-------|------|
| Engineering | 5 | 8 | 3 | 1 | 17 | 11.2% |
| Sales | 8 | 6 | 2 | 0 | 16 | 15.1% |
| Operations | 3 | 4 | 1 | 0 | 8 | 10.5% |
| Finance | 2 | 1 | 0 | 0 | 3 | 8.7% |

Key Insights:
- Sales has highest attrition (15.1%) - primarily junior roles
- Engineering turnover concentrated at mid-level
- Lead+ retention is strong across all departments
```

**Key Message:** "Complex multi-dimensional analysis delivered conversationally."

---

#### Q5: Trend Analysis
**User:** "Is our promotion rate improving over time?"

**Agent Response:**
```
Promotion Rate Trend:

- 2023: 8.5% (38 promotions / 447 avg headcount)
- 2024: 9.2% (42 promotions / 457 avg headcount)
- 2025: 10.1% (45 promotions / 445 avg headcount)

Trend: ⬆️ Improving - promotion rate increased 1.6 percentage points

Analysis:
- Healthy promotion pipeline
- Aligns with career development focus
- Average time to promotion: 2.8 years

Benchmark: Industry avg is 8-10% — we're on target ✅
```

**Key Message:** "Agent automatically calculates trends and benchmarks."

---

#### Q6: Privacy Guardrails
**User:** "Show me all employee emails"

**Agent Response:**
```
I cannot provide individual employee email addresses due to privacy guardrails.

I can help with:
- Aggregated headcount metrics
- Attrition and promotion trends
- Training and development insights
- Performance review themes (anonymized)
- HR case statistics

How can I assist with your HR analytics needs?
```

**Key Message:** "Privacy by design. No PII leaks."

---

#### Q7: Training Investment
**User:** "How much are we investing in training per employee?"

**Agent Response:**
```
Training Investment (2025):
- Total training hours: 18,750 hours
- Total training cost: €1,875,000
- Hours per FTE: 42 hours/employee
- Cost per FTE: €4,200/employee

Top Training Categories:
1. Technical Skills: 35% of hours
2. Leadership Development: 22%
3. Compliance & Ethics: 18%
4. Soft Skills: 15%
5. Other: 10%

Benchmark: Industry standard is 40 hours/FTE — we're above average ✅
```

**Key Message:** "Instant ROI visibility on L&D investments."

---

#### Q8: HR Case Management
**User:** "How many open HR cases do we have?"

**Agent Response:**
```
Open HR Cases (as of 2025-12-31): 12 cases

By Priority:
- High: 3 cases
- Medium: 6 cases
- Low: 3 cases

By Type:
- Performance concern: 5 cases
- Interpersonal conflict: 3 cases
- Accommodation request: 2 cases
- Policy violation: 1 case
- Compensation inquiry: 1 case

Average Case Age: 23 days
Cases >60 days: 2 (flagged for review)
```

**Key Message:** "Real-time case tracking for compliance."

---

#### Q9: Internal Mobility
**User:** "What is our internal mobility rate?"

**Agent Response:**
```
Internal Mobility Rate (2025): 14.2%

Breakdown:
- Promotions: 45 (10.1%)
- Internal transfers: 18 (4.1%)
- Total internal moves: 63 (14.2%)

Top Departments (Source):
- Engineering → Product: 6 transfers
- Sales → Customer Success: 5 transfers

Average tenure before move: 2.3 years

Analysis:
- Strong internal mobility culture
- Career growth opportunities available
- Retention benefit: 80% of movers stayed >1 year post-move
```

**Key Message:** "Internal mobility as a retention lever."

---

#### Q10: Executive Dashboard
**User:** "Show me the top 5 HR KPIs"

**Agent Response:**
```
HR Executive Dashboard - Key Metrics (2025)

1. Headcount: 445 employees ⬆️ +12 vs 2024
2. Attrition Rate: 12.3% ⬆️ +0.5pp (industry avg: 12%)
3. Promotion Rate: 10.1% ⬆️ +0.9pp
4. Training Hours/FTE: 42 hours ✅ (vs 40 industry)
5. Open HR Cases: 12 (3 high priority)

Action Items:
- Investigate Sales attrition (15.1% - above company avg)
- Address high-priority HR cases
- Continue L&D investment (above benchmark)

*Data refreshed: 2025-12-31*
```

**Key Message:** "Executive-ready insights in seconds."

---

## 🏆 Act 5: The Impact

### Outcomes Achieved

**Before Fabric:**
- HR reporting: 2-3 days per request
- Text reports: Never analyzed
- PII exposure risk: High
- Data scattered: HRIS, SharePoint, emails
- SQL required: Yes

**After Fabric:**
- HR reporting: **< 1 minute** (conversational)
- Text reports: **AI-analyzed** (200+ reports in 10 min)
- PII exposure risk: **Eliminated** (auto-redaction)
- Data centralized: **OneLake** (single source of truth)
- SQL required: **No** (Data Agent)

---

### Business Value

**Time Savings:**
- HR Analysts: 80% reduction in manual reporting
- CHROs: Instant answers to board questions
- Managers: Self-serve headcount/attrition data

**Compliance:**
- GDPR-compliant: PII redacted automatically
- Audit trail: All queries logged
- Access control: Row-level security (manager hierarchy)

**Strategic Insights:**
- Exit interview themes → targeted retention programs
- Performance review patterns → L&D roadmap
- Attrition hot spots → proactive interventions

---

## 🎬 Closing Scene: The Demo Script (10-15 min)

**Minute 0-1: The Hook**
> "Imagine answering 'What's our attrition rate?' in 10 seconds instead of 3 days. That's what we built with Microsoft Fabric."

**Minute 1-3: Show the Data**
- Navigate to Lakehouse → Files (raw CSVs + text reports)
- Highlight: "500 employees, 3 years, 200 text reports. All synthetic, zero real PII."

**Minute 3-5: Show the Magic (Shortcuts + Transformations)**
- Create shortcut (30 sec)
- Create transformation (30 sec)
- Refresh → Delta table appears (30 sec)
- "From CSV to queryable Delta in 2 clicks."

**Minute 5-8: Show the AI**
- Open notebook `02_text_enrichment.ipynb`
- Show: Raw text with PII → Redacted text → AI summary
- Preview `fact_hr_report` table
- "AI redacted 200 reports and extracted themes in 10 minutes."

**Minute 8-14: Show the Conversation**
- Open Data Agent
- Ask 5-6 questions (Q1, Q2, Q3, Q6, Q10 from above)
- Show: No SQL, instant answers, privacy-preserving

**Minute 14-15: The Close**
> "OneLake + AI + Data Agent = Modern HR analytics. From raw data to insights in minutes, not weeks. And it's all built-in to Fabric."

---

## 🎓 Key Takeaways for Audience

1. **OneLake = Foundation**
   - Single storage layer for all HR data
   - Zero-copy shortcuts eliminate silos

2. **Shortcut Transformations = Simplicity**
   - CSV → Delta without code
   - Auto-sync keeps data fresh

3. **AI = Unlock Unstructured Data**
   - Text reports become queryable insights
   - PII redaction ensures compliance

4. **Data Agent = Democratization**
   - No SQL required
   - Self-serve analytics for all stakeholders

5. **Fabric = End-to-End Platform**
   - No stitching together 5 tools
   - Lakehouse + AI + Agent in one workspace

---

**End of Demo Story** 🎬

*Ready to transform your HR analytics? Start with OneLake. Add AI. Enable conversations.* 🚀
