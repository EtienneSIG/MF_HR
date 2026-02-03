# HR Employee Lifecycle - Data Dictionary

**Generated:** 2026-02-03 18:21:10
**Seed:** 42
**Employees:** 500
**Date Range:** 2023-01-01 to 2025-12-31

---

## Tables Overview

| Table | Rows | Primary Key | Description |
|-------|------|-------------|-------------|
| departments | 12 | department_id | Organizational departments |
| positions | 45 | position_id | Job positions and salary bands |
| employees | 500 | employee_id | Employee master data |
| lifecycle_events | 9617 | event_id | All lifecycle events (hire, promotion, etc.) |
| compensation_history | 4570 | comp_id | Salary and compensation changes |
| absences | 16737 | absence_id | Employee absences and leaves |
| training_records | 10780 | training_id | Training and development records |
| hr_cases | 142 | case_id | HR cases (grievances, incidents) |

---

## Relationships

```
employees (employee_id)
├── FK: position_id → positions
├── FK: department_id → departments
├── FK: manager_id → employees (self-referencing)
│
├── lifecycle_events (employee_id)
│   ├── FK: from_position_id → positions
│   ├── FK: to_position_id → positions
│   ├── FK: from_department_id → departments
│   └── FK: to_department_id → departments
│
├── compensation_history (employee_id)
├── absences (employee_id)
│   └── FK: approved_by_manager_id → employees
├── training_records (employee_id)
└── hr_cases (employee_id)
```

---

## Table: departments

| Column | Type | Description |
|--------|------|-------------|
| department_id | STRING | Primary key (DEPT_XXX) |
| department_name | STRING | Department name |
| division | STRING | Parent division |
| cost_center | STRING | Cost center code |
| headcount_target | INTEGER | Target headcount |
| budget_eur | INTEGER | Annual budget (EUR) |

---

## Table: positions

| Column | Type | Description |
|--------|------|-------------|
| position_id | STRING | Primary key (POS_XXX) |
| job_title | STRING | Job title |
| job_family | STRING | Job family (Engineering, Sales, etc.) |
| job_level | STRING | Seniority level |
| salary_band | STRING | Salary band (junior, senior, etc.) |
| min_salary_eur | INTEGER | Minimum salary for band |
| max_salary_eur | INTEGER | Maximum salary for band |
| is_people_manager | BOOLEAN | Is a people manager role |

---

## Table: employees

| Column | Type | Description |
|--------|------|-------------|
| employee_id | STRING | Primary key (EMP_XXXXXX) |
| first_name | STRING | First name (FICTIONAL) |
| last_name | STRING | Last name (FICTIONAL) |
| email | STRING | Email (FICTIONAL - @example.com) |
| phone | STRING | Phone (FICTIONAL) |
| hire_date | DATE | Date of hire |
| termination_date | DATE | Date of termination (NULL if active) |
| status | STRING | Employment status (active/terminated) |
| position_id | STRING | FK to positions |
| department_id | STRING | FK to departments |
| manager_id | STRING | FK to employees (manager) |
| work_location | STRING | Country/region |
| employment_type | STRING | Full-Time/Part-Time |

---

## Table: lifecycle_events

| Column | Type | Description |
|--------|------|-------------|
| event_id | STRING | Primary key (EVT_XXXXXXXX) |
| employee_id | STRING | FK to employees |
| event_type | STRING | Event type (hire, promotion, etc.) |
| event_date | DATE | Date of event |
| from_position_id | STRING | Position before event (for moves/promotions) |
| to_position_id | STRING | Position after event |
| from_department_id | STRING | Department before event |
| to_department_id | STRING | Department after event |
| notes | STRING | Event notes |

**Event Types:**
- hire, onboarding_completed, probation_completed
- internal_move, promotion
- performance_review, training_completed
- parental_leave_start, sick_leave_long
- disciplinary_action
- exit_interview, resignation, termination

---

## Table: compensation_history

