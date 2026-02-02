# HR Employee Lifecycle - Data Schema

## Table Summary

| Layer | Table | Type | Rows (approx) | Primary Key | Description |
|-------|-------|------|---------------|-------------|-------------|
| Bronze | bronze_employees | Fact | 500 | employee_id | Raw employee master data |
| Bronze | bronze_departments | Dimension | 12 | department_id | Raw departments |
| Bronze | bronze_positions | Dimension | 45 | position_id | Raw positions & salary bands |
| Bronze | bronze_lifecycle_events | Fact | 4000 | event_id | Raw lifecycle events |
| Bronze | bronze_compensation_history | Fact | 1500 | comp_id | Raw compensation changes |
| Bronze | bronze_absences | Fact | 3000 | absence_id | Raw absences & leaves |
| Bronze | bronze_training_records | Fact | 2500 | training_id | Raw training records |
| Bronze | bronze_hr_cases | Fact | 150 | case_id | Raw HR cases |
| Silver | dim_employee | Dimension (SCD2) | 500 | employee_key | Curated employees with history |
| Silver | dim_department | Dimension | 12 | department_id | Departments |
| Silver | dim_position | Dimension | 45 | position_id | Positions |
| Silver | dim_date | Dimension | 1096 | date_key | Date dimension (3 years) |
| Gold | fact_lifecycle_event | Fact | 4000 | event_id | Lifecycle events (star schema) |
| Gold | fact_compensation | Fact | 1500 | comp_id | Compensation history (star schema) |
| Gold | fact_absence | Fact | 3000 | absence_id | Absences (star schema) |
| Gold | fact_training | Fact | 2500 | training_id | Training (star schema) |
| Gold | fact_hr_case | Fact | 150 | case_id | HR cases (star schema) |
| Gold | fact_hr_report | Fact | 200 | report_id | AI-enriched text reports |

---

## Bronze Layer (Raw Data)

### bronze_employees

**Purpose:** Raw employee master data from source system

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| employee_id | STRING | NO | Employee ID (EMP_XXXXXX) |
| first_name | STRING | NO | First name (FICTIONAL) |
| last_name | STRING | NO | Last name (FICTIONAL) |
| email | STRING | YES | Email address (fake@example.com) |
| phone | STRING | YES | Phone number (fictional) |
| hire_date | DATE | NO | Date of hire |
| termination_date | DATE | YES | Termination date (NULL if active) |
| status | STRING | NO | Employment status (active/terminated) |
| position_id | STRING | NO | FK → positions |
| department_id | STRING | NO | FK → departments |
| manager_id | STRING | YES | FK → employees (self-reference) |
| work_location | STRING | YES | Country/region |
| employment_type | STRING | NO | Full-Time / Part-Time |

**Sample Row:**
```
employee_id: EMP_000123
first_name: Sophie
last_name: Martin
email: sophie.martin@example.com
phone: +33 6 45 78 92 13
hire_date: 2023-04-15
termination_date: NULL
status: active
position_id: POS_008
department_id: DEPT_002
manager_id: EMP_000045
work_location: France
employment_type: Full-Time
```

---

### bronze_departments

**Purpose:** Organizational departments

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| department_id | STRING | NO | Department ID (DEPT_XXX) |
| department_name | STRING | NO | Department name |
| division | STRING | YES | Parent division |
| cost_center | STRING | YES | Cost center code |
| headcount_target | INTEGER | YES | Target headcount |
| budget_eur | INTEGER | YES | Annual budget (EUR) |

**Sample Row:**
```
department_id: DEPT_001
department_name: Engineering
division: Technology
cost_center: CC-1234
headcount_target: 80
budget_eur: 6400000
```

---

### bronze_positions

