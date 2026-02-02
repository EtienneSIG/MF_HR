# Microsoft Fabric Setup Guide
# HR Employee Lifecycle Demo - Data Agent Configuration

This guide provides step-by-step instructions to deploy the HR Employee Lifecycle demo in Microsoft Fabric.

---

## Prerequisites

✅ Microsoft Fabric workspace (with appropriate permissions)  
✅ Synthetic data generated (run `00_generate_synthetic_hr_data.ipynb`)  
✅ Data files ready in `data/raw/hr/` and `data/raw/reports_txt/`

---

## Phase 1: Create Lakehouse & Upload Data

### Step 1: Create a Lakehouse

1. Navigate to your **Microsoft Fabric workspace**
2. Click **+ New** → **Lakehouse**
3. Name: `hr_lakehouse`
4. Click **Create**

### Step 2: Upload Raw Data Files

**Option A: Upload via UI (Recommended for small datasets)**

1. In `hr_lakehouse`, navigate to **Files**
2. Create folder: `hr_raw`
   - Click **New subfolder** → Name: `hr_raw`
3. Upload CSV files:
   - Click `hr_raw` folder
   - Click **Upload** → **Upload files**
   - Select all 8 CSV files from `data/raw/hr/`:
     - employees.csv
     - departments.csv
     - positions.csv
     - lifecycle_events.csv
     - compensation_history.csv
     - absences.csv
     - training_records.csv
     - hr_cases.csv
   - Click **Upload**

4. Create folder: `reports_txt`
   - Back to **Files** root
   - Click **New subfolder** → Name: `reports_txt`
5. Upload text reports:
   - Click `reports_txt` folder
   - Click **Upload** → **Upload files**
   - Select all .txt files from `data/raw/reports_txt/` (~200 files)
   - Click **Upload**

**Option B: Upload via Notebook (For automation)**

```python
# In a Fabric notebook attached to hr_lakehouse

import pandas as pd
from pathlib import Path

# Define local path (adjust if needed)
local_hr_path = Path("../data/raw/hr")

# Upload CSVs to Files/hr_raw
for csv_file in local_hr_path.glob("*.csv"):
    df = pd.read_csv(csv_file)
    lakehouse_path = f"Files/hr_raw/{csv_file.name}"
    
    # Write to Lakehouse Files (not Delta yet)
    spark_df = spark.createDataFrame(df)
    spark_df.write.mode("overwrite").format("parquet").save(lakehouse_path)
    print(f"✅ Uploaded {csv_file.name}")

# Upload text reports
local_reports_path = Path("../data/raw/reports_txt")
# Note: For text files, use notebookutils or manual upload
```

---

## Phase 2: Create OneLake Shortcuts

### Step 3: Create Shortcuts to Raw Files

**Purpose:** Connect raw files to Lakehouse without copying data

1. In `hr_lakehouse` → **Files** → `hr_raw`
2. For each CSV file:
   - Right-click file → **Create shortcut**
   - Type: **OneLake**
   - Select: Current workspace > hr_lakehouse > Files > hr_raw > [file]
   - Click **Create**

**Result:** Shortcuts appear in Lakehouse explorer (with shortcut icon)

---

## Phase 3: Apply Shortcut Transformations (Bronze Layer)

### Step 4: Auto-Sync CSV to Delta Tables

**Purpose:** Automatically convert CSV files to Delta format (Bronze layer)

1. Navigate to `hr_lakehouse` → **Tables** (left sidebar)
2. Click **New shortcut transformation**
3. Configure transformation:
   - **Source:** OneLake shortcut
   - **Select shortcut:** `Files/hr_raw/employees.csv`
   - **Transformation type:** Auto-sync to Delta
   - **Target table name:** `bronze_employees`
   - **Schedule:** Every 1 hour (or On-demand for demo)
   - Click **Create**

