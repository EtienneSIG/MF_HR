# Questions de Démo - Fabric Data Agent

## 🎯 Objectif

Cette liste contient **15 questions "wow effect"** à poser au **Fabric Data Agent** pendant la démo.
Chaque question illustre une capacité différente et crée un impact auprès de l'audience.

Les questions sont organisées par **niveau de complexité** et **cas d'usage métier**.

---

## ✅ Questions Niveau 1 : Exploration Simple

### 1. Quel est notre effectif actuel ?

**Attendu** :
- Réponse : "445 employés actifs (au 31 décembre 2025)"
- Tables utilisées : `dim_employee`
- Graphique suggéré : Card / KPI

**Pourquoi c'est "wow"** : Question ultra-simple, réponse instantanée. Démo que le Data Agent comprend le français naturel.

---

### 2. Combien de départements avons-nous ?

**Attendu** :
- Réponse : 
  - 12 départements répartis en 4 divisions
  - Technology: 4 depts
  - Sales & Marketing: 3 depts
  - Operations: 3 depts
  - Corporate Functions: 2 depts
- Tables utilisées : `dim_department`
- Graphique suggéré : Treemap ou Table

**Pourquoi c'est "wow"** : Le Data Agent structure automatiquement la réponse de manière hiérarchique.

---

### 3. Combien d'heures de formation avons-nous dispensées en 2025 ?

**Attendu** :
- Réponse : "18 750 heures (42h par employé)"
- Tables utilisées : `fact_training`, `dim_employee`
- Filtre : `YEAR(training_date) = 2025`

**Pourquoi c'est "wow"** : Calcul automatique du ratio per-FTE sans le demander explicitement.

---

## 📊 Questions Niveau 2 : Agrégations et Calculs

### 4. Quel est notre taux d'attrition en 2025 ?

**Attendu** :
- Réponse : "12.3% (55 départs / 447 headcount moyen)"
- Tables utilisées : `fact_lifecycle_event`, `dim_employee`
- Calcul : Attrition Rate avec détail volontaire vs involontaire
- Graphique suggéré : Gauge avec benchmark 15%

**Pourquoi c'est "wow"** : Calcul métrique complexe (attrition = exits / avg headcount × 100%) fait automatiquement.

---

### 5. Combien de promotions avons-nous eu cette année ?

**Attendu** :
- Réponse : "45 promotions (taux de 10.1%)"
- Tables utilisées : `fact_lifecycle_event`, `dim_employee`
- Filtre : `event_type = 'promotion'`, `YEAR(event_date) = 2025`
- Graphique suggéré : KPI card + trend

**Pourquoi c'est "wow"** : Jointure implicite et calcul du taux de promotion.

---

### 6. Quel département a le taux d'attrition le plus élevé ?

**Attendu** :
- Réponse : "Sales : 15.1% (16 départs / 106 headcount moyen)"
- Tables utilisées : `fact_lifecycle_event`, `dim_employee`, `dim_department`
- Tri : `ORDER BY attrition_rate DESC LIMIT 1`
- Graphique suggéré : Bar chart horizontal (tous depts)

**Pourquoi c'est "wow"** : Ranking automatique avec multi-table join et calcul par groupe.

---

## 🔍 Questions Niveau 3 : Analyse Avancée

### 7. Quelles sont les raisons principales de départ (exit interviews) ?

**Attendu** :
- Réponse : Liste des 5 top raisons (opportunités carrière 32%, compensation 24%, équilibre vie pro/perso 18%...)
- Tables utilisées : `fact_hr_report` (avec champs IA : `topics`, `report_summary`)
- Source : Exit interviews analysés par IA
- Graphique suggéré : Treemap ou word cloud

**Pourquoi c'est "wow"** : ✨ **Utilise l'IA pour extraire insights des textes** (PII redacted). Démo de l'AI Shortcut Transformations.

---

### 8. Montre-moi l'évolution du headcount par trimestre sur 2 ans

**Attendu** :
- Réponse : Table/graphique avec Q1 2024 à Q4 2025 (8 trimestres)
- Tables utilisées : `dim_employee`, `dim_date`
- Calcul : Snapshot par trimestre avec variation vs trimestre précédent
- Graphique suggéré : Line chart avec marqueurs

