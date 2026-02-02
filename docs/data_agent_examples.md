# Exemples de Questions pour Fabric Data Agent

## 🎯 Objectif

Ce document fournit **20 exemples de questions** avec les **réponses attendues** pour tester et valider le Fabric Data Agent.

Chaque exemple inclut :
- La question posée
- La réponse attendue (format et contenu)
- Les tables utilisées
- Le type de visualisation suggéré

---

## 📊 Catégorie 1 : Exploration Simple (5 questions)

### 1. Quel est notre effectif actuel ?

**Réponse attendue** :
> **Effectif actuel (au 31 décembre 2025) :** 445 employés actifs
> 
> **Répartition par division :**
> - Technology : 180 employés (40%)
> - Sales & Marketing : 135 employés (30%)
> - Operations : 85 employés (19%)
> - Corporate Functions : 45 employés (11%)
> 
> *Source : table `dim_employee` (WHERE is_current = TRUE AND status = 'active')*

**Tables** : `dim_employee`  
**Visualisation** : Card/KPI + Donut chart  
**Complexité** : ⭐ (très simple)

---

### 2. Combien de départements avons-nous ?

**Réponse attendue** :
> **12 départements** répartis en 4 divisions :
> - Technology (4 depts) : Engineering, Data & AI, Product, IT Operations
> - Sales & Marketing (3 depts) : Sales, Marketing, Customer Success
> - Operations (3 depts) : Operations, Supply Chain, Facilities
> - Corporate Functions (2 depts) : Finance, HR
> 
> *Source : table `dim_department`*

**Tables** : `dim_department`  
**Visualisation** : Table ou Treemap  
**Complexité** : ⭐ (simple)

---

### 3. Combien d'événements de lifecycle avons-nous enregistrés en 2025 ?

**Réponse attendue** :
> **1 342 événements** enregistrés en 2025 :
> - Performance reviews : 385 (29%)
> - Embauches : 132 (10%)
> - Promotions : 45 (3%)
> - Départs (démissions + licenciements) : 55 (4%)
> - Autres (formations, congés, mutations...) : 725 (54%)
> 
> *Source : table `fact_lifecycle_event` (WHERE YEAR(event_date) = 2025)*

**Tables** : `fact_lifecycle_event`, `dim_date`  
**Visualisation** : Stacked bar chart  
**Complexité** : ⭐ (simple)

---

### 4. Quelle est la répartition hommes/femmes ? 

**Réponse attendue** :
> **ATTENTION : Données démographiques sensibles non disponibles**
> 
> Ce dataset ne contient pas de données de genre/diversité pour des raisons de conformité RGPD.
> 
> Les métriques disponibles sont :
> - Effectif par département
> - Effectif par niveau de poste
> - Effectif par type de contrat
> 
> *Note : Dataset synthétique à visée de démonstration technique uniquement*

**Tables** : N/A  
**Visualisation** : N/A  
**Complexité** : ⭐ (explication de limitation)

---

### 5. Quel est le nombre total d'heures de formation dispensées en 2025 ?

**Réponse attendue** :
> **18 750 heures** de formation dispensées en 2025
> 
> **Détails :**
> - 2 438 formations complétées
> - 445 employés actifs
> - **42 heures par employé** (moyenne)
> 
> **Benchmark :** Standard industrie = 40h/employé → Nous sommes **au-dessus** ✅
> 
> *Source : table `fact_training` (WHERE YEAR(training_date) = 2025)*

**Tables** : `fact_training`, `dim_employee`  
**Visualisation** : Card/KPI  
**Complexité** : ⭐ (simple)

---

## 📈 Catégorie 2 : Agrégations et Calculs (5 questions)

### 6. Quel est notre taux d'attrition en 2025 ?