4. **Repeat for all 8 CSV files:**
   - `employees.csv` → `bronze_employees`
   - `departments.csv` → `bronze_departments`
   - `positions.csv` → `bronze_positions`
   - `lifecycle_events.csv` → `bronze_lifecycle_events`
   - `compensation_history.csv` → `bronze_compensation_history`
   - `absences.csv` → `bronze_absences`
   - `training_records.csv` → `bronze_training_records`
   - `hr_cases.csv` → `bronze_hr_cases`

5. **Trigger initial sync:**
   - For each transformation, click **Refresh now**
   - Wait 1-2 minutes for all tables to materialize

6. **Verify Bronze tables:**
   - Navigate to `hr_lakehouse` → **Tables**
   - Confirm 8 tables prefixed with `bronze_` appear
   - Click any table → **Preview** to see data

---

## Phase 4: Run Silver Transformation Notebook

### Step 5: Execute Silver Modeling

**Purpose:** Clean, standardize, and create dimensions/facts (Silver → Gold)

1. Upload notebook `01_silver_modeling.ipynb` to workspace:
   - Workspace → **+ New** → **Import notebook**
   - Select `notebooks/01_silver_modeling.ipynb`
   - Click **Upload**

2. Attach notebook to `hr_lakehouse`:
   - Open notebook
   - Top-left → **Lakehouse:** `hr_lakehouse` (if not auto-attached)

3. **Run all cells:**
   - Click **Run all** (or Ctrl+Shift+Enter)
   - Wait ~2-3 minutes

4. **Verify Silver/Gold tables created:**
   - `hr_lakehouse` → **Tables**
   - Confirm new tables:
     - **Dimensions:** `dim_employee`, `dim_department`, `dim_position`, `dim_date`
     - **Facts:** `fact_lifecycle_event`, `fact_compensation`, `fact_absence`, `fact_training`, `fact_hr_case`

---

## Phase 5: Run Text Enrichment with AI

### Step 6: AI-Powered PII Redaction & Summarization

**Purpose:** Process text reports to redact PII and generate summaries

1. Upload notebook `02_text_enrichment.ipynb`:
   - Workspace → **+ New** → **Import notebook**
   - Select `notebooks/02_text_enrichment.ipynb`

2. Attach to `hr_lakehouse`

3. **Configure Fabric AI Functions:**
   - In notebook, verify AI functions are enabled:
     ```python
     from synapse.ml.services import *
     # This uses Fabric's built-in AI capabilities
     ```
   
   - **If AI Functions not available:**
     - Use regex-based PII redaction (fallback included in notebook)
     - Skip summarization or use rule-based summarization

4. **Run all cells:**
   - Click **Run all**
   - Wait ~5-10 minutes (AI processing 200 texts)

5. **Verify output:**
   - `hr_lakehouse` → **Tables**
   - Confirm `fact_hr_report` table exists
   - Preview table:
     - `report_text_redacted`: PII replaced with `[EMAIL]`, `[PHONE]`, etc.
     - `report_summary`: AI-generated summaries
     - `topics`: Extracted topics

---

## Phase 6: Create Semantic Model (Optional)

### Step 7: Build Power BI Semantic Model

**Purpose:** Define relationships and measures for Data Agent

**Option A: Direct Lake (Recommended)**
- Data Agent directly queries Delta tables in Lakehouse
- No separate semantic model needed
- Skip to Phase 7

**Option B: Power BI Semantic Model**
1. Open **Power BI Desktop**
2. **Get Data** → **OneLake data hub**
3. Select `hr_lakehouse`
4. Import tables:
   - All `dim_*` tables
   - All `fact_*` tables
5. **Define relationships:**
   - `fact_*[employee_key]` → `dim_employee[employee_key]`
   - `fact_*[date_key]` → `dim_date[date_key]`
   - `fact_lifecycle_event[from_position_id]` → `dim_position[position_id]`
   - `fact_lifecycle_event[to_position_id]` → `dim_position[position_id]` (inactive)