**Pourquoi c'est "wow"** : Analyse temporelle avec calculs de variations automatiques (QoQ, YoY).

---

### 9. Quels sont les thèmes principaux des performance reviews Q4 2025 ?

**Attendu** :
- Réponse : 
  - Points forts : Expertise technique (68%), Collaboration (53%)...
  - Axes de développement : Pensée stratégique (38%), Délégation (29%)...
  - Distribution ratings : 5/5 (12%), 4/5 (56%)...
- Tables utilisées : `fact_hr_report` (report_type = 'performance_review', champs IA)
- Filtre : Q4 2025

**Pourquoi c'est "wow"** : ✨ **Analyse sémantique IA avancée** sur 112 comptes rendus. Extraction automatique de thèmes sans lire les textes manuellement.

---

## 📈 Questions Niveau 4 : Insights Stratégiques

### 10. Quel est le taux de mobilité interne (promotions + mutations) ?

**Attendu** :
- Réponse : "14.6% (45 promotions + 20 mutations internes = 65 mouvements / 447 employés)"
- Tables utilisées : `fact_lifecycle_event`, `dim_employee`
- Filtre : `event_type IN ('promotion', 'internal_move')`
- Graphique suggéré : Sankey diagram (flux inter-départements)

**Pourquoi c'est "wow"** : Calcul composite (2 types d'événements) + suggestion de visualisation avancée (Sankey).

---

### 11. Compare l'attrition par cohorte d'embauche (2023 vs 2024 vs 2025)

**Attendu** :
- Réponse : Table comparative avec taux de rétention par cohorte
  - Cohorte 2023 : 77.6% rétention (28 départs / 125 embauches)
  - Cohorte 2024 : 87.0% rétention (18 départs / 138 embauches)
  - Cohorte 2025 : 93.2% rétention (9 départs / 132 embauches)
- Tables utilisées : `fact_lifecycle_event`, `dim_employee`, `dim_date`
- Graphique suggéré : Stacked area chart (cohortes)

**Pourquoi c'est "wow"** : ✨ **Analyse longitudinale de cohortes** - complexité élevée (groupement par hire year + calcul rétention).

---

### 12. Combien investissons-nous en formation par employé ?

**Attendu** :
- Réponse : "4 200 EUR/employé (42h/employé, taux de complétion 87%)"
- Tables utilisées : `fact_training`, `dim_employee`
- Calcul : Total cost / headcount, total hours / headcount
- Benchmark : "Au-dessus de la moyenne industrie (40h/FTE)"

**Pourquoi c'est "wow"** : Calcul multi-dimensionnel + contexte benchmark automatique.

---

## 🎯 Questions Niveau 5 : Conversation Complexe

### 13. Pourquoi notre attrition augmente-t-elle ?

**Attendu** :
- Réponse structurée :
  - **Tendance** : 11.5% → 11.8% → 12.3% (2023-2025)
  - **Facteurs** : 
    1. Compression salariale (40% impact)
    2. Ralentissement promotions (25%)
    3. Départements spécifiques Sales/CS (20%)
    4. Contexte marché emploi (15%)
  - **Recommandations** : Ajustement salarial, accélération promotions, coaching managers
- Tables utilisées : Analyse croisée multi-tables
- Graphique suggéré : Waterfall (impact par facteur)

**Pourquoi c'est "wow"** : ✨ **Question conversationnelle "pourquoi"** → Data Agent fait une analyse root cause multi-factorielle. Démo de raisonnement complexe.

---

### 14. Où devrions-nous concentrer nos efforts de rétention ?

**Attendu** :
- Réponse segmentée :
  - **Segment #1** : Talents intermédiaires high-performers (78 employés, attrition 18.5%)
  - **Segment #2** : New hires 12-18 mois (65 employés, attrition 15.2%)
  - **Segment #3** : Départements Sales & CS (162 employés, attrition 14.8%)
  - **ROI** : Budget 950K EUR → Économie 3.5M EUR (évite 24 départs)
- Tables utilisées : Analyse prédictive multi-critères
- Graphique suggéré : Quadrant chart (risque vs impact)

**Pourquoi c'est "wow"** : ✨ **Segmentation stratégique + calcul ROI** → Data Agent propose une stratégie actionnable avec chiffres business. Démo de conseil RH data-driven.

---

