# GitHub Copilot Instructions - HR Employee Lifecycle

## 📋 Contexte du Projet

Ce repository contient une **démo Microsoft Fabric** pour illustrer :
- OneLake + Shortcuts
- AI Shortcut Transformations (rapports RH texte → tables structurées + PII redaction)
- Fabric Data Agent (questions RH en langage naturel)
- Employee Lifecycle Analytics (recrutement, mobilité, performance, départs)

**Langue principale** : Français (code en anglais, docs en français)

---

## 🏗️ Structure du Repo

```
Scenario 10 - HR/
├── data/
│   └── raw/
│       ├── hr/                  # 8 CSV (employees, departments, events...)
│       └── reports_txt/         # ~200 fichiers .txt (comptes rendus RH)
├── notebooks/
│   ├── 00_generate_synthetic_hr_data.ipynb
│   ├── 01_silver_modeling.ipynb
│   ├── 02_text_enrichment.ipynb
│   └── 03_semantic_and_agent_assets.md
├── agent/
│   ├── agent_instructions.md
│   └── example_queries.json
├── docs/
│   ├── schema.md
│   ├── demo_story.md
│   ├── data_dictionary.md
│   └── fabric_setup.md
├── config.yaml
├── requirements.txt
├── README.md
└── AGENTS.md (ce fichier)
```

---

## 🎯 Conventions de Code

### Noms de Variables et Colonnes

- **Colonnes de tables** : `snake_case` (ex: `employee_id`, `event_type`)
- **Variables Python** : `snake_case` (ex: `employees_df`, `report_metadata`)
- **Constantes** : `UPPER_SNAKE_CASE` (ex: `CONFIG_FILE`, `SEED`)
- **Noms de classes** : `PascalCase` (ex: `HRDataGenerator`)

### Identifiants Métier

Format standardisé :
- Employees : `EMP_XXXXXX` (6 chiffres)
- Departments : `DEPT_XXX` (3 chiffres)
- Positions : `POS_XXX` (3 chiffres)
- Events : `EVT_XXXXXXXX` (8 chiffres)
- Cases : `CASE_XXXXXX` (6 chiffres)
- Reports : `RPT_XXXXXXXX` (8 chiffres)
- Training : `TRN_XXXXXXX` (7 chiffres)

### Dates et Formats

- **Dates** : ISO 8601 (`YYYY-MM-DD` ou `YYYY-MM-DD HH:MM:SS`)
- **Encoding** : UTF-8 (tous les fichiers)
- **CSV separator** : virgule (`,`)
- **Decimal separator** : point (`.`)

---

## 🔧 Commandes Fréquentes

### Génération de Données

```powershell
# Exécuter dans Fabric Notebook ou localement
# Ouvrir 00_generate_synthetic_hr_data.ipynb et exécuter toutes les cellules
```

### Vérifications

```powershell
# Vérifier le nombre de lignes générées
Get-ChildItem data\raw\hr\*.csv | ForEach-Object { 
    Write-Host "$($_.Name): $((Get-Content $_.FullName | Measure-Object -Line).Lines - 1) lignes"
}

# Compter les rapports texte
(Get-ChildItem data\raw\reports_txt\*.txt).Count

# Vérifier l'encodage UTF-8
Get-Content data\raw\hr\employees.csv -Encoding UTF8 | Select-Object -First 5
```

---

## 📝 Guidelines de Modification

### Ajouter une Nouvelle Colonne à une Table

1. Modifier la fonction `generate_XXX()` dans le notebook de génération
2. Mettre à jour `docs/schema.md` (description de la colonne)
3. Régénérer les données
4. Mettre à jour le Semantic Model dans Fabric (si déployé)

**Exemple** : Ajouter `remote_work_eligible` (boolean) dans `employees`

```python
# Dans generate_employees()
employee = {
    'employee_id': f'EMP_{i+1:06d}',
    # ... autres colonnes
    'remote_work_eligible': random.random() < 0.65,  # 65% éligibles
    'hire_date': ...
}
```

### Ajouter un Nouveau Type d'Événement

1. Éditer `config.yaml` → `business_params.lifecycle_events`
2. Ajouter l'événement avec weight et avg_per_employee
3. Optionnel : ajouter template de rapport dans `_get_report_templates()`
4. Relancer la génération

**Exemple** :

```yaml
lifecycle_events:
  - event_type: "sabbatical_leave"
    weight: 2
    avg_per_employee: 0.05
```

### Modifier les Templates de Rapports

Les templates sont dans `_get_report_templates()` du notebook de génération.

**Structure** :
- Par `report_type` (performance_review, exit_interview, disciplinary_note...)
- Inclusion de PII fictives (emails, téléphones, noms) pour démo redaction

Ajouter un nouveau template pour un type de rapport spécifique.

---

## 🧪 Tests et Validation

### Vérifier la Cohérence Référentielle