**Réponse attendue** :
> **Taux d'attrition annuel (2025) :** 12.3%
> 
> **Détails :**
> - Total départs : 55 employés
>   - Démissions (voluntary) : 38 (69%)
>   - Licenciements (involuntary) : 17 (31%)
> - Headcount moyen : 447 employés
> 
> **Tendance :**
> - 2023 : 11.5%
> - 2024 : 11.8%
> - 2025 : 12.3% ⬆️ (+0.5pp)
> 
> **Benchmark :** < 15% (bon) → Nous sommes **dans la norme** ✅
> 
> *Source : tables `fact_lifecycle_event`, `dim_employee`*

**Tables** : `fact_lifecycle_event`, `dim_employee`, `dim_date`  
**Visualisation** : Line chart (tendance) + Gauge (vs benchmark)  
**Complexité** : ⭐⭐ (calcul métrique)

---

### 7. Quel département a le taux d'attrition le plus élevé ?

**Réponse attendue** :
> **Département avec attrition la plus élevée (2025) : Sales (15.1%)**
> 
> **Top 5 départements :**
> 1. Sales : 15.1% (16 départs / 106 headcount moyen)
> 2. Customer Success : 14.2% (8 départs / 56 headcount moyen)
> 3. Engineering : 11.2% (17 départs / 152 headcount moyen)
> 4. Marketing : 10.8% (6 départs / 55 headcount moyen)
> 5. Product : 9.5% (4 départs / 42 headcount moyen)
> 
> **Insight :** Sales et Customer Success ont une attrition supérieure à la moyenne entreprise (12.3%). Principales raisons identifiées (via exit interviews IA) :
> - Compensation non compétitive (35%)
> - Quotas/pression de performance (28%)
> - Opportunités de carrière ailleurs (22%)
> 
> *Source : tables `fact_lifecycle_event`, `dim_employee`, `dim_department`, `fact_hr_report`*

**Tables** : `fact_lifecycle_event`, `dim_employee`, `dim_department`, `fact_hr_report`  
**Visualisation** : Bar chart (horizontal)  
**Complexité** : ⭐⭐⭐ (multi-table join + calcul par groupe)

---

### 8. Combien de promotions avons-nous eu en 2025 ?

**Réponse attendue** :
> **45 promotions** en 2025
> 
> **Taux de promotion :** 10.1% (45 promus / 445 employés actifs)
> 
> **Répartition par niveau :**
> - Junior → Intermediate : 18 promotions (40%)
> - Intermediate → Senior : 15 promotions (33%)
> - Senior → Lead : 8 promotions (18%)
> - Lead → Principal/Manager : 4 promotions (9%)
> 
> **Délai moyen avant promotion :**
> - Junior → Intermediate : 2.1 ans
> - Intermediate → Senior : 2.8 ans
> - Senior → Lead : 3.5 ans
> 
> **Benchmark :** Taux de promotion 8-10% (sain) → Nous sommes **légèrement au-dessus** ✅
> 
> *Source : tables `fact_lifecycle_event`, `dim_position`, `dim_employee`*

**Tables** : `fact_lifecycle_event`, `dim_position`, `dim_employee`  
**Visualisation** : Waterfall chart (flux par niveau)  
**Complexité** : ⭐⭐⭐ (calculs temporels + agrégations)

---

### 9. Quel est le salaire moyen par niveau de poste ?

**Réponse attendue** :
> **Salaire moyen par niveau (2025) :**
> 
> | Niveau | Salaire Moyen | Médiane | Écart-type | Effectif |
> |--------|---------------|---------|------------|----------|
> | Junior (L1-L2) | 45 000 EUR | 44 500 EUR | 5 200 EUR | 125 |
> | Intermediate (L3-L4) | 62 000 EUR | 61 000 EUR | 8 100 EUR | 180 |
> | Senior (L5-L6) | 82 000 EUR | 80 500 EUR | 11 500 EUR | 95 |
> | Lead (L7-L8) | 105 000 EUR | 103 000 EUR | 14 200 EUR | 35 |
> | Principal/Executive (L9+) | 135 000 EUR | 132 000 EUR | 22 000 EUR | 10 |
> 
> **Note :** Salaires affichés uniquement pour groupes ≥ 10 employés (conformité RGPD).
> 
> *Source : table `fact_compensation` (effective_date = dernière en date pour chaque employé)*