**Purpose:** Job positions and salary bands

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| position_id | STRING | NO | Position ID (POS_XXX) |
| job_title | STRING | NO | Job title |
| job_family | STRING | YES | Job family (Engineering, Sales, etc.) |
| job_level | STRING | YES | Seniority level (Junior, Senior, etc.) |
| salary_band | STRING | YES | Salary band category |
| min_salary_eur | INTEGER | YES | Min salary for band |
| max_salary_eur | INTEGER | YES | Max salary for band |
| is_people_manager | BOOLEAN | YES | People manager flag |

**Sample Row:**
```
position_id: POS_008
job_title: Senior Engineering
job_family: Engineering
job_level: Senior
salary_band: senior
min_salary_eur: 65000
max_salary_eur: 95000
is_people_manager: FALSE
```

---

### bronze_lifecycle_events

**Purpose:** All employee lifecycle events

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| event_id | STRING | NO | Event ID (EVT_XXXXXXXX) |
| employee_id | STRING | NO | FK → employees |
| event_type | STRING | NO | Type of event (see below) |
| event_date | DATE | NO | Event date |
| from_position_id | STRING | YES | Position before (for moves/promotions) |
| to_position_id | STRING | YES | Position after |
| from_department_id | STRING | YES | Department before |
| to_department_id | STRING | YES | Department after |
| notes | STRING | YES | Event notes |

**Event Types:**
- `hire` - New hire
- `onboarding_completed` - Onboarding finished
- `probation_completed` - Probation period ended
- `internal_move` - Transfer to another department
- `promotion` - Promotion to higher level
- `performance_review` - Annual/periodic review
- `training_completed` - Training course completed
- `parental_leave_start` - Parental leave begins
- `sick_leave_long` - Extended sick leave
- `disciplinary_action` - Disciplinary incident
- `exit_interview` - Exit interview conducted
- `resignation` - Voluntary resignation
- `termination` - Involuntary termination

---

### bronze_compensation_history

**Purpose:** Salary and compensation changes

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| comp_id | STRING | NO | Compensation record ID |
| employee_id | STRING | NO | FK → employees |
| effective_date | DATE | NO | Effective date of change |
| base_salary_eur | INTEGER | NO | Base annual salary (EUR) |
| currency | STRING | NO | Currency code |
| bonus_target_pct | INTEGER | YES | Bonus target % of base |
| equity_grant_eur | INTEGER | YES | Equity grant value (EUR) |
| compensation_review_reason | STRING | YES | Reason (hire, promotion, annual_review) |

---

### bronze_absences

**Purpose:** Employee absences and leaves

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| absence_id | STRING | NO | Absence ID |
| employee_id | STRING | NO | FK → employees |
| absence_type | STRING | NO | Type (vacation, sick_leave, parental_leave, etc.) |
| start_date | DATE | NO | Start date |
| end_date | DATE | NO | End date |
| days_taken | INTEGER | NO | Number of days |
| approval_status | STRING | YES | Status (approved, pending) |
| approved_by_manager_id | STRING | YES | FK → employees (manager) |

---

### bronze_training_records

**Purpose:** Training and development records

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| training_id | STRING | NO | Training record ID |
| employee_id | STRING | NO | FK → employees |
| training_name | STRING | NO | Training course name |
| training_category | STRING | YES | Category (Technical, Leadership, etc.) |
| training_date | DATE | NO | Training date |
| completion_status | STRING | YES | Status (completed, in_progress) |
| hours | INTEGER | YES | Training hours |
| cost_eur | INTEGER | YES | Training cost (EUR) |
| provider | STRING | YES | Training provider |

---

### bronze_hr_cases

**Purpose:** HR cases and incidents

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| case_id | STRING | NO | Case ID |
| employee_id | STRING | NO | FK → employees |
| case_type | STRING | NO | Type (performance_concern, harassment_complaint, etc.) |
| case_date | DATE | NO | Case opened date |
| case_status | STRING | NO | Status (open, investigating, resolved, closed) |
| priority | STRING | YES | Priority (low, medium, high) |
| assigned_to_hr_specialist | STRING | YES | Assigned HR specialist |
| resolution_date | DATE | YES | Resolution date (NULL if open) |
| description | STRING | YES | Case description |