```python
# Après génération, lancer ces checks

import pandas as pd

employees_df = pd.read_csv('data/raw/hr/employees.csv')
events_df = pd.read_csv('data/raw/hr/lifecycle_events.csv')
cases_df = pd.read_csv('data/raw/hr/hr_cases.csv')

# Tous les employee_id dans events existent dans employees ?
assert events_df['employee_id'].isin(employees_df['employee_id']).all()

# Tous les employee_id dans cases existent dans employees ?
assert cases_df['employee_id'].isin(employees_df['employee_id']).all()

# Tous les manager_id existent (ou sont NULL)
managers = employees_df['manager_id'].dropna()
assert managers.isin(employees_df['employee_id']).all()

print("✅ Cohérence référentielle OK")
```

### Vérifier les Distributions

```python
# Distribution des statuts
print(employees_df['status'].value_counts(normalize=True))
# Attendu : active ~88%, terminated ~12%

# Distribution des événements
print(events_df['event_type'].value_counts(normalize=True))
# Attendu : performance_review ~30%, hire ~10%, etc.

# Tenure moyen
tenure_days = (pd.to_datetime('2025-12-31') - pd.to_datetime(employees_df['hire_date'])).dt.days
print(f"Tenure moyen: {tenure_days.mean() / 365:.1f} ans")
# Attendu : ~3-5 ans
```

---

## 🚨 Erreurs Fréquentes et Solutions

### Erreur : `UnicodeDecodeError` lors de la lecture des CSV

**Cause** : Encodage incorrect (BOM ou non UTF-8)

**Solution** :
```python
# Forcer UTF-8 sans BOM
df.to_csv(filepath, index=False, encoding='utf-8')
```

### Erreur : Les dates sont en STRING dans Fabric

**Cause** : Inférence de schéma incorrecte

**Solution** : Caster manuellement
```python
from pyspark.sql.functions import to_timestamp
df = df.withColumn("hire_date", to_timestamp("hire_date", "yyyy-MM-dd"))
```

### Erreur : Rapports texte vides ou mal formatés

**Cause** : Problème dans génération de templates

**Solution** : Vérifier que :
- Les templates retournent bien des strings
- L'encodage UTF-8 est préservé
- Les headers (EMPLOYEE_ID, DATE, REPORT_TYPE) sont présents

### Erreur : Relations cassées dans Semantic Model

**Cause** : FK orphelines ou colonnes mal nommées

**Solution** :
- Vérifier que tous les employee_id dans tables fact existent dans dim_employee
- Vérifier que tous les department_id existent dans dim_department
- Revalider les noms de colonnes (snake_case strict)

---

## 📚 Documentation à Maintenir

### Après Modification des Notebooks

1. Mettre à jour `docs/schema.md` si colonnes changées
2. Mettre à jour `README.md` si flux changé
3. Mettre à jour `agent/example_queries.json` si nouvelles métriques

### Après Modification de `config.yaml`

1. Documenter les nouveaux paramètres dans `README.md`
2. Mettre à jour les valeurs par défaut dans `docs/fabric_setup.md`

---

## 🎨 Suggestions d'Extension

### Idées pour Améliorer la Démo

1. **Ajouter prédiction attrition** : Score ML basé sur tenure, performance, absences
2. **Sentiment analysis** : Analyser sentiment dans rapports de sortie
3. **Diversity metrics** : Ajouter dimensions démographiques (avec précautions RGPD)
4. **Succession planning** : Table de successeurs potentiels par poste clé
5. **Skills inventory** : Table de compétences par employé

### Nouvelles Tables Possibles

```python
# Table : skills_inventory
{
    'employee_id': 'EMP_XXXXXX',
    'skill_category': 'Technical|Leadership|Language',
    'skill_name': str,
    'proficiency_level': 'Beginner|Intermediate|Advanced|Expert',
    'certified': bool,
    'last_assessed': datetime
}

# Table : succession_plan
{
    'position_id': 'POS_XXX',
    'successor_employee_id': 'EMP_XXXXXX',
    'readiness': 'Ready Now|1-2 Years|2-3 Years',
    'development_plan': str
}

# Table : employee_engagement_survey
{
    'survey_id': 'SURV_XXXXXX',
    'employee_id': 'EMP_XXXXXX',
    'survey_date': datetime,
    'engagement_score': int,  # 0-100
    'recommend_score': int  # eNPS
}
```

---

## 🔐 Sécurité et Conformité

### PII (Personally Identifiable Information)

**Toutes les PII dans ce repo sont FICTIVES** :
- Emails : générés par Faker (`@example.com`)
- Téléphones : générés par Faker (formats européens fictifs)
- Noms : générés par Faker (noms européens aléatoires)
- Adresses : NON incluses (pas nécessaire pour la démo)

**Redaction dans les rapports texte** :
- Les PII détectées par AI Transformations sont marquées pour démo
- Pas de vraie PII à redacter (tout est synthétique)

### RGPD / GDPR

**Ce dataset ne contient AUCUNE donnée réelle**, donc :
- ✅ Pas de consentement requis (données synthétiques)
- ✅ Pas de droit à l'oubli (employés fictifs)
- ✅ Utilisable librement pour formation/démo

**⚠️ ATTENTION** : Ne jamais utiliser de vraies données RH dans ce repo.

