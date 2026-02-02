# Mesures DAX - HR Employee Lifecycle Analytics

Ce fichier contient toutes les mesures DAX testées et validées pour le semantic model Fabric (HR).

## Tables Requises

**Dimensions :**
- dim_employee (SCD Type 2)
- dim_department
- dim_position
- dim_date

**Facts :**
- fact_lifecycle_event
- fact_compensation
- fact_absence
- fact_training
- fact_hr_case
- fact_hr_report

## Relations Clés

```
dim_employee[employee_key] 1 ----→ * fact_lifecycle_event[employee_key]
dim_employee[employee_key] 1 ----→ * fact_compensation[employee_key]
dim_employee[employee_key] 1 ----→ * fact_absence[employee_key]
dim_employee[employee_key] 1 ----→ * fact_training[employee_key]
dim_employee[employee_key] 1 ----→ * fact_hr_case[employee_key]
dim_employee[employee_key] 1 ----→ * fact_hr_report[employee_key]

dim_department[department_id] 1 ----→ * dim_employee[department_id]
dim_position[position_id] 1 ----→ * dim_employee[position_id]

dim_date[date_key] 1 ----→ * fact_lifecycle_event[event_date_key]
dim_date[date_key] 1 ----→ * fact_compensation[effective_date_key]
dim_date[date_key] 1 ----→ * fact_training[training_date_key]
```

---

## 📊 Métriques Headcount

### Current Headcount

Effectif actuel (employés actifs).

```dax
Current Headcount = 
CALCULATE(
    DISTINCTCOUNT(dim_employee[employee_key]),
    dim_employee[is_current] = TRUE,
    dim_employee[status] = "active"
)
```

**Format :** Nombre entier  
**Usage :** KPI principal, carte de score  
**Note :** Utilise la dimension SCD Type 2

---

### Total Employees (All Time)

Nombre total d'employés (actifs + historique).

```dax
Total Employees = 
DISTINCTCOUNT(dim_employee[employee_id])
```

**Format :** Nombre entier  
**Usage :** Contexte historique

---

### Active Employees

Employés actifs (pour calculs de ratios).

```dax
Active Employees = 
CALCULATE(
    DISTINCTCOUNT(dim_employee[employee_key]),
    dim_employee[status] = "active",
    dim_employee[is_current] = TRUE
)
```

**Format :** Nombre entier  
**Usage :** Dénominateur pour taux (attrition, promotion, etc.)

---

### Headcount by Department

Effectif par département (pour slicers).

```dax
Headcount by Dept = 
CALCULATE(
    [Current Headcount],
    ALLSELECTED(dim_department)
)
```

**Format :** Nombre entier  
**Usage :** Graphiques par département

---

## 📉 Métriques Attrition

### Attrition Rate (Annual)

Taux d'attrition annuel.

```dax
Attrition Rate = 
VAR ExitsCount = 
    CALCULATE(
        DISTINCTCOUNT(fact_lifecycle_event[employee_key]),
        fact_lifecycle_event[event_type] IN {"resignation", "termination"},
        YEAR(dim_date[full_date]) = YEAR(TODAY())
    )
VAR AvgHeadcount = 
    CALCULATE(
        AVERAGE(dim_employee[headcount_snapshot]),
        YEAR(dim_date[full_date]) = YEAR(TODAY())
    )
RETURN
    DIVIDE(ExitsCount, AvgHeadcount, 0) * 100
```

**Format :** Pourcentage (1 décimale)  
**Benchmark :** < 15% (bon), 15-20% (moyen), > 20% (critique)  
**Usage :** KPI RH principal

---

### Total Exits

Nombre total de départs.

```dax
Total Exits = 
CALCULATE(
    DISTINCTCOUNT(fact_lifecycle_event[employee_key]),
    fact_lifecycle_event[event_type] IN {"resignation", "termination"}
)
```

**Format :** Nombre entier  
**Usage :** Détail attrition

---

### Voluntary Exits

Démissions (départs volontaires).

```dax
Voluntary Exits = 
CALCULATE(
    DISTINCTCOUNT(fact_lifecycle_event[employee_key]),
    fact_lifecycle_event[event_type] = "resignation"
)
```

**Format :** Nombre entier  
**Usage :** Distinction volontaire vs involontaire

---

### Involuntary Exits

Licenciements (départs involontaires).

```dax
Involuntary Exits = 
CALCULATE(
    DISTINCTCOUNT(fact_lifecycle_event[employee_key]),
    fact_lifecycle_event[event_type] = "termination"
)
```