**Tables** : `fact_compensation`, `dim_position`, `dim_employee`  
**Visualisation** : Bar chart avec écart-type (error bars)  
**Complexité** : ⭐⭐⭐ (calculs statistiques + filtres confidentialité)

---

### 10. Combien investissons-nous en formation par employé ?

**Réponse attendue** :
> **Investissement Formation (2025) :**
> - **Total heures :** 18 750 heures
> - **Coût total :** 1 875 000 EUR
> - **Par employé :** 42 heures/an et 4 200 EUR/an
> 
> **Répartition par catégorie :**
> 1. Compétences techniques : 6 563 h (35%)
> 2. Développement leadership : 4 125 h (22%)
> 3. Conformité & Éthique : 3 375 h (18%)
> 4. Soft skills : 2 813 h (15%)
> 5. Autre : 1 875 h (10%)
> 
> **Taux de complétion :** 87% (2 438 complétées / 2 800 inscriptions)
> 
> **Benchmark :** 40h/employé/an (industrie) → Nous sommes **au-dessus** (+5%) ✅
> 
> *Source : tables `fact_training`, `dim_employee`*

**Tables** : `fact_training`, `dim_employee`  
**Visualisation** : KPI cards + Donut chart (catégories)  
**Complexité** : ⭐⭐ (agrégations simples)

---

## 🔍 Catégorie 3 : Analyses Avancées (5 questions)

### 11. Quelles sont les raisons principales de départ (exit interviews) ?

**Réponse attendue** :
> **Raisons de départ identifiées (2025) - Basé sur 38 exit interviews analysés par IA**
> 
> **Top 5 raisons :**
> 1. **Opportunités de carrière ailleurs** : 32% (12 mentions)
>    - Promotions non obtenues en interne
>    - Progression de carrière limitée
> 
> 2. **Compensation non compétitive** : 24% (9 mentions)
>    - Salaire inférieur au marché
>    - Absence d'augmentation significative
> 
> 3. **Équilibre vie pro/perso** : 18% (7 mentions)
>    - Surcharge de travail
>    - Flexibilité insuffisante
> 
> 4. **Problèmes managériaux** : 15% (6 mentions)
>    - Manque de support du manager
>    - Feedback insuffisant
> 
> 5. **Autre (relocation, études, santé...)** : 11% (4 mentions)
> 
> **Sentiment moyen exit interviews :** 2.8/5 (neutre à légèrement négatif)
> 
> **Recommandation :** Créer un programme de rétention ciblé sur les niveaux intermédiaires avec :
> - Revue des salaires (benchmark marché)
> - Accélération du processus de promotion
> - Formation managériale sur feedback et support
> 
> *Source : table `fact_hr_report` (report_type = 'exit_interview'), champs `report_summary` et `topics` (IA)*

**Tables** : `fact_hr_report`, `fact_lifecycle_event`, `dim_employee`  
**Visualisation** : Treemap (raisons) + Sentiment gauge  
**Complexité** : ⭐⭐⭐⭐ (analyse texte IA + agrégations)

---

### 12. Montre-moi l'évolution du headcount par trimestre sur les 2 dernières années

