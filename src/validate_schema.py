"""
Script de Validation des Noms de Colonnes - HR Employee Lifecycle Demo

Vérifie que tous les noms de colonnes correspondent au schéma attendu
et que les données sont cohérentes pour les DAX queries.

Usage:
    cd src
    python validate_schema.py
"""

import pandas as pd
import sys
from pathlib import Path

class SchemaValidator:
    def __init__(self, data_root='../data/raw'):
        self.data_root = Path(data_root)
        self.errors = []
        self.warnings = []
        
    def validate_all(self):
        """Exécute toutes les validations"""
        print("=" * 80)
        print("VALIDATION DES SCHEMAS - HR Employee Lifecycle Demo")
        print("=" * 80)
        print()
        
        # Validation des tables HR
        self.validate_hr_tables()
        
        # Validation des rapports texte
        self.validate_text_reports()
        
        # Validation des relations
        self.validate_relationships()
        
        # Afficher le résumé
        self.print_summary()
        
        return len(self.errors) == 0
    
    def validate_hr_tables(self):
        """Valide les tables HR"""
        print("--- Validation HR Tables ---")
        
        # dim_employees (CRITIQUE pour DAX)
        employees = self.load_csv('hr/dim_employees.csv')
        if employees is not None:
            self.check_columns(employees, 'employees', [
                'employee_id', 'first_name', 'last_name', 'email', 'phone',
                'hire_date', 'termination_date', 'status',
                'position_id', 'department_id', 'manager_id',
                'work_location', 'employment_type'
            ])
            
            # Vérifier format employee_id
            sample_id = employees['employee_id'].iloc[0]
            if not sample_id.startswith('EMP_'):
                self.errors.append("employees.employee_id doit être au format 'EMP_XXXXXX'")
            
            # Vérifier status values
            if 'status' in employees.columns:
                statuses = employees['status'].unique()
                expected_statuses = {'active', 'terminated'}
                invalid_statuses = set(statuses) - expected_statuses
                if invalid_statuses:
                    self.errors.append(
                        f"employees.status contient des valeurs invalides: {invalid_statuses}. "
                        f"Attendu: {expected_statuses}"
                    )
                else:
                    print(f"  ✅ employees.status correct (active, terminated)")
        
        # dim_departments
        departments = self.load_csv('hr/dim_departments.csv')
        if departments is not None:
            self.check_columns(departments, 'departments', [
                'department_id', 'department_name', 'division',
                'cost_center', 'headcount_target', 'budget_eur'
            ])
            
            # Vérifier format department_id
            sample_id = departments['department_id'].iloc[0]
            if not sample_id.startswith('DEPT_'):
                self.errors.append("departments.department_id doit être au format 'DEPT_XXX'")
        
        # dim_positions
        positions = self.load_csv('hr/dim_positions.csv')
        if positions is not None:
            self.check_columns(positions, 'positions', [
                'position_id', 'job_title', 'job_family', 'job_level',
                'salary_band', 'min_salary_eur', 'max_salary_eur', 'is_people_manager'
            ])
        
        # lifecycle_events (CRITIQUE)
        events = self.load_csv('hr/lifecycle_events.csv')
        if events is not None:
            self.check_columns(events, 'lifecycle_events', [
                'event_id', 'employee_id', 'event_date', 'event_type',
                'from_position_id', 'to_position_id',
                'from_department_id', 'to_department_id', 'notes'
            ])
            
            # Vérifier event_type values
            if 'event_type' in events.columns:
                event_types = events['event_type'].unique()
                print(f"  ℹ️  Types d'événements: {len(event_types)} types trouvés")
                
                # Vérifier événements critiques
                critical_types = {'hire', 'promotion', 'resignation', 'termination'}
                found_critical = set(event_types) & critical_types
                if len(found_critical) < len(critical_types):
                    missing = critical_types - found_critical
                    self.warnings.append(
                        f"lifecycle_events: événements critiques manquants: {missing}"
                    )
        
        # compensation_history
        compensation = self.load_csv('hr/compensation_history.csv')
        if compensation is not None:
            self.check_columns(compensation, 'compensation_history', [
                'comp_id', 'employee_id', 'effective_date',
                'base_salary_eur', 'bonus_target_pct', 'equity_grant_eur',
                'compensation_review_reason'
            ])
            
            # Vérifier salaires positifs
            if 'base_salary_eur' in compensation.columns:
                min_salary = compensation['base_salary_eur'].min()
                if min_salary <= 0:
                    self.errors.append(
                        f"compensation_history.base_salary_eur doit être > 0. "
                        f"Trouvé min={min_salary}"
                    )
                else:
                    print(f"  ✅ compensation_history.base_salary_eur correct (> 0)")
        
        # fact_absences
        absences = self.load_csv('hr/fact_absences.csv')
        if absences is not None:
            self.check_columns(absences, 'absences', [
                'absence_id', 'employee_id', 'start_date', 'end_date',
                'absence_type', 'days_taken', 'approval_status'
            ])
        
        # training_records
        training = self.load_csv('hr/training_records.csv')
        if training is not None:
            self.check_columns(training, 'training_records', [
                'training_id', 'employee_id', 'training_date',
                'training_name', 'training_category',
                'completion_status', 'hours', 'cost_eur', 'provider'
            ])
        
        # fact_hr_cases
        cases = self.load_csv('hr/fact_hr_cases.csv')
        if cases is not None:
            self.check_columns(cases, 'hr_cases', [
                'case_id', 'employee_id', 'case_date', 'case_type',
                'case_status', 'priority', 'assigned_to_hr_specialist',
                'resolution_date'
            ])
        
        print()
    
    def validate_text_reports(self):
        """Valide les rapports texte"""
        print("--- Validation Rapports Texte ---")
        
        reports_dir = self.data_root / 'reports_txt'
        
        if not reports_dir.exists():
            self.warnings.append("Dossier reports_txt/ manquant (optionnel pour AI transformations)")
            print(f"  ⚠️  Dossier reports_txt/ non trouvé (optionnel)")
            return
        
        txt_files = list(reports_dir.glob('*.txt'))
        
        if len(txt_files) == 0:
            self.warnings.append("Aucun fichier .txt trouvé dans reports_txt/")
            print(f"  ⚠️  Aucun rapport texte trouvé")
        else:
            print(f"  ✅ {len(txt_files)} rapports texte trouvés")
            
            # Vérifier un échantillon de rapports
            sample_report = txt_files[0]
            try:
                with open(sample_report, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Vérifier présence de headers attendus
                    required_headers = ['EMPLOYEE_ID:', 'DATE:', 'REPORT_TYPE:']
                    missing_headers = [h for h in required_headers if h not in content]
                    
                    if missing_headers:
                        self.warnings.append(
                            f"Rapport {sample_report.name}: headers manquants: {missing_headers}"
                        )
                    else:
                        print(f"  ✅ Format de rapport correct (headers présents)")
            except Exception as e:
                self.errors.append(f"Erreur lecture rapport {sample_report.name}: {e}")
        
        print()
    
    def validate_relationships(self):
        """Valide les relations entre tables (foreign keys)"""
        print("--- Validation Relations (Foreign Keys) ---")
        
        # Charger les tables principales
        employees = self.load_csv('hr/employees.csv')
        departments = self.load_csv('hr/departments.csv')
        positions = self.load_csv('hr/positions.csv')
        events = self.load_csv('hr/lifecycle_events.csv')
        compensation = self.load_csv('hr/compensation_history.csv')
        
        if employees is None or departments is None or positions is None:
            self.errors.append("Impossible de valider les relations: tables manquantes")
            return
        
        # Vérifier employees.department_id → departments.department_id
        invalid_depts = ~employees['department_id'].isin(departments['department_id'])
        if invalid_depts.any():
            self.errors.append(
                f"{invalid_depts.sum()} employees avec department_id invalide"
            )
        else:
            print(f"  ✅ employees.department_id → departments.department_id (100% valide)")
        
        # Vérifier employees.position_id → positions.position_id
        invalid_positions = ~employees['position_id'].isin(positions['position_id'])
        if invalid_positions.any():
            self.errors.append(
                f"{invalid_positions.sum()} employees avec position_id invalide"
            )
        else:
            print(f"  ✅ employees.position_id → positions.position_id (100% valide)")
        
        # Vérifier employees.manager_id → employees.employee_id (auto-référence)
        managers = employees['manager_id'].dropna()
        invalid_managers = ~managers.isin(employees['employee_id'])
        if invalid_managers.any():
            self.errors.append(
                f"{invalid_managers.sum()} employees avec manager_id invalide"
            )
        else:
            print(f"  ✅ employees.manager_id → employees.employee_id (100% valide)")
        
        # Vérifier lifecycle_events.employee_id → employees.employee_id
        if events is not None:
            invalid_event_employees = ~events['employee_id'].isin(employees['employee_id'])
            if invalid_event_employees.any():
                self.errors.append(
                    f"{invalid_event_employees.sum()} lifecycle_events avec employee_id invalide"
                )
            else:
                print(f"  ✅ lifecycle_events.employee_id → employees.employee_id (100% valide)")
        
        # Vérifier compensation_history.employee_id → employees.employee_id
        if compensation is not None:
            invalid_comp_employees = ~compensation['employee_id'].isin(employees['employee_id'])
            if invalid_comp_employees.any():
                self.errors.append(
                    f"{invalid_comp_employees.sum()} compensation_history avec employee_id invalide"
                )
            else:
                print(f"  ✅ compensation_history.employee_id → employees.employee_id (100% valide)")
        
        print()
    
    def check_columns(self, df, table_name, expected_columns):
        """Vérifie que les colonnes attendues sont présentes"""
        missing = set(expected_columns) - set(df.columns)
        extra = set(df.columns) - set(expected_columns)
        
        if missing:
            self.errors.append(f"{table_name}: colonnes manquantes: {missing}")
        
        if extra:
            self.warnings.append(f"{table_name}: colonnes inattendues: {extra}")
        
        if not missing and not extra:
            print(f"  ✅ {table_name}: {len(expected_columns)} colonnes valides")
    
    def load_csv(self, relative_path):
        """Charge un CSV et gère les erreurs"""
        filepath = self.data_root / relative_path
        
        if not filepath.exists():
            self.errors.append(f"Fichier manquant: {filepath}")
            return None
        
        try:
            return pd.read_csv(filepath, encoding='utf-8')
        except Exception as e:
            self.errors.append(f"Erreur lecture {filepath}: {e}")
            return None
    
    def print_summary(self):
        """Affiche le résumé des validations"""
        print("=" * 80)
        print("RÉSUMÉ DE VALIDATION")
        print("=" * 80)
        
        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} AVERTISSEMENT(S):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if self.errors:
            print(f"\n❌ {len(self.errors)} ERREUR(S):")
            for error in self.errors:
                print(f"  - {error}")
            print("\n🔧 ACTIONS REQUISES:")
            print("  1. Corriger les erreurs listées ci-dessus")
            print("  2. Régénérer les données avec generate_hr_data.py")
            print("  3. Relancer ce script de validation")
            print("\n❌ VALIDATION ÉCHOUÉE")
        else:
            print("\n✅ VALIDATION RÉUSSIE - Tous les schémas sont corrects !")
            print("\n✅ Les DAX queries devraient fonctionner correctement.")
        
        print("=" * 80)


def main():
    """Point d'entrée principal"""
    validator = SchemaValidator()
    success = validator.validate_all()
    
    # Exit code pour CI/CD
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