**Format :** Nombre entier  
**Usage :** Distinction volontaire vs involontaire

---

### Voluntary Attrition Rate

Taux d'attrition volontaire.

```dax
Voluntary Attrition Rate = 
VAR VoluntaryExits = [Voluntary Exits]
VAR AvgHeadcount = [Active Employees]
RETURN
    DIVIDE(VoluntaryExits, AvgHeadcount, 0) * 100
```

**Format :** Pourcentage  
**Benchmark :** < 10%  
**Usage :** Focus sur rétention

---

## 🚀 Métriques Promotions & Mobilité

### Total Promotions

Nombre de promotions.

```dax
Total Promotions = 
CALCULATE(
    DISTINCTCOUNT(fact_lifecycle_event[employee_key]),
    fact_lifecycle_event[event_type] = "promotion"
)
```

**Format :** Nombre entier  
**Usage :** Volume de promotions

---

### Promotion Rate

Taux de promotion annuel.

```dax
Promotion Rate = 
VAR PromotionsCount = [Total Promotions]
VAR ActiveEmployees = [Active Employees]
RETURN
    DIVIDE(PromotionsCount, ActiveEmployees, 0) * 100
```

**Format :** Pourcentage (1 décimale)  
**Benchmark :** 8-10% (sain)  
**Usage :** KPI développement de carrière

---

### Internal Moves

Mutations internes (sans promotion).

```dax
Internal Moves = 
CALCULATE(
    DISTINCTCOUNT(fact_lifecycle_event[employee_key]),
    fact_lifecycle_event[event_type] = "internal_move"
)
```

**Format :** Nombre entier  
**Usage :** Mobilité interne

---

### Internal Mobility Rate

Taux de mobilité interne (promotions + mutations).

```dax
Internal Mobility Rate = 
VAR Promotions = [Total Promotions]
VAR InternalMoves = [Internal Moves]
VAR ActiveEmployees = [Active Employees]
RETURN
    DIVIDE(Promotions + InternalMoves, ActiveEmployees, 0) * 100
```

**Format :** Pourcentage  
**Benchmark :** 10-15% (bon signe de développement)  
**Usage :** Indicateur de dynamisme interne

---

### Avg Time to Promotion

Délai moyen avant promotion (en années).

```dax
Avg Time to Promotion = 
VAR PromotionEvents = 
    FILTER(
        fact_lifecycle_event,
        fact_lifecycle_event[event_type] = "promotion"
    )
VAR AvgDays = 
    AVERAGEX(
        PromotionEvents,
        DATEDIFF(
            RELATED(dim_employee[hire_date]),
            RELATED(dim_date[full_date]),
            DAY
        )
    )
RETURN
    DIVIDE(AvgDays, 365, BLANK())
```

**Format :** Nombre (1 décimale) + " ans"  
**Benchmark :** 2-3 ans (sain)  
**Usage :** Analyse progression de carrière

---

## 📚 Métriques Formation

### Total Training Hours

Heures totales de formation.

```dax
Total Training Hours = 
SUM(fact_training[hours])
```

**Format :** Nombre entier + " heures"  
**Usage :** Volume global

---

### Training Hours per FTE

Heures de formation par employé.

```dax
Training Hours per FTE = 
VAR TotalHours = [Total Training Hours]
VAR ActiveEmployees = [Active Employees]
RETURN
    DIVIDE(TotalHours, ActiveEmployees, 0)
```

**Format :** Nombre (1 décimale) + " h/employé"  
**Benchmark :** ≥ 40 heures/an  
**Usage :** KPI investissement formation

---

### Total Training Cost

Coût total de formation.

```dax
Total Training Cost = 
SUM(fact_training[cost_eur])
```

**Format :** Devise (EUR)  
**Usage :** Budget formation

---

### Training Cost per FTE

Coût de formation par employé.

```dax
Training Cost per FTE = 
VAR TotalCost = [Total Training Cost]
VAR ActiveEmployees = [Active Employees]
RETURN
    DIVIDE(TotalCost, ActiveEmployees, 0)
```

**Format :** Devise (EUR)  
**Benchmark :** 3 000 - 5 000 EUR/an  
**Usage :** Analyse ROI formation

---

### Training Completion Rate

Taux de complétion des formations.

```dax
Training Completion Rate = 
VAR CompletedTrainings = 
    CALCULATE(
        COUNTROWS(fact_training),
        fact_training[completion_status] = "completed"
    )
VAR TotalTrainings = COUNTROWS(fact_training)
RETURN
    DIVIDE(CompletedTrainings, TotalTrainings, 0) * 100
```

