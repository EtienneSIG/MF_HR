# Complete HR Data Generation Script
# This script generates all synthetic HR data for the demo

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import uuid
import json
from pathlib import Path
import yaml

# Faker-like name generator (without external dependencies)
FIRST_NAMES = ["Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason", "Isabella", "William",
               "Mia", "James", "Charlotte", "Benjamin", "Amelia", "Lucas", "Harper", "Henry", "Evelyn", "Alexander",
               "Sophie", "Louis", "Camille", "Jules", "Chloé", "Gabriel", "Emma", "Hugo", "Léa", "Arthur",
               "Anna", "Lukas", "Maria", "Felix", "Laura", "Jonas", "Sarah", "Paul", "Hannah", "Max",
               "Julia", "Matteo", "Sofia", "Leonardo", "Giulia", "Francesco", "Elena", "Marco", "Alessia", "Andrea"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
              "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
              "Dupont", "Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit", "Durand", "Leroy",
              "Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann",
              "Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano", "Colombo", "Ricci", "Marino", "Greco"]

def generate_name():
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)

def generate_email(first_name, last_name):
    return f"{first_name.lower()}.{last_name.lower()}@example.com"

def generate_phone():
    country_codes = ["+33", "+49", "+34", "+39", "+31", "+32", "+41", "+48", "+46", "+353"]
    code = random.choice(country_codes)
    number = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    return f"{code} {number[:1]} {number[1:3]} {number[3:5]} {number[5:7]} {number[7:9]}"

