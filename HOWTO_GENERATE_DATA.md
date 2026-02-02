# How to Generate HR Demo Data

## Option 1: Run Python Script Directly (Recommended)

### Prerequisites
- Python 3.8 or higher
- pip

### Steps

1. **Install dependencies**
```powershell
cd "Scenario 10 - HR"
pip install -r requirements.txt
```

2. **Run the generator**
```powershell
cd src
python generate_hr_data.py
```

3. **Wait ~2-3 minutes**

4. **Verify output**
```powershell
# Check CSV files
Get-ChildItem ..\data\raw\hr\*.csv

# Check text reports
Get-ChildItem ..\data\raw\reports_txt\*.txt | Measure-Object

# View data dictionary
Get-Content ..\docs\data_dictionary.md
```

### Expected Output
```
✅ Departments: 12 rows
✅ Positions: 45 rows
✅ Employees: 500 rows
✅ Lifecycle Events: ~4000 rows
✅ Compensation History: ~1500 rows
✅ Absences: ~3000 rows
✅ Training Records: ~2500 rows
✅ HR Cases: ~150 rows
✅ Generated 200+ text reports
✅ Data dictionary saved
✅ VALIDATION COMPLETE
```

---

## Option 2: Run in Fabric Notebook (for Lakehouse integration)

### Steps

1. **Upload notebook to Fabric**
   - Upload `notebooks/00_generate_synthetic_hr_data.ipynb`
   - Attach to your Lakehouse

2. **Run all cells**
   - Click "Run all" (or Ctrl+Shift+Enter)

3. **Data will be generated directly in Lakehouse Files**

---

## Customization

### Change Number of Employees

Edit `config.yaml`:
```yaml
volumes:
  employees: 1000  # Change from 500 to 1000
```

### Change Date Range

Edit `config.yaml`:
```yaml
date_ranges:
  start_date: "2020-01-01"  # Extend back to 2020
  end_date: "2026-12-31"    # Extend to 2026
```

### Add New Department

Edit `config.yaml`:
```yaml
volumes:
  departments: 15  # Increase from 12
```

Then re-run generator.

---

## Troubleshooting

**Error: `ModuleNotFoundError: No module named 'pandas'`**
- Solution: `pip install pandas numpy pyyaml`

**Error: `FileNotFoundError: config.yaml not found`**
- Solution: Make sure you're in the `src/` directory when running

**Error: Data quality validation fails**
- Solution: This is expected if you modify config heavily. Check error messages for specific issues.

**Data looks wrong / unrealistic**
- Solution: Check your `config.yaml` for typos. The seed is deterministic, so same config = same data.

---

## Next Steps After Generation

1. **Review the data**
   - Open CSV files in Excel/VS Code
   - Read some .txt reports to see PII examples
   - Review `docs/data_dictionary.md`

2. **Upload to Fabric**
   - Follow `notebooks/03_semantic_and_agent_assets.md`

3. **Run transformation notebooks**
   - `01_silver_modeling.ipynb`
   - `02_text_enrichment.ipynb`

4. **Create Data Agent**
   - Use `agent/agent_instructions.md`
   - Import `agent/example_queries.json`

---

**That's it! You now have a complete synthetic HR dataset ready for Microsoft Fabric.**
