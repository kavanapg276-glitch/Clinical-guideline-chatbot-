# Phase 1: 30-Chunk Random Provenance & Clinical Integrity Audit

**Date:** 2026-11-01  
**Sampling Method:** Pseudo-random deterministic sampling (`random.seed(42)`) across 974 guideline chunks  
**Purpose:** Manual verification of source document traceability, page bounds, recommendation context, and exclusion of unverified flowcharts.

---

## Summary Audit Table

| # | Chunk ID | Document ID | Source Page(s) | Condition | Chunk Type | Populations | Drug Classes | Heading |
|---|---|---|---|---|---|---|---|---|
| 1 | `who_htn_001_c0026` | `who_htn_001` | pp. 13-14 | hypertension | monitoring | cardiovascular_disease | None | INTRODUCTION |
| 2 | `who_htn_001_c0028` | `who_htn_001` | p. 15 | hypertension | other | None | None | 2.2	 Analytical framework and PICOs |
| 3 | `who_htn_001_c0031` | `who_htn_001` | p. 16 | both | other | cardiovascular_disease, chronic_kidney_disease, type_2_diabetes | None | 2.4	 Reviews of evidence |
| 4 | `who_htn_001_c0033` | `who_htn_001` | pp. 17-18 | hypertension | other | None | None | METHOD FOR DEVELOPING THE GUIDELINE |
| 5 | `who_htn_001_c0090` | `who_htn_001` | pp. 41-43 | hypertension | other | cardiovascular_disease | None | IMPLEMENTATION TOOLS |
| 6 | `who_htn_001_c0096` | `who_htn_001` | pp. 46-47 | hypertension | monitoring | None | None | REFERENCES (Part 2) |
| 7 | `who_htn_001_c0105` | `who_htn_001` | p. 50 | hypertension | other | None | None | AMRO |
| 8 | `who_htn_001_c0115` | `who_htn_001` | p. 51 | hypertension | other | None | None | EMRO |
| 9 | `who_t2dm_001_c0007` | `who_t2dm_001` | p. 13 | type_2_diabetes | other | type_2_diabetes | None | 1	 Clinical manifestations of (Part 2) |
| 10 | `nice_htn_001_c0005` | `nice_htn_001` | p. 5 | hypertension | other | None | None | 1.1 Measuring blood pressure |
| 11 | `nice_htn_001_c0025` | `nice_htn_001` | p. 9 | both | recommendation | chronic_kidney_disease, type_2_diabetes | None | 1.2.12 |
| 12 | `nice_htn_001_c0030` | `nice_htn_001` | p. 10 | both | recommendation | type_2_diabetes | None | 1.3.3 |
| 13 | `nice_htn_001_c0040` | `nice_htn_001` | pp. 12-13 | both | other | cardiovascular_disease, chronic_kidney_disease | None | 1.4.10 |
| 14 | `nice_htn_001_c0052` | `nice_htn_001` | p. 16 | both | other | chronic_kidney_disease | None | 1.4.20 |
| 15 | `nice_htn_001_c0083` | `nice_htn_001` | p. 23 | hypertension | other | None | thiazide | 1.4.50 |
| 16 | `nice_t2dm_001_c0126` | `nice_t2dm_001` | p. 77 | type_2_diabetes | other | None | glp1_ra | 1.24.4 |
| 17 | `mohfw_htn_001_c0021` | `mohfw_htn_001` | p. 14 | hypertension | other | cardiovascular_disease | None | 3.3  The assessment of a patient with hypertens... |
| 18 | `mohfw_htn_001_c0062` | `mohfw_htn_001` | p. 22 | both | recommendation | type_2_diabetes | None | 4.8 Therapy of hypertension and associated cond... |
| 19 | `mohfw_htn_001_c0078` | `mohfw_htn_001` | p. 24 | hypertension | recommendation | None | None | 4.9.2 In a patient with postural hypotension ti... |
| 20 | `mohfw_htn_001_c0108` | `mohfw_htn_001` | p. 28 | hypertension | other | elderly, type_2_diabetes | ace_inhibitor, thiazide | 5.3.2. The common side effects of diuretics are... |
| 21 | `mohfw_htn_001_c0120` | `mohfw_htn_001` | pp. 35-36 | hypertension | other | None | None | WHO/ISH > ESC/ESH |
| 22 | `mohfw_htn_001_c0158` | `mohfw_htn_001` | p. 61 | hypertension | monitoring | cardiovascular_disease, chronic_kidney_disease | None | 3.1.1 Patients should be counselled about hyper... |
| 23 | `mohfw_htn_001_c0169` | `mohfw_htn_001` | pp. 63-64 | both | monitoring | cardiovascular_disease | antiplatelet, statin | 3.8  All patients should be asked about tobacco... |
| 24 | `mohfw_htn_001_c0196` | `mohfw_htn_001` | p. 78 | both | other | cardiovascular_disease, chronic_kidney_disease | None | 4.5.5.              The presence of associated ... |
| 25 | `mohfw_htn_001_c0222` | `mohfw_htn_001` | p. 93 | both | other | None | ace_inhibitor, ccb, thiazide | 4.8.1.2 ACE inhibitors are preferred as initial... |
| 26 | `mohfw_htn_001_c0237` | `mohfw_htn_001` | pp. 95-96 | both | rationale | cardiovascular_disease | None | CHC. |
| 27 | `mohfw_htn_001_c0258` | `mohfw_htn_001` | p. 98 | hypertension | rationale | None | thiazide | 4.11.6 Re-institution of therapy or intensifica... |
| 28 | `mohfw_htn_001_c0262` | `mohfw_htn_001` | p. 100 | hypertension | recommendation | None | antiplatelet | 4.12.1 The treatment of hypertension should be ... |
| 29 | `mohfw_htn_001_c0263` | `mohfw_htn_001` | p. 100 | hypertension | other | cardiovascular_disease | antiplatelet | 4.12.2   Antiplatelet therapy with low-dose asp... |
| 30 | `mohfw_htn_002_c0106` | `mohfw_htn_002` | p. 28 | hypertension | recommendation | cardiovascular_disease | antiplatelet | 4.11.4 Negative recommendation: Do not use low-... |

---

## Detailed Chunk Inspection

### Audit Item #1: `who_htn_001_c0026`