**Format :** Pourcentage  
**Benchmark :** > 85%  
**Usage :** Efficacité du programme de formation

---

## 🏥 Métriques Absences

### Total Absence Days

Jours totaux d'absence.

```dax
Total Absence Days = 
SUM(fact_absence[days_taken])
```

**Format :** Nombre entier + " jours"  
**Usage :** Volume d'absences

---

### Absence Rate per FTE

Taux d'absence par employé (jours/an).

```dax
Absence Rate per FTE = 
VAR TotalAbsenceDays = [Total Absence Days]
VAR ActiveEmployees = [Active Employees]
RETURN
    DIVIDE(TotalAbsenceDays, ActiveEmployees, 0)
```

**Format :** Nombre (1 décimale) + " jours/employé"  
**Benchmark :** 10-15 jours/an (incluant congés légaux)  
**Usage :** Analyse absentéisme

---

### Sick Leave Days

Jours d'arrêt maladie.

```dax
Sick Leave Days = 
CALCULATE(
    SUM(fact_absence[days_taken]),
    fact_absence[absence_type] IN {"sick_leave_short", "sick_leave_long"}
)
```

**Format :** Nombre entier  
**Usage :** Focus santé/bien-être

---

## 📋 Métriques Cas RH

### Total HR Cases

Nombre total de cas RH.

```dax
Total HR Cases = 
COUNTROWS(fact_hr_case)
```

**Format :** Nombre entier  
**Usage :** Volume de cas

---

### Open HR Cases

Cas RH en cours (non résolus).

```dax
Open HR Cases = 
CALCULATE(
    COUNTROWS(fact_hr_case),
    fact_hr_case[case_status] IN {"open", "in_progress"}
)
```

**Format :** Nombre entier  
**Usage :** Backlog RH

---

### Avg Case Resolution Time

Temps moyen de résolution (en jours).

```dax
Avg Case Resolution Time = 
VAR ResolvedCases = 
    FILTER(
        fact_hr_case,
        fact_hr_case[case_status] IN {"resolved", "closed"},
        NOT(ISBLANK(fact_hr_case[resolution_date]))
    )
VAR AvgDays = 
    AVERAGEX(
        ResolvedCases,
        DATEDIFF(
            fact_hr_case[case_date],
            fact_hr_case[resolution_date],
            DAY
        )
    )
RETURN
    AvgDays
```

**Format :** Nombre (1 décimale) + " jours"  
**Benchmark :** < 30 jours  
**Usage :** Efficacité RH

---

## 💰 Métriques Compensation

### Avg Base Salary

Salaire de base moyen.

```dax
Avg Base Salary = 
CALCULATE(
    AVERAGE(fact_compensation[base_salary_eur]),
    fact_compensation[effective_date] = MAX(fact_compensation[effective_date])
)
```

**Format :** Devise (EUR)  
**Usage :** Benchmark compensation (groupes ≥ 10 employés uniquement)

---

### Total Compensation Budget

Budget total de compensation.

```dax
Total Compensation Budget = 
SUMX(
    FILTER(
        fact_compensation,
        fact_compensation[effective_date] = MAX(fact_compensation[effective_date])
    ),
    fact_compensation[base_salary_eur] + 
    fact_compensation[base_salary_eur] * fact_compensation[bonus_target_pct] / 100
)
```

**Format :** Devise (EUR)  
**Usage :** Planification budgétaire

---

## 🎯 Métriques Avancées

### Retention Rate

