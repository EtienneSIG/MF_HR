# HR Employee Lifecycle Analytics - Microsoft Fabric Demo

## 🎯 Vue d'Ensemble

Cette démo illustre une solution complète d'analytique RH sur **Microsoft Fabric** avec :
- ✅ **OneLake + Shortcuts** : Ingestion de données RH brutes
- ✅ **Shortcut Transformations** : Matérialisation automatique en Delta tables (Bronze → Silver)
- ✅ **AI Transformations** : Redaction PII + Summarization des rapports RH
- ✅ **Star Schema** : Modèle dimensionnel pour analytics
- ✅ **Fabric Data Agent** : Conversations en langage naturel sur les données RH

---

## 📊 Cas d'Usage

Analyser le cycle de vie complet des employés :
- Recrutement et onboarding
- Mobilité interne et promotions
- Performance et formation
- Absences et congés
- Départs (démissions / licenciements)
- Cas RH (disciplinaires, conflits, réclamations)

**~500 employés** | **3 ans d'historique** | **200+ rapports RH textuels**

---

## 📁 Structure du Repo

```
Scenario 10 - HR/
├── notebooks/
│   ├── 00_generate_synthetic_hr_data.ipynb   # Génération données synthétiques
│   ├── 01_silver_modeling.ipynb              # Transformation Bronze → Silver
│   ├── 02_text_enrichment.ipynb              # AI PII redaction + summarization
│   └── 03_semantic_and_agent_assets.md       # Setup Fabric Data Agent
├── agent/
│   ├── agent_instructions.md                  # System prompt Data Agent
│   └── example_queries.json                   # 25+ exemples de questions
├── data/
│   └── raw/                                   # Données brutes générées
│       ├── hr/
│       │   ├── employees.csv
│       │   ├── departments.csv
│       │   ├── positions.csv
│       │   ├── lifecycle_events.csv
│       │   ├── compensation_history.csv
│       │   ├── absences.csv
│       │   ├── training_records.csv
│       │   └── hr_cases.csv
│       └── reports_txt/                       # ~200 rapports .txt
├── docs/
│   ├── schema.md                              # Dictionnaire de données
│   ├── demo_story.md                          # Scénario narratif
│   └── data_dictionary.md                     # Documentation générée
├── config.yaml
├── requirements.txt
├── AGENTS.md
└── README.md (ce fichier)
```

---

## 🚀 Démarrage Rapide

### 1️⃣ Générer les Données Synthétiques

```python
# Ouvrir le notebook notebooks/00_generate_synthetic_hr_data.ipynb
# Exécuter toutes les cellules (Ctrl+Shift+Enter)
```

**Output** :
- `data/raw/hr/*.csv` : 8 tables CSV
- `data/raw/reports_txt/*.txt` : ~200 rapports textuels
- `docs/data_dictionary.md` : Schéma relationnel complet

**Durée** : ~2-3 minutes

---

### 2️⃣ Créer le Lakehouse dans Fabric

1. Ouvrir **Microsoft Fabric** (app.fabric.microsoft.com)
2. Créer un **Workspace** : `HR_Analytics_Demo`
3. Créer un **Lakehouse** : `hr_lakehouse`

---

### 3️⃣ Uploader les Fichiers Bruts

**Option A : Via UI**
1. Ouvrir `hr_lakehouse` → **Files**
2. Créer dossier `hr_raw`
3. Uploader tous les CSV de `data/raw/hr/`
4. Créer dossier `reports_txt`
5. Uploader tous les .txt de `data/raw/reports_txt/`

**Option B : Via Notebook**
```python
# Dans un notebook Fabric
import os
for csv_file in ["employees.csv", "departments.csv", ...]:
    df = pd.read_csv(f"path/to/local/{csv_file}")
    df.write.format("delta").mode("overwrite").save(f"Files/hr_raw/{csv_file}")
```

---

### 4️⃣ Configurer les Shortcut Transformations

1. **Bronze Layer** : Créer shortcuts vers `hr_raw/`
   - Clic droit sur dossier `hr_raw` → **New shortcut**
   - Sélectionner **OneLake**
   - Pointer vers `Files/hr_raw/`

2. **Shortcut Transformation (CSV → Delta)**
   - Clic droit sur shortcut → **New shortcut transformation**
   - Type : **Auto-sync to Delta**
   - Output : `Tables/bronze_employees` (répéter pour chaque CSV)

3. **Attendre la synchronisation** (1-2 min)

---

### 5️⃣ Exécuter les Notebooks de Transformation

#### **Notebook 01 : Silver Modeling**