**Réponse attendue** :
> **Évolution Headcount (Q1 2024 - Q4 2025)**
> 
> | Trimestre | Headcount | Variation vs trimestre précédent | Variation vs année précédente |
> |-----------|-----------|----------------------------------|-------------------------------|
> | Q1 2024 | 438 | +3 (+0.7%) | +15 (+3.5%) |
> | Q2 2024 | 452 | +14 (+3.2%) | +18 (+4.1%) |
> | Q3 2024 | 461 | +9 (+2.0%) | +22 (+5.0%) |
> | Q4 2024 | 457 | -4 (-0.9%) | +19 (+4.3%) |
> | Q1 2025 | 448 | -9 (-2.0%) | +10 (+2.3%) |
> | Q2 2025 | 455 | +7 (+1.6%) | +3 (+0.7%) |
> | Q3 2025 | 450 | -5 (-1.1%) | -11 (-2.4%) |
> | Q4 2025 | 445 | -5 (-1.1%) | -12 (-2.6%) |
> 
> **Tendance :** Croissance en 2024 (+4.3% YoY), légère décroissance en 2025 (-2.6% YoY)
> 
> **Insight :** Ralentissement des embauches en 2025 (contexte économique) couplé à une attrition stable (12.3%).
> 
> *Source : tables `dim_employee`, `dim_date` (snapshots trimestriels)*

**Tables** : `dim_employee`, `dim_date`  
**Visualisation** : Line chart avec marqueurs  
**Complexité** : ⭐⭐⭐ (agrégations temporelles)

---

### 13. Quels sont les thèmes principaux des performance reviews Q4 2025 ?

**Réponse attendue** :
> **Thèmes Performance Reviews Q4 2025** - Basé sur 112 résumés IA
> 
> **Points forts identifiés :**
> 1. **Expertise technique** : 68% des reviews
>    - Maîtrise des technologies
>    - Innovation et veille
> 
> 2. **Collaboration en équipe** : 53%
>    - Esprit d'équipe
>    - Partage de connaissances
> 
> 3. **Résolution de problèmes** : 47%
>    - Approche analytique
>    - Solutions créatives
> 
> 4. **Initiative et proactivité** : 42%
>    - Autonomie
>    - Proposition d'améliorations
> 
> **Axes de développement :**
> 1. **Pensée stratégique** : 38% des reviews
> 2. **Délégation efficace** : 29%
> 3. **Gestion des parties prenantes** : 25%
> 4. **Compétences de présentation** : 22%
> 
> **Distribution des ratings :**
> - Exceptionnel (5/5) : 13 (12%)
> - Fort (4/5) : 63 (56%)
> - Satisfaisant (3/5) : 31 (28%)
> - À améliorer (2/5) : 5 (4%)
> 
> **Recommandation :** Créer un programme "Strategic Leadership" pour développer la pensée stratégique (besoin identifié chez 42 managers).
> 
> *Source : table `fact_hr_report` (report_type = 'performance_review'), champs `report_summary` et `topics` (IA)*

**Tables** : `fact_hr_report`, `dim_employee`, `dim_date`  
**Visualisation** : Word cloud (thèmes) + Donut (ratings)  
**Complexité** : ⭐⭐⭐⭐ (analyse texte IA avancée)

---

### 14. Quel est le taux de mobilité interne (promotions + mutations) ?

**Réponse attendue** :
> **Taux de Mobilité Interne (2025) :** 14.6%
> 
> **Détails :**
> - Promotions : 45 (10.1%)
> - Mutations internes (changement dept/poste) : 20 (4.5%)
> - **Total mouvements internes :** 65 (14.6%)
> - Headcount moyen : 447 employés
> 
> **Flux de mobilité par division :**
> - Technology → Sales : 5 mutations
> - Sales → Customer Success : 4 mutations
> - Operations → Technology : 3 mutations
> - Autres flux : 8 mutations
> 
> **Délai moyen avant mobilité :** 2.6 ans
> 
> **Benchmark :** Taux de mobilité interne 10-15% (sain) → Nous sommes **au sommet de la fourchette** ✅
> 
> **Insight :** Forte mobilité interne = signe de développement de carrière actif et de rétention des talents.
> 
> *Source : tables `fact_lifecycle_event`, `dim_employee`, `dim_department`, `dim_position`*

**Tables** : `fact_lifecycle_event`, `dim_employee`, `dim_department`, `dim_position`  
**Visualisation** : Sankey diagram (flux inter-départements) + KPI cards  
**Complexité** : ⭐⭐⭐⭐ (analyse de flux avec plusieurs dimensions)