| Column | Type | Description |
|--------|------|-------------|
| comp_id | STRING | Primary key (COMP_XXXXXXXX) |
| employee_id | STRING | FK to employees |
| effective_date | DATE | Compensation effective date |
| base_salary_eur | INTEGER | Base salary (EUR) |
| currency | STRING | Currency code |
| bonus_target_pct | INTEGER | Bonus target percentage |
| equity_grant_eur | INTEGER | Equity grant value (EUR) |
| compensation_review_reason | STRING | Reason for change (hire, promotion, annual_review) |

---

## Table: absences

| Column | Type | Description |
|--------|------|-------------|
| absence_id | STRING | Primary key (ABS_XXXXXXXX) |
| employee_id | STRING | FK to employees |
| absence_type | STRING | Type of absence |
| start_date | DATE | Start date |
| end_date | DATE | End date |
| days_taken | INTEGER | Number of days |
| approval_status | STRING | Approval status |
| approved_by_manager_id | STRING | FK to employees (manager) |

**Absence Types:**
- vacation, sick_leave_short, sick_leave_long
- parental_leave, unpaid_leave

---

## Table: training_records

| Column | Type | Description |
|--------|------|-------------|
| training_id | STRING | Primary key (TRN_XXXXXXX) |
| employee_id | STRING | FK to employees |
| training_name | STRING | Training course name |
| training_category | STRING | Training category |
| training_date | DATE | Training date |
| completion_status | STRING | Completion status |
| hours | INTEGER | Training hours |
| cost_eur | INTEGER | Training cost (EUR) |
| provider | STRING | Training provider |

---

## Table: hr_cases

| Column | Type | Description |
|--------|------|-------------|
| case_id | STRING | Primary key (CASE_XXXXXX) |
| employee_id | STRING | FK to employees |
| case_type | STRING | Type of case |
| case_date | DATE | Case opened date |
| case_status | STRING | Current status |
| priority | STRING | Priority level |
| assigned_to_hr_specialist | STRING | Assigned HR specialist ID |
| resolution_date | DATE | Resolution date (NULL if open) |
| description | STRING | Case description |

**Case Types:**
- performance_concern, interpersonal_conflict
- accommodation_request, policy_violation
- compensation_inquiry, harassment_complaint
- workplace_safety

---

## Text Reports (in data/raw/reports_txt/)

**Format:** `report_type_XXXX.txt`

**Linked to:**
- Performance reviews → lifecycle_events (performance_review)
- Exit interviews → lifecycle_events (exit_interview)
- Case notes → hr_cases
- Onboarding feedback → lifecycle_events (onboarding_completed)

**Structure:**
```
REPORT_TYPE: <type>
EMPLOYEE_ID: <id>
EVENT_ID or CASE_ID: <id>
DATE: <date>

<narrative text with PII for redaction demo>
```

---

## Data Quality Metrics

- **Referential Integrity:** All FK constraints validated
- **Duplicate Keys:** None
- **Missing Required Fields:** < 0.1%
- **Active Employees:** 439 (87.8%)
- **Terminated Employees:** 61 (12.2%)

---

## Key HR Metrics (Calculated)

### Headcount
```
Current Headcount = COUNT(employees WHERE status = 'active')
```

### Attrition Rate
```
Annual Attrition Rate = (Exits in Year / Avg Headcount in Year) × 100%
```

### Tenure
```
Average Tenure = AVG(TODAY() - hire_date) for active employees
```

### Time to Fill
```
Time to Fill = AVG(hire_date - requisition_date) - NOT IN THIS DATASET
```

### Promotion Rate
```
Promotion Rate = (Promotions in Period / Headcount) × 100%
```

### Internal Mobility
```
Internal Mobility Rate = (Transfers + Promotions) / Headcount
```

### Training Investment
```
Training Hours per FTE = SUM(training hours) / Headcount
Training Cost per FTE = SUM(training cost) / Headcount
```

---

**⚠️ IMPORTANT: All data in this dataset is SYNTHETIC and FICTIONAL. No real personal data is included.**