```python
# notebooks/01_silver_modeling.ipynb
# - Lit les tables bronze_*
# - Nettoyage (dates, enums, nulls)
# - Crée dim_employee, dim_department, dim_position, dim_date
# - Crée fact_lifecycle_event, fact_compensation, fact_absence, fact_training, fact_hr_case
```

**Output** : Tables Silver dans `Tables/silver_*` et dimensions/facts dans `Tables/gold_*`

---

#### **Notebook 02 : Text Enrichment (AI)**

```python
# notebooks/02_text_enrichment.ipynb
# - Lit reports_txt/*.txt
# - PII Detection + Redaction (emails, téléphones, noms)
# - Summarization avec Fabric AI Functions
# - Topic Extraction
# - Output : fact_hr_report Delta table
```

**Output** : `Tables/gold_fact_hr_report`

---

### 6️⃣ Créer le Data Agent

1. **Créer un Semantic Model (optionnel)**
   - Power BI Desktop : Importer tables Gold
   - Définir relations (employee_key, date_key)
   - Créer mesures DAX (cf. `docs/dax_measures.md`)
   - Publier dans Fabric Workspace

2. **Créer le Data Agent**
   - Workspace → **+ New** → **Data Agent**
   - Nom : `HR_Lifecycle_Agent`
   - Source : Sélectionner Semantic Model OU Direct Lake (Lakehouse)
   - **System Instructions** : Copier/coller `agent/agent_instructions.md`
   - **Example Queries** : Importer `agent/example_queries.json`

3. **Tester le Data Agent**
   - Poser des questions (cf. section "10 Questions WOW")

---

## 💬 10 Questions "WOW" pour le Data Agent

### 1. **Headcount & Attrition**
> "Quel est notre headcount actuel et comment a-t-il évolué sur les 3 dernières années ?"

### 2. **Taux d'Attrition**
> "Quel est notre taux d'attrition annuel ? Quel département a le plus fort turnover ?"

### 3. **Promotions**
> "Combien d'employés ont été promus en 2025 ? Quel est le temps moyen avant promotion ?"

### 4. **Mobilité Interne**
> "Montre-moi les transferts inter-départements des 6 derniers mois."

### 5. **Performance Reviews**
> "Résume les thèmes principaux des performance reviews de Q4 2025."  
> *(AI summarization des rapports textuels)*

### 6. **Formation**
> "Quel type de formation est le plus suivi par les ingénieurs ?"

### 7. **Absences**
> "Quelle est la moyenne de jours d'absence par employé par an ?"

### 8. **Cas RH**
> "Combien de cas RH ouverts actuellement ? Quel est le type le plus fréquent ?"

### 9. **Exit Interviews**
> "Quelles sont les raisons principales de départ mentionnées dans les exit interviews ?"  
> *(AI topic extraction sur les rapports de sortie)*

### 10. **KPIs Exécutifs**
> "Affiche le dashboard des 5 KPIs RH clés : headcount, attrition, temps de recrutement, formation, satisfaction."

---

## 📖 Scénario de Démo (10-15 minutes)

### **Slide 1 : Contexte (1 min)**
> "Vous êtes DRH d'une scale-up tech de 500 employés. Vous devez piloter le cycle de vie complet : recrutement, mobilité, performance, départs."

### **Slide 2 : Données Brutes dans OneLake (2 min)**
- Montrer `Files/hr_raw/` : 8 CSV + rapports .txt
- Souligner : **Aucune donnée réelle** (tout synthétique, RGPD-safe)
- Montrer un fichier .txt : contient PII fictives (emails, téléphones)

### **Slide 3 : Shortcut Transformations (2 min)**
- Montrer shortcuts OneLake
- Montrer **Auto-sync to Delta** : CSV → Bronze tables
- Bénéfice : **Zéro ETL**, synchronisation automatique

### **Slide 4 : AI Redaction + Summarization (3 min)**
- Montrer `fact_hr_report` avec colonnes :
  - `report_text_redacted` : PII remplacées par `[EMAIL]`, `[PHONE]`, etc.
  - `report_summary` : Résumé 2-3 phrases généré par AI
  - `topics` : Thèmes extraits (performance, conflict, resignation_reason)
- Bénéfice : **Conformité RGPD** + **Insights en langage naturel**

### **Slide 5 : Star Schema & Semantic Model (2 min)**
- Montrer architecture :
  - **Dimensions** : dim_employee (SCD Type 2), dim_department, dim_position, dim_date
  - **Facts** : fact_lifecycle_event, fact_compensation, fact_absence, fact_training, fact_hr_case, fact_hr_report