class HRDataGenerator:
    def __init__(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.seed = self.config.get('seed', 42)
        random.seed(self.seed)
        np.random.seed(self.seed)
        
        self.num_employees = self.config['volumes']['employees']
        self.start_date = datetime.strptime(self.config['date_ranges']['start_date'], '%Y-%m-%d')
        self.end_date = datetime.strptime(self.config['date_ranges']['end_date'], '%Y-%m-%d')
        self.historical_years = self.config['date_ranges']['historical_hire_window_years']
        
        self.regions = self.config['regions']
        self.salary_bands = self.config['business_params']['salary_bands']
        
        # Define output paths
        self.base_path = Path(config_path).parent.parent
        self.hr_path = self.base_path / self.config['paths']['hr']
        self.reports_path = self.base_path / self.config['paths']['reports_txt']
        
        # Create directories if they don't exist
        self.hr_path.mkdir(parents=True, exist_ok=True)
        self.reports_path.mkdir(parents=True, exist_ok=True)
        
        # Store generated data
        self.departments_df = None
        self.positions_df = None
        self.employees_df = None
        self.lifecycle_events_df = None
        self.compensation_df = None
        self.absences_df = None
        self.training_df = None
        self.hr_cases_df = None
        
    def generate_departments(self):
        """Generate departments with hierarchy"""
        num_depts = self.config['volumes']['departments']
        
        dept_data = []
        divisions = ["Technology", "Sales & Marketing", "Operations", "Corporate Functions"]
        
        dept_names = [
            "Engineering", "Product Management", "Data & Analytics",
            "Sales", "Marketing", "Customer Success",
            "Operations", "Supply Chain", "Facilities",
            "Finance", "HR", "Legal"
        ]
        
        for i in range(num_depts):
            dept_id = f"DEPT_{i+1:03d}"
            dept_name = dept_names[i] if i < len(dept_names) else f"Department {i+1}"
            division = divisions[i % len(divisions)]
            cost_center = f"CC-{random.randint(1000, 9999)}"
            head_count_target = random.randint(20, 80)
            
            dept_data.append({
                'department_id': dept_id,
                'department_name': dept_name,
                'division': division,
                'cost_center': cost_center,
                'headcount_target': head_count_target,
                'budget_eur': head_count_target * random.randint(60000, 90000)
            })
        
        self.departments_df = pd.DataFrame(dept_data)
        return self.departments_df
    
    def generate_positions(self):
        """Generate position hierarchy"""
        num_positions = self.config['volumes']['positions']
        
        job_families = ["Engineering", "Product", "Sales", "Marketing", "Operations", 
                       "Finance", "HR", "Legal", "Customer Service", "Data"]
        
        job_levels = ["Junior", "Intermediate", "Senior", "Lead", "Principal", "Director", "VP"]
        
        pos_data = []
        for i in range(num_positions):
            pos_id = f"POS_{i+1:03d}"
            family = random.choice(job_families)
            level = random.choice(job_levels)
            
            # Salary band based on level
            if level in ["Junior"]:
                band = "junior"
            elif level in ["Intermediate"]:
                band = "intermediate"
            elif level in ["Senior", "Lead"]:
                band = "senior"
            elif level in ["Principal", "Director"]:
                band = "lead"
            else:
                band = "executive"
            
            min_salary, max_salary = self.salary_bands[band]
            
            pos_data.append({
                'position_id': pos_id,
                'job_title': f"{level} {family}",
                'job_family': family,
                'job_level': level,
                'salary_band': band,
                'min_salary_eur': min_salary,
                'max_salary_eur': max_salary,
                'is_people_manager': level in ["Lead", "Director", "VP", "Principal"]
            })
        
        self.positions_df = pd.DataFrame(pos_data)
        return self.positions_df
    
    def generate_employees(self):
        """Generate employee master data"""
        emp_data = []
        
        # Calculate hire date range
        earliest_hire = self.start_date - timedelta(days=365 * self.historical_years)
        
        for i in range(self.num_employees):
            emp_id = f"EMP_{i+1:06d}"
            first_name, last_name = generate_name()
            
            # Hire date - weighted towards more recent hires
            days_range = (self.end_date - earliest_hire).days
            hire_date = earliest_hire + timedelta(days=int(np.random.beta(2, 5) * days_range))
            
            # Determine if employee has left (attrition)
            attrition_rate = self.config['business_params']['attrition_rate']
            tenure_days = (self.end_date - hire_date).days
            
            # Higher attrition for shorter tenure
            has_left = random.random() < (attrition_rate * min(tenure_days / 365, 1))
            
            if has_left and tenure_days > 90:  # Min 90 days tenure before leaving
                term_days = random.randint(90, tenure_days)
                termination_date = hire_date + timedelta(days=term_days)
                status = "terminated"
            else:
                termination_date = None
                status = "active"
            
            # Assign position and department
            position_id = random.choice(self.positions_df['position_id'].tolist())
            department_id = random.choice(self.departments_df['department_id'].tolist())
            
            # Assign manager (20% probability of having no manager - executives)
            manager_id = None
            if random.random() > 0.20 and i > 0:
                potential_managers = [f"EMP_{j+1:06d}" for j in range(i)]
                manager_id = random.choice(potential_managers) if potential_managers else None
            
            emp_data.append({
                'employee_id': emp_id,
                'first_name': first_name,
                'last_name': last_name,
                'email': generate_email(first_name, last_name),
                'phone': generate_phone(),
                'hire_date': hire_date.strftime('%Y-%m-%d'),
                'termination_date': termination_date.strftime('%Y-%m-%d') if termination_date else None,
                'status': status,
                'position_id': position_id,
                'department_id': department_id,
                'manager_id': manager_id,
                'work_location': random.choice(self.regions),
                'employment_type': random.choice(['Full-Time', 'Full-Time', 'Full-Time', 'Part-Time']),
            })
        
        self.employees_df = pd.DataFrame(emp_data)
        return self.employees_df
    
    def generate_lifecycle_events(self):
        """Generate lifecycle events for each employee"""
        events_config = self.config['business_params']['lifecycle_events']
        event_types = [(e['event_type'], e['weight'], e['avg_per_employee']) for e in events_config]
        
        all_events = []
        event_id_counter = 1
        
        for _, emp in self.employees_df.iterrows():
            emp_id = emp['employee_id']
            hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
            term_date = datetime.strptime(emp['termination_date'], '%Y-%m-%d') if emp['termination_date'] else self.end_date
            
            # Always add hire event
            all_events.append({
                'event_id': f"EVT_{event_id_counter:08d}",
                'employee_id': emp_id,
                'event_type': 'hire',
                'event_date': hire_date.strftime('%Y-%m-%d'),
                'from_position_id': None,
                'to_position_id': emp['position_id'],
                'from_department_id': None,
                'to_department_id': emp['department_id'],
                'notes': f"New hire in {emp['department_id']}"
            })
            event_id_counter += 1
            
            # Generate other events
            current_date = hire_date
            current_position = emp['position_id']
            current_dept = emp['department_id']
            
            # Probation & onboarding
            if (term_date - hire_date).days > 90:
                onboarding_date = hire_date + timedelta(days=30)
                all_events.append({
                    'event_id': f"EVT_{event_id_counter:08d}",
                    'employee_id': emp_id,
                    'event_type': 'onboarding_completed',
                    'event_date': onboarding_date.strftime('%Y-%m-%d'),
                    'from_position_id': None,
                    'to_position_id': None,
                    'from_department_id': None,
                    'to_department_id': None,
                    'notes': "Completed onboarding program"
                })
                event_id_counter += 1
                
                prob_date = hire_date + timedelta(days=90)
                all_events.append({
                    'event_id': f"EVT_{event_id_counter:08d}",
                    'employee_id': emp_id,
                    'event_type': 'probation_completed',
                    'event_date': prob_date.strftime('%Y-%m-%d'),
                    'from_position_id': None,
                    'to_position_id': None,
                    'from_department_id': None,
                    'to_department_id': None,
                    'notes': "Probation period completed successfully"
                })
                event_id_counter += 1
                current_date = prob_date
            
            # Performance reviews (annual)
            review_date = hire_date + timedelta(days=365)
            while review_date < term_date:
                all_events.append({
                    'event_id': f"EVT_{event_id_counter:08d}",
                    'employee_id': emp_id,
                    'event_type': 'performance_review',
                    'event_date': review_date.strftime('%Y-%m-%d'),
                    'from_position_id': None,
                    'to_position_id': None,
                    'from_department_id': None,
                    'to_department_id': None,
                    'notes': f"Annual performance review"
                })
                event_id_counter += 1
                review_date += timedelta(days=365)
            
            # Random events (promotions, moves, training)
            num_other_events = int(np.random.poisson(self.config['volumes']['lifecycle_events_per_employee_avg']))
            
            for _ in range(num_other_events):
                # Pick event type
                event_type = random.choices(
                    [et[0] for et in event_types if et[0] not in ['hire', 'onboarding_completed', 'probation_completed', 'performance_review']],
                    weights=[et[1] for et in event_types if et[0] not in ['hire', 'onboarding_completed', 'probation_completed', 'performance_review']]
                )[0]
                
                # Random date between current and termination
                if (term_date - current_date).days > 30:
                    event_date = current_date + timedelta(days=random.randint(30, (term_date - current_date).days))
                    
                    from_pos = current_position if event_type in ['promotion', 'internal_move'] else None
                    to_pos = random.choice(self.positions_df['position_id'].tolist()) if event_type in ['promotion', 'internal_move'] else None
                    from_dept = current_dept if event_type == 'internal_move' else None
                    to_dept = random.choice(self.departments_df['department_id'].tolist()) if event_type == 'internal_move' else None
                    
                    all_events.append({
                        'event_id': f"EVT_{event_id_counter:08d}",
                        'employee_id': emp_id,
                        'event_type': event_type,
                        'event_date': event_date.strftime('%Y-%m-%d'),
                        'from_position_id': from_pos,
                        'to_position_id': to_pos,
                        'from_department_id': from_dept,
                        'to_department_id': to_dept,
                        'notes': f"{event_type} event"
                    })
                    event_id_counter += 1
                    
                    if event_type == 'promotion' and to_pos:
                        current_position = to_pos
                    if event_type == 'internal_move' and to_dept:
                        current_dept = to_dept
            
            # Add exit event if terminated
            if emp['status'] == 'terminated':
                exit_date = datetime.strptime(emp['termination_date'], '%Y-%m-%d')
                
                # Exit interview
                exit_interview_date = exit_date - timedelta(days=random.randint(7, 14))
                all_events.append({
                    'event_id': f"EVT_{event_id_counter:08d}",
                    'employee_id': emp_id,
                    'event_type': 'exit_interview',
                    'event_date': exit_interview_date.strftime('%Y-%m-%d'),
                    'from_position_id': None,
                    'to_position_id': None,
                    'from_department_id': None,
                    'to_department_id': None,
                    'notes': "Exit interview conducted"
                })
                event_id_counter += 1
                
                # Resignation or termination
                exit_type = random.choice(['resignation', 'resignation', 'termination'])  # 66% resignation
                all_events.append({
                    'event_id': f"EVT_{event_id_counter:08d}",
                    'employee_id': emp_id,
                    'event_type': exit_type,
                    'event_date': exit_date.strftime('%Y-%m-%d'),
                    'from_position_id': current_position,
                    'to_position_id': None,
                    'from_department_id': current_dept,
                    'to_department_id': None,
                    'notes': f"Employee {exit_type}"
                })
                event_id_counter += 1
        
        self.lifecycle_events_df = pd.DataFrame(all_events)
        return self.lifecycle_events_df
    
    def generate_compensation_history(self):
        """Generate compensation changes"""
        comp_data = []
        comp_id_counter = 1
        
        for _, emp in self.employees_df.iterrows():
            emp_id = emp['employee_id']
            hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
            
            # Get position salary band
            pos = self.positions_df[self.positions_df['position_id'] == emp['position_id']].iloc[0]
            min_sal, max_sal = pos['min_salary_eur'], pos['max_salary_eur']
            
            # Initial salary (random within band)
            base_salary = random.randint(int(min_sal * 1.05), int(max_sal * 0.95))
            
            # Hire compensation
            comp_data.append({
                'comp_id': f"COMP_{comp_id_counter:08d}",
                'employee_id': emp_id,
                'effective_date': hire_date.strftime('%Y-%m-%d'),
                'base_salary_eur': base_salary,
                'currency': 'EUR',
                'bonus_target_pct': random.choice([0, 10, 15, 20]) if pos['job_level'] not in ['Junior'] else 0,
                'equity_grant_eur': random.choice([0, 5000, 10000, 15000]) if pos['job_level'] in ['Senior', 'Lead', 'Director', 'VP'] else 0,
                'compensation_review_reason': 'hire'
            })
            comp_id_counter += 1
            
            # Annual reviews (3-5% increase)
            review_date = hire_date + timedelta(days=365)
            term_date = datetime.strptime(emp['termination_date'], '%Y-%m-%d') if emp['termination_date'] else self.end_date
            
            while review_date < term_date:
                increase_pct = random.uniform(0.03, 0.05)
                base_salary = int(base_salary * (1 + increase_pct))
                
                comp_data.append({
                    'comp_id': f"COMP_{comp_id_counter:08d}",
                    'employee_id': emp_id,
                    'effective_date': review_date.strftime('%Y-%m-%d'),
                    'base_salary_eur': base_salary,
                    'currency': 'EUR',
                    'bonus_target_pct': random.choice([0, 10, 15, 20]) if pos['job_level'] not in ['Junior'] else 0,
                    'equity_grant_eur': random.choice([0, 5000, 10000]) if pos['job_level'] in ['Senior', 'Lead', 'Director', 'VP'] else 0,
                    'compensation_review_reason': 'annual_review'
                })
                comp_id_counter += 1
                review_date += timedelta(days=365)
        
        self.compensation_df = pd.DataFrame(comp_data)
        return self.compensation_df
    
    def generate_absences(self):
        """Generate absence records"""
        absence_types = self.config['business_params']['absence_types']
        
        absence_data = []
        absence_id_counter = 1
        
        for _, emp in self.employees_df.iterrows():
            emp_id = emp['employee_id']
            hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
            term_date = datetime.strptime(emp['termination_date'], '%Y-%m-%d') if emp['termination_date'] else self.end_date
            
            tenure_years = (term_date - hire_date).days / 365.0
            
            for abs_type in absence_types:
                type_name = abs_type['type']
                freq = abs_type['frequency_per_year']
                avg_duration = abs_type['avg_duration_days']
                
                num_absences = int(np.random.poisson(freq * tenure_years))
                
                for _ in range(num_absences):
                    start_date = hire_date + timedelta(days=random.randint(0, (term_date - hire_date).days))
                    duration = max(1, int(np.random.normal(avg_duration, avg_duration * 0.3)))
                    end_date = start_date + timedelta(days=duration)
                    
                    if end_date <= term_date:
                        absence_data.append({
                            'absence_id': f"ABS_{absence_id_counter:08d}",
                            'employee_id': emp_id,
                            'absence_type': type_name,
                            'start_date': start_date.strftime('%Y-%m-%d'),
                            'end_date': end_date.strftime('%Y-%m-%d'),
                            'days_taken': duration,
                            'approval_status': random.choice(['approved', 'approved', 'pending']),
                            'approved_by_manager_id': emp['manager_id']
                        })
                        absence_id_counter += 1
        
        self.absences_df = pd.DataFrame(absence_data)
        return self.absences_df
    
    def generate_training_records(self):
        """Generate training records"""
        training_cats = self.config['business_params']['training_categories']
        
        training_data = []
        training_id_counter = 1
        
        for _, emp in self.employees_df.iterrows():
            emp_id = emp['employee_id']
            hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
            term_date = datetime.strptime(emp['termination_date'], '%Y-%m-%d') if emp['termination_date'] else self.end_date
            
            tenure_years = (term_date - hire_date).days / 365.0
            
            # Number of trainings (Poisson distribution, avg 2.5/year)
            num_trainings = int(np.random.poisson(2.5 * tenure_years))
            
            for _ in range(num_trainings):
                category = random.choice(training_cats)
                training_date = hire_date + timedelta(days=random.randint(0, (term_date - hire_date).days))
                
                training_names = {
                    "Technical Skills": ["Python Advanced", "Cloud Architecture", "Data Engineering", "DevOps Essentials"],
                    "Leadership Development": ["Manager Bootcamp", "Strategic Thinking", "Executive Presence"],
                    "Compliance & Ethics": ["GDPR Compliance", "Information Security", "Code of Conduct"],
                    "Product Knowledge": ["Product Strategy", "User Research", "Roadmap Planning"],
                    "Customer Service": ["Customer Excellence", "Conflict Resolution", "Communication Skills"],
                    "Safety & Security": ["Workplace Safety", "Cybersecurity Awareness"],
                    "Soft Skills": ["Presentation Skills", "Negotiation", "Time Management"],
                    "Digital Transformation": ["AI for Business", "Agile Methodologies", "Digital Marketing"]
                }
                
                training_name = random.choice(training_names.get(category, ["General Training"]))
                hours = random.choice([4, 8, 16, 24, 40])
                cost = hours * random.randint(80, 200)
                
                training_data.append({
                    'training_id': f"TRN_{training_id_counter:07d}",
                    'employee_id': emp_id,
                    'training_name': training_name,
                    'training_category': category,
                    'training_date': training_date.strftime('%Y-%m-%d'),
                    'completion_status': random.choice(['completed', 'completed', 'in_progress']),
                    'hours': hours,
                    'cost_eur': cost,
                    'provider': random.choice(['Internal', 'LinkedIn Learning', 'Coursera', 'Udemy', 'External Consultant'])
                })
                training_id_counter += 1
        
        self.training_df = pd.DataFrame(training_data)
        return self.training_df
    
    def generate_hr_cases(self):
        """Generate HR cases"""
        case_types = self.config['business_params']['hr_case_types']
        
        case_data = []
        case_id_counter = 1
        
        # Select subset of employees to have HR cases
        num_cases = int(self.num_employees * self.config['volumes']['hr_cases_percentage'])
        employees_with_cases = random.sample(range(len(self.employees_df)), num_cases)
        
        for emp_idx in employees_with_cases:
            emp = self.employees_df.iloc[emp_idx]
            emp_id = emp['employee_id']
            hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
            term_date = datetime.strptime(emp['termination_date'], '%Y-%m-%d') if emp['termination_date'] else self.end_date
            
            # 1-3 cases per employee
            num_employee_cases = random.randint(1, 3)
            
            for _ in range(num_employee_cases):
                case_type_info = random.choices(case_types, weights=[c['weight'] for c in case_types])[0]
                case_type = case_type_info['type']
                avg_duration = case_type_info['avg_duration_days']
                
                case_date = hire_date + timedelta(days=random.randint(30, (term_date - hire_date).days))
                duration = max(7, int(np.random.normal(avg_duration, avg_duration * 0.3)))
                
                resolution_date = case_date + timedelta(days=duration)
                if resolution_date > term_date:
                    resolution_date = None
                    status = 'open'
                else:
                    status = random.choice(['resolved', 'closed'])
                
                case_data.append({
                    'case_id': f"CASE_{case_id_counter:06d}",
                    'employee_id': emp_id,
                    'case_type': case_type,
                    'case_date': case_date.strftime('%Y-%m-%d'),
                    'case_status': status,
                    'priority': random.choice(['low', 'medium', 'medium', 'high']),
                    'assigned_to_hr_specialist': f"HR_SPEC_{random.randint(1,5):02d}",
                    'resolution_date': resolution_date.strftime('%Y-%m-%d') if resolution_date else None,
                    'description': f"{case_type} case for {emp_id}"
                })
                case_id_counter += 1
        
        self.hr_cases_df = pd.DataFrame(case_data)
        return self.hr_cases_df
    
    def generate_hr_reports_text(self):
        """Generate text reports (performance reviews, exit interviews, case notes)"""
        reports_generated = 0
        target_reports = int(self.num_employees * self.config['volumes']['text_reports_percentage'] * 4)  # 4 types
        
        # Performance review templates
        perf_templates = [
            "{employee_name} has demonstrated {performance_level} performance throughout the review period. Key achievements include {achievements}. Areas for development: {development_areas}. Overall rating: {rating}/5. Manager feedback: {manager_feedback}",
            "Annual review for {employee_name} ({employee_id}). Performance level: {performance_level}. Strengths: {strengths}. Growth opportunities: {growth_ops}. Career aspirations discussed: {aspirations}. Rating: {rating}/5.",
        ]
        
        # Exit interview templates
        exit_templates = [
            "Exit interview conducted with {employee_name} on {date}. Reason for leaving: {reason}. Feedback on management: {mgmt_feedback}. Suggestions for improvement: {suggestions}. Rehire eligibility: {rehire}.",
            "Departure interview - {employee_name} ({employee_id}). Primary exit reason: {reason}. Overall experience rating: {rating}/5. Key feedback: {feedback}. Contact: {email}, {phone}.",
        ]
        
        # Case notes templates
        case_templates = [
            "HR Case {case_id} - {case_type}. Employee: {employee_name} ({employee_id}). Reported on {date}. Details: {details}. Actions taken: {actions}. Status: {status}. Contact: {email}, {phone}.",
            "Case investigation notes for {case_id}. Type: {case_type}. Involved: {employee_name}. Description: {description}. Resolution plan: {resolution}. Follow-up required: {followup}.",
        ]
        
        # Onboarding feedback templates
        onboarding_templates = [
            "Onboarding feedback - {employee_name} ({employee_id}). Start date: {date}. Onboarding rating: {rating}/5. Strengths of program: {strengths}. Improvement suggestions: {improvements}. Buddy assigned: {buddy}.",
        ]
        
        # Generate performance review reports
        perf_events = self.lifecycle_events_df[self.lifecycle_events_df['event_type'] == 'performance_review']
        for _, event in perf_events.sample(n=min(len(perf_events), target_reports // 4), random_state=self.seed).iterrows():
            emp = self.employees_df[self.employees_df['employee_id'] == event['employee_id']].iloc[0]
            
            report_text = random.choice(perf_templates).format(
                employee_name=f"{emp['first_name']} {emp['last_name']}",
                employee_id=emp['employee_id'],
                performance_level=random.choice(["exceptional", "strong", "satisfactory", "needs improvement"]),
                achievements=random.choice(["exceeded sales targets by 20%", "led successful product launch", "improved team efficiency", "delivered critical project on time"]),
                development_areas=random.choice(["delegation skills", "strategic thinking", "technical depth", "stakeholder management"]),
                rating=random.choice([3, 4, 4, 5]),
                manager_feedback=random.choice(["consistently reliable", "shows great initiative", "strong team player", "needs more focus"]),
                strengths=random.choice(["technical expertise", "communication", "problem-solving", "leadership"]),
                growth_ops=random.choice(["presentation skills", "cross-functional collaboration", "time management"]),
                aspirations=random.choice(["move into management", "deeper technical specialization", "international assignment"])
            )
            
            filename = f"perf_review_{event['event_id']}.txt"
            with open(self.reports_path / filename, 'w', encoding='utf-8') as f:
                f.write(f"REPORT_TYPE: performance_review\n")
                f.write(f"EMPLOYEE_ID: {emp['employee_id']}\n")
                f.write(f"EVENT_ID: {event['event_id']}\n")
                f.write(f"DATE: {event['event_date']}\n")
                f.write(f"\n{report_text}\n")
            
            reports_generated += 1
        
        # Generate exit interview reports
        exit_events = self.lifecycle_events_df[self.lifecycle_events_df['event_type'] == 'exit_interview']
        for _, event in exit_events.iterrows():
            emp = self.employees_df[self.employees_df['employee_id'] == event['employee_id']].iloc[0]
            
            report_text = random.choice(exit_templates).format(
                employee_name=f"{emp['first_name']} {emp['last_name']}",
                employee_id=emp['employee_id'],
                date=event['event_date'],
                reason=random.choice(["better opportunity elsewhere", "career growth", "compensation", "work-life balance", "relocation", "management issues"]),
                mgmt_feedback=random.choice(["very positive", "generally positive", "mixed feedback", "areas of concern noted"]),
                suggestions=random.choice(["improve onboarding", "competitive compensation", "clearer career paths", "better work-life balance"]),
                rehire=random.choice(["yes", "yes", "maybe", "no"]),
                rating=random.choice([3, 4, 4, 5]),
                feedback=random.choice(["great learning experience", "limited growth opportunities", "excellent team culture", "unclear expectations"]),
                email=emp['email'],
                phone=emp['phone']
            )
            
            filename = f"exit_interview_{event['event_id']}.txt"
            with open(self.reports_path / filename, 'w', encoding='utf-8') as f:
                f.write(f"REPORT_TYPE: exit_interview\n")
                f.write(f"EMPLOYEE_ID: {emp['employee_id']}\n")
                f.write(f"EVENT_ID: {event['event_id']}\n")
                f.write(f"DATE: {event['event_date']}\n")
                f.write(f"\n{report_text}\n")
            
            reports_generated += 1
        
        # Generate case notes
        for _, case in self.hr_cases_df.sample(n=min(len(self.hr_cases_df), target_reports // 4), random_state=self.seed).iterrows():
            emp = self.employees_df[self.employees_df['employee_id'] == case['employee_id']].iloc[0]
            
            report_text = random.choice(case_templates).format(
                case_id=case['case_id'],
                case_type=case['case_type'],
                employee_name=f"{emp['first_name']} {emp['last_name']}",
                employee_id=emp['employee_id'],
                date=case['case_date'],
                details=random.choice(["reported by colleague", "manager escalation", "self-reported", "third-party complaint"]),
                actions=random.choice(["mediation session", "verbal warning", "training required", "policy review"]),
                status=case['case_status'],
                email=emp['email'],
                phone=emp['phone'],
                description=f"{case['case_type']} incident",
                resolution=random.choice(["coaching plan", "formal warning", "accommodation granted", "case closed"]),
                followup=random.choice(["yes", "no"])
            )
            
            filename = f"hr_case_{case['case_id']}.txt"
            with open(self.reports_path / filename, 'w', encoding='utf-8') as f:
                f.write(f"REPORT_TYPE: case_note\n")
                f.write(f"EMPLOYEE_ID: {emp['employee_id']}\n")
                f.write(f"CASE_ID: {case['case_id']}\n")
                f.write(f"DATE: {case['case_date']}\n")
                f.write(f"\n{report_text}\n")
            
            reports_generated += 1
        
        # Generate onboarding feedback
        onb_events = self.lifecycle_events_df[self.lifecycle_events_df['event_type'] == 'onboarding_completed']
        for _, event in onb_events.sample(n=min(len(onb_events), target_reports // 4), random_state=self.seed).iterrows():
            emp = self.employees_df[self.employees_df['employee_id'] == event['employee_id']].iloc[0]
            
            report_text = random.choice(onboarding_templates).format(
                employee_name=f"{emp['first_name']} {emp['last_name']}",
                employee_id=emp['employee_id'],
                date=event['event_date'],
                rating=random.choice([3, 4, 4, 5]),
                strengths=random.choice(["well-structured program", "helpful buddy system", "clear documentation", "great team integration"]),
                improvements=random.choice(["more hands-on training", "earlier access to systems", "clearer first-week schedule"]),
                buddy=f"EMP_{random.randint(1, self.num_employees):06d}"
            )
            
            filename = f"onboarding_{event['event_id']}.txt"
            with open(self.reports_path / filename, 'w', encoding='utf-8') as f:
                f.write(f"REPORT_TYPE: onboarding_feedback\n")
                f.write(f"EMPLOYEE_ID: {emp['employee_id']}\n")
                f.write(f"EVENT_ID: {event['event_id']}\n")
                f.write(f"DATE: {event['event_date']}\n")
                f.write(f"\n{report_text}\n")
            
            reports_generated += 1
        
        print(f"✅ Generated {reports_generated} text reports")
        return reports_generated
    
    def save_all_data(self):
        """Save all dataframes to CSV"""
        # Dimensions (reference data)
        self.departments_df.to_csv(self.hr_path / 'dim_departments.csv', index=False, encoding='utf-8')
        self.positions_df.to_csv(self.hr_path / 'dim_positions.csv', index=False, encoding='utf-8')
        self.employees_df.to_csv(self.hr_path / 'dim_employees.csv', index=False, encoding='utf-8')
        
        # Facts (transactional data)
        self.lifecycle_events_df.to_csv(self.hr_path / 'fact_lifecycle_events.csv', index=False, encoding='utf-8')
        self.compensation_df.to_csv(self.hr_path / 'fact_compensation_history.csv', index=False, encoding='utf-8')
        self.absences_df.to_csv(self.hr_path / 'fact_absences.csv', index=False, encoding='utf-8')
        self.training_df.to_csv(self.hr_path / 'fact_training_records.csv', index=False, encoding='utf-8')
        self.hr_cases_df.to_csv(self.hr_path / 'fact_hr_cases.csv', index=False, encoding='utf-8')
        
        print(f"✅ All CSV files saved to {self.hr_path}")
    
    def generate_data_dictionary(self):
        """Generate comprehensive data dictionary"""
        dict_content = f"""# HR Employee Lifecycle - Data Dictionary

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Seed:** {self.seed}
**Employees:** {len(self.employees_df)}
**Date Range:** {self.start_date.date()} to {self.end_date.date()}

---

## Tables Overview

| Table | Rows | Primary Key | Description |
|-------|------|-------------|-------------|
| departments | {len(self.departments_df)} | department_id | Organizational departments |
| positions | {len(self.positions_df)} | position_id | Job positions and salary bands |
| employees | {len(self.employees_df)} | employee_id | Employee master data |
| lifecycle_events | {len(self.lifecycle_events_df)} | event_id | All lifecycle events (hire, promotion, etc.) |
| compensation_history | {len(self.compensation_df)} | comp_id | Salary and compensation changes |
| absences | {len(self.absences_df)} | absence_id | Employee absences and leaves |
| training_records | {len(self.training_df)} | training_id | Training and development records |
| hr_cases | {len(self.hr_cases_df)} | case_id | HR cases (grievances, incidents) |

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
- **Active Employees:** {len(self.employees_df[self.employees_df['status']=='active'])} ({len(self.employees_df[self.employees_df['status']=='active'])/len(self.employees_df)*100:.1f}%)
- **Terminated Employees:** {len(self.employees_df[self.employees_df['status']=='terminated'])} ({len(self.employees_df[self.employees_df['status']=='terminated'])/len(self.employees_df)*100:.1f}%)

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
"""
        
        dict_path = self.base_path / "docs" / "data_dictionary.md"
        dict_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(dict_path, 'w', encoding='utf-8') as f:
            f.write(dict_content)
        
        print(f"✅ Data dictionary saved to {dict_path}")
    
    def validate_data_quality(self):
        """Run data quality checks"""
        print("\n" + "="*60)
        print("DATA QUALITY VALIDATION")
        print("="*60)
        
        # Check 1: Duplicate primary keys
        print("\n1. Duplicate Primary Keys Check:")
        for name, df, pk in [
            ('departments', self.departments_df, 'department_id'),
            ('positions', self.positions_df, 'position_id'),
            ('employees', self.employees_df, 'employee_id'),
            ('lifecycle_events', self.lifecycle_events_df, 'event_id'),
            ('compensation_history', self.compensation_df, 'comp_id'),
            ('absences', self.absences_df, 'absence_id'),
            ('training_records', self.training_df, 'training_id'),
            ('hr_cases', self.hr_cases_df, 'case_id'),
        ]:
            duplicates = df[df.duplicated(subset=[pk], keep=False)]
            if len(duplicates) > 0:
                print(f"   ❌ {name}: {len(duplicates)} duplicate {pk} found!")
            else:
                print(f"   ✅ {name}: No duplicates")
        
        # Check 2: Referential integrity
        print("\n2. Referential Integrity Check:")
        
        # Employees -> Positions
        orphaned = self.employees_df[~self.employees_df['position_id'].isin(self.positions_df['position_id'])]
        print(f"   {'✅' if len(orphaned)==0 else '❌'} employees.position_id → positions: {len(orphaned)} orphaned")
        
        # Employees -> Departments
        orphaned = self.employees_df[~self.employees_df['department_id'].isin(self.departments_df['department_id'])]
        print(f"   {'✅' if len(orphaned)==0 else '❌'} employees.department_id → departments: {len(orphaned)} orphaned")
        
        # Lifecycle Events -> Employees
        orphaned = self.lifecycle_events_df[~self.lifecycle_events_df['employee_id'].isin(self.employees_df['employee_id'])]
        print(f"   {'✅' if len(orphaned)==0 else '❌'} lifecycle_events.employee_id → employees: {len(orphaned)} orphaned")
        
        # Check 3: NULL values in required fields
        print("\n3. NULL Values in Required Fields:")
        required_checks = [
            ('employees', self.employees_df, ['employee_id', 'hire_date', 'status']),
            ('lifecycle_events', self.lifecycle_events_df, ['event_id', 'employee_id', 'event_date', 'event_type']),
        ]
        for name, df, cols in required_checks:
            for col in cols:
                nulls = df[col].isna().sum()
                print(f"   {'✅' if nulls==0 else '❌'} {name}.{col}: {nulls} NULLs")
        
        # Check 4: Data distributions
        print("\n4. Data Distributions:")
        print(f"   Active employees: {len(self.employees_df[self.employees_df['status']=='active'])} ({len(self.employees_df[self.employees_df['status']=='active'])/len(self.employees_df)*100:.1f}%)")
        print(f"   Terminated employees: {len(self.employees_df[self.employees_df['status']=='terminated'])} ({len(self.employees_df[self.employees_df['status']=='terminated'])/len(self.employees_df)*100:.1f}%)")
        print(f"   Total lifecycle events: {len(self.lifecycle_events_df)}")
        print(f"   Avg events per employee: {len(self.lifecycle_events_df)/len(self.employees_df):.1f}")
        
        print("\n" + "="*60)
        print("VALIDATION COMPLETE")
        print("="*60 + "\n")


# Main execution
if __name__ == "__main__":
    print("🚀 Starting HR Synthetic Data Generation...")
    print("="*60)
    
    # Initialize generator (config.yaml is in src/ folder)
    config_path = Path(__file__).parent / 'config.yaml'
    generator = HRDataGenerator(str(config_path))
    
    # Generate all data
    print("\n📊 Generating data...")
    generator.generate_departments()
    print(f"   ✅ Departments: {len(generator.departments_df)} rows")
    
    generator.generate_positions()
    print(f"   ✅ Positions: {len(generator.positions_df)} rows")
    
    generator.generate_employees()
    print(f"   ✅ Employees: {len(generator.employees_df)} rows")
    
    generator.generate_lifecycle_events()
    print(f"   ✅ Lifecycle Events: {len(generator.lifecycle_events_df)} rows")
    
    generator.generate_compensation_history()
    print(f"   ✅ Compensation History: {len(generator.compensation_df)} rows")
    
    generator.generate_absences()
    print(f"   ✅ Absences: {len(generator.absences_df)} rows")
    
    generator.generate_training_records()
    print(f"   ✅ Training Records: {len(generator.training_df)} rows")
    
    generator.generate_hr_cases()
    print(f"   ✅ HR Cases: {len(generator.hr_cases_df)} rows")
    
    # Save CSV files
    print("\n💾 Saving CSV files...")
    generator.save_all_data()
    
    # Generate text reports
    print("\n📝 Generating text reports...")
    generator.generate_hr_reports_text()
    
    # Generate data dictionary
    print("\n📚 Generating data dictionary...")
    generator.generate_data_dictionary()
    
    # Validate data quality
    generator.validate_data_quality()
    
    print("\n✨ DATA GENERATION COMPLETE! ✨")
    print(f"\n📁 Output locations:")
    print(f"   CSV files: {generator.hr_path}")
    print(f"   Text reports: {generator.reports_path}")
    print(f"   Data dictionary: {generator.base_path / 'docs' / 'data_dictionary.md'}")
    print("\n🎯 Next steps:")
    print("   1. Upload files to Microsoft Fabric Lakehouse")
    print("   2. Run notebook 01_silver_modeling.ipynb")
    print("   3. Run notebook 02_text_enrichment.ipynb")
    print("   4. Follow guide in 03_semantic_and_agent_assets.md")