---

## Silver Layer (Curated Dimensions)

### dim_employee (SCD Type 2)

**Purpose:** Employee dimension with slowly changing dimension tracking

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| employee_key | INTEGER | NO | Surrogate key (auto-increment) |
| employee_id | STRING | NO | Business key (EMP_XXXXXX) |
| first_name | STRING | NO | First name |
| last_name | STRING | NO | Last name |
| email | STRING | YES | Email |
| phone | STRING | YES | Phone |
| hire_date | DATE | NO | Hire date |
| termination_date | DATE | YES | Termination date |
| status | STRING | NO | Status (active/terminated) |
| position_id | STRING | NO | Current position ID |
| department_id | STRING | NO | Current department ID |
| manager_id | STRING | YES | Current manager ID |
| work_location | STRING | YES | Work location |
| employment_type | STRING | NO | Employment type |
| **effective_start_date** | DATE | NO | SCD effective start |
| **effective_end_date** | DATE | YES | SCD effective end (NULL if current) |
| **is_current** | BOOLEAN | NO | Current record flag |
| **record_source** | STRING | YES | Source system |
| **created_at** | TIMESTAMP | NO | Record creation timestamp |
| **updated_at** | TIMESTAMP | YES | Last update timestamp |

**SCD Type 2 Example:**
```
employee_key: 123
employee_id: EMP_000050
position_id: POS_005
department_id: DEPT_001
effective_start_date: 2023-04-15
effective_end_date: 2024-06-01
is_current: FALSE

employee_key: 456
employee_id: EMP_000050  ← Same employee
position_id: POS_012     ← Promoted
department_id: DEPT_001
effective_start_date: 2024-06-01
effective_end_date: NULL
is_current: TRUE
```

---

### dim_department

**Purpose:** Department dimension

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| department_id | STRING | NO | PK (DEPT_XXX) |
| department_name | STRING | NO | Department name |
| division | STRING | YES | Parent division |
| cost_center | STRING | YES | Cost center code |
| headcount_target | INTEGER | YES | Target headcount |
| budget_eur | INTEGER | YES | Annual budget |

---

### dim_position

**Purpose:** Position dimension

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| position_id | STRING | NO | PK (POS_XXX) |
| job_title | STRING | NO | Job title |
| job_family | STRING | YES | Job family |
| job_level | STRING | YES | Seniority level |
| salary_band | STRING | YES | Salary band |
| min_salary_eur | INTEGER | YES | Min salary |
| max_salary_eur | INTEGER | YES | Max salary |
| is_people_manager | BOOLEAN | YES | Manager flag |

---

### dim_date

**Purpose:** Standard date dimension (3 years: 2023-2025)

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| date_key | INTEGER | NO | PK (YYYYMMDD format) |
| full_date | DATE | NO | Full date |
| year | INTEGER | NO | Year |
| quarter | INTEGER | NO | Quarter (1-4) |
| month | INTEGER | NO | Month (1-12) |
| month_name | STRING | NO | Month name |
| day | INTEGER | NO | Day of month |
| day_of_week | INTEGER | NO | Day of week (1=Monday) |
| day_of_week_name | STRING | NO | Day name |
| week_of_year | INTEGER | NO | ISO week number |
| is_weekend | BOOLEAN | NO | Weekend flag |
| is_holiday | BOOLEAN | NO | Holiday flag (optional) |
| fiscal_year | INTEGER | YES | Fiscal year |
| fiscal_quarter | INTEGER | YES | Fiscal quarter |

---

## Gold Layer (Fact Tables)

### fact_lifecycle_event