- Relations : employee_key, date_key
- Métriques DAX pré-calculées

### **Slide 6 : Data Agent en Action (5 min)**
- Poser les 10 questions WOW (ci-dessus)
- Montrer :
  - Réponses en français
  - Visualisations automatiques (tableaux, graphiques)
  - Drill-down : cliquer sur un département → détails
  - Explications : "Comment as-tu calculé ce KPI ?"

### **Slide 7 : Conclusion (1 min)**
> "Avec Fabric : OneLake + AI + Data Agent, vous passez de **silos RH** à une **vue 360° pilotable en conversation**."

---

## 🧮 Métriques RH Calculées

### **Headcount**
```
Headcount Actuel = COUNT(employees WHERE status = 'active')
```

### **Attrition Rate**
```
Attrition Annuel = (Exits / AVG(Headcount)) × 100%
```

### **Time to Fill**
```
Time to Fill = Hire Date - Requisition Date (moy. 45-60 jours)
```

### **Promotion Rate**
```
Promotion Rate = (Promotions / Headcount) × 100%
```

### **Training Hours per FTE**
```
Training Hours per FTE = SUM(training_hours) / Headcount
```

### **Internal Mobility Rate**
```
Internal Mobility = (Transfers + Promotions) / Headcount
```

### **Case Resolution Time**
```
Avg Case Resolution Time = AVG(resolution_date - case_date)
```

---

## 🔐 Conformité RGPD / Données Synthétiques

**⚠️ ATTENTION** : Ce repo contient **UNIQUEMENT des données fictives**.

- **Noms** : Générés par Faker (noms européens aléatoires)
- **Emails** : Format `prenom.nom@example.com` (domaine fictif)
- **Téléphones** : Format européen fictif (ex: +33 6 XX XX XX XX)
- **Aucune vraie donnée personnelle**

**Démo PII Redaction** :
- Les rapports textuels incluent des PII fictives
- Le notebook 02 détecte et redacte ces PII
- Seule la version redactée est exposée dans le Data Agent

**En production réelle** :
- Appliquer RBAC (Row-Level Security) par manager_id
- Anonymiser/pseudonymiser selon RGPD
- Audit trail des accès
- Retention policies

---

## 📚 Documentation Complémentaire

- [`docs/schema.md`](docs/schema.md) : Schéma complet des 16 tables
- [`docs/demo_story.md`](docs/demo_story.md) : Scénario narratif "Du Recrutement au Départ"
- [`agent/agent_instructions.md`](agent/agent_instructions.md) : System prompt Data Agent
- [`agent/example_queries.json`](agent/example_queries.json) : 25 questions exemple
- [`notebooks/03_semantic_and_agent_assets.md`](notebooks/03_semantic_and_agent_assets.md) : Setup détaillé Fabric

---

## 🛠️ Customisation

### Modifier les Volumes
Éditer `config.yaml` :
```yaml
volumes:
  employees: 1000  # Au lieu de 500
  lifecycle_events_per_employee_avg: 10  # Au lieu de 8
```
Relancer `00_generate_synthetic_hr_data.ipynb`

### Ajouter un Type d'Événement
Éditer `config.yaml` :
```yaml
lifecycle_events:
  - event_type: "sabbatical_leave"
    weight: 2
    avg_per_employee: 0.05
```

### Ajouter un Rapport Texte
Éditer le notebook 00, section "Generate HR Reports" :
```python
report_templates['sabbatical_request'] = {
    'opening': "Employee {employee_id} has requested a sabbatical...",
    ...
}
```

---

## 🏆 Bénéfices de la Solution

| Avant | Après (avec Fabric) |
|-------|---------------------|
| Données RH éparpillées (Excel, SIRH, emails) | **OneLake centralisé** |
| Rapports manuels (copier/coller) | **Auto-refresh Delta** |
| Aucune analyse des comptes rendus RH | **AI summarization + topic extraction** |
| Requêtes SQL complexes | **Conversations Data Agent** |
| PII exposées dans rapports | **Redaction automatique** |
| Délai 2-3 jours pour un KPI | **Réponse instantanée** |

---

## 📞 Support

Questions sur :
- **Code** : Voir `AGENTS.md` (conventions Copilot)
- **Fabric** : [Documentation officielle](https://learn.microsoft.com/en-us/fabric/)
- **Data Agent** : `agent/agent_instructions.md`

---

**Prêt à déployer ? Commencez par `notebooks/00_generate_synthetic_hr_data.ipynb` ! 🚀**