6. **Create measures** (see `docs/dax_measures.md`)
7. **Publish to workspace:**
   - File → Publish → Select workspace
   - Name: `HR_Semantic_Model`

---

## Phase 7: Create Fabric Data Agent

### Step 8: Configure Data Agent

1. Navigate to **Workspace**
2. Click **+ New** → **Data Agent** (or **Copilot** depending on Fabric version)
3. **Configure agent:**
   - **Name:** `HR_Lifecycle_Agent`
   - **Description:** "AI assistant for HR employee lifecycle analytics"
   
4. **Select data source:**
   - **Option A (Recommended):** Direct Lake
     - Select `hr_lakehouse`
     - Tables: All `dim_*` and `fact_*` tables
   
   - **Option B:** Semantic Model
     - Select `HR_Semantic_Model` (if created in Step 7)

5. **System Instructions:**
   - Click **Edit instructions**
   - **Copy/paste content from:** `agent/agent_instructions.md`
   - This file contains:
     - Data model explanation
     - Metric definitions
     - Privacy guardrails (no PII exposure)
     - Response formatting guidelines
     - Example Q&A patterns
   - Click **Save**

6. **Example Queries (Optional but Recommended):**
   - Click **Add example queries**
   - **Import JSON:** `agent/example_queries.json`
   - OR manually add top 10 questions:
     1. "What is our current headcount?"
     2. "What's our attrition rate this year?"
     3. "How many promotions happened in 2025?"
     4. "Show me training hours per employee"
     5. "What are the main themes from recent exit interviews?"
     6. "Which departments have highest attrition?"
     7. "What is our internal mobility rate?"
     8. "How many open HR cases do we have?"
     9. "What's the average time to promotion?"
     10. "Show top 5 HR KPIs"

7. **Advanced Settings (Optional):**
   - **Row-Level Security:** Configure if needed (manager hierarchy)
   - **Max response length:** 500 tokens
   - **Temperature:** 0.3 (more factual, less creative)

8. **Click Create**

---

## Phase 8: Test the Data Agent

### Step 9: Verify Agent Responses

1. Open `HR_Lifecycle_Agent`
2. **Test basic query:**
   ```
   What is our current headcount?
   ```
   **Expected response:**
   - Should return ~445 active employees
   - Breakdown by division
   - No individual names/emails

3. **Test AI-powered query:**
   ```
   What are the main reasons employees are leaving, based on exit interviews?
   ```
   **Expected response:**
   - Top themes from AI-summarized exit interviews
   - Categories like "career growth", "compensation", "work-life balance"
   - No exposed PII from original texts

4. **Test privacy guardrail:**
   ```
   Show me all employee emails
   ```
   **Expected response:**
   - Agent should refuse or only show employee_id
   - No PII exposed

5. **Test complex query:**
   ```
   Show attrition rate by department and seniority level for 2025
   ```
   **Expected response:**
   - Multi-dimensional table
   - Percentages calculated correctly

6. **Test trend analysis:**
   ```
   Is our promotion rate improving over time?
   ```
   **Expected response:**
   - Year-over-year trend (2023 → 2024 → 2025)
   - Visual trend indicator (if supported)

---

## Phase 9: Demo Preparation

### Step 10: Prepare Demo Script

**10-Minute Demo Flow:**

1. **Intro (1 min):**
   - "We're analyzing 500 employees across 3 years"
   - "All data is synthetic - GDPR-safe for demo"

2. **Show Raw Data (1 min):**
   - Navigate to `hr_lakehouse` → **Files** → `hr_raw`
   - Show CSV files
   - Open one .txt report (show PII like emails, phones)

3. **Show Shortcut Transformations (2 min):**
   - Navigate to **Tables** → `bronze_employees`
   - Explain: "Auto-synced from CSV to Delta, zero ETL"
   - Show refresh schedule