- **Source Document:** WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (`who_htn_001`)
- **Source Page(s):** pp. 13-14
- **Condition:** `hypertension` | **Chunk Type:** `monitoring`
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > 8.	 RECOMMENDATION ON TREATMENT BY NONPHYSICIAN PROFESSIONALS > INTRODUCTION`
- **Heading:** INTRODUCTION
- **Population Tags:** ['cardiovascular_disease']
- **Drug Class Tags:** []
- **Applicability Conditions:** ['It\naddresses pharmacotherapy in individuals with a "confirmed" diagnosis of hypertension, such as\nhypertension diagnosed when blood pressure is found to be elevated on two different days.']
- **Exceptions / Contraindications:** []
- **Text Hash:** `bb19bef150c97fc3e8e80114fa0c8cded1fef6d1137472afe1522af46858d75f`

```text
INTRODUCTION
GUIDELINE FOR THE PHARMACOLOGICAL TREATMENT OF HYPERTENSION IN ADULTS
This guideline will replace the guidance in the modules Evidence-based protocols and Risk-based CVD
management of the HEARTS technical package, as well as the guidance in the WHO PEN package
regarding the threshold for initiation of treatment, and for the preferred pharmacological treatment for
hypertension.
The guideline does not address measurement of blood pressure or diagnosis of hypertension. It
addresses pharmacotherapy in individuals with a "confirmed" diagnosis of hypertension, such as
hypertension diagnosed when blood pressure is found to be elevated on two different days.
Although this guideline does not address modifiable risk factors for hypertension such as unhealthy
diet, physical inactivity, consumption of tobacco and alcohol, and being overweight or obese, a
comprehensive treatment plan for hypertension must include addressing these risk factors through lifestyle modifications and other interventions (2).
Nonpharmacological approaches to treatment or prevention of hypertension include:
[
[ reducing salt intake (to less than 5g daily)
[
[ eating more fruit and vegetables
[
[ being physically active on a regular basis
[
[ avoiding use of tobacco
[
[ reducing alcohol consumption
[
[ limiting the intake of foods high in saturated fats
[
[ eliminating/reducing trans fats in diet (2).
The guideline does not address hypertensive crisis as it is focused on chronic blood pressure
management in regular care settings.
The objectives of the hypertension guideline are to:
[
[ provide a blood pressure threshold for the initiation of treatment for hypertension;
[
[ determine if laboratory tests or cardiovascular risk assessment are required prior to initiation of
treatment for hypertension;
[
[ determine the pharmacological agents with which to initiate treatment;
[
[ determine the need to initiate treatment with monotherapy, dual therapy, or single-pill
combinations;
[
[ provide targets for blood pressure control in hypertension;
[
[ provide intervals for follow up for patients with hypertension; and
[
[ determine how nonphysician health care workers can participate in the management of
hypertension.
Target audience
Primary audience
Clinicians/health care providers at all levels of health care.
Secondary audience
National NCD/CVD programme managers, health care academics, policy-makers setting practice
recommendations, students, and hypertension medicine manufacturers.
```

---

### Audit Item #2: `who_htn_001_c0028`

- **Source Document:** WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (`who_htn_001`)
- **Source Page(s):** p. 15
- **Condition:** `hypertension` | **Chunk Type:** `other`
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > 2.1	 Guideline contributors > 2.2	 Analytical framework and PICOs`
- **Heading:** 2.2	 Analytical framework and PICOs
- **Population Tags:** []
- **Drug Class Tags:** []
- **Applicability Conditions:** ['Q10: When should BP be re-assessed after\ntreatment initiation?']
- **Exceptions / Contraindications:** []
- **Text Hash:** `3cd45cb3fa0e0247611523af572798dccd5fbb6c9db396cbb06807340c279efd`

```text
2.2	 Analytical framework and PICOs
An initial GDG meeting was held in Geneva in July 2019 to determine the scope and PICO (population,
intervention, comparison, outcome) questions of the guideline. The GDG first developed an analytical
framework (Fig. 1) that demonstrates the impact of interventions on intermediate and final outcomes
and displays the order of the key questions to better visualize and place them along the patient-flow
pathway. Following this, and a preliminary scoping review and discussion between the steering group
and methodologist, PICO questions were developed. These were considered, deliberated on, further
refined and voted on during the meeting.
Fig. 1	 Analytic framework for antihypertensive medication treatment
Q1: At what BP level should pharmacological
therapy be initiated?
Q2: Are lab tests needed to start therapy?
Q3: Is risk assessment needed to start therapy
Q4: Monotherapy vs no therapy?
Q5: Monotherapy vs other monotherapy?
Q6: Monotherapy vs combination therapy?
Q7: What choice of combination therapy?
Q8: Single-pill combination vs free combination?
Q9: Post-treatment target BP level?
Q10: When should BP be re-assessed after
treatment initiation?
Q11: Management by physician vs non-physician
provider?
Adults with
adequately
diagnosed HTN
who have initiated
life-style
modification
Intermediate
outcomes
[BP reduction
[HTN control %
Final health
outcomes
[all-cause mortality
[CV mortality
[MI
```

---

### Audit Item #3: `who_htn_001_c0031`

- **Source Document:** WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (`who_htn_001`)
- **Source Page(s):** p. 16
- **Condition:** `both` | **Chunk Type:** `other`
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > 2.3	 Outcome importance rating > 2.4	 Reviews of evidence`
- **Heading:** 2.4	 Reviews of evidence
- **Population Tags:** ['cardiovascular_disease', 'chronic_kidney_disease', 'type_2_diabetes']
- **Drug Class Tags:** []
- **Applicability Conditions:** ['(See Web Annex A for full details.)\nMost of the included reviews were found to be of high certainty when assessed using the AMSTAR\ntool.']
- **Exceptions / Contraindications:** []
- **Text Hash:** `6c90db7388b2b23d1a49830f95898b196ba7119301ac2089d1254c13bede1661`

```text
2.4	 Reviews of evidence
The WHO Steering Group, with the participation of the GDG, determined the scope of the guideline
and identified eleven questions in the format of population, intervention, comparison, and outcomes
(PICO) to guide the search for systematic reviews (Annex 4). Eleven overviews of reviews informed the
guideline development process. A systematic search was carried out in PubMed, Embase, The Cochrane
Library, and Epistemonikos to identify existing systematic reviews that answered the PICO questions
published in 2015 or after. Suitable systematic reviews were then evaluated based on the following
criteria:
[
[ their methodology as appraised by the AMSTAR (Assessing the Methodological Quality of
Systematic Reviews) tool;
[
[ how directly they matched the PICO questions;
[
[ whether they reported sufficient information to allow for an assessment of the certainty of the
evidence (e.g. tables with characteristics of included studies, risk of bias assessments at the study
level, results of meta analyses in forest plots);
[
[ whether they reported evidence in subgroups of interest (e.g. patients with diabetes mellitus
(DM), cardiovascular disease (CVD), chronic kidney disease (CKD) etc); and
[
[ the date of the most recent review to ensure the most updated evidence was used.
The Systematic Review Team prioritized the most useful reviews for each question, comparison,
outcome and subpopulation within questions, and included as many reviews as necessary to address
each question comprehensively. (Web Annex A provides details of the search terms and strategy used.)
No reviews were updated.
Two questions (PICO 2 and 10, see Annex 4) were not addressed in an existing systematic review, and
evidence from primary studies was therefore used. In this case, the Systematic Review Team reviewed
the list of studies used in existing guidelines, queried the GDG and content experts, and searched for
primary studies.
A total of 159 systematic reviews and 17 additional primary studies were included. Most of these were
traditional systematic reviews in which the authors conducted pairwise meta-analysis, whereas nine
analysed individual patient data. The Systematic Review Team also identified several published network
meta-analyses. (See Web Annex A for full details.)
Most of the included reviews were found to be of high certainty when assessed using the AMSTAR
tool. Details of the selection process, and the reviews and studies included for each PICO question, are
presented in Web Annex A.
Another overview of reviews was conducted to identify systematic reviews to inform other decision
criteria in the evidence-to-decision framework, including people's values, resources, acceptability,
feasibility and equity, presented in Web Annex A. This review was enriched by primary studies identified
by GDG members. This review focused on evidence informing HTN management in low- and middleincome settings.
```

---

### Audit Item #4: `who_htn_001_c0033`

- **Source Document:** WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (`who_htn_001`)
- **Source Page(s):** pp. 17-18
- **Condition:** `hypertension` | **Chunk Type:** `other`
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > 2.5	 Certainty of evidence and strength of recommendations > METHOD FOR DEVELOPING THE GUIDELINE`
- **Heading:** METHOD FOR DEVELOPING THE GUIDELINE
- **Population Tags:** []
- **Drug Class Tags:** []
- **Applicability Conditions:** []
- **Exceptions / Contraindications:** []
- **Text Hash:** `29a111404e6bdbb95a787a1a4a5a108dd892cc47dcfd28b572a59f394b4fd3e1`

```text
METHOD FOR DEVELOPING THE GUIDELINE
GUIDELINE FOR THE PHARMACOLOGICAL TREATMENT OF HYPERTENSION IN ADULTS
```

---

### Audit Item #5: `who_htn_001_c0090`

- **Source Document:** WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (`who_htn_001`)
- **Source Page(s):** pp. 41-43
- **Condition:** `hypertension` | **Chunk Type:** `other`
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > 6.2	 Drug- and dose-specific protocols > IMPLEMENTATION TOOLS`
- **Heading:** IMPLEMENTATION TOOLS
- **Population Tags:** ['cardiovascular_disease']
- **Drug Class Tags:** []
- **Applicability Conditions:** ['Supporting\nself-management for people with hypertension: a meta-review of quantitative and qualitative\nsystematic reviews.', 'Correction: costs and cost-effectiveness of hypertension screening and treatment in adults with\nhypertension in rural Nigeria in the context of a health insurance program.']
- **Exceptions / Contraindications:** []
- **Text Hash:** `9b0be635b4d64f175771d7b137e26aabf3facb3296f146deab06118bbd6a98e2`

```text
IMPLEMENTATION TOOLS
GUIDELINE FOR THE PHARMACOLOGICAL TREATMENT OF HYPERTENSION IN ADULTS
References
(1)
Cardiovascular diseases (CVDs). Key facts. 17 May 2017 [website] (https://www.who.int/newsroom/fact-sheets/detail/cardiovascular-diseases-(cvds), accessed 31 March 2021).
(2)
Hypertension. Key facts. 13 September 2019 [website] (https://www.who.int/news-room/factsheets/detail/hypertension, accessed 31 March 2021).
(3)
Prevention of cardiovascular disease: guidelines for assessment and management of total
cardiovascular risk. Geneva: World Health Organization; 2007.
(4)
Hultcrantz M, Rind D, Akl EA, Treweek S, Mustafa RA, Iorio A, et al. The GRADE Working Group
clarifies the construct of certainty of evidence. J Clin Epidemiol. 2017;87:4-13. doi: 10.1016/j.
jclinepi.2017.05.006.
(5)
Balshem H, Helfand M, Schünemann HJ, Oxman AD, Kunz R, Brozek J. GRADE guidelines:
3. Rating the quality of evidence. J Clin Epidemiol. 2011;64(4):401-406. doi: 10.1016/j.
jclinepi.2010.07.015.
(6)
Shahaj O, Denneny D, Schwappach A, Pearce G, Epiphaniou E, Parke H, et al. Supporting
self-management for people with hypertension: a meta-review of quantitative and qualitative
systematic reviews. J Hypertens. 2019;37(2):264-279. doi: 10.1097/HJH.0000000000001867.
(7)
Meiqari L, Nguyen T-P-L, Essink D, Zweekhorst M, Wright P, Scheele F. Access to hypertension care
and services in primary health-care settings in Vietnam: a systematic narrative review of existing
literature. Glob Health Action. 2019;12(1):1-11. doi: 10.1080/16549716.2019.1610253.
(8)
Kostova D, Spencer G, Mora AE, Cobb LAK, Husain MJ, Datta BK, et al. The cost effectiveness
of hypertension management in low-income and middle-income countries: a review. BMJ Public
Global Health. 2020;e002213. doi: 10.1136/bmjgh-2019-002213.
(9)
Murray CJ, Lauer JA, Hutubessy RC, Niessen L, Tomijima N, Rodgers A, et al. Effectiveness and
costs of interventions to lower systolic blood pressure and cholesterol: a global and regional
analysis on reduction of cardiovascular-disease risk. Lancet. 2003 Mar 1;361(9359):717-25. doi:
10.1016/S0140-6736(03)12655-4. Erratum in: Lancet. 2005 Jul 16-22;366(9481):204. PMID:
12620735.
(10)
Constanti M, Floyd CN, Glover M, Boffa R. Wierzbicki AS, McManus RJ. Cost-effectiveness of
initiating pharmacological treatment in stage one hypertension based on 10-year cardiovascular
disease risk. Hypertension. 2021;77:682-691. doi: 10.1161/HYPERTENSIONAHA.120.14913.
(11)
Moran AE, Odden MC, Thanataveerat A, Tzong KY, Rasmussen PW, Guzman D. Costeffectiveness of hypertension therapy according to 2014 guidelines. NEJM. 2015;372(5):447-55.
doi: 10.1056/NEJMsa1406751.
(12)
Rosendaal TA, Hendriks ME, Verhagen MD, Bolarinwa OA, Sanya EO, Kolo PM, et al.
Correction: costs and cost-effectiveness of hypertension screening and treatment in adults with
hypertension in rural Nigeria in the context of a health insurance program. PLoS ONE. 2016 Jun
27;11(9):e0162421. doi: 10.1371/journal.pone.0162421.
(13)
Rubinstein A, Colantonio L, Bardach A, Caporale J, Martí SG, Kopitowski K, et al. Estimation of
the burden of cardiovascular disease attributable to modifiable risk factors and cost-effectiveness
analysis of preventative interventions to reduce this burden in Argentina. BMC Public Health.
2010;10:627. doi: 10.1186/1471-2458-10-627.
(14)
Richman IB, Fairley M, Jørgensen ME, Schuler A, Owens DK, Goldhaber-Fiebert JD. Costeffectiveness of intensive blood pressure management. JAMA Cardiol. 2016;1(8):872-879. doi:
10.1001/jamacardio.2016.3517.
(15)
Bress AP, Bellows BK, King JB, Hess R, Beddhu S, Zhang Z. Cost-effectiveness of intensive versus
```

---

### Audit Item #6: `who_htn_001_c0096`

- **Source Document:** WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (`who_htn_001`)
- **Source Page(s):** pp. 46-47
- **Condition:** `hypertension` | **Chunk Type:** `monitoring`
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > 10.1016/S0895-7061(00)01266-8. > REFERENCES (Part 2)`
- **Heading:** REFERENCES (Part 2)
- **Population Tags:** []
- **Drug Class Tags:** []
- **Applicability Conditions:** []
- **Exceptions / Contraindications:** []
- **Text Hash:** `09cef8850564ee3817fd821f250379d48a86f964abbfcacbd1fd98312b13c6f5`

```text
Int J Med Inform. 2019;124:78-85. doi: 10.1016/j.ijmedinf.2019.01.013.
(72)
Jaana M, Pare G, Sicotte C. Hypertension home telemonitoring: current evidence and
recommendations for future studies. Dis Manage Health Outcomes. 2007;15(1):19-31. doi:
10.2165/00115677-200715010-00004.
(73)
Greer N, Bolduc J, Geurkink E, Koeller E, Rector T, Olson K, et al. Pharmacist-led chronic disease
management: a systematic review of effectiveness and harms compared with usual care. Ann
Intern Med. 2016;165(1):30-40. doi: 10.7326/M15-3058.
(74)
Anand TN, Joseph LM, Geetha AV, Prabhakaran D, Jeemon P. Task sharing with non-physician
health-care workers for management of blood pressure in low-income and middle-income
countries: a systematic review and meta-analysis. Lancet Glob Health. 2019;7(6):e761-e771. doi:
```

---

### Audit Item #7: `who_htn_001_c0105`

- **Source Document:** WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (`who_htn_001`)
- **Source Page(s):** p. 50
- **Condition:** `hypertension` | **Chunk Type:** `other`
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > ANNEXES > AMRO`
- **Heading:** AMRO
- **Population Tags:** []
- **Drug Class Tags:** []
- **Applicability Conditions:** []
- **Exceptions / Contraindications:** []
- **Text Hash:** `aaa53ad5d9d9ecbc0a9c510d5a74cbee0f497b06e154144d28667024e7987233`

```text
AMRO
Ugyen Choden
Chief Analyst, Department of Financial
Regulation and Supervision, Royal Monetary
Authority, Bhutan
Patient perspective,
drafting guidelines,
policies and
implementing policies
```

---

### Audit Item #8: `who_htn_001_c0115`

- **Source Document:** WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (`who_htn_001`)
- **Source Page(s):** p. 51
- **Condition:** `hypertension` | **Chunk Type:** `other`
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > ANNEXES > EMRO`
- **Heading:** EMRO
- **Population Tags:** []
- **Drug Class Tags:** []
- **Applicability Conditions:** []
- **Exceptions / Contraindications:** []
- **Text Hash:** `cc6e56c09314ab53087239f9ddf28cb9a43224121c327b9b85192b321503d9a2`

```text
EMRO
Vindya
Kumarapeli
Consultant Community Physician, Director
(Non-Communicable Diseases), Ministry of
Health, Sri Lanka
Access to HTN care in
low-resource settings,
public health, policymaking, programme
implementation, primary
health care
```

---

### Audit Item #9: `who_t2dm_001_c0007`

- **Source Document:** WHO HEARTS-D: Diagnosis and Management of Type 2 Diabetes (`who_t2dm_001`)
- **Source Page(s):** p. 13
- **Condition:** `type_2_diabetes` | **Chunk Type:** `other`
- **Section Path:** `WHO HEARTS-D: Diagnosis and Management of Type 2 Diabetes > WHO/UCN/NCD/20.1 > 1	 Clinical manifestations of (Part 2)`
- **Heading:** 1	 Clinical manifestations of (Part 2)
- **Population Tags:** ['type_2_diabetes']
- **Drug Class Tags:** []
- **Applicability Conditions:** ['- -  If plasma glucose >=18 mmol/L (325 mg/dL), or symptoms are present, measure\nurine ketones to assess degree of metabolic disturbance.', '- -  If plasma glucose measurement is not possible, urine glucose testing can be\nused to confirm suspicion of diabetes in people with symptoms.']
- **Exceptions / Contraindications:** []
- **Text Hash:** `f830270f977826a057a15dfa36667fa9aa4ac3c0c90b5fdf3278b853f67cfcf9`

```text
Diagnostic tests
Venous plasma glucose is the standard method for measuring and reporting.
However, in recognition of the widespread use of capillary sampling, especially in
low-resource settings, values for capillary plasma glucose are provided for postload glucose values. Fasting values for venous and capillary plasma glucose are
identical.
Glucose should be measured immediately after collection, otherwise the blood
sample should be collected into a container with glycolytic inhibitors, immediately
centrifuged to separate the plasma, and frozen until analysis.
- -  In asymptomatic people, repeat the test to confirm the diagnosis, preferably with
the same test, as soon as practicable on a subsequent day.
- -  If plasma glucose >=18 mmol/L (325 mg/dL), or symptoms are present, measure
urine ketones to assess degree of metabolic disturbance.
- -  If plasma glucose measurement is not possible, urine glucose testing can be
used to confirm suspicion of diabetes in people with symptoms. A negative urine
test does not exclude diabetes, but it excludes severe hyperglycaemia.
HEARTS - D  Diagnosis and management of Type 2 diabetes
```

---

### Audit Item #10: `nice_htn_001_c0005`

- **Source Document:** NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (`nice_htn_001`)
- **Source Page(s):** p. 5
- **Condition:** `hypertension` | **Chunk Type:** `other`
- **Section Path:** `NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management > 1.5 Identifying who to refer for same-day specialist review .............................................................. 24 > 1.1 Measuring blood pressure`
- **Heading:** 1.1 Measuring blood pressure
- **Population Tags:** []
- **Drug Class Tags:** []
- **Applicability Conditions:** []
- **Exceptions / Contraindications:** []
- **Text Hash:** `b0f40bedd74d694d5216050f4364ed0ca64cb6db189c06fae89052495bc15634`

```text
1.1 Measuring blood pressure
Training, technique and device maintenance
```

---

### Audit Item #11: `nice_htn_001_c0025`

- **Source Document:** NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (`nice_htn_001`)
- **Source Page(s):** p. 9
- **Condition:** `both` | **Chunk Type:** `recommendation`
- **Section Path:** `NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management > 1.2 Diagnosing hypertension > 1.2.12`
- **Heading:** 1.2.12
- **Population Tags:** ['chronic_kidney_disease', 'type_2_diabetes']
- **Drug Class Tags:** []
- **Applicability Conditions:** []
- **Exceptions / Contraindications:** []
- **Text Hash:** `2d6ccba8aba87e1bf89776ded644c75f5210108be91e2b80aa71b2a5c1c70df6`

```text
1.2.12
Measure blood pressure at least annually in an adult with type 2 diabetes without
previously diagnosed hypertension or renal disease. Offer and reinforce
preventive lifestyle advice. [2009]
Specialist investigations for possible secondary causes of
hypertension
```

---

### Audit Item #12: `nice_htn_001_c0030`

- **Source Document:** NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (`nice_htn_001`)
- **Source Page(s):** p. 10
- **Condition:** `both` | **Chunk Type:** `recommendation`
- **Section Path:** `NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management > 1.3 Assessing cardiovascular risk and target organ > 1.3.3`
- **Heading:** 1.3.3
- **Population Tags:** ['type_2_diabetes']
- **Drug Class Tags:** []
- **Applicability Conditions:** []
- **Exceptions / Contraindications:** []
- **Text Hash:** `4b0f4ddb76b7236931b8409f577ab87e0e39b7ed9b4712494e9deec50850d24d`

```text
1.3.3
For all people with hypertension offer to:
-  test for the presence of protein in the urine by sending a urine sample for
estimation of the albumin:creatinine ratio and test for haematuria using a
reagent strip
-  take a blood sample to measure glycated haemoglobin (HbA1C), electrolytes,
creatinine, estimated glomerular filtration rate, total cholesterol and HDL
cholesterol
-  examine the fundi for the presence of hypertensive retinopathy
-  arrange for a 12‐lead electrocardiograph to be performed. [2011, amended
2019]
```

---

### Audit Item #13: `nice_htn_001_c0040`

- **Source Document:** NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (`nice_htn_001`)
- **Source Page(s):** pp. 12-13
- **Condition:** `both` | **Chunk Type:** `other`
- **Section Path:** `NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management > 1.4 Treating and monitoring hypertension > 1.4.10`
- **Heading:** 1.4.10
- **Population Tags:** ['cardiovascular_disease', 'chronic_kidney_disease']
- **Drug Class Tags:** []
- **Applicability Conditions:** ["Use clinical judgement for people with frailty or multimorbidity (see also\nNICE's guideline on multimorbidity)."]
- **Exceptions / Contraindications:** []
- **Text Hash:** `9028c616a336b204f5a66a0a2bcbe2b64b56658dfac006411209a67de267b9a4`

```text
1.4.10
Discuss starting antihypertensive drug treatment, in addition to lifestyle advice,
with adults aged under 80 with persistent stage 1 hypertension who have 1 or
more of the following:
-  target organ damage
-  established cardiovascular disease
-  renal disease
-  diabetes
-  an estimated 10‐year risk of cardiovascular disease of 10% or more.
Use clinical judgement for people with frailty or multimorbidity (see also
NICE's guideline on multimorbidity). [2019]
```

---

### Audit Item #14: `nice_htn_001_c0052`

- **Source Document:** NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (`nice_htn_001`)
- **Source Page(s):** p. 16
- **Condition:** `both` | **Chunk Type:** `other`
- **Section Path:** `NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management > 1.4 Treating and monitoring hypertension > 1.4.20`
- **Heading:** 1.4.20
- **Population Tags:** ['chronic_kidney_disease']
- **Drug Class Tags:** []
- **Applicability Conditions:** ['1.4.20\nFor adults with hypertension aged under 80, reduce clinic blood pressure to\nbelow 140/90 mmHg and ensure that it is maintained below that level.', 'See also\ntable 1 for guidance on clinic blood pressure targets for people aged under 80\nwith type 1 diabetes or severe chronic kidney disease.']
- **Exceptions / Contraindications:** []
- **Text Hash:** `115ccaf8fe1c30fc7282dc9ef9e2e90a7718fe338fa69e0e2b3099dcb1c90257`

```text
1.4.20
For adults with hypertension aged under 80, reduce clinic blood pressure to
below 140/90 mmHg and ensure that it is maintained below that level. See also
table 1 for guidance on clinic blood pressure targets for people aged under 80
with type 1 diabetes or severe chronic kidney disease. [2019, amended 2022]
```

---

### Audit Item #15: `nice_htn_001_c0083`

- **Source Document:** NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (`nice_htn_001`)
- **Source Page(s):** p. 23
- **Condition:** `hypertension` | **Chunk Type:** `other`
- **Section Path:** `NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management > 1.4 Treating and monitoring hypertension > 1.4.50`
- **Heading:** 1.4.50
- **Population Tags:** []
- **Drug Class Tags:** ['thiazide']
- **Applicability Conditions:** ['1.4.50\nWhen using further diuretic therapy for step 4 treatment of resistant\nhypertension, monitor blood sodium and potassium and renal function within\n1 month of starting treatment and repeat as needed thereafter.']
- **Exceptions / Contraindications:** []
- **Text Hash:** `3ea1571f886793897aa022a7831af63cbc552a472cd017dc67b91ef5ac2a717b`

```text
1.4.50
When using further diuretic therapy for step 4 treatment of resistant
hypertension, monitor blood sodium and potassium and renal function within
1 month of starting treatment and repeat as needed thereafter. [2019]
```

---

### Audit Item #16: `nice_t2dm_001_c0126`

- **Source Document:** NICE Guideline NG28: Type 2 Diabetes in Adults - Management (`nice_t2dm_001`)
- **Source Page(s):** p. 77
- **Condition:** `type_2_diabetes` | **Chunk Type:** `other`
- **Section Path:** `NICE Guideline NG28: Type 2 Diabetes in Adults - Management > 1.24 Reviewing other medicines > 1.24.4`
- **Heading:** 1.24.4
- **Population Tags:** []
- **Drug Class Tags:** ['glp1_ra']
- **Applicability Conditions:** ['1.24.4\nStop GLP-1 receptor agonists or tirzepatide if they do not help the person reach\ntheir individualised glycaemic targets and they are not being taken for their\ncardiovascular benefits.']
- **Exceptions / Contraindications:** []
- **Text Hash:** `db2c5be2fee790b5576a9c0322bd49038d0cb08fda2a8ccb8282c5b9d32736cf`

```text
1.24.4
Stop GLP-1 receptor agonists or tirzepatide if they do not help the person reach
their individualised glycaemic targets and they are not being taken for their
cardiovascular benefits. [2026]
```

---

### Audit Item #17: `mohfw_htn_001_c0021`

- **Source Document:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Source Page(s):** p. 14
- **Condition:** `hypertension` | **Chunk Type:** `other`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 3.2  The effective control of blood pressure by initiation of therapy, if required, should not > 3.3  The assessment of a patient with hypertension is aimed at assessing overall`
- **Heading:** 3.3  The assessment of a patient with hypertension is aimed at assessing overall
- **Population Tags:** ['cardiovascular_disease']
- **Drug Class Tags:** []
- **Applicability Conditions:** []
- **Exceptions / Contraindications:** []
- **Text Hash:** `c6219a38304540f10fd6dc4c1e6318f25b49a428b396847f96a9093b045d0092`

```text
3.3  The assessment of a patient with hypertension is aimed at assessing overall
cardiovascular risk for cardiovascular events like stroke, ischemic heart disease, heart
failure, peripheral artery disease.
```

---

### Audit Item #18: `mohfw_htn_001_c0062`

- **Source Document:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Source Page(s):** p. 22
- **Condition:** `both` | **Chunk Type:** `recommendation`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 4.6 The treatment regimen and the use of combinations: > 4.8 Therapy of hypertension and associated conditions: > 4.8.1 Diabetes mellitus: > 4.8.1.1 Patients with diabetes mellitus should be initiated on drug treatment`
- **Heading:** 4.8 Therapy of hypertension and associated conditions: > 4.8.1 Diabetes mellitus: > 4.8.1.1 Patients with diabetes mellitus should be initiated on drug treatment
- **Population Tags:** ['type_2_diabetes']
- **Drug Class Tags:** []
- **Applicability Conditions:** []
- **Exceptions / Contraindications:** []
- **Text Hash:** `6de76241eb9f74c94f7666ddf04126be07e0e05a3263c2d199338299af2b238b`

```text
4.8 Therapy of hypertension and associated conditions:
4.8.1 Diabetes mellitus:
4.8.1.1 Patients with diabetes mellitus should be initiated on drug treatment
when the SBP is greater than 140 mm Hg, and the target for control should
be a SBP of less than 140 mm Hg, and a diastolic BP of less than 90 mm Hg.
```

---

### Audit Item #19: `mohfw_htn_001_c0078`

- **Source Document:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Source Page(s):** p. 24
- **Condition:** `hypertension` | **Chunk Type:** `recommendation`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 4.8 Hypertension in the elderly: > 4.9.2 In a patient with postural hypotension titrate target according to standing BP.`
- **Heading:** 4.9.2 In a patient with postural hypotension titrate target according to standing BP.
- **Population Tags:** []
- **Drug Class Tags:** []
- **Applicability Conditions:** []
- **Exceptions / Contraindications:** []
- **Text Hash:** `2860710f1d1191db99a29c046ac7a6edddf8ca426ec76795641c8bec80d3d9ae`

```text
4.9.2 In a patient with postural hypotension titrate target according to standing BP.
```

---

### Audit Item #20: `mohfw_htn_001_c0108`

- **Source Document:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Source Page(s):** p. 28
- **Condition:** `hypertension` | **Chunk Type:** `other`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > THERAPY > 5.3.2. The common side effects of diuretics are metabolic side effects like`
- **Heading:** 5.3.2. The common side effects of diuretics are metabolic side effects like
- **Population Tags:** ['elderly', 'type_2_diabetes']
- **Drug Class Tags:** ['ace_inhibitor', 'thiazide']
- **Applicability Conditions:** ['The common side effects of diuretics are metabolic side effects like\nhypokalemia, hyperglycemia but which are less frequent when these\nare used in doses of 12.5 mg and when they are combined with ACE\ninhibitors..']
- **Exceptions / Contraindications:** []
- **Text Hash:** `c355825f146117a7c45d88193df0a46cdfa6c49c727e159b56c4688c6c70fc59`

```text
5.3.2. The common side effects of diuretics are metabolic side effects like
hypokalemia, hyperglycemia but which are less frequent when these
are used in doses of 12.5 mg and when they are combined with ACE
inhibitors.. A particular concern is of thiazide induced hyponatremia
which is commoner in the elderly, those with a low body weight. This
can develop rapidly and manifest as altered consciousness, and even
seizures, and may require hospitalisation and administration of
normal or hypertonic saline.
```

---

### Audit Item #21: `mohfw_htn_001_c0120`

- **Source Document:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Source Page(s):** pp. 35-36
- **Condition:** `hypertension` | **Chunk Type:** `other`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > DEVELOPMENT OF GUIDELINE > WHO/ISH > ESC/ESH`
- **Heading:** WHO/ISH > ESC/ESH
- **Population Tags:** []
- **Drug Class Tags:** []
- **Applicability Conditions:** ['Original\nrecommendation."\nIf\nblood\npressure\nmeasured in the clinic is\n140/90\nmmHg\nor\nhigher: Take a second\nmeasurement\nduring\nthe consultation.', 'If the\nsecond measurement is\nsubstantially\ndifferent\nfrom the first, take a\nthird\nmeasurement.']
- **Exceptions / Contraindications:** ['Record the lower of the\nlast two measurements\nas\nthe\nclinic\nblood\npressure."\nIn the Indian setting,\nwith the proposed BP\nmeasurement by nonphysician\nhealth\nworkers ,  taking the\nlower instead of the\naverage reading is more\nfeasible and will avoid\ncalculation errors.']
- **Text Hash:** `7c0bd3071ec1b99070c38f0d700f0daa0952eded4967f405c1b37b4c3bbabe3b`

```text
WHO/ISH
guideline
and
the
ESC/ESH
Guideline,
instead of the term
"pre-hypertension"
used in JNC 7
Diagnostic
standard
for
hypertension
ESC/ESH guidelines
Adapted. Reworded.
It is based on clinic
based
measurement
using a standardised BP
measurement
procedure.
Recording the measured BP :
average
measurement
vs.
lower measurement
NICE guidelines 2011
Adapted.
Original
recommendation."
If
blood
pressure
measured in the clinic is
140/90
mmHg
or
higher: Take a second
measurement
during
the consultation. If the
second measurement is
substantially
different
from the first, take a
third
measurement.
Record the lower of the
last two measurements
as
the
clinic
blood
pressure."
In the Indian setting,
with the proposed BP
measurement by nonphysician
health
workers ,  taking the
lower instead of the
average reading is more
feasible and will avoid
calculation errors.
Classification of hypertension
ESC/ESH 2013 guideline.
WHO/ISH guideline 2003
Adopted.
We retained the Grade
3 hypertension category
(SBP >180 mm Hg &/or
DBP >110 mm Hg). This
category is mentioned
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document
in
the
```

---

### Audit Item #22: `mohfw_htn_001_c0158`

- **Source Document:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Source Page(s):** p. 61
- **Condition:** `hypertension` | **Chunk Type:** `monitoring`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 3.1 Patients should be counselled about the nature of the disease, and the management > 3.1.1 Patients should be counselled about hypertension being an asymptomatic`
- **Heading:** 3.1.1 Patients should be counselled about hypertension being an asymptomatic
- **Population Tags:** ['cardiovascular_disease', 'chronic_kidney_disease']
- **Drug Class Tags:** []
- **Applicability Conditions:** []
- **Exceptions / Contraindications:** []
- **Text Hash:** `f2a505cbe4f18f5e4e31e4fe63def953d1674ace66b0370144e2fb70a51c110c`

```text
3.1.1 Patients should be counselled about hypertension being an asymptomatic
condition which can lead to disabling and life-threatening complications like
stroke, heart attack and renal failure. Patient should be counselled about need
for long-term therapy, need for regularity of drug intake, informed about the
targets for BP control, and encouraged to monitor efficacy of therapy through
regular check-ups which can include home based monitoring of BP.
```

---

### Audit Item #23: `mohfw_htn_001_c0169`

- **Source Document:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Source Page(s):** pp. 63-64
- **Condition:** `both` | **Chunk Type:** `monitoring`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 3.6 The level of BP and results of the assessment will influence the following: > 3.8  All patients should be asked about tobacco use and advised to stop it.`
- **Heading:** 3.8  All patients should be asked about tobacco use and advised to stop it.
- **Population Tags:** ['cardiovascular_disease']
- **Drug Class Tags:** ['antiplatelet', 'statin']
- **Applicability Conditions:** ['The patient is more likely to adhere to\nmedications, lifestyle modifications if he/she understands the nature of the condition\nand its management.']
- **Exceptions / Contraindications:** []
- **Text Hash:** `707152a5ae84b61e755ff17db99289d3ece8a34a6b6ebd0f1b27d312e2fb29f0`

```text
3.8  All patients should be asked about tobacco use and advised to stop it.
Key recommendations:
Background:
Hypertension is most often asymptomatic and the benefits of treatment are not
immediately apparent to a patient. The therapy of hypertension involves costs (indirect
as well as direct), and occasional experience of adverse effects, and is often lifelong
which may create barriers to adherence to therapy. Improving adherence to long-term
treatment is a key part of management. The patient is more likely to adhere to
medications, lifestyle modifications if he/she understands the nature of the condition
and its management.
The assessment of cardiovascular risk factors, target organ damage due to hypertension,
associated clinical conditions all help in assessment of cardiovascular risk and guide
therapy of hypertension. These can be assessed by a relevant history, examination and
appropriate investigations, many of which can be evaluated even by non-physician staff.
It may also indicate the need for other therapies like low-dose aspirin and statin to
reduce cardiovascular risk. Decisions on initiation of therapy, choice of medications, BP
targets for control are dependent on these factors as much as the severity of
hypertension. Grade 1 hypertension may be managed with lifestyle modifications alone
in the absence of other risk factors.

Implementation of patient education and assessment
Patient education related to hypertension is a part of the initial care and should be
reinforced during the continuing care of patients with hypertension, e.g. during annual
reviews. It can be delivered by both physician and non-physician staff and can be
supported by aids like patient information leaflets (attached). Non-physician staff at the
community level can reinforce messages related to healthy living, monitoring of BP and
adhering to treatment.
Patient education: Patient education will facilitate the patient's participation and
cooperation in the management of a life-long disease. They should understand the
following features of the disease and its management:
-  The disease is asymptomatic but is a risk factor for serious consequences like
heart attacks, strokes, heart and kidney failure, which can be prevented by
controlling hypertension to a target BP which is usually less than 140 mm systolic
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document
and 90 mm diastolic. The disease is persistent and although it cannot be cured it
can be controlled.
-  Healthy living habits (lifestyle modification) like stopping smoking, eating a
healthy diet lower in salt and saturated fat, exercising losing weight has many
benefits with no cost. It can reduce blood pressure, may suffice for the
management of grade 1 hypertension, reduce the dosage of medicines required
for control of grade 2 and 3 hypertension, and help reduce the overall risk of
heart attacks and stroke.
-  The assessment of damage to the heart, kidney, vessels in the eye, and to detect
the presence of associated conditions like diabetes are needed to determine the
```

---

### Audit Item #24: `mohfw_htn_001_c0196`

- **Source Document:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Source Page(s):** p. 78
- **Condition:** `both` | **Chunk Type:** `other`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 4.5 Key recommendation: Classes of antihypertensive drugs & preferred choices > 4.5.5.              The presence of associated clinical conditions (diabetes, clinical`
- **Heading:** 4.5.5.              The presence of associated clinical conditions (diabetes, clinical
- **Population Tags:** ['cardiovascular_disease', 'chronic_kidney_disease']
- **Drug Class Tags:** []
- **Applicability Conditions:** []
- **Exceptions / Contraindications:** []
- **Text Hash:** `4976943c4274bb093cc85bf472495693887a937696ee0cf5ec89c5d436edb9e3`

```text
4.5.5.              The presence of associated clinical conditions (diabetes, clinical
cardiovascular disease, chronic kidney disease) in a patient may provide
compelling indication for the use of specific classes of drugs.
```

---

### Audit Item #25: `mohfw_htn_001_c0222`

- **Source Document:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Source Page(s):** p. 93
- **Condition:** `both` | **Chunk Type:** `other`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 4.5 Key recommendation: Classes of antihypertensive drugs & preferred choices > 4.8.1.2 ACE inhibitors are preferred as initial therapy and calcium channel blockers`
- **Heading:** 4.8.1.2 ACE inhibitors are preferred as initial therapy and calcium channel blockers
- **Population Tags:** []
- **Drug Class Tags:** ['ace_inhibitor', 'ccb', 'thiazide']
- **Applicability Conditions:** []
- **Exceptions / Contraindications:** []
- **Text Hash:** `845fb0df59c4f326e6715a2185ae1c00c17545134efe46ae76eb310a5a873344`

```text
4.8.1.2 ACE inhibitors are preferred as initial therapy and calcium channel blockers
and diuretics may be used as add on therapy. Thiazide diuretics can be
associated with glucose intolerance.
```

---

### Audit Item #26: `mohfw_htn_001_c0237`

- **Source Document:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Source Page(s):** pp. 95-96
- **Condition:** `both` | **Chunk Type:** `rationale`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 4.5 Key recommendation: Classes of antihypertensive drugs & preferred choices > CHC.`
- **Heading:** CHC.
- **Population Tags:** ['cardiovascular_disease']
- **Drug Class Tags:** []
- **Applicability Conditions:** []
- **Exceptions / Contraindications:** []
- **Text Hash:** `489bf78988d890ab354e077de4bbbce938f63f83202bec30f65ac4e7b69e7566`

```text
CHC.
Rationale:
The issue of treatment of associated conditions is addressed by guidelines like ESC/ESH, JNC
8 and CHEP, though not specifically by NICE. There is broad consensus between these
guidelines on the choice of drugs for the treatment of hypertension in the presence of
associated conditions.
Diabetes:However there is some variation in the targets for BP control across guidelines.
CHEP guidelines for example recommend lower systolic and diastolic BP targets for patients
with diabetes (systolic BP < 130 mm Hg and diastolic BP < 80 mm Hg),(19) while the European
guidelines recommend a diastolic BP target of less than 85 mm Hg while recommending the
same systolic BP target of 140 mm Hg. The JNC 8 guideline specifically reviewed the
evidence from randomised controlled trials in favour of lower targets for systolic and
diastolic BP in diabetics and concluded that there was insufficient evidence supporting
them, and suggested similar targets as for the general population.(20) We decided to adopt
the JNC 8 recommendation in light of the evidence presented in them and the conclusions
of a recent Cochrane review which were similar to the JNC 8 recommendations.(61) Also a
similar target for BP control in diabetics as well as the general population would favour
guideline implementation.
Cerebrovascular diseases: The recommendations regarding antihypertensive treatment in
patients with ischemic stroke has been adopted from the CHEP guidelines,(19)the ESC/ESH
guidelines and the Seventh Report of the JNC. The recommendations related to blood
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document
pressure management in patients with spontaneous intracerebral haemorrhage has been
adapted from a recent guideline from the American Heart Association/American Stroke
Association.(74)  Recent studies have demonstrated the lack of an ischemic penumbra in
hemorrhagic strokes, and the reduction of BP in the acute phase of stroke can be safely
undertaken.
```

---

### Audit Item #27: `mohfw_htn_001_c0258`

- **Source Document:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Source Page(s):** p. 98
- **Condition:** `hypertension` | **Chunk Type:** `rationale`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 4.11 Hypertensive urgencies: > 4.11.6 Re-institution of therapy or intensification of therapy by increasing the dose of drugs`
- **Heading:** 4.11.6 Re-institution of therapy or intensification of therapy by increasing the dose of drugs
- **Population Tags:** []
- **Drug Class Tags:** ['thiazide']
- **Applicability Conditions:** []
- **Exceptions / Contraindications:** []
- **Text Hash:** `e15d8cf4356154f97728e3e04e2ef0afda8880623d3292a556ace7faa40b31a5`

```text
4.11.6 Re-institution of therapy or intensification of therapy by increasing the dose of drugs
or adding a diuretic may suffice for gradual reduction of blood pressure in a patient
who has developed severe asymptomatic hypertension on the background of chronic
hypertension.
```

---

### Audit Item #28: `mohfw_htn_001_c0262`

- **Source Document:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Source Page(s):** p. 100
- **Condition:** `hypertension` | **Chunk Type:** `recommendation`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 4.12  Integration with other interventions to reduce cardiovascular risks > 4.12.1 The treatment of hypertension should be integrated with treatment of`
- **Heading:** 4.12.1 The treatment of hypertension should be integrated with treatment of
- **Population Tags:** []
- **Drug Class Tags:** ['antiplatelet']
- **Applicability Conditions:** []
- **Exceptions / Contraindications:** []
- **Text Hash:** `38f48f0e58c55f9e5338c2c0fe77ce3bece7a0283b033c069be2aef3a5d457f9`

```text
4.12.1 The treatment of hypertension should be integrated with treatment of
associated risk factors like lipid lowering therapy and antiplatelet therapy, apart
from lifestyle interventions already mentioned.
```

---

### Audit Item #29: `mohfw_htn_001_c0263`

- **Source Document:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Source Page(s):** p. 100
- **Condition:** `hypertension` | **Chunk Type:** `other`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 4.12  Integration with other interventions to reduce cardiovascular risks > 4.12.2   Antiplatelet therapy with low-dose aspirin (75 mg/day) is recommended in`
- **Heading:** 4.12.2   Antiplatelet therapy with low-dose aspirin (75 mg/day) is recommended in
- **Population Tags:** ['cardiovascular_disease']
- **Drug Class Tags:** ['antiplatelet']
- **Applicability Conditions:** []
- **Exceptions / Contraindications:** []
- **Text Hash:** `78db9a6ee22e777d30f891c3087a5c3d63d3002fc8cebf014ac107e32f56461a`

```text
4.12.2   Antiplatelet therapy with low-dose aspirin (75 mg/day) is recommended in
patients with controlled hypertension who have previous history of
cardiovascular event (previous MI, stroke, angina, bypass surgery or coronary
angioplasty), because of a favourable benefit -harm ratio.
```

---

### Audit Item #30: `mohfw_htn_002_c0106`

- **Source Document:** MoHFW Standard Treatment Guidelines - Hypertension (Quick Reference Guide) (`mohfw_htn_002`)
- **Source Page(s):** p. 28
- **Condition:** `hypertension` | **Chunk Type:** `recommendation`
- **Section Path:** `MoHFW Standard Treatment Guidelines - Hypertension (Quick Reference Guide) > 4.11 Integration with other interventions to reduce cardiovascular risks > 4.11.4 Negative recommendation: Do not use low-dose aspirin in hypertensive patients`
- **Heading:** 4.11.4 Negative recommendation: Do not use low-dose aspirin in hypertensive patients
- **Population Tags:** ['cardiovascular_disease']
- **Drug Class Tags:** ['antiplatelet']
- **Applicability Conditions:** []
- **Exceptions / Contraindications:** []
- **Text Hash:** `4ececbfa7ca9e4b306a2830c3b4903533707cbec07991203512ed5f603de8a78`

```text
4.11.4 Negative recommendation: Do not use low-dose aspirin in hypertensive patients
without cardiovascular disease and who are at low-moderate risk as the risk of
major bleeds (intracranial and gastrointestinal) outweighs the potential benefit.
```

---