### 15. Résume-moi les insights RH clés pour le comité de direction

**Attendu** :
- Réponse exécutive structurée :
  - **Headline Metrics** : 5 KPIs clés (headcount, attrition, promotions, formation, cas RH)
  - **Top 3 Risques** : Attrition Sales/CS, fuite talents intermédiaires, ralentissement croissance
  - **Top 3 Réussites** : Mobilité interne, investissement formation, pipeline de talents
  - **Budget & ROI** : Plan de rétention 1.68M EUR (ROI 2.3x)
  - **Décisions requises** : 4 points d'arbitrage pour ComDir
- Tables utilisées : Vue 360° (toutes tables)
- Graphique suggéré : Executive dashboard multi-KPI

**Pourquoi c'est "wow"** : ✨ **Synthèse exécutive complète** → Data Agent agit comme un vrai Business Partner RH. Format prêt pour présentation ComDir. **Démo ultime de l'agent conversationnel.**

---

## 🎨 Scénario de Démo Recommandé (10-15 min)

### Acte 1 : Fondations (3 min)

1. **Question 1** : "Quel est notre effectif actuel ?"
   - Démo : Simplicité, français naturel
   
2. **Question 4** : "Quel est notre taux d'attrition en 2025 ?"
   - Démo : Calcul métrique complexe automatique

### Acte 2 : Analyse Multi-Dimensionnelle (4 min)

3. **Question 6** : "Quel département a le taux d'attrition le plus élevé ?"
   - Démo : Ranking, multi-table join
   
4. **Question 10** : "Quel est le taux de mobilité interne ?"
   - Démo : Calcul composite, suggestion Sankey diagram

### Acte 3 : IA sur Texte (3 min) ✨

5. **Question 7** : "Quelles sont les raisons principales de départ ?"
   - Démo : **AI Shortcut Transformations** - extraction insights depuis exit interviews
   
6. **Question 9** : "Quels sont les thèmes principaux des performance reviews Q4 2025 ?"
   - Démo : **IA sémantique avancée** - analyse 112 comptes rendus

### Acte 4 : Insights Stratégiques (3 min) ✨

7. **Question 13** : "Pourquoi notre attrition augmente-t-elle ?"
   - Démo : **Analyse root cause** - raisonnement complexe
   
8. **Question 15** : "Résume-moi les insights RH clés pour le comité de direction"
   - Démo : **Synthèse exécutive** - format business ready

### Transition (2 min)

Montrer les graphiques Power BI générés à partir des réponses.

---

## 💡 Conseils pour la Démo

**Préparation** :
- ✅ Tester les 15 questions en amont (vérifier les réponses)
- ✅ Préparer des variations de questions (reformulations)
- ✅ Avoir le schema.md ouvert (référence rapide)

**Pendant la démo** :
- ⚡ Commencer par questions simples (1, 2, 3) pour rassurer
- ⚡ Monter progressivement en complexité (4 → 6 → 9 → 13)
- ⚡ Insister sur les questions IA (7, 9) → **différenciateur clé**
- ⚡ Finir en apothéose avec question 15 (résumé exécutif)

**Points à souligner** :
- 🎯 Pas de SQL à écrire → Français naturel
- 🎯 Calculs automatiques (attrition, ratios, benchmarks)
- 🎯 IA intégrée (PII redaction, extraction de thèmes, sentiment)
- 🎯 Recommandations actionnables (ROI, segmentation, priorités)

**Gestion des erreurs** :
- Si réponse incorrecte : Reformuler la question
- Si calcul faux : Vérifier les relations dans le semantic model
- Si timeout : Simplifier la question (moins de dimensions)

---

## 🚀 Questions Bonus (Pour Q&A)

**Si temps supplémentaire** :

16. "Quels employés risquent de partir dans les 6 prochains mois ?" (Prédictif ML)
17. "Comment se compare notre investissement formation vs nos peers ?" (Benchmark externe)
18. "Quelle est l'évolution des salaires par niveau de poste ?" (Compensation analytics)
19. "Quel est le temps moyen de résolution des cas RH ?" (Efficacité RH)
20. "Montre-moi le funnel de recrutement 2025" (Talent acquisition)

---

**Ces questions couvrent tous les cas d'usage : exploration simple, calculs, IA textuelle, stratégie, prédictif !** 🎯