4. **Show AI Transformation (2 min):**
   - Navigate to `fact_hr_report` table
   - Compare columns:
     - `report_text_original` (with PII) — **DO NOT EXPOSE IN DEMO**
     - `report_text_redacted` ([EMAIL], [PHONE])
     - `report_summary` (AI-generated)
     - `topics` (AI-extracted)
   - Explain: "Fabric AI auto-redacted PII and summarized"

5. **Data Agent Q&A (4 min):**
   - Open `HR_Lifecycle_Agent`
   - Ask 5 "wow" questions (see README.md)
   - Highlight:
     - Conversational interface
     - No SQL required
     - Privacy-preserving (no PII in responses)
     - AI-powered insights from text reports

6. **Wrap-up (1 min):**
   - "From raw files → AI enrichment → conversational analytics"
   - "OneLake + AI + Data Agent = Modern HR analytics"

---

## Troubleshooting

### Issue: Shortcut Transformation Not Working

**Symptoms:** Bronze tables not appearing after "Refresh now"

**Solutions:**
1. Verify shortcut path is correct (`Files/hr_raw/employees.csv`)
2. Check file format (must be CSV with header row)
3. Ensure no special characters in column names
4. Try manual trigger: Transformations → Select transformation → **Refresh now**
5. Check logs: Transformations → Select transformation → **View details** → **Logs**

---

### Issue: AI Functions Not Available

**Symptoms:** `fact_hr_report` creation fails with "AI function not found"

**Solutions:**
1. **Check Fabric capacity tier:**
   - AI functions require F64 or higher
   - Workspace settings → Capacity: Verify tier
2. **Use fallback regex redaction:**
   - Notebook includes regex-based PII detection
   - Uncomment fallback code in `02_text_enrichment.ipynb`
3. **Skip AI summarization:**
   - Generate reports without `report_summary` column
   - Use only `topics` (rule-based extraction)

---

### Issue: Data Agent Exposes PII

**Symptoms:** Agent returns employee names, emails in responses

**Solutions:**
1. **Verify system instructions:**
   - Agent settings → **Edit instructions**
   - Confirm `agent/agent_instructions.md` content is pasted
   - Check "Privacy Guardrails" section is included
2. **Test explicitly:**
   - Ask: "Show me employee names for department X"
   - Agent should refuse or only show employee_id
3. **Retrain if needed:**
   - Delete and recreate agent with correct instructions

---

### Issue: Agent Can't Answer Questions

**Symptoms:** "I don't have access to this data" errors

**Solutions:**
1. **Verify data source connection:**
   - Agent settings → Data source: Confirm `hr_lakehouse` or semantic model selected
   - Tables: Verify all `dim_*` and `fact_*` tables are checked
2. **Check table relationships:**
   - If using semantic model, verify relationships are active
   - Data Agent needs FK relationships to join tables
3. **Simplify question:**
   - Instead of: "Show me the thing"
   - Try: "What is the current headcount?"

---

## Next Steps

### Enhancements to Consider

1. **Add Real-Time Ingestion:**
   - Use Event Streams to ingest new hire/exit events
   - Update Delta tables in real-time

2. **Add Predictive Analytics:**
   - Build ML model for attrition prediction
   - Store predictions in `fact_attrition_risk` table

3. **Integrate with HRIS:**
   - Connect to Workday/SAP SuccessFactors via API
   - Replace synthetic data with real (anonymized) data

4. **Add Row-Level Security:**
   - Configure manager hierarchy in semantic model
   - Managers only see their directs & indirects

5. **Create Power BI Report:**
   - Build executive dashboard
   - Embed Data Agent chat widget

---

## Resources

- **Microsoft Fabric Docs:** https://learn.microsoft.com/en-us/fabric/
- **Data Agent Guide:** https://learn.microsoft.com/en-us/fabric/data-science/data-agent
- **OneLake Shortcuts:** https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts
- **AI Functions:** https://learn.microsoft.com/en-us/fabric/data-science/ai-services

---

**You're now ready to demo HR Employee Lifecycle Analytics with Fabric! 🎉**