**Purpose:** Star schema fact table for lifecycle events

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| event_id | STRING | NO | PK (EVT_XXXXXXXX) |
| employee_key | INTEGER | NO | FK → dim_employee |
| event_date_key | INTEGER | NO | FK → dim_date |
| event_type | STRING | NO | Event type |
| from_position_id | STRING | YES | FK → dim_position |
| to_position_id | STRING | YES | FK → dim_position |
| from_department_id | STRING | YES | FK → dim_department |
| to_department_id | STRING | YES | FK → dim_department |
| notes | STRING | YES | Event notes |

**Measures:**
- Total Events
- Hires
- Exits (Resignations + Terminations)
- Promotions
- Internal Transfers

---

### fact_compensation

**Purpose:** Star schema fact table for compensation

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| comp_id | STRING | NO | PK |
| employee_key | INTEGER | NO | FK → dim_employee |
| effective_date_key | INTEGER | NO | FK → dim_date |
| base_salary_eur | INTEGER | NO | Base salary |
| bonus_target_pct | INTEGER | YES | Bonus % |
| equity_grant_eur | INTEGER | YES | Equity grant |
| compensation_review_reason | STRING | YES | Reason |

**Measures:**
- Average Salary
- Total Compensation Cost
- Compa-Ratio (actual/midpoint)

---

### fact_absence

**Purpose:** Star schema fact table for absences

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| absence_id | STRING | NO | PK |
| employee_key | INTEGER | NO | FK → dim_employee |
| start_date_key | INTEGER | NO | FK → dim_date |
| end_date_key | INTEGER | NO | FK → dim_date |
| absence_type | STRING | NO | Type |
| days_taken | INTEGER | NO | Days |
| approval_status | STRING | YES | Status |

**Measures:**
- Total Absence Days
- Absence Rate (days per FTE)
- Absence by Type

---

### fact_training

**Purpose:** Star schema fact table for training

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| training_id | STRING | NO | PK |
| employee_key | INTEGER | NO | FK → dim_employee |
| training_date_key | INTEGER | NO | FK → dim_date |
| training_name | STRING | NO | Training name |
| training_category | STRING | YES | Category |
| completion_status | STRING | YES | Status |
| hours | INTEGER | YES | Hours |
| cost_eur | INTEGER | YES | Cost |
| provider | STRING | YES | Provider |

**Measures:**
- Total Training Hours
- Training Hours per FTE
- Total Training Cost
- Cost per FTE

---

### fact_hr_case

**Purpose:** Star schema fact table for HR cases

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| case_id | STRING | NO | PK |
| employee_key | INTEGER | NO | FK → dim_employee |
| case_date_key | INTEGER | NO | FK → dim_date |
| case_type | STRING | NO | Type |
| case_status | STRING | NO | Status |
| priority | STRING | YES | Priority |
| assigned_to_hr_specialist | STRING | YES | Specialist |
| resolution_date | DATE | YES | Resolution date |
| description | STRING | YES | Description |

**Measures:**
- Open Cases
- Closed Cases
- Avg Resolution Time (days)
- Cases by Type

---

### fact_hr_report (AI-Enriched)

**Purpose:** AI-transformed text reports with PII redaction and summaries

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| report_id | STRING | NO | PK (RPT_XXXXXXXX) |
| employee_key | INTEGER | NO | FK → dim_employee |
| event_id | STRING | YES | FK → fact_lifecycle_event (nullable) |
| case_id | STRING | YES | FK → fact_hr_case (nullable) |
| report_type | STRING | NO | Type (performance_review, exit_interview, case_note, onboarding_feedback) |
| report_date_key | INTEGER | NO | FK → dim_date |
| **report_text_original** | STRING | YES | **⚠️ Original text with PII (audit only)** |
| **report_text_redacted** | STRING | NO | **✅ Redacted text ([EMAIL], [PHONE], etc.)** |
| **report_summary** | STRING | YES | **✅ AI-generated summary (2-3 sentences)** |
| **topics** | STRING | YES | **✅ AI-extracted topics (comma-separated)** |
| **sentiment** | STRING | YES | **✅ AI-detected sentiment (positive/neutral/negative)** |
| word_count | INTEGER | YES | Word count |
| pii_detected_flag | BOOLEAN | YES | PII detection flag |
| processing_timestamp | TIMESTAMP | YES | AI processing timestamp |