---

### 15. Compare l'attrition par cohorte d'embauche (2023 vs 2024 vs 2025)

**Réponse attendue** :
> **Attrition par Cohorte d'Embauche**
> 
> | Cohorte | Embauches Initiales | Départs à Date | Taux de Rétention | Tenure Moyen Départs |
> |---------|---------------------|----------------|-------------------|----------------------|
> | 2023 | 125 | 28 | 77.6% | 1.8 ans |
> | 2024 | 138 | 18 | 87.0% | 0.9 ans |
> | 2025 | 132 | 9 | 93.2% | 0.4 ans |
> 
> **Insight Clé :**
> - **Cohorte 2023** : Attrition la plus élevée (22.4% à 2 ans de tenure)
>   - Pic de départs entre 12-18 mois (période post-probation)
>   - Principales raisons : opportunités externes, compensation
> 
> - **Cohorte 2024** : Rétention améliorée (87% à 1 an)
>   - Programme onboarding renforcé (impact positif)
> 
> - **Cohorte 2025** : Trop tôt pour évaluer (< 1 an tenure)
> 
> **Recommandation :** Focus sur rétention 12-24 mois post-embauche :
> - Check-in RH systématique à 12 mois
> - Revue de compensation à 18 mois
> - Plan de carrière formalisé avant 2 ans
> 
> *Source : tables `fact_lifecycle_event`, `dim_employee`, `dim_date`*

**Tables** : `fact_lifecycle_event`, `dim_employee`, `dim_date`  
**Visualisation** : Stacked area chart (cohortes) + Table comparative  
**Complexité** : ⭐⭐⭐⭐⭐ (analyse longitudinale de cohortes)

---

## 🎯 Catégorie 4 : Questions Conversationnelles (5 questions)

### 16. Pourquoi notre attrition augmente-t-elle ?