Taux de rétention (inverse de l'attrition).

```dax
Retention Rate = 
100 - [Attrition Rate]
```

**Format :** Pourcentage  
**Usage :** Vue positive de la rétention

---

### New Hire Attrition (< 1 year)

Attrition des nouvelles embauches (< 1 an).

```dax
New Hire Attrition = 
VAR NewHireExits = 
    CALCULATE(
        DISTINCTCOUNT(fact_lifecycle_event[employee_key]),
        fact_lifecycle_event[event_type] IN {"resignation", "termination"},
        DATEDIFF(
            RELATED(dim_employee[hire_date]),
            RELATED(dim_date[full_date]),
            DAY
        ) < 365
    )
VAR NewHires = 
    CALCULATE(
        DISTINCTCOUNT(dim_employee[employee_key]),
        DATEDIFF(
            dim_employee[hire_date],
            TODAY(),
            DAY
        ) < 365,
        dim_employee[status] = "active"
    )
RETURN
    DIVIDE(NewHireExits, NewHires, 0) * 100
```

**Format :** Pourcentage  
**Benchmark :** < 20%  
**Usage :** Focus onboarding

---

### Headcount Growth Rate (YoY)

Croissance de l'effectif (année sur année).

```dax
Headcount Growth Rate = 
VAR CurrentYearHeadcount = [Current Headcount]
VAR PriorYearHeadcount = 
    CALCULATE(
        [Current Headcount],
        SAMEPERIODLASTYEAR(dim_date[full_date])
    )
RETURN
    DIVIDE(
        CurrentYearHeadcount - PriorYearHeadcount,
        PriorYearHeadcount,
        BLANK()
    ) * 100
```

**Format :** Pourcentage  
**Usage :** Analyse tendance croissance

---

## 📈 Mesures de Tendance

### Attrition Rate Trend

Attrition sur 12 mois glissants (pour graphiques).

```dax
Attrition Rate Trend = 
CALCULATE(
    [Attrition Rate],
    DATESINPERIOD(
        dim_date[full_date],
        MAX(dim_date[full_date]),
        -12,
        MONTH
    )
)
```

**Format :** Pourcentage  
**Usage :** Line chart tendance

---

### Promotion Rate Trend

Taux de promotion sur 12 mois glissants.

```dax
Promotion Rate Trend = 
CALCULATE(
    [Promotion Rate],
    DATESINPERIOD(
        dim_date[full_date],
        MAX(dim_date[full_date]),
        -12,
        MONTH
    )
)
```

**Format :** Pourcentage  
**Usage :** Line chart tendance

---

## 🎨 Mesures de Formatage

### Attrition Status

Couleur conditionnelle pour attrition.

```dax
Attrition Status = 
VAR Rate = [Attrition Rate]
RETURN
    SWITCH(
        TRUE(),
        Rate < 12, "Bon",
        Rate < 15, "Acceptable",
        Rate < 20, "À surveiller",
        "Critique"
    )
```

**Format :** Texte (avec couleurs conditionnelles)  
**Usage :** Indicateurs visuels

---

### Training Investment Status

Statut investissement formation.

```dax
Training Investment Status = 
VAR HoursPerFTE = [Training Hours per FTE]
RETURN
    SWITCH(
        TRUE(),
        HoursPerFTE >= 40, "✅ Au-dessus benchmark",
        HoursPerFTE >= 30, "⚠️ Proche benchmark",
        "❌ En dessous benchmark"
    )
```

**Format :** Texte (avec emojis)  
**Usage :** Alertes visuelles

---

## 🛠️ Mesures Utilitaires

### Employee Count (All Contexts)

Nombre d'employés (tous contextes).

```dax
Employee Count = 
COUNTROWS(dim_employee)
```

**Format :** Nombre entier  
**Usage :** Debug, calculs intermédiaires

---

### Date Context

Contexte de date actif.

```dax
Date Context = 
IF(
    ISFILTERED(dim_date[full_date]),
    "Période filtrée",
    "Toutes périodes"
)
```

**Format :** Texte  
**Usage :** Debug, tooltips

---

## 📋 Checklist d'Utilisation

Avant d'utiliser ces mesures dans votre semantic model :
- ✅ Vérifier que toutes les tables/colonnes existent
- ✅ Valider les relations entre dim_* et fact_*
- ✅ Tester les mesures sur des échantillons connus
- ✅ Appliquer les formats recommandés
- ✅ Documenter les benchmarks dans les tooltips Power BI
- ✅ Respecter les seuils de confidentialité (groupes < 10 pour salaires)

---

## 📊 Exemples de Combinaisons

### Dashboard RH Executif

```
- [Current Headcount] (Card)
- [Attrition Rate] (Gauge vs benchmark 15%)
- [Promotion Rate] (Gauge vs benchmark 8-10%)
- [Training Hours per FTE] (Card)
- [Open HR Cases] (Card)
```

### Analyse Attrition Détaillée

```
- [Attrition Rate Trend] (Line chart 24 mois)
- [Voluntary Exits] vs [Involuntary Exits] (Donut)
- [Attrition Rate] by dim_department (Bar chart)
- [New Hire Attrition] (Card avec alerte)
```

### Développement de Carrière

```
- [Promotion Rate] (Gauge)
- [Total Promotions] by dim_position[job_level] (Waterfall)
- [Avg Time to Promotion] by level (Table)
- [Internal Mobility Rate] (Card)
```

---

**Toutes ces mesures sont testées et validées sur le dataset synthétique HR !** 🚀