**Sample Row:**
```
report_id: RPT_00000123
employee_key: 456
event_id: EVT_00045678
report_type: exit_interview
report_text_redacted: "Exit interview conducted with [NAME] on 2025-11-15. Reason for leaving: career growth. Feedback on management: generally positive. Suggestions for improvement: clearer career paths. Contact: [EMAIL], [PHONE]. Rehire eligibility: yes."
report_summary: "Employee left for better career opportunities. Management feedback was positive, but suggested clearer promotion pathways."
topics: "career_growth, management_feedback, rehire_eligible"
sentiment: "neutral"
pii_detected_flag: TRUE
```

---

## Relationships (Star Schema)

```
dim_employee (employee_key)
  ├─ fact_lifecycle_event (employee_key) [1:N]
  ├─ fact_compensation (employee_key) [1:N]
  ├─ fact_absence (employee_key) [1:N]
  ├─ fact_training (employee_key) [1:N]
  ├─ fact_hr_case (employee_key) [1:N]
  └─ fact_hr_report (employee_key) [1:N]

dim_department (department_id)
  ├─ dim_employee (department_id) [1:N]
  ├─ fact_lifecycle_event (from_department_id) [1:N]
  └─ fact_lifecycle_event (to_department_id) [1:N]

dim_position (position_id)
  ├─ dim_employee (position_id) [1:N]
  ├─ fact_lifecycle_event (from_position_id) [1:N]
  └─ fact_lifecycle_event (to_position_id) [1:N]

dim_date (date_key)
  ├─ fact_lifecycle_event (event_date_key) [1:N]
  ├─ fact_compensation (effective_date_key) [1:N]
  ├─ fact_absence (start_date_key) [1:N]
  ├─ fact_absence (end_date_key) [1:N]
  ├─ fact_training (training_date_key) [1:N]
  ├─ fact_hr_case (case_date_key) [1:N]
  └─ fact_hr_report (report_date_key) [1:N]
```

---

## Data Flow

```
RAW FILES (CSV + TXT)
  ↓
ONELAKE SHORTCUTS
  ↓
SHORTCUT TRANSFORMATIONS (Auto-Sync)
  ↓
BRONZE LAYER (Delta Tables)
  ↓ (Notebook: 01_silver_modeling.ipynb)
SILVER LAYER (Dimensions + Facts)
  ↓ (Notebook: 02_text_enrichment.ipynb)
GOLD LAYER (Star Schema + AI Reports)
  ↓
FABRIC DATA AGENT (Conversational Analytics)
```

---

## Key Metrics Calculated from Schema

### Headcount
```sql
SELECT COUNT(DISTINCT employee_key)
FROM dim_employee
WHERE is_current = TRUE AND status = 'active'
```

### Attrition Rate
```sql
SELECT 
  (COUNT(DISTINCT CASE WHEN event_type IN ('resignation', 'termination') THEN employee_key END) 
   / AVG(headcount)) * 100 AS attrition_rate_pct
FROM fact_lifecycle_event
WHERE event_date >= '2025-01-01'
```

### Promotion Rate
```sql
SELECT 
  (COUNT(DISTINCT CASE WHEN event_type = 'promotion' THEN employee_key END)
   / COUNT(DISTINCT employee_key)) * 100 AS promotion_rate_pct
FROM fact_lifecycle_event
WHERE event_date >= '2025-01-01'
```

### Training Hours per FTE
```sql
SELECT 
  SUM(hours) / (SELECT COUNT(*) FROM dim_employee WHERE is_current = TRUE)
FROM fact_training
WHERE training_date >= '2025-01-01'
```

---

**End of Schema Documentation**