**Réponse attendue** :
> **Analyse de l'augmentation de l'attrition (2023-2025)**
> 
> **Tendance :** 11.5% (2023) → 11.8% (2024) → 12.3% (2025) [+0.8pp sur 2 ans]
> 
> **Facteurs contributifs identifiés :**
> 
> 1. **Compression salariale (40% de l'impact)**
>    - Salaires marché ont augmenté de 8% en 2024-2025
>    - Nos augmentations moyennes : 4.5%
>    - Écart créé → départs pour compensation
> 
> 2. **Ralentissement promotions (25% de l'impact)**
>    - Taux de promotion : 10.5% (2023) → 10.1% (2025)
>    - Délai moyen avant promotion : 2.6 ans → 2.9 ans
>    - Frustration talents intermédiaires
> 
> 3. **Départements spécifiques (20% de l'impact)**
>    - Sales : 15.1% attrition (vs 12.3% moyenne)
>    - Customer Success : 14.2%
>    - Problèmes de management et pression quotas
> 
> 4. **Contexte marché emploi (15% de l'impact)**
>    - Guerre des talents tech
>    - Opportunités de remote work ailleurs
> 
> **Recommandations prioritaires :**
> 1. Ajustement salarial ciblé (niveaux L3-L5, écart > 10% vs marché)
> 2. Accélération processus de promotion (objectif < 2.5 ans)
> 3. Coaching managers Sales et Customer Success
> 4. Politique remote work plus flexible
> 
> *Source : Analyse croisée `fact_lifecycle_event`, `fact_compensation`, `fact_hr_report`, données marché (externe)*

**Tables** : `fact_lifecycle_event`, `fact_compensation`, `fact_hr_report`, `dim_employee`, `dim_department`  
**Visualisation** : Combo chart (tendance + drivers) + Waterfall (impact)  
**Complexité** : ⭐⭐⭐⭐⭐ (analyse root cause multi-factorielle)

---

### 17. Où devrions-nous concentrer nos efforts de rétention ?

**Réponse attendue** :
> **Priorités de Rétention - Analyse Data-Driven**
> 
> **🎯 Segment #1 : Talents Intermédiaires High-Performers (Risque ÉLEVÉ)**
> - **Profil :** Niveaux L3-L5, tenure 2-4 ans, rating ≥ 4/5
> - **Population :** 78 employés (17% de l'effectif)
> - **Attrition observée :** 18.5% (vs 12.3% moyenne) ⚠️
> - **Raisons départ :** Compensation (42%), Promotions (35%), Opportunités externes (23%)
> - **Actions :**
>   - Revue salariale immédiate (benchmark marché + ajustement)
>   - Fast-track promotion (réduire délai à 2 ans max)
>   - Retention bonuses ciblés (10-15K EUR)
>   - **Budget estimé :** 780K EUR, **ROI :** Évite 14 départs (coût remplacement ~2M EUR)
> 
> **🎯 Segment #2 : New Hires 12-18 Mois (Risque MOYEN)**
> - **Profil :** Embauches 2024, tenure 12-18 mois
> - **Population :** 65 employés
> - **Attrition observée :** 15.2% (pic post-probation)
> - **Actions :**
>   - Check-in RH systématique à 12 mois
>   - Programme de mentorat renforcé
>   - Clarification plan de carrière
>   - **Budget estimé :** 50K EUR (ressources RH), **ROI :** Évite 10 départs (~1.2M EUR)
> 
> **🎯 Segment #3 : Départements Sales & Customer Success (Risque MOYEN-ÉLEVÉ)**
> - **Population :** 162 employés
> - **Attrition :** 14.8% (vs 12.3%)
> - **Actions :**
>   - Formation managériale (feedback, coaching)
>   - Revue quotas et structure de commission
>   - Amélioration work-life balance (flexible hours)
>   - **Budget estimé :** 120K EUR, **ROI :** Réduction attrition de 2pp (~300K EUR économie)
> 
> **📊 Synthèse Investissement vs ROI :**
> - **Total budget rétention :** 950K EUR
> - **Départs évités :** ~24 employés
> - **Économie coûts de remplacement :** ~3.5M EUR
> - **ROI net :** +2.55M EUR (269% return)
> 
> *Source : Analyse prédictive sur `fact_lifecycle_event`, `fact_compensation`, `fact_hr_report`, `dim_employee`*

**Tables** : Toutes (analyse holistique)  
**Visualisation** : Quadrant chart (risque vs impact) + Budget breakdown  
**Complexité** : ⭐⭐⭐⭐⭐ (segmentation avancée + analyse ROI)

---

### 18. Comment se compare notre investissement formation vs nos peers ?

**Réponse attendue** :
> **Benchmark Investissement Formation (2025)**
> 
> | Métrique | TechCorp (Nous) | Industrie Tech | Écart | Statut |
> |----------|-----------------|----------------|-------|--------|
> | **Heures par FTE/an** | 42h | 40h | +2h (+5%) | ✅ Au-dessus |
> | **Coût par FTE/an** | 4 200 EUR | 3 800 EUR | +400 EUR (+11%) | ✅ Au-dessus |
> | **Taux de complétion** | 87% | 75% | +12pp | ✅ Nettement supérieur |
> | **% budget RH** | 8.5% | 7.2% | +1.3pp | ✅ Engagement fort |
> 
> **Répartition par catégorie (vs benchmark) :**
> - Compétences techniques : 35% (nous) vs 42% (industrie) → **Sous-pondéré** ⚠️
> - Leadership : 22% vs 18% → Au-dessus ✅
> - Compliance : 18% vs 12% → Au-dessus ✅
> - Soft skills : 15% vs 20% → **Sous-pondéré** ⚠️
> 
> **Impact mesuré :**
> - Corrélation formation ↔ rétention : +0.42 (modérée positive)
> - Employés formés >50h/an : attrition 9.2% (vs 14.1% pour <30h/an)
> - Promotions : 65% ont suivi programme leadership dans les 12 mois précédents
> 
> **Recommandations :**
> 1. ✅ Maintenir volume global (42h/FTE)
> 2. ⚠️ Augmenter formation technique (+5pp) pour rester compétitifs
> 3. ⚠️ Renforcer soft skills (+3pp) pour développement holistique
> 4. ✅ Excellent taux de complétion - continuer approche actuelle
> 
> *Source : tables `fact_training` (interne), données benchmarks Deloitte/Gartner 2025 (externe)*

**Tables** : `fact_training`, `dim_employee`, données externes  
**Visualisation** : Bullet charts (vs benchmark) + Scatter plot (formation vs rétention)  
**Complexité** : ⭐⭐⭐⭐ (comparaison externe + analyse corrélation)

---

### 19. Quels employés risquent de partir dans les 6 prochains mois ?

**Réponse attendue** :
> **Analyse Prédictive - Risque de Départ Q1-Q2 2026**
> 
> ⚠️ **IMPORTANT :** Cette analyse est basée sur des patterns historiques. Elle identifie des **signaux de risque**, pas des certitudes.
> 
> **Profils à Risque Élevé (38 employés identifiés) :**
> 
> **Cluster 1 : "Compensation Laggards" (15 employés)**
> - Salaire < 10% en dessous de la médiane de leur niveau
> - Tenure 2-4 ans (window de mobilité externe)
> - Performance ≥ 4/5 (attractifs pour concurrents)
> - **Probabilité de départ :** 68%
> - **Action :** Revue salariale urgente
> 
> **Cluster 2 : "Promotion Passed-Over" (12 employés)**
> - Tenure > 3 ans sans promotion
> - Performance 4-5/5
> - Pairs promus récemment
> - **Probabilité de départ :** 55%
> - **Action :** Discussion plan de carrière + promotion accélérée
> 
> **Cluster 3 : "Disengaged High-Performers" (11 employés)**
> - Aucune formation suivie en 12 derniers mois
> - Aucun événement positif (bonus, reconnaissance) récent
> - Diminution participation (absentéisme +15%)
> - **Probabilité de départ :** 48%
> - **Action :** One-on-one RH + programme re-engagement
> 
> **📊 Modèle Prédictif :**
> - Variables utilisées : compensation, tenure, performance, promotions, formation, absences
> - Précision historique : 72% (testé sur cohortes 2023-2024)
> - Faux positifs : 28% (employés identifiés mais qui restent)
> - **Recommandation :** Utiliser comme outil de priorisation, pas de décision
> 
> **💡 Prochaines Étapes :**
> 1. RH contacte les 38 employés pour check-in (Q1 2026)
> 2. Managers informés (liste confidentielle)
> 3. Budget rétention alloué : 450K EUR
> 4. Suivi mensuel (mise à jour scoring)
> 
> *Source : Modèle prédictif ML sur `fact_lifecycle_event`, `fact_compensation`, `fact_training`, `fact_absence`, `dim_employee`*  
> *Note : Dataset synthétique - en production, utiliser Azure ML ou Fabric Data Science*

**Tables** : Toutes (modèle ML)  
**Visualisation** : Scatter plot (risque vs impact) + Risk matrix  
**Complexité** : ⭐⭐⭐⭐⭐ (machine learning / scoring prédictif)

---

### 20. Résume-moi les insights RH clés pour le comité de direction

**Réponse attendue** :
> **📊 Executive Summary - HR KPIs Q4 2025**
> 
> ---
> 
> **🎯 Headline Metrics**
> 
> | KPI | Actuel | Cible | Statut | Tendance |
> |-----|--------|-------|--------|----------|
> | **Headcount** | 445 | 450 | ⚠️ -1.1% | ⬇️ (vs Q4 2024) |
> | **Attrition annuel** | 12.3% | <12% | ⚠️ Légèrement au-dessus | ⬆️ (+0.5pp vs 2024) |
> | **Promotion rate** | 10.1% | 8-10% | ✅ Dans fourchette | ➡️ Stable |
> | **Training hrs/FTE** | 42h | ≥40h | ✅ Au-dessus | ⬆️ (+2h vs 2024) |
> | **HR case resolution** | 28 jours | <30 jours | ✅ Objectif atteint | ⬇️ Amélioration |
> 
> ---
> 
> **🚨 Top 3 Risques**
> 
> 1. **Attrition Sales & Customer Success (15%)**
>    - 📍 Impact : Perte de revenus, coûts de remplacement
>    - 🔍 Root cause : Compression salariale + pression quotas
>    - 💡 Action : Revue comp + coaching managers (Budget : 250K EUR)
> 
> 2. **Talents Intermédiaires en fuite (18.5% attrition)**
>    - 📍 Impact : Perte de succession pipeline
>    - 🔍 Root cause : Opportunités externes + promotions lentes
>    - 💡 Action : Fast-track program + retention bonuses (Budget : 780K EUR)
> 
> 3. **Ralentissement croissance headcount (-2.6% YoY)**
>    - 📍 Impact : Capacité d'exécution limitée
>    - 🔍 Root cause : Gel embauches + attrition stable
>    - 💡 Action : Plan de recrutement Q1 2026 (objectif +25 FTE)
> 
> ---
> 
> **✅ Top 3 Réussites**
> 
> 1. **Mobilité interne forte (14.6%)**
>    - Développement de carrière actif
>    - Rétention des talents (65 mouvements internes vs 55 départs)
> 
> 2. **Investissement formation au-dessus marché (+11%)**
>    - 42h/FTE vs 40h industrie
>    - Corrélation positive avec rétention (-5pp attrition si >50h/an)
> 
> 3. **Performance reviews : 68% rating ≥4/5**
>    - Pipeline de talents solide
>    - Culture de high performance
> 
> ---
> 
> **💰 Budget & ROI Recommandé (2026)**
> 
> | Initiative | Budget | Départs Évités | ROI Net |
> |------------|--------|----------------|---------|
> | Retention program (comp + bonuses) | 1 030K EUR | ~34 | +3.8M EUR |
> | Formation technique renforcée | 150K EUR | Indirect (compétitivité) | TBD |
> | Recrutement Q1-Q2 2026 | 500K EUR | +25 FTE | Revenue growth |
> | **TOTAL** | **1 680K EUR** | **ROI estimé : 2.3x** | - |
> 
> ---
> 
> **🎯 Décisions Requises ComDir**
> 
> 1. ✅ Approuver budget rétention 1M EUR (Q1 2026)
> 2. ✅ Valider plan de recrutement +25 FTE
> 3. ⚠️ Arbitrage allocation (Sales vs Tech vs Ops)
> 4. 📅 Prochaine revue : Avril 2026 (post Q1)
> 
> ---
> 
> *Source : Toutes tables HR (synthèse complète)*  
> *Préparé par : HR Analytics AI Assistant | Date : 2025-12-31*

**Tables** : Toutes (vue 360° exécutive)  
**Visualisation** : Executive dashboard (multi-KPI) + Risk matrix  
**Complexité** : ⭐⭐⭐⭐⭐ (synthèse stratégique complète)

---

## 🏁 Résumé

| Catégorie | Nb Questions | Complexité Moyenne | Tables Principales |
|-----------|--------------|--------------------|--------------------|
| Exploration Simple | 5 | ⭐ | dim_employee, dim_department |
| Agrégations et Calculs | 5 | ⭐⭐ - ⭐⭐⭐ | fact_*, dim_* |
| Analyses Avancées | 5 | ⭐⭐⭐⭐ | fact_lifecycle_event, fact_hr_report (IA) |
| Conversationnelles | 5 | ⭐⭐⭐⭐⭐ | Toutes (analyses holistiques) |

**Total : 20 exemples couvrant tous les niveaux de complexité** 🚀