**Best practices RGPD dans un vrai contexte** :
- Minimisation des données (collecter uniquement le nécessaire)
- Anonymisation/pseudonymisation
- Contrôle d'accès strict (RBAC)
- Audit trail des accès
- Retention policies

---

## 🤖 Utilisation de Copilot sur ce Repo

### Questions Fréquentes à Poser

**Génération de code** :
- "Ajoute une colonne `last_promotion_date` dans employees"
- "Crée une fonction pour calculer le temps moyen avant promotion"
- "Ajoute un template de rapport pour 'internal_move'"

**Modification de config** :
- "Change les volumes pour avoir 1000 employés et 5 ans d'historique"
- "Ajoute un nouveau type de cas RH 'return_to_work'"

**Debugging** :
- "Pourquoi certains employés n'ont pas de manager_id ?"
- "Comment corriger les FK orphelines dans lifecycle_events ?"

**Documentation** :
- "Génère un exemple de requête SQL pour calculer le taux d'attrition par département"
- "Ajoute un diagramme de flux du lifecycle employé dans demo_story.md"

**Métriques RH** :
- "Explique le calcul du Time to Fill et crée une mesure DAX"
- "Comment calculer le Promotion Rate ?"

### Prompts Efficaces

✅ **Bon prompt** :
> "Dans le notebook de génération, ajoute une colonne `performance_trend` (string: 'improving', 'stable', 'declining') dans employees basée sur les 2 dernières performance reviews."

❌ **Prompt vague** :
> "Ajoute une colonne performance"

### Contexte à Fournir

Lorsque vous posez une question à Copilot, mentionner :
- Le fichier/notebook concerné
- Le type de modification (ajout, suppression, refactoring)
- Les contraintes (format, distribution, cohérence, RGPD)

---

## 🧮 Métriques RH de Référence

### Headcount & Growth

**Formule** :
```
Headcount = COUNT(employees WHERE status = 'active')
Net Headcount Change = Hires - (Resignations + Terminations)
Growth Rate = Net Change / Starting Headcount
```

---

### Attrition Rate

**Formule** :
```
Attrition Rate = (Exits / Average Headcount) × 100%

Voluntary Attrition = (Resignations / Average Headcount) × 100%
Involuntary Attrition = (Terminations / Average Headcount) × 100%
```

**Objectifs** :
- Attrition total : <15% annuel
- Voluntary : <10%
- Regrettable attrition (high performers) : <5%

---

### Time in Role

**Formule** :
```
Time in Role = Current Date - Last Promotion/Move Date
Average Time in Role = AVG(Time in Role) by Position/Level
```

**Benchmarks** :
- Individual contributor : 2-3 ans
- Manager : 3-4 ans
- Executive : 4-6 ans

---

### Promotion Rate

**Formule** :
```
Promotion Rate = (Promotions / Eligible Population) × 100%
```

**Objectifs** :
- Junior to Mid : 15-20% eligible promoted annually
- Mid to Senior : 10-15%
- Senior to Lead : 5-10%

---

### Time to Fill

**Formule** :
```
Time to Fill = Hire Date - Requisition Open Date
Average Time to Fill = AVG(Time to Fill) by Position Level
```

**Benchmarks** :
- Junior roles : 30-45 jours
- Senior roles : 60-90 jours
- Executive : 90-120 jours

---

### Training Hours per Employee

**Formule** :
```
Training Hours per FTE = SUM(Training Hours) / Headcount
```

**Objectif** : ≥40 heures/an/employé

---

### Internal Mobility Rate

**Formule** :
```
Internal Mobility Rate = (Internal Moves + Promotions) / Headcount
```

**Objectif** : 10-15% annuel

---

## ✅ Checklist avant Commit

Avant de commit des modifications :

- [ ] Code formaté (PEP8 pour Python)
- [ ] Notebooks s'exécutent sans erreur
- [ ] Données générées testées (volumes corrects, FK cohérentes)
- [ ] `docs/schema.md` mis à jour si schéma changé
- [ ] `README.md` mis à jour si flux changé
- [ ] Pas de données réelles ajoutées (PII fictives uniquement)
- [ ] Encodage UTF-8 vérifié sur tous les fichiers
- [ ] Config YAML valide (pas d'erreur de syntaxe)
- [ ] Métriques RH cohérentes (attrition <100%, tenure >0, etc.)
- [ ] Agent instructions mises à jour si nouvelles tables

---

## 📞 Support

Pour questions techniques sur le code :
- Ouvrir une issue GitHub
- Utiliser Copilot Chat avec contexte du fichier

Pour questions sur Microsoft Fabric :
- Consulter `docs/fabric_setup.md`
- Voir la [documentation officielle](https://learn.microsoft.com/en-us/fabric/)

Pour questions sur les métriques RH :
- Consulter `agent/agent_instructions.md` (formules, benchmarks)

---

**Happy coding! 🚀**

*Ces instructions sont optimisées pour GitHub Copilot et Copilot Chat dans le contexte RH/People Analytics.*
