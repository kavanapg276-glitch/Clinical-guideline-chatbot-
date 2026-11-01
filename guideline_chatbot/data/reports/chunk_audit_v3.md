# Clinical Guideline Chunk Audit Report (v3)

**Generated:** 2026-11-01  
**Milestone:** Stage A Complete Remediation Audit  
**Scope:** 10 Specific Audit Focus Chunks + 25 Stratified Recommendation Chunks (MoHFW, ICMR, WHO, NICE)  
**Format:** Plain Markdown, Full Metadata, Exact Chunk Text, and FULL Uncompressed Source Page Text (No `<details>` collapsing)  

---

## Summary of Ten Audit Focus Chunks

| # | Chunk ID | Issuer & Doc | Classification | Indexed | Audit Focus & Resolution |
|---|---|---|---|---|---|
| 1 | `nice_htn_001_c0046` | NICE NG136 | `recommendation` | True | Rec 1.4.20: T1DM/CKD cross-reference stripped from population tags; captured in `cross_references`. |
| 2 | `nice_htn_001_c0056` | NICE NG136 | `recommendation` | True | Rec 1.4.31: T1DM cross-reference stripped from population tags; tagged CVD. |
| 3 | `nice_htn_001_c0052` | NICE NG136 | `recommendation` | True | Rec 1.4.26: Beta-blocker indication in isolated systolic hypertension. |
| 4 | `who_htn_001_c0069` | WHO HTN 2021 | `methods` | False | Implementation tools & clinical questions reclassified as methods; excluded from retrieval. |
| 5 | `who_htn_001_c0071` | WHO HTN 2021 | `methods` | False | PICO narrative question reclassified as methods; excluded from retrieval. |
| 6 | `who_htn_001_c0120` | WHO HTN 2021 | `methods` | False | Evidence summary / PICO narrative reclassified as methods; excluded from retrieval. |
| 7 | `who_htn_001_c0029` | WHO HTN 2021 | `methods` | False | PICO narrative & search strategy reclassified as methods; excluded from retrieval. |
| 8 | `mohfw_htn_001_c0121` | MoHFW STG | `table` | True | Antihypertensive drug therapy table extracted cleanly with row structure. |
| 9 | `nice_t2dm_001_c0080` | NICE NG28 | `contributors` | False | Committee member and contributor list reclassified; excluded from retrieval. |
| 10 | `nice_t2dm_001_c0101` | NICE NG28 | `rationale` | True | Committee rationale decoupled from normative recommendation. |

---

## Section 1: Ten Specific Focus Chunks

### Focus Chunk #1: `nice_htn_001_c0046`

- **Document Name:** NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (`nice_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 16–16
- **Heading:** 1.4.20
- **Section Path:** `NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management > 1.4 Treating and monitoring hypertension > 1.4.20`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `["See also\ntable 1 for guidance on clinic blood pressure targets for people aged under 80\nwith type 1 diabetes or severe chronic kidney disease."]`
- **Recommendation Year:** `2022`
- **Last Updated:** `2026-02-26`

#### Exact Chunk Text

```text
1.4.20
For adults with hypertension aged under 80, reduce clinic blood pressure to
below 140/90 mmHg and ensure that it is maintained below that level. See also
table 1 for guidance on clinic blood pressure targets for people aged under 80
with type 1 diabetes or severe chronic kidney disease. [2019, amended 2022]
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: nice_htn_001 | PAGE 16] ===
• training and advice on using home blood pressure monitors 
• information about what to do if they are not achieving their target blood 
pressure. 
Be aware that the corresponding measurements for HBPM are 5 mmHg lower 
than for clinic measurements (see recommendation 1.2.8 for diagnostic 
thresholds). [2019] 
1.4.20 
For adults with hypertension aged under 80, reduce clinic blood pressure to 
below 140/90 mmHg and ensure that it is maintained below that level. See also 
table 1 for guidance on clinic blood pressure targets for people aged under 80 
with type 1 diabetes or severe chronic kidney disease. [2019, amended 2022] 
1.4.21 
For adults with hypertension aged 80 and over, reduce clinic blood pressure to 
below 150/90 mmHg and ensure that it is maintained below that level. Use clinical 
judgement for people with frailty or multimorbidity (see NICE's guideline on 
multimorbidity). See also table 2 for guidance on clinic blood pressure targets for 
people aged 80 and over with type 1 diabetes or severe chronic kidney disease. 
[2019, amended 2022] 
1.4.22 
When using ABPM or HBPM to monitor the response to treatment in adults with 
hypertension, use the average blood pressure level taken during the person's 
usual waking hours (see recommendations 1.2.6 and 1.2.7). Reduce blood 
pressure and ensure that it is maintained: 
• below 135/85 mmHg for adults aged under 80 
• below 145/85 mmHg for adults aged 80 and over. 
Use clinical judgement for people with frailty or multimorbidity (see also 
NICE's guideline on multimorbidity). [2019, amended 2022] 
Hypertension in adults: diagnosis and management (NG136)
© NICE 2026. All rights reserved. Subject to Notice of rights (https://www.nice.org.uk/terms-and-
conditions#notice-of-rights).
Page 16 of
52
```

---

### Focus Chunk #2: `nice_htn_001_c0056`

- **Document Name:** NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (`nice_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 19–19
- **Heading:** 1.4.31
- **Section Path:** `NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management > 1.4 Treating and monitoring hypertension > 1.4.31`
- **Population Tags:** `["cardiovascular_disease"]`
- **Drug Class Tags:** `["ace_inhibitor", "arb"]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `["- blood pressure management in NICE's guideline on type 1 diabetes in\nadults.", "For a short explanation of why the committee made the recommendation on choosing\nantihypertensive drug treatment for people with cardiovascular disease and how this\nmight affect practice, see the rationale and impact section on choosing\nantihypertensive drug treatment for people with cardiovascular disease.", "Full details of the evidence and the committee's discussion are in the evidence review\nK: pharmacological treatment in cardiovascular disease."]`
- **Recommendation Year:** `2022`
- **Last Updated:** `2026-02-26`

#### Exact Chunk Text

```text
1.4.31
For people with cardiovascular disease:
-  Follow the recommendations for disease-specific indications in the NICE
guideline on their condition (for example, when prescribing an ACE inhibitor
or an ARB for secondary prevention of myocardial infarction). Relevant
recommendations include:
- drug therapy for secondary prevention in NICE's guideline on acute
coronary syndromes
- treatment after stabilisation in NICE's guideline on acute heart failure
- treating heart failure with reduced ejection fraction in NICE's guideline on
chronic heart failure
- drugs for secondary prevention of cardiovascular disease in NICE's
guideline on stable angina
- blood pressure management in NICE's guideline on type 1 diabetes in
adults.
-  If their blood pressure remains uncontrolled, offer antihypertensive drug
treatment in line with the recommendations in this section. [2022]
For a short explanation of why the committee made the recommendation on choosing
antihypertensive drug treatment for people with cardiovascular disease and how this
might affect practice, see the rationale and impact section on choosing
antihypertensive drug treatment for people with cardiovascular disease.
Full details of the evidence and the committee's discussion are in the evidence review
K: pharmacological treatment in cardiovascular disease.
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: nice_htn_001 | PAGE 19] ===
antagonists: not for use in pregnancy, how to use for breastfeeding and 
clarification on breastfeeding. 
1.4.31 
For people with cardiovascular disease: 
• Follow the recommendations for disease-specific indications in the NICE 
guideline on their condition (for example, when prescribing an ACE inhibitor 
or an ARB for secondary prevention of myocardial infarction). Relevant 
recommendations include: 
－ drug therapy for secondary prevention in NICE's guideline on acute 
coronary syndromes 
－ treatment after stabilisation in NICE's guideline on acute heart failure 
－ treating heart failure with reduced ejection fraction in NICE's guideline on 
chronic heart failure 
－ drugs for secondary prevention of cardiovascular disease in NICE's 
guideline on stable angina 
－ blood pressure management in NICE's guideline on type 1 diabetes in 
adults. 
• If their blood pressure remains uncontrolled, offer antihypertensive drug 
treatment in line with the recommendations in this section. [2022] 
For a short explanation of why the committee made the recommendation on choosing 
antihypertensive drug treatment for people with cardiovascular disease and how this 
might affect practice, see the rationale and impact section on choosing 
antihypertensive drug treatment for people with cardiovascular disease. 
Full details of the evidence and the committee's discussion are in the evidence review 
K: pharmacological treatment in cardiovascular disease. 
Step 1 treatment 
1.4.32 
Offer an ACE inhibitor or an ARB to adults starting step 1 antihypertensive 
Hypertension in adults: diagnosis and management (NG136)
© NICE 2026. All rights reserved. Subject to Notice of rights (https://www.nice.org.uk/terms-and-
conditions#notice-of-rights).
Page 19 of
52
```

---

### Focus Chunk #3: `nice_htn_001_c0052`

- **Document Name:** NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (`nice_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 18–18
- **Heading:** 1.4.26
- **Section Path:** `NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management > 1.4 Treating and monitoring hypertension > 1.4.26`
- **Population Tags:** `["chronic_kidney_disease"]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `["If possible, offer\ntreatment with drugs taken only once a day."]`
- **Exceptions:** `null`
- **Cross References:** `["see NICE's guideline on chronic kidney disease."]`
- **Recommendation Year:** `2004`
- **Last Updated:** `2026-02-26`

#### Exact Chunk Text

```text
1.4.26
For guidance on choice of antihypertensive medicine in people with chronic
kidney disease, see NICE's guideline on chronic kidney disease. If possible, offer
treatment with drugs taken only once a day. [2004]
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: nice_htn_001 | PAGE 18] ===
type 2 diabetes. They replace the recommendations on diagnosing and managing 
hypertension in NICE's guideline on type 2 diabetes in adults. For guidance on choosing 
antihypertensive drug treatment in people with type 1 diabetes, see also the section on 
control of cardiovascular risk in NICE's guideline on type 1 diabetes. 
Note that ACE inhibitors and angiotensin II receptor antagonists should not be used in 
pregnant or breastfeeding women or women planning pregnancy unless absolutely 
necessary, in which case the potential risks and benefits should be discussed. Follow 
the MHRA safety advice on ACE inhibitors and angiotensin II receptor antagonists: not 
for use in pregnancy, recommendations on how to use for breastfeeding and the 
related clarification on breastfeeding. 
1.4.26 
For guidance on choice of antihypertensive medicine in people with chronic 
kidney disease, see NICE's guideline on chronic kidney disease. If possible, offer 
treatment with drugs taken only once a day. [2004] 
1.4.27 
Prescribe non-proprietary drugs if these are appropriate and minimise cost. 
[2004] 
1.4.28 
Offer people with isolated systolic hypertension (systolic blood pressure 
160 mmHg or more) the same treatment as people with both raised systolic and 
diastolic blood pressure. [2004] 
1.4.29 
Offer antihypertensive drug treatment to women of childbearing potential with 
diagnosed hypertension in line with the recommendations in this guideline. For 
women considering pregnancy or who are pregnant or breastfeeding, manage 
hypertension in line with the recommendations on management of pregnancy 
with chronic hypertension, and on antihypertensive treatment while 
breastfeeding in NICE's guideline on hypertension in pregnancy. [2010, amended 
2019] 
1.4.30 
When choosing antihypertensive drug treatment for adults of Black African or 
African–Caribbean family origin, consider an angiotensin II receptor blocker 
(ARB), in preference to an angiotensin-converting enzyme (ACE) inhibitor. [2019] 
Follow the MHRA safety advice on ACE inhibitors and angiotensin II receptor 
Hypertension in adults: diagnosis and management (NG136)
© NICE 2026. All rights reserved. Subject to Notice of rights (https://www.nice.org.uk/terms-and-
conditions#notice-of-rights).
Page 18 of
52
```

---

### Focus Chunk #4: `who_htn_001_c0069`

- **Document Name:** WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (`who_htn_001`)
- **Chunk Type:** `methods`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `False`
- **Page Range:** 36–36
- **Heading:** 5.3	 Evaluation
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > 5.2	 Implementation and dissemination > 5.3	 Evaluation`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
5.3	 Evaluation
WHO will monitor uptake and implementation of the guideline in national policies and programmes by
reviewing the number of countries that have adapted or endorsed the guideline nationally.
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: who_htn_001 | PAGE 36] ===
GUIDELINE FOR THE PHARMACOLOGICAL TREATMENT OF HYPERTENSION IN ADULTS
5	 Publication, implementation, 
evaluation and research gaps
5.1	 Publication 
This guideline is available to download from the WHO website. Given that an overview of published 
systematic reviews was used for the development of the guideline, all reviews are already published and 
available online. 
5.2	 Implementation and dissemination 
WHO regional and country offices, through their contacts with ministries of health, will encourage 
implementation at country level. WHO will provide technical assistance if substantial country adaptation 
is required. The HEARTS technical package, which is currently being implemented in 18 countries 
and has significant partner endorsement, membership and engagement, will be the platform used to 
implement and disseminate this guideline. The package will be revised to include the implementation 
tools from this guideline. Separate implementation aspects are being considered as implementation or 
derivative tools for nonphysician treatment and the treatment of hypertension in areas of humanitarian 
crises, following publication of the guideline. Implementation support will be extended to countries 
through all three levels of WHO.
5.3	 Evaluation 
WHO will monitor uptake and implementation of the guideline in national policies and programmes by 
reviewing the number of countries that have adapted or endorsed the guideline nationally. 
5.4	 Future updating of the guideline 
The guideline is expected to be valid for a period of five years. This period reflects the fact that new 
research findings are likely to become available in the meantime but also represents a feasible time 
frame, considering the costs, time and other resources that are needed for the updating process. If the 
evidence base or user needs change before the five-year mark, consideration will be given to producing 
updates sooner.
5.5	 Research gaps
Several research gaps were identified by the GDG according to the theme of the PICOs. 
Thresholds to determine initiation of therapy and targets to achieve for control
[
[ More evidence is required regarding treatment of those in the SBP 130–139 range who fall into 
one or more of the following subgroups: diabetes, chronic kidney disease, heart failure, 65 years 
or older.
[
[ There is a need for better outcomes data from, for example, trials that include heart failure and 
cognitive impairment among outcomes.
[
[ Clinical significance of adverse events registered in clinical trials needs greater clarity. 
[
[ There is a need to quantify the difference in estimates between blinded, placebo-controlled trials 
and unblinded, active control trials using a standard framework.
24
```

---

### Focus Chunk #5: `who_htn_001_c0071`

- **Document Name:** WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (`who_htn_001`)
- **Chunk Type:** `methods`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `False`
- **Page Range:** 36–37
- **Heading:** 5.5	 Research gaps
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > 5.4	 Future updating of the guideline > 5.5	 Research gaps`
- **Population Tags:** `["cardiovascular_disease", "chronic_kidney_disease"]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
5.5	 Research gaps
Several research gaps were identified by the GDG according to the theme of the PICOs.
Thresholds to determine initiation of therapy and targets to achieve for control
[
[ More evidence is required regarding treatment of those in the SBP 130-139 range who fall into
one or more of the following subgroups: diabetes, chronic kidney disease, heart failure, 65 years
or older.
[
[ There is a need for better outcomes data from, for example, trials that include heart failure and
cognitive impairment among outcomes.
[
[ Clinical significance of adverse events registered in clinical trials needs greater clarity.
[
[ There is a need to quantify the difference in estimates between blinded, placebo-controlled trials
and unblinded, active control trials using a standard framework.
[
[ There is a need for periodic analysis of trials in order to capture effects of changes over time in
background epidemiology of CVD, non-BP treatments, competing risks, etc.
[
[ More evidence is needed in LICs, MICs and other non-North American/European countries.
[
[ An assessment of the feasibility, resource needs, and costs of intensive treatment in real clinical
practice is needed. The resource commitment required for more intensive treatment in LMICs
needs to be quantified.
[
[ The opportunity cost of directing resources towards achieving SBP <130 in high-risk individuals
needs to be established.
[
[ Research is needed on the feasibility, acceptability, and efficacy of intensive treatment, especially
in high-risk populations in LICs and MICs.
Laboratory tests to determine initiation of treatment
[
[ A greater understanding of the essential tests to be performed in all patients to reduce costs and
improve outcomes is required.
Role of cardiovascular risk in hypertension treatment
[
[ An exploration is needed of key operational aspects of the implementation of a risk-based
approach to CVD prevention and BP-lowering pharmacological treatment in primary health care
settings.
Monotherapy versus combination therapy
[
[ A comparison is required of long-term data about hard clinical endpoints between monotherapy
and combination therapy.
[
[ There is a need for research studies on real-world experiences, designed and statistically powered,
to determine if there is a difference in clinical outcomes, such as reduction in MACE, mortality,
and serious adverse events, between single-pill combinations vs multiple-pill combinations.
[
[ Health economic analyses are needed to quantify cost-effectiveness and budget implications of
implementing incremental initial combination therapy compared with initial monotherapy.
Frequency of re-assessment
[
[ Criteria establishing the clinical definition of stable BP control will be needed to guide the
selection of patients for less frequent follow-up visits.
[
[ Research is needed for early and accurate identification of patients less likely to achieve BP control
and less likely to follow up as requested by their health care provider.
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: who_htn_001 | PAGE 36] ===
GUIDELINE FOR THE PHARMACOLOGICAL TREATMENT OF HYPERTENSION IN ADULTS
5	 Publication, implementation, 
evaluation and research gaps
5.1	 Publication 
This guideline is available to download from the WHO website. Given that an overview of published 
systematic reviews was used for the development of the guideline, all reviews are already published and 
available online. 
5.2	 Implementation and dissemination 
WHO regional and country offices, through their contacts with ministries of health, will encourage 
implementation at country level. WHO will provide technical assistance if substantial country adaptation 
is required. The HEARTS technical package, which is currently being implemented in 18 countries 
and has significant partner endorsement, membership and engagement, will be the platform used to 
implement and disseminate this guideline. The package will be revised to include the implementation 
tools from this guideline. Separate implementation aspects are being considered as implementation or 
derivative tools for nonphysician treatment and the treatment of hypertension in areas of humanitarian 
crises, following publication of the guideline. Implementation support will be extended to countries 
through all three levels of WHO.
5.3	 Evaluation 
WHO will monitor uptake and implementation of the guideline in national policies and programmes by 
reviewing the number of countries that have adapted or endorsed the guideline nationally. 
5.4	 Future updating of the guideline 
The guideline is expected to be valid for a period of five years. This period reflects the fact that new 
research findings are likely to become available in the meantime but also represents a feasible time 
frame, considering the costs, time and other resources that are needed for the updating process. If the 
evidence base or user needs change before the five-year mark, consideration will be given to producing 
updates sooner.
5.5	 Research gaps
Several research gaps were identified by the GDG according to the theme of the PICOs. 
Thresholds to determine initiation of therapy and targets to achieve for control
[
[ More evidence is required regarding treatment of those in the SBP 130–139 range who fall into 
one or more of the following subgroups: diabetes, chronic kidney disease, heart failure, 65 years 
or older.
[
[ There is a need for better outcomes data from, for example, trials that include heart failure and 
cognitive impairment among outcomes.
[
[ Clinical significance of adverse events registered in clinical trials needs greater clarity. 
[
[ There is a need to quantify the difference in estimates between blinded, placebo-controlled trials 
and unblinded, active control trials using a standard framework.
24

=== [SOURCE PDF: who_htn_001 | PAGE 37] ===
[
[ There is a need for periodic analysis of trials in order to capture effects of changes over time in 
background epidemiology of CVD, non-BP treatments, competing risks, etc.
[
[ More evidence is needed in LICs, MICs and other non-North American/European countries.
[
[ An assessment of the feasibility, resource needs, and costs of intensive treatment in real clinical 
practice is needed. The resource commitment required for more intensive treatment in LMICs 
needs to be quantified.
[
[ The opportunity cost of directing resources towards achieving SBP <130 in high-risk individuals 
needs to be established.
[
[ Research is needed on the feasibility, acceptability, and efficacy of intensive treatment, especially 
in high-risk populations in LICs and MICs.
Laboratory tests to determine initiation of treatment
[
[ A greater understanding of the essential tests to be performed in all patients to reduce costs and 
improve outcomes is required.
Role of cardiovascular risk in hypertension treatment
[
[ An exploration is needed of key operational aspects of the implementation of a risk-based 
approach to CVD prevention and BP-lowering pharmacological treatment in primary health care 
settings.
Monotherapy versus combination therapy
[
[ A comparison is required of long-term data about hard clinical endpoints between monotherapy 
and combination therapy.
[
[ There is a need for research studies on real-world experiences, designed and statistically powered, 
to determine if there is a difference in clinical outcomes, such as reduction in MACE, mortality, 
and serious adverse events, between single-pill combinations vs multiple-pill combinations.
[
[ Health economic analyses are needed to quantify cost-effectiveness and budget implications of 
implementing incremental initial combination therapy compared with initial monotherapy.
Frequency of re-assessment
[
[ Criteria establishing the clinical definition of stable BP control will be needed to guide the 
selection of patients for less frequent follow-up visits.
[
[ Research is needed for early and accurate identification of patients less likely to achieve BP control 
and less likely to follow up as requested by their health care provider.
[
[ Better evidence is needed on the timing, frequency, and intensity of interventions that improve 
treatment adherence.
Team-based care for hypertension
[
[ Evidence is needed that remote monitoring and use of community HCWs/navigators can assist in 
the management of BP.
[
[ Evidence of the feasibility, costs, and effectiveness of community/home-based monitoring of BP is 
needed.
PUBLICATION, IMPLEMENTATION, EVALUATION AND RESEARCH GAPS
25
```

---

### Focus Chunk #6: `who_htn_001_c0120`

- **Document Name:** WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (`who_htn_001`)
- **Chunk Type:** `methods`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `False`
- **Page Range:** 57–57
- **Heading:** ANNEXES (Part 2)
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > ANNEXES > ANNEXES (Part 2)`
- **Population Tags:** `["cardiovascular_disease", "chronic_kidney_disease"]`
- **Drug Class Tags:** `["ace_inhibitor", "arb", "ccb", "thiazide"]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
(BB, CCB, diuretics, ACEi, or ARB vs BB, CCB, diuretics, ACEi, or ARB in head-to-
head studies) should be used as first-line agents?
P
Adult men and women with HTN requiring pharmacological treatment
I
BB, CCB, diuretics, ACEi, or ARB
C
BB, CCB, diuretics, ACEi, or ARB (head-to-head studies)
O
Death (all-cause mortality), cardiovascular death (death from MI, sudden cardiac death or
stroke), stroke, cognitive impairment/dementia, myocardial infarction, end-stage renal disease
and heart failure events
Adverse effects such as bradycardia, acute kidney injury, angioedema, asthma, electrolyte
abnormalities or hypotension
Blood pressure reduction and control (if data on CVD events are absent)
s
Based on different effect modifiers such as: estimated cardiovascular risk; pre-existing CAD,
stroke, diabetes, age, sex, chronic kidney disease and race/ethnicity, level of baseline blood
pressure
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: who_htn_001 | PAGE 57] ===
3	
Should cardiovascular risk assessment be used to guide initiation of 
antihypertensive medications?
P
Adult men and women without pre-identified CVD
I
Initiating antihypertensives drug therapy based on a formal CVD risk estimation
C
Initiating antihypertensives drug therapy without formal CVD risk assessment (i.e. using only 
BP threshold)
O
Death (all-cause mortality), cardiovascular death (death from MI, sudden cardiac death or 
stroke), stroke, myocardial infarction, end-stage renal disease heart failure events, cognitive 
impairment/dementia, and adverse events
Proportion of people prescribed with antihypertensives
BP levels
s
BP levels
4	
In adults with hypertension requiring pharmacological treatment, which drugs 
should be used as first-line agents? 
P
Adult men and women with hypertension requiring pharmacological treatment
I
BB, CCB, diuretics, ACEi, or ARB
C
Placebo
O
Death (all-cause mortality), cardiovascular death (death from MI, sudden cardiac death or 
stroke), stroke, cognitive impairment/dementia, myocardial infarction, end-stage renal disease 
and heart failure events
Adverse effects such as bradycardia, acute kidney injury, angioedema, asthma, electrolyte 
abnormalities or hypotension
BP reduction and control (if data on CVD events are absent)
s
Based on different effect modifiers such as: estimated cardiovascular risk; pre-existing CAD, 
stroke, diabetes, age, sex, chronic kidney disease and race/ethnicity, level of baseline BP
5	
In adults with hypertension requiring pharmacological treatment, which drugs 
(BB, CCB, diuretics, ACEi, or ARB vs BB, CCB, diuretics, ACEi, or ARB in head-to-
head studies) should be used as first-line agents? 
P
Adult men and women with HTN requiring pharmacological treatment
I
BB, CCB, diuretics, ACEi, or ARB
C
BB, CCB, diuretics, ACEi, or ARB (head-to-head studies)
O
Death (all-cause mortality), cardiovascular death (death from MI, sudden cardiac death or 
stroke), stroke, cognitive impairment/dementia, myocardial infarction, end-stage renal disease 
and heart failure events
Adverse effects such as bradycardia, acute kidney injury, angioedema, asthma, electrolyte 
abnormalities or hypotension
Blood pressure reduction and control (if data on CVD events are absent)
s
Based on different effect modifiers such as: estimated cardiovascular risk; pre-existing CAD, 
stroke, diabetes, age, sex, chronic kidney disease and race/ethnicity, level of baseline blood 
pressure
ANNEXES
45
```

---

### Focus Chunk #7: `who_htn_001_c0029`

- **Document Name:** WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (`who_htn_001`)
- **Chunk Type:** `methods`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `False`
- **Page Range:** 17–17
- **Heading:** 2.5	 Certainty of evidence and strength of recommendations
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > 2.4	 Reviews of evidence > 2.5	 Certainty of evidence and strength of recommendations`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `["When making\nrecommendations, GRADE defines the certainty of a body of evidence as \"the extent of our confidence\nthat the estimates of an effect are adequate to support a particular decision or recommendation\" (5).", "When there were systematic reviews\naddressing the relative effects in specific subpopulations, separate evidence profiles were constructed\nfor each subpopulation."]`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
2.5	 Certainty of evidence and strength of recommendations

The GDG rated the certainty of evidence and developed the recommendations using the GRADE
(Grading of Recommendations Assessment, Development and Evaluation) approach (4). When making
recommendations, GRADE defines the certainty of a body of evidence as "the extent of our confidence
that the estimates of an effect are adequate to support a particular decision or recommendation" (5).

Members of the GDG, with the help of the methodologist, developed evidence profiles to summarize
relative and absolute estimates of effects, and an assessment of the certainty of the evidence. One
evidence profile for each comparison within a PICO question was constructed, using the online
Guideline Development Tool GRADEpro (https://gradepro.org). When there were systematic reviews
addressing the relative effects in specific subpopulations, separate evidence profiles were constructed
for each subpopulation.

According to the GRADE approach, the certainty of the evidence can be high, moderate, low, or very
low. Bodies of evidence from randomized controlled trials - which comprised almost the totality of those
included in this guideline - start the assessment as high-certainty evidence but can be down-rated due
to considerations of risk of bias, inconsistency, imprecision, indirectness, and publication bias.

Table 1 presents an explanation of the different levels of certainty of the evidence (5).

Table 1 Certainty of evidence and its implications

| Certaintylevel | Defi nition |
| --- | --- |
| High | Weareveryconfidentthatthetrueeffectliesclosetothatoftheestimate of effect . |
| Moderate | Wearemoderatelyconfidentintheeffectestimate (Thetrueeffectislikelyto . be close to the estimate of effect butthereisapossibilitythatitissubstantially, different) . |
| Low | Ourconfidenceintheeffectestimateislimited (Thetrueeffectmaybe . substantiallydifferentfromtheestimateoftheeffect) . |
| Verylow | Wehaveverylittleconfidenceintheeffectestimate (Thetrueeffectislikelytobe . substantiallydifferentfromtheestimateofeffect) . |

The strength of the recommendations reflects the degree of confidence of the GDG that the desirable
effects (e.g. beneficial health outcomes) of the recommendations outweigh the undesirable effects
(e.g. adverse effects). The strength of recommendations in this guideline was graded into two
categories:

A strong recommendation is one for which the GDG was confident that the desirable effects of
adhering to the recommendation outweigh the undesirable effects.

A weak or conditional recommendation is one for which the GDG concluded that the desirable
effects of adhering to the recommendation probably outweigh the undesirable effects, but was not
confident about these trade-offs.
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: who_htn_001 | PAGE 17] ===
2.5	 Certainty of evidence and strength of recommendations 
The GDG rated the certainty of evidence and developed the recommendations using the GRADE 
(Grading of Recommendations Assessment, Development and Evaluation) approach (4). When making 
recommendations, GRADE defines the certainty of a body of evidence as “the extent of our confidence 
that the estimates of an effect are adequate to support a particular decision or recommendation” (5). 
Members of the GDG, with the help of the methodologist, developed evidence profiles to summarize 
relative and absolute estimates of effects, and an assessment of the certainty of the evidence. One 
evidence profile for each comparison within a PICO question was constructed, using the online 
Guideline Development Tool GRADEpro (https://gradepro.org). When there were systematic reviews 
addressing the relative effects in specific subpopulations, separate evidence profiles were constructed 
for each subpopulation.
According to the GRADE approach, the certainty of the evidence can be high, moderate, low, or very 
low. Bodies of evidence from randomized controlled trials – which comprised almost the totality of those 
included in this guideline – start the assessment as high-certainty evidence but can be down-rated due 
to considerations of risk of bias, inconsistency, imprecision, indirectness, and publication bias. 
Table 1 presents an explanation of the different levels of certainty of the evidence (5). 
Table 1 Certainty of evidence and its implications
Certainty level
Definition
High
We are very confident that the true effect lies close to that of the estimate 
of effect.
Moderate
We are moderately confident in the effect estimate. (The true effect is likely to 
be close to the estimate of effect, but there is a possibility that it is substantially 
different.)
Low
Our confidence in the effect estimate is limited. (The true effect may be 
substantially different from the estimate of the effect.)
Very low
We have very little confidence in the effect estimate. (The true effect is likely to be 
substantially different from the estimate of effect.)
The strength of the recommendations reflects the degree of confidence of the GDG that the desirable 
effects (e.g. beneficial health outcomes) of the recommendations outweigh the undesirable effects 
(e.g. adverse effects). The strength of recommendations in this guideline was graded into two 
categories: 
A strong recommendation is one for which the GDG was confident that the desirable effects of 
adhering to the recommendation outweigh the undesirable effects. 
A weak or conditional recommendation is one for which the GDG concluded that the desirable 
effects of adhering to the recommendation probably outweigh the undesirable effects, but was not 
confident about these trade-offs.
METHOD FOR DEVELOPING THE GUIDELINE
5
```

---

### Focus Chunk #8: `mohfw_htn_001_c0121`

- **Document Name:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Chunk Type:** `table`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 40–41
- **Heading:** | INTRODUCTION |  |  |
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > INTRODUCTION > | INTRODUCTION |  |  |`
- **Population Tags:** `["cardiovascular_disease", "elderly", "pregnancy", "young_adults"]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
| INTRODUCTION |  |  |
| NICE | What populationisrecommended for targeted screening? If high risk population request to define, itandalsodocumenttheevidence on which recommendation is based | The population groups at high risk are older adults (>50 - 60 years), persons with diabetes obesity especially those, with a higher abdominal circumference, current smokers those with any, cardiovascular disease and those with, family history of premature cardiovasculardisease . Predictors for the presence of hypertension have been developed in Indian cohort studies and these risk scores are again based on age current, smoking presenceofabdominalobesity, |
| IHG | Saltintakerecommendationto be correctedanduniformthroughout thedocument . | Wehavementionedadietaryintakeof6 gm salt per day for the general . population and have added a qualifier, that this limit may be reconsidered in somepatientswhoareengagedinheavy manual labour under hot climatic conditions where substantial loss of salt, in sweat may occur as seen in some, studies . |
| --- | --- | --- |
| IHG | The age cut off for screening shouldbe30years ratherthan18, years . | This lower cut-off is based on the US Preventive Services Task Force recommendations A cut off above 30 . years conveys an impression that younger adults (including pregnant women) cannot have hypertension This . isnotsoasexplainedbelow: 1 Hypertension including essential . hypertension may present earlier than 30 years Studies . have shown that hypertension wasprevalentin15%ofchildren in the 5 -16 year age group (NMJI 2007Rajetal) . 2 Patients with secondary . hypertension including chronic renaldiseasemaypresentbefore thirtyyears 3 Pregnancy induced . hypertension: We envisage that thisguidelinewillbefollowedby a guideline on pregnancy induced hypertension This is a . major cause of maternal morbidity and mortality and all, pregnant women in India (most ofthemlessthan30years)need tobescreenedfor hypertension as part of antenatal care This . guideline will create the platform for screening of antenatalwomen . A large number of persons with high normalBPmaybeidentifiedbyscreening whocanprogresstohypertension IFthe . recommendations of this guideline on weight reduction tobacco cessation and, salt reduction are implemented we, might prevent their progression to essentialhypertensionwiththem . |
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: mohfw_htn_001 | PAGE 40] ===
40 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
in patients with Grade 3 
hypertension. 
Treatment 
of 
Hypertension 
with 
associated 
clinical 
conditions 
CHEP 
guidelines 
for 
treatment of hypertension 
with 
stroke, 
chronic 
kidney 
disease, 
heart 
disease 
Adapted reworded 
Review poor response to BP 
medications  
CHEP guidelines
Adapted. 
Supplemental table 10 
describes factors that 
underlie poor response 
to therapy. 
 
The scope of the guideline, an illustrative format of the guideline developed by the Medicine 
sub-group was presented in a Task Force meeting on 26.8.2015. This scope was developed 
after extensive online consultation on an ongoing basis.  
 
 
5. Submission of the draft STG for peer review:  
 
We submitted the draft STG inclusive of annexure to the Task Force in November 2015.  
 
6. Peer review:  
 
We received general and specific comments In January 2016, which helped improve the 
clarity of our draft. Some of the comments were of a substantive nature and are 
discussed in the following table. Many others were pointed in the text of the guidelines 
and included requests for references etc. 
 
S.No 
Comment 
Response 
INTRODUCTION 
NICE  
What population is recommended 
for targeted   screening? If high 
risk population, request to define 
it and also document the evidence 
on which recommendation is 
based 
The population groups at high risk are 
older adults (>50 - 60 years), persons 
with diabetes, obesity especially those 
with a higher abdominal circumference, 
current 
smokers, 
those 
with 
any 
cardiovascular disease, and those with 
family 
history 
of 
premature 
cardiovascular disease.   
Predictors 
for 
the 
presence 
of 
hypertension have been developed in 
Indian cohort studies and these risk 
scores are again based on age, current 
smoking, presence of abdominal obesity

=== [SOURCE PDF: mohfw_htn_001 | PAGE 41] ===
41 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
IHG
Salt intake recommendation to be 
corrected and uniform throughout 
the document. 
We have mentioned a dietary intake of 6 
gm. salt per day for the general 
population, and have added a qualifier 
that this limit may be reconsidered in 
some patients who are engaged in heavy 
manual 
labour 
under 
hot 
climatic 
conditions, where substantial loss of salt 
in sweat may occur, as seen in some 
studies.  
IHG
The age cut off for screening 
should be 30 years, rather than 18 
years.  
This lower cut-off is based on the US 
Preventive 
Services 
Task 
Force 
recommendations. A cut off above 30 
years 
conveys 
an 
impression 
that 
younger 
adults 
(including 
pregnant 
women) cannot have hypertension. This 
is not so as explained below: 
1. Hypertension including essential 
hypertension 
may 
present 
earlier than 30 years. Studies 
have shown that hypertension 
was prevalent in 15% of children 
in the 5-16 year age group (NMJI 
2007 Raj et al). 
2. Patients 
with 
secondary 
hypertension including chronic 
renal disease may present before 
thirty years 
 
3. Pregnancy 
induced 
hypertension: We envisage that 
this guideline will be followed by 
a 
guideline 
on 
pregnancy 
induced hypertension. This is a 
major 
cause 
of 
maternal 
morbidity and mortality, and all 
pregnant women in India (most 
of them less than 30 years) need 
to be screened for hypertension 
as part of antenatal care. This 
guideline 
will 
create 
the 
platform 
for 
screening 
of 
antenatal women. 
A large number of persons with high 
normal BP may be identified by screening 
who can progress to hypertension. IF the 
recommendations of this guideline on 
weight reduction, tobacco cessation, and 
salt reduction are implemented, we 
might prevent their progression to 
essential hypertension with them. 
SCOPE OF HT GUIDELINE
IHG
The choice of BP measuring device 
should be discussed with Health 
Technology 
Assessment 
and 
finalized. 
India is committed to phasing out 
mercury and alternatives have to be 
considered. 
Electronic 
digital 
oscillometric devices are emerging as the 
clinical standard for BP measurement 
worldwide, and have proved to be
```

---

### Focus Chunk #9: `nice_t2dm_001_c0080`

- **Document Name:** NICE Guideline NG28: Type 2 Diabetes in Adults - Management (`nice_t2dm_001`)
- **Chunk Type:** `contributors`
- **Condition:** `type_2_diabetes`
- **Indexed For Retrieval:** `False`
- **Page Range:** 37–38
- **Heading:** 1.13.2 > Why the committee made these recommendations (Part 3)
- **Section Path:** `NICE Guideline NG28: Type 2 Diabetes in Adults - Management > 1.13 People with type 2 diabetes and no relevant > 1.13.2 > Why the committee made these recommendations (Part 3)`
- **Population Tags:** `["type_2_diabetes"]`
- **Drug Class Tags:** `["glp1_ra", "metformin", "sglt2_inhibitor"]`
- **Applicability Conditions:** `null`
- **Exceptions:** `["The committee agreed that\neven though the evidence was limited for people with no relevant comorbidities, this\nbenefit would also be seen in people for whom metformin is contraindicated.", "Therefore, because the committee wanted people with type 2 diabetes to continue to\ngain the cardiovascular benefits seen in the evidence, they recommended\nmonotherapy with an SGLT-2 inhibitor when metformin is contraindicated."]`
- **Cross References:** `["Full details of the evidence and the committee's discussion are in:\n-  evidence review E: initial management\n-  evidence review F: subsequent management."]`
- **Recommendation Year:** `None`
- **Last Updated:** `2026-02-18`

#### Exact Chunk Text

```text
committee agreed that there are benefits to recommending modified-release
metformin first. This is because, when compared with standard-release metformin,
modified-release metformin:
-  has similar clinical effectiveness on HbA1c and weight reduction
-  has similar safety results for hypoglycaemia
-  is associated, in evidence outside of the protocol for the review, with reductions in
gastrointestinal adverse events
-  is likely to be better adhered to, and the committee was aware of the downstream
costs of non-adherence (for example, cardiovascular and renal adverse events,
further appointments and investigations), and
-  can fluctuate in price but, in December 2025, cost less than standard-release
metformin.
The committee noted that standard-release metformin may be preferable for people
with difficulty swallowing because unlike modified-release metformin, it can be
crushed and is available in a liquid form. This may be appropriate for people with
dementia or with learning disabilities in whom dysphagia is more common. The
committee did not make a recommendation about this because they were aware that
NEWT guidelines provide further information to support decision making for people
with swallowing difficulties.
The committee agreed that this should be addressed in a conversation between the
person and the healthcare professional when prescribing the medication.
GLP-1 receptor agonists and tirzepatide
GLP-1 receptor agonists and tirzepatide were not found to be or did not have
evidence for clinical or cost effectiveness for this population, so were not
recommended.
Medicines for people who cannot take metformin
The evidence showed that SGLT-2 inhibitors reduced cardiovascular events compared
with placebo when metformin is the background therapy. The committee agreed that
even though the evidence was limited for people with no relevant comorbidities, this
benefit would also be seen in people for whom metformin is contraindicated.
Therefore, because the committee wanted people with type 2 diabetes to continue to
gain the cardiovascular benefits seen in the evidence, they recommended
monotherapy with an SGLT-2 inhibitor when metformin is contraindicated.
Recommendation for research
The committee reviewed real-world evidence that SGLT-2 inhibitors are underprescribed, particularly to women and older people, people from some ethnic
backgrounds, and people who have experienced higher levels of deprivation when sex
and age are accounted for. They agreed that further research is needed to
understand the reasons behind this so made a recommendation for research on
improving access to SGLT-2 inhibitors.
Full details of the evidence and the committee's discussion are in:
-  evidence review E: initial management
-  evidence review F: subsequent management.
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: nice_t2dm_001 | PAGE 37] ===
Conclusion 
Taking the evidence into account, the committee agreed that combining metformin 
with an SGLT-2 inhibitor is the most clinically effective therapy option, and that this 
should be the standard initial treatment for people with no relevant comorbidities. 
Modified compared to standard-release metformin 
There was limited evidence comparing standard-release and modified-release 
metformin for people with type 2 diabetes and no relevant comorbidities, and the 
committee agreed that there are benefits to recommending modified-release 
metformin first. This is because, when compared with standard-release metformin, 
modified-release metformin: 
• has similar clinical effectiveness on HbA1c and weight reduction 
• has similar safety results for hypoglycaemia 
• is associated, in evidence outside of the protocol for the review, with reductions in 
gastrointestinal adverse events 
• is likely to be better adhered to, and the committee was aware of the downstream 
costs of non-adherence (for example, cardiovascular and renal adverse events, 
further appointments and investigations), and 
• can fluctuate in price but, in December 2025, cost less than standard-release 
metformin. 
The committee noted that standard-release metformin may be preferable for people 
with difficulty swallowing because unlike modified-release metformin, it can be 
crushed and is available in a liquid form. This may be appropriate for people with 
dementia or with learning disabilities in whom dysphagia is more common. The 
committee did not make a recommendation about this because they were aware that 
NEWT guidelines provide further information to support decision making for people 
with swallowing difficulties. 
The committee agreed that this should be addressed in a conversation between the 
person and the healthcare professional when prescribing the medication. 
Type 2 diabetes in adults: management (NG28)
© NICE 2026. All rights reserved. Subject to Notice of rights (https://www.nice.org.uk/terms-and-
conditions#notice-of-rights).
Page 37 of
131

=== [SOURCE PDF: nice_t2dm_001 | PAGE 38] ===
GLP-1 receptor agonists and tirzepatide 
GLP-1 receptor agonists and tirzepatide were not found to be or did not have 
evidence for clinical or cost effectiveness for this population, so were not 
recommended. 
Medicines for people who cannot take metformin 
The evidence showed that SGLT-2 inhibitors reduced cardiovascular events compared 
with placebo when metformin is the background therapy. The committee agreed that 
even though the evidence was limited for people with no relevant comorbidities, this 
benefit would also be seen in people for whom metformin is contraindicated. 
Therefore, because the committee wanted people with type 2 diabetes to continue to 
gain the cardiovascular benefits seen in the evidence, they recommended 
monotherapy with an SGLT-2 inhibitor when metformin is contraindicated. 
Recommendation for research 
The committee reviewed real-world evidence that SGLT-2 inhibitors are under-
prescribed, particularly to women and older people, people from some ethnic 
backgrounds, and people who have experienced higher levels of deprivation when sex 
and age are accounted for. They agreed that further research is needed to 
understand the reasons behind this so made a recommendation for research on 
improving access to SGLT-2 inhibitors. 
Full details of the evidence and the committee's discussion are in: 
• evidence review E: initial management 
• evidence review F: subsequent management. 
Type 2 diabetes in adults: management (NG28)
© NICE 2026. All rights reserved. Subject to Notice of rights (https://www.nice.org.uk/terms-and-
conditions#notice-of-rights).
Page 38 of
131
```

---

### Focus Chunk #10: `nice_t2dm_001_c0101`

- **Document Name:** NICE Guideline NG28: Type 2 Diabetes in Adults - Management (`nice_t2dm_001`)
- **Chunk Type:** `rationale`
- **Condition:** `type_2_diabetes`
- **Indexed For Retrieval:** `True`
- **Page Range:** 61–61
- **Heading:** How the recommendations might affect practice > Metformin
- **Section Path:** `NICE Guideline NG28: Type 2 Diabetes in Adults - Management > 1.17 People living with obesity > How the recommendations might affect practice > Metformin`
- **Population Tags:** `["cardiovascular_disease", "chronic_kidney_disease"]`
- **Drug Class Tags:** `["metformin", "sglt2_inhibitor"]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `2026-02-18`

#### Exact Chunk Text

```text
How the recommendations might affect practice
Metformin
The recommendations about the use of metformin may lead to a change in current
practice but should not lead to a significant cost or resource impact. The price of
modified-release metformin can fluctuate but, in December 2025, was lower than the
cost of standard-release metformin.
SGLT-2 inhibitors
SGLT-2 inhibitors were recommended by NICE in 2022. They were recommended for
some people at high risk of developing cardiovascular disease.
However, real-world evidence shows that SGLT-2 inhibitors are under-prescribed
throughout the UK. The recommendations may increase the number of people who
are offered SGLT-2 inhibitors, which will increase prescribing costs. But broader
access to SGLT-2 inhibitors may also result in long-term medicine costs being
partially offset by fewer people needing treatment for atherosclerotic cardiovascular
disease.
Number of appointments related to these medicines
The recommendations may lead to an increase in the number of appointments
required to optimise the medications being added. The committee believes this can
be managed and will lead to reductions in the long term because:
-  SGLT-2 inhibitors can be prescribed at the same time as metformin, with a plan
for starting medicines sequentially
-  the cardiovascular and renal benefits of SGLT-2 inhibitors will reduce the number
of appointments needed to treat atherosclerotic cardiovascular disease,
established heart failure and chronic kidney disease.
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: nice_t2dm_001 | PAGE 61] ===
How the recommendations might affect practice 
Metformin 
The recommendations about the use of metformin may lead to a change in current 
practice but should not lead to a significant cost or resource impact. The price of 
modified-release metformin can fluctuate but, in December 2025, was lower than the 
cost of standard-release metformin. 
SGLT-2 inhibitors 
SGLT-2 inhibitors were recommended by NICE in 2022. They were recommended for 
some people at high risk of developing cardiovascular disease. 
However, real-world evidence shows that SGLT-2 inhibitors are under-prescribed 
throughout the UK. The recommendations may increase the number of people who 
are offered SGLT-2 inhibitors, which will increase prescribing costs. But broader 
access to SGLT-2 inhibitors may also result in long-term medicine costs being 
partially offset by fewer people needing treatment for atherosclerotic cardiovascular 
disease. 
Number of appointments related to these medicines 
The recommendations may lead to an increase in the number of appointments 
required to optimise the medications being added. The committee believes this can 
be managed and will lead to reductions in the long term because: 
• SGLT-2 inhibitors can be prescribed at the same time as metformin, with a plan 
for starting medicines sequentially 
• the cardiovascular and renal benefits of SGLT-2 inhibitors will reduce the number 
of appointments needed to treat atherosclerotic cardiovascular disease, 
established heart failure and chronic kidney disease. 
Type 2 diabetes in adults: management (NG28)
© NICE 2026. All rights reserved. Subject to Notice of rights (https://www.nice.org.uk/terms-and-
conditions#notice-of-rights).
Page 61 of
131
```

---

## Section 2: Twenty-Five Stratified Sampled Recommendations

### Sampled MOHFW Recommendation #1: `mohfw_htn_001_c0058`

- **Document Name:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 21–21
- **Heading:** 4.6.9. Add-on drugs for control of BP drugs should be added at intervals of 2-4 weeks. > 4.6.10. Negative recommendation: ACE Inhibitors should not be combined with
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 4.6 The treatment regimen and the use of combinations: > 4.6.9. Add-on drugs for control of BP drugs should be added at intervals of 2-4 weeks. > 4.6.10. Negative recommendation: ACE Inhibitors should not be combined with`
- **Population Tags:** `[]`
- **Drug Class Tags:** `["ace_inhibitor", "arb"]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
4.6.9. Add-on drugs for control of BP drugs should be added at intervals of 2-4 weeks.
4.6.10. Negative recommendation: ACE Inhibitors should not be combined with
Angiotensin receptor blockers.
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: mohfw_htn_001 | PAGE 21] ===
21 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
4.6.6. The preferred 2 drug combinations are combination of calcium channel 
blockers with ACE inhibitors, ACE inhibitors with low dose diuretics, and 
calcium channel blockers with low dose diuretics. 
4.6.7. Prescription of a single pill combination of antihypertensive drugs in a defined 
proportion may be considered if available, after BP has been stabilised with a 
dose of two drugs given singly in the same proportion. 
4.6.8. The practitioner should aim for patients to reach target BP levels with an 
effective treatment regimen, whether 1, 2, or 3 drugs, within 6 to 8 weeks.  
4.6.9. Add-on drugs for control of BP drugs should be added at intervals of 2-4 weeks. 
4.6.10. Negative recommendation: ACE Inhibitors should not be combined with 
Angiotensin receptor blockers.  
4.6.10 Negative recommendation: Avoid prescribing a combination of beta-blockers 
and diuretics as they can increase the risk of diabetes mellitus in those at risk, 
e.g. persons with impaired glucose tolerance or obesity and metabolic 
syndrome. 
4.6.11. If the BP is not controlled despite use of 3 anti-hypertensives, then the hypertension 
should be termed resistant and the patient should be referred to a specialist at 
the medical college for further evaluation and management.  
 
4.7. 
Recommendation: Review and respond to possible causes of poor response 
to BP medications  
4.7.1 When a patient does not respond to two drugs given in full doses, the 
physician should review the underlying issues -related to  
§ BP measurements,  
§ poor adherence to drug and lifestyle modifications, including 
stoppage of medicines due to belief in other systems of medicine 
§ suboptimal treatment regimens,  
§ presence of associated conditions,  
§ use of non-antihypertensive drugs which can interfere with the action 
of anti-hypertensives, and  
§ Consider the possibility of secondary hypertension.
```

---

### Sampled MOHFW Recommendation #2: `mohfw_htn_001_c0033`

- **Document Name:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 17–17
- **Heading:** 4.3.2 Drug therapy in patients with grade I hypertension uncomplicated by any
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > KEY RECOMMENDATIONS: THERAPEUTIC RECOMMENDATIONS > 4.3.2 Drug therapy in patients with grade I hypertension uncomplicated by any`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
4.3.2 Drug therapy in patients with grade I hypertension uncomplicated by any
organ damage, without coexisting diabetes mellitus, clinical cardiovascular
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: mohfw_htn_001 | PAGE 17] ===
17 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
KEY RECOMMENDATIONS: THERAPEUTIC RECOMMENDATIONS 
Lifestyle modifications and initiation of drug therapy 
 
4.1. 
Overall aim: The overall aim of the management of hypertension is not only 
reduction of BP to target levels but also to lower the cardiovascular risk of 
the patient. Management of hypertension should be tailored to the individual 
and his or her circumstances.  
4.2. 
Lifestyle measures including reduction of salt intake, stopping tobacco 
intake, and reduction of body weight in those who are obese, are part of 
management of all patients with hypertension.  
4.2.1 These lifestyle measures may be sufficient for treatment of Grade 1 
hypertension, may reduce the doses required for control of 
hypertension, and will also reduce the cardiovascular risk in all grades 
of hypertension.  
 
 
4.2.2. A trial of lifestyle measures should be monitored for 1-3 months 
following diagnosis of Grade 1 hypertension. The lower range of 
durations should be considered in the presence of other risk factors 
like age, obesity, lipid levels, and smoking status. 
4.3.1 Drug therapy is indicated  in patients with Grade 1 hypertension with  
• 
Any sign of target organ damage (LVH on ECG, proteinuria on 
urinalysis, hypertensive retinopathy on fundus examination). 
• 
Any evidence of coronary artery disease, congestive heart failure, 
cerebrovascular disease (clinical cardiovascular disease), PAD 
• 
Diabetes 
• 
Presence of chronic kidney disease 
• 
Patients with 3 or more risk factors1 (including age, gender, 
smoking, obesity, dyslipidemia, diabetes, impaired fasting glucose, 
family history of premature coronary artery disease). 
4.3.2 Drug therapy in patients with grade I hypertension uncomplicated by any 
organ damage, without coexisting diabetes mellitus, clinical cardiovascular 
                                                        
1 Age > 55 in men, >65 in women; Male gender; smoking; diabetes; obesity including abdominal obesity; 
impaired fasting glucose ( FBS 100-125 mg/dl); dyslipidaemia (high LDL, high TG, low HDL); family history of 
premature coronary artery disease
```

---

### Sampled MOHFW Recommendation #3: `mohfw_htn_001_c0186`

- **Document Name:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 78–78
- **Heading:** 4.5.5.2 Preferred drugs for patients with heart failure and hypertension are > 4.5.5.3 Preferred drugs for patients with coronary artery disease and
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 4.5 Key recommendation: Classes of antihypertensive drugs & preferred choices > 4.5.5.2 Preferred drugs for patients with heart failure and hypertension are > 4.5.5.3 Preferred drugs for patients with coronary artery disease and`
- **Population Tags:** `["cardiovascular_disease"]`
- **Drug Class Tags:** `["ace_inhibitor", "beta_blocker", "ccb", "thiazide"]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
4.5.5.2 Preferred drugs for patients with heart failure and hypertension are
ACE inhibitors, diuretics (including loop diuretics) and beta-blockers.
4.5.5.3 Preferred drugs for patients with coronary artery disease and
hypertension are beta-blockers, ACE Inhibitors or calcium channel
blockers.
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: mohfw_htn_001 | PAGE 78] ===
78 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
pressure, and on outcomes, although beta-blockers have been associated 
with lesser protection against strokes. All combinations of drugs are not 
however similarly efficacious, and some are preferred. 
 4.5.3.     The different classes of drugs have differing side effect profiles and 
requirements for monitoring, which may influence their use and prescription 
in the health system.  
 4.5.4           In the absence of any associated clinical conditions (noted below) providing a 
compelling indication for the use of a particular drug , a long acting calcium 
channel blocker, a low dose thiazide diuretic, or a  low cost ACE inhibitor may 
be used as the initial antihypertensive drug.  
      4.5.5.              The presence of associated clinical conditions (diabetes, clinical 
cardiovascular disease, chronic kidney disease) in a patient may provide 
compelling indication for the use of specific classes of drugs.  
4.5.5.1   Preferred drugs for treatment of patients with diabetes and hypertension 
are ACE inhibitors, especially in those with proteinuria.  Calcium 
channel blockers /low dose diuretics may be used in addition if 
required to achieve control. 
4.5.5.2 Preferred drugs for patients with heart failure and hypertension are 
ACE inhibitors, diuretics (including loop diuretics) and beta-blockers. 
4.5.5.3 Preferred drugs for patients with coronary artery disease and 
hypertension are beta-blockers, ACE Inhibitors or calcium channel 
blockers. 
4.5.6 
The specific drugs within these classes recommended on the basis of 
availability and affordability include amlodipine, (a long acting calcium channel 
blocker); enalapril or lisinopril, (ACE inhibitor); low dose hydrochlorothiazide, 
(thiazide) and if required and losartan, (a low cost angiotensin II receptor 
blocker).  
4.5.7 
Angiotensin receptor blockers have a mode of action, efficacy and indications 
similar to ACE inhibitors, but are currently more expensive than them.  They 
should therefore be used in the place of ACE inhibitors, in case there are side 
effects with ACE inhibitors like cough, angioedema.  
Background:  
Current guidelines suggest that all the 4 drug classes of antihypertensive drugs–thiazide 
diuretics, calcium channel blockers, ACE inhibitors, Angiotensin receptors blockers for 
initiation as well as add-on agents to control BP.(20) Beta-blockers are not considered first
```

---

### Sampled MOHFW Recommendation #4: `mohfw_htn_001_c0178`

- **Document Name:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `both`
- **Indexed For Retrieval:** `True`
- **Page Range:** 76–77
- **Heading:** 4.4.4 Current evidence based on trials of BP targets of <130 mm and < 85 mm
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 4.3 Initiation of drug therapy > 4.4.4 Current evidence based on trials of BP targets of <130 mm and < 85 mm`
- **Population Tags:** `["cardiovascular_disease", "elderly", "type_2_diabetes"]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `["If the BP does not show a\ndownward trend on the follow up, medicines from other classes may be added to achieve\nthe target BP."]`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
4.4.4 Current evidence based on trials of BP targets of <130 mm and < 85 mm
diastolic in patients with diabetes have failed to show significant overall
benefit on cardiovascular disease outcomes, and have been accompanied by
increased frequency of serious adverse events. Therefore we currently
recommend the standard BP target of <140 mm systolic and <90 mm in
patients with diabetes in India.
Background:
Healthcare providers and patients alike need to know the target BP to be achieved as part of
control of hypertension. This has been an evolving area of debate and investigations, and
this issue has been addressed by recent guidelines like the JNC 8 which have systematically
reviewed the evidence. The interim results of a recent study - the Systolic Blood Pressure
Intervention Trial (SPRINT) which involved intensive reduction of BP < 120 mm are
provocative in terms of potential for reduction of mortality, which have to be weighed
against increased incidence of serious adverse events noted.(58)
Implementation:
The target BP may be achieved at 6-8 weeks, for which the patient can be assessed at 2-4
weekly intervals for achievement of target BP. At each visit lifestyle interventions can be
emphasised, adherence may be assessed and reinforced. If the BP does not show a
downward trend on the follow up, medicines from other classes may be added to achieve
the target BP.

Rationale:
Target BP: There is agreement among all evidence based guidelines for the targets of
Systolic BP <= 140 and diastolic BP <= 90 mm Hg in the general adult population. (18-21) We
have therefore adopted the same targets. A recent study the Systolic Blood Pressure
Intervention trial (SPRINT) has examined the effect of reduction of systolic blood pressure
below 120 mm on cardiovascular outcomes in non-diabetic patients who were considered at
high risk for cardiovascular outcomes.(58) There was a 25% relative risk reduction in the
primary outcome, but this was achieved with a mean of 3 antihypertensive drugs, and there
was a significantly increased frequency of serious adverse events including hypotension,
syncope, electrolyte abnormalities. Also there was a three-fold higher risk of more than 30%
decline in GFR in the intensive treatment group.(58) Since the trial excluded diabetics, the
generalisation of these results to diabetics is questionable, especially with the lack of
benefit on outcomes in the ACCORD trial which examined the role of intensive BP reduction
in diabetics.(59)We feel that these results deserve a nuanced discussion about their
generalisability in the context of our health system, where intensive monitoring and access
to care is particularly challenging for a large part of our population. Therefore we continue
to propose the targets of <140 mm systolic for the general.
Targets for elderly: The definition of elderly differs across guidelines, as JNC 8 guidelines
categorised as elderly as those over 60 years (20), while all other guidelines have defined the
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: mohfw_htn_001 | PAGE 76] ===
76 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
4.4. 
Treatment goals for management of hypertension:  
4.4.1 The current target for control of BP for patients under 80 years of age should 
be less than systolic blood pressure less than 140 mm and diastolic blood 
pressure less than 90 mm. 
4.4.2 The current target for control of BP for patients 80 years or older should be 
less than 150 mm systolic and less than 90 mm diastolic. 
4.4.3 A recent trial (SPRINT trial) in non-diabetic population at high cardiovascular 
risk has shown a reduction in cardiovascular mortality in patients in the 
intensive treatment group where the goal BP was less than 120 mm systolic 
and 80 mm diastolic. However this was accompanied by more than 2 fold 
increased frequency of serious adverse events and increase in serum 
creatinine. Based on the currently available evidence we do not recommend 
this lower target generally for physicians and patients in India, except for 
individual patients and physicians in situations who have agreed upon these 
targets and where close monitoring for adverse effects is feasible.  
4.4.4 Current evidence based on trials of BP targets of <130 mm and < 85 mm 
diastolic in patients with diabetes have failed to show significant overall 
benefit on cardiovascular disease outcomes, and have been accompanied by 
increased frequency of serious adverse events. Therefore we currently 
recommend the standard BP target of <140 mm systolic and <90 mm in 
patients with diabetes in India. 
Background:  
Healthcare providers and patients alike need to know the target BP to be achieved as part of 
control of hypertension. This has been an evolving area of debate and investigations, and 
this issue has been addressed by recent guidelines like the JNC 8 which have systematically 
reviewed the evidence. The interim results of a recent study – the Systolic Blood Pressure 
Intervention Trial (SPRINT) which involved intensive reduction of BP < 120 mm are 
provocative in terms of potential for reduction of mortality, which have to be weighed 
against increased incidence of serious adverse events noted.(58) 
Implementation:  
The target BP may be achieved at 6-8 weeks, for which the patient can be assessed at 2-4 
weekly intervals for achievement of target BP. At each visit lifestyle interventions can be 
emphasised, adherence may be assessed and reinforced. If the BP does not show a 
downward trend on the follow up, medicines from other classes may be added to achieve 
the target BP. 
 
Rationale:

=== [SOURCE PDF: mohfw_htn_001 | PAGE 77] ===
77 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
Target BP: There is agreement among all evidence based guidelines for the targets of 
Systolic BP ≤ 140 and diastolic BP ≤ 90 mm Hg in the general adult population. (18-21) We 
have therefore adopted the same targets. A recent study the Systolic Blood Pressure 
Intervention trial (SPRINT) has examined the effect of reduction of systolic blood pressure 
below 120 mm on cardiovascular outcomes in non-diabetic patients who were considered at 
high risk for cardiovascular outcomes.(58) There was a 25% relative risk reduction in the 
primary outcome, but this was achieved with a mean of 3 antihypertensive drugs, and there 
was a significantly increased frequency of serious adverse events including hypotension, 
syncope, electrolyte abnormalities. Also there was a three-fold higher risk of more than 30% 
decline in GFR in the intensive treatment group.(58) Since the trial excluded diabetics, the 
generalisation of these results to diabetics is questionable, especially with the lack of 
benefit on outcomes in the ACCORD trial which examined the role of intensive BP reduction 
in diabetics.(59)We feel that these results deserve a nuanced discussion about their 
generalisability in the context of our health system, where intensive monitoring and access 
to care is particularly challenging for a large part of our population. Therefore we continue 
to propose the targets of <140 mm systolic for the general. 
Targets for elderly: The definition of elderly differs across guidelines, as JNC 8 guidelines 
categorised as elderly as those over 60 years (20), while all other guidelines have defined the 
elderly as people above 80 years of age. (18, 19, 21) . There is agreement among all guidelines, 
based on data from the HYVET study,(60) that the target for BP of systolic BP of ≤150 mm and 
diastolic BP ≤90 mm Hg should be considered for patients above 80 years of age.  
Targets for patients with diabetes: Earlier guidelines like the JNC 7(29) recommended target 
BP of <130 mm Hg systolic and <80 mm Hg diastolic for patient populations e.g. diabetics, 
but recent evidence based guidelines like JNC 8 revised these targets to <140 mm systolic 
and <90 mm diastolic, based on appraisal of evidence from randomised controlled trials (20). 
A large randomised controlled trial – the ACCORD (Action to Control Cardiovascular Risk in 
Diabetes) found that there was no significant cardiovascular benefit in the intensive BP 
reduction group where BP was lowered less than 120 mm Hg except a reduction in stroke. 
(59) In the intensive treatment group there was a more than 2 fold higher risk of serious 
adverse effects (hypotension, hyperkalemia, angioedema) and elevation of serum 
creatinine. The most recent Cochrane review on this subject has recommended the 
standard BP target of <140 mm Hg and <90 mm Hg since “evidence from randomized trials 
does not support blood pressure targets lower than the standard targets in people with 
elevated blood pressure and diabetes.”(61). 
4.5 Key recommendation: Classes of antihypertensive drugs & preferred choices 
 
4.5.1            The primary issue in treatment of hypertension is reduction of cardiovascular 
risk by effective control of blood pressure. Overall the benefits of 
antihypertensive treatment are due to lowering of blood pressure rather 
than choice of therapy. Many patients will require more than one drug for 
control of hypertension. 
4.5.2.         All classes of drugs- calcium channel blockers, ACE inhibitors/ARBs, diuretics; 
beta-blockers have approximately the same efficacy on lowering of blood
```

---

### Sampled MOHFW Recommendation #5: `mohfw_htn_001_c0172`

- **Document Name:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 73–73
- **Heading:** 4.3.3.1 Drug therapy is initiated in patients with Grade 2 hypertension
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 4.3 Initiation of drug therapy > 4.3.3.1 Drug therapy is initiated in patients with Grade 2 hypertension`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `["If the initial screening by the non-physician\nmedical staff."]`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
4.3.3.1 Drug therapy is initiated in patients with Grade 2 hypertension
on confirmation of the diagnosis on repeat BP measurements
in the visits subsequent to the initial visit when Grade 2 HT was
first detected. If the initial screening by the non-physician
medical staff.
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: mohfw_htn_001 | PAGE 73] ===
73 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
cardiovascular disease should be initiated after a trial of 1-3 months 
of lifestyle modifications. 
4.3.3. Drug therapy is indicated in all patients with Grade 2 and Grade 3   
hypertension and should be combined with lifestyle measures. 
4.3.3.1 Drug therapy is initiated in patients with Grade 2 hypertension 
on confirmation of the diagnosis on repeat BP measurements 
in the visits subsequent to the initial visit when Grade 2 HT was 
first detected. If the initial screening by the non-physician 
medical staff. 
4.3.3.2. Drug therapy in patients with Grade 3 hypertension is initiated 
after repeat measurements in the initial visit confirm the severe 
elevation of the blood pressure. 
Background:   
The management of elevated BP involves lifestyle modifications and drug therapy when 
indicated. Hypertension is a major modifiable risk factor for mortality due to stroke, 
myocardial infarction.(53) In India for example the incidence of stroke is 119-145 per 100,000 
population with a case fatality which varies between 27-42%.(54)There is evidence from 
multiple randomised controlled trials and meta-analysis that BP reduction leads to reduction 
in CAD, stroke and total mortality. The meta-analysis suggested a linear relationship with 
increasing reduction in SBP and DBP resulting in greater CHD and stroke reduction.(5, 55) 
Implementation:  
Advice on lifestyle modification can be given by both physician and trained non-physician 
staff, and brief descriptions of this advice are given in the annexure of this guideline.  
Initiation of drug therapy can be done at any facility starting at the PHC level and above 
after confirming the diagnosis of hypertension and severity of hypertension (grade 1 or 
grade 2 or grade 3).  
Before initiation of therapy the patient will be educated about hypertension, and assessed 
for other cardiovascular risk factors (e.g. diabetes), presence of target organ damage, and 
associated clinical conditions (coronary artery disease, stroke or TIA, and renal disease) as 
discussed in the section on assessment.  
The drug therapy to be initiated will depend on the presence of compelling indications 
related to these associated clinical conditions, and in case there are no compelling 
indications for the use of a specific class of drugs, any drug from the first line classes of 
antihypertensives like calcium channel blockers, ACE inhibitors/Angiotensin receptor 
blockers, and low dose thiazide diuretics may be used.  The availability of a core list of 4 
drugs representative of the main groups of anti-hypertensive drugs need to be ensured at 
all health facilities. These include a long acting calcium channel blocker(amlodipine), ACE 
inhibitor (enalapril),  low dose thiazide diuretic (hydrochlorothiazide), and a cardioselective 
beta-blocker(atenolol) all of which are listed in the National List of Essential Medicines
```

---

### Sampled MOHFW Recommendation #6: `mohfw_htn_001_c0072`

- **Document Name:** MoHFW STG - Hypertension (Background Document) (`mohfw_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 23–23
- **Heading:** 4.8.4.2
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 4.8 Therapy of hypertension and associated conditions: > 4.8.4.2`
- **Population Tags:** `["cardiovascular_disease"]`
- **Drug Class Tags:** `["ace_inhibitor", "arb"]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
4.8.4.2
In patients with a history of stroke or TIA, initiation of drug treatment
should be considered even with Grade 1 hypertension, and a systolic BP
of less than 140 mm Hg should be targeted. An ACE inhibitor/ARB is
considered an initial drug.
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: mohfw_htn_001 | PAGE 23] ===
23 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
4.8.3.3 
Use of ACE inhibitors and Thiazide or thiazide like diuretics should be 
used as other antihypertensive agents, and in the presence of volume 
overload, loop diuretics like frusemide may be used.   
 
4.8.4 Cerebrovascular disease:  
4.8.4.1     Prevention of stroke can occur with all classes of antihypertensive drugs if 
BP is effectively controlled. 
4.8.4.2 
In patients with a history of stroke or TIA, initiation of drug treatment 
should be considered even with Grade 1 hypertension, and a systolic BP 
of less than 140 mm Hg should be targeted. An ACE inhibitor/ARB is 
considered an initial drug. 
4.8.4.3 
In the first 72 hours of an ischemic stroke, do not administer 
antihypertensive treatment, since excessive lowering of BP can 
exacerbate the existing ischemia.  
4.8.4.4 
In patients who are not undergoing thrombolytic therapy for ischemic 
stroke, extreme values of BP, e.g. systolic BP  > 220 mm Hg or diastolic BP 
> 120 mm Hg should be treated by agents to reduce mean arterial 
pressure by about 15% in the first hour and no more than 25% in the first 
24 hours and with gradual reduction thereafter. In patients who are 
candidates for thrombolytic therapy, BP above systolic of 185 mm Hg and 
diastolic of 110 mm Hg should be treated cautiously and maintained 
below these levels.  
4.8.4.5 
In patients with intracerebral haemorrhage, with SBP > 200 mm Hg or 
MAP2>150 mm Hg, aggressive reduction of blood pressure with 
intravenous infusion of antihypertensives is indicated and the patient 
should be examined every 5 minutes. 
4.8.4.6 
In patients with intracerebral haemorrhage , with SBP >180 mm Hg or 
MAP > 130 mm Hg, modest reduction of BP to 160/90 is indicated using 
an intermittent or continuous IV infusion with frequent re-examination is 
indicated. 
 
4.8 Hypertension in the elderly:  
                                                        
2 MAP = Mean arterial pressure which is calculated as follows MAP = SBP +2(DBP)where SBP is systolic blood 
pressure and DBP is diastolic blood pressure                                                    3
```

---

### Sampled ICMR Recommendation #7: `icmr_t2dm_001_c0003`

- **Document Name:** ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11) (`icmr_t2dm_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `type_2_diabetes`
- **Indexed For Retrieval:** `True`
- **Page Range:** 1–1
- **Heading:** Diagnostic Awareness Banner
- **Section Path:** `ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11) > Diagnostic Awareness Banner`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
DIAGNOSTIC AWARENESS BANNER: KEEP LOW THRESHOLD FOR DIAGNOSIS. MAKE SURE TO FOLLOW UP TO MEET TARGETS. Routine opportunistic screening and early diagnosis are critical to prevent microvascular and macrovascular complications.
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: icmr_t2dm_001 | PAGE 1] ===
Standard Treatment Workﬂow (STW)
DIABETES MELLITUS TYPE 2
ICD-10-E11
      KEEP LOW THRESHOLD FOR DIAGNOSIS. MAKE SURE TO FOLLOW UP TO MEET TARGETS
ABBREVIATIONS
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and 
are based on expert opinions and available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by 
the treating physician. There will be no indemnity for direct or indirect consequences. Kindly visit the website of DHR for more information: (stw.icmr.org.in) for more information.
©Department of Health Research, Ministry of Health & Family Welfare, Government of India.
Osmotic 
symptoms
ie., polyuria, 
polydipsia and 
polyphagia 
May be asymptomatic
Weight loss
Non healing 
wounds
Paraesthesia
Recurrent 
infections
Blurring of 
vision
DIAGNOSIS
EXAMINATION:
BMI 
waist 
circumference
BP Peripheral 
pulses
Hypertension
Dyslipidaemia CAD CKD
Skin, oral 
cavity, foot 
Fundus 
(dilated) 
examination
ASSESS
INVESTIGATION
• HbA1c 
• Creatinine 
• K+
• Fasting lipid proﬁle
• Urine routine examination 
and spot albumin: creatinine 
ratio#
• LFT/ ALT, AST
• ECG
• Others like Echo, USG 
abdomen as indicated
#These may best be carried 
out after initial glycaemic 
control 
METABOLIC TARGETS
• HbA1c </= 7 .0% (except elderly and 
those with signiﬁcant comorbid 
conditions) where higher target may 
be acceptable
• Pre-prandial capillary plasma 
glucose: 80-130 mg/dl
• Post-prandial capillary plasma 
glucose: <180 mg/dl
• BP=140/90 (130/80 in CKD) LDL: < 100 
mg/dl (< 70mg/dl in CAD)
TREATMENT
• Dietary modiﬁcation
• Avoidance of tobacco and restriction/ 
avoidance of alcohol
• Physical activity
• Pharmacotherapy:
› HbA1c < 8.5%: Monotherapy- Metformin
› HbA1c 8.5-10%: Dual therapy- Metformin 
+ SU’s/TZD/ DPPIVi/SGLT2i /AGI/GLP-1RA
› HbA1c > 10%: Basal Insulin+ Metformin + 
another OAD / triple OAD combination
OR
OR
OR
CO-MORBIDITIES:
SYMPTOMS
SCREENING FOR DIABETES MELLITUS
IN PREGNANCY
• H/O GDM/Pre-existing diabetes
• All pregnant women to be screened in 1st trimester with FPG
• FPG ≥ 126 and/or HbA1c ≥ 6.5% to be considered pre-existing diabetes
• FPG between 92-125 to be considered as GDM
• All those women with normal screening in 1st trimester to get a 75 g-oral 
glucose tolerance test done at 24-28 weeks
• All GDM women to be tested 6 weeks post-partum and once every 3 years
• PREDIABETES: should be tested yearly 
IN AN APPARENTLY NORMAL ADULT
• In obese or overweight (BMI ≥ 27.5 
or ≥ 23 kg/m2) with any of the 
following risk factors
• First degree relative with diabetes
• History of cardiovascular disease
• BP (≥ 140/90 mmHg)
• Dyslipidemia (TG > 250 mg/dL, 
HDL <40 mg/dl in male, <50 mg/dl 
in female
• Physical inactivity
• Polycystic ovary syndrome (PCOS)
• Insulin resistance (acanthosis 
nigricans)
• Adults > 30 years of age
• Previous history of GDM
  IN AN ADULT WITH ILLNESS
• In any adult/adolescent who presents with one of the following 
illness/complaints
• Osmotic symptoms (polyuria, polydipsia, polyphagia, nocturia)
• Unexplained weight loss
• Unexplained depression or dementia
• Acute coronary syndrome
• Deep seated infections (liver abscess, lower lobe pneumonia, tuberculosis, 
pyelonephritis, abscesses, septic arthritis, osteomyelitis)
• Recurrent infections (tinea, oral thrush, onychomycosis, cystitis-urinary 
tract infection, sinusitis, STI, cellulitis, carbuncle)
• Non-healing ulcers (foot ulcers-infected/neuropathic)
• Exogenous/iatrogenic Cushing’s syndrome
Department of Health Research
Ministry of Health and Family Welfare, Government of India
PREDIABETES: 
Impaired fasting glucose: FPG 100-125 mg/dL; Impaired 
glucose tolerance: 140-199 mg/dL; HbA1c 5.7-6.4%
ALT: Alanine transaminase
AST: Aspartate aminotransferase
BMI: Body mass index
BP: Blood pressure
CAD: Coronary artery disease
CGM: Continuous glucose monitor
CKD: Chronic kidney disease
DTR: Deep tendon reﬂex
ECG: Electrocardiogram
FPG: Fasting plasma glucose
GDM: Gestational diabetes mellitus
HDL: High-density lipoprotein
LDL: Low-density lipoprotein
LFT: Liver function test
OAD: Oral antidiabetic drug
OGTT: Oral glucose tolerance test
SMBG: Self-monitoring of blood 
           glucose
TG: Triglyceride
• Endocrinology: for uncontrolled hyperglycemia
• Ophthalmology: at initial evaluation and every year 
• Nephrology: for deranged renal function
• Cardiology: for CAD/HF/arrhythmia
REFERRALS
MONITORING
• Blood glucose; FPG and 2 hours PPG once monthly 
more frequent as required including SMBG or CGM
• HbA1c every 6-12 months ( 3 monthly if uncontrolled)
• Annual monitoring : ECG, urine ACR (albumin 
creatinine ratio),dilated fundoscopy,foot examination
Pin-prick 
sensation, 
monoﬁlament 
test ,vibration, 
DTR
FPG ≥126 
mg/dl 
(after 8hr 
fasting)
2-h plasma
 glucose ≥200
 mg/dl 
during OGTT
HbA1C ≥
6.5%
Diabetes 
symptoms  
+ random 
plasma 
glucose ≥
200 mg/dl
July/ 2022
```

---

### Sampled ICMR Recommendation #8: `icmr_htn_001_c0003`

- **Document Name:** ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) (`icmr_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 1–1
- **Heading:** Population Screening and Risk Factors for Hypertension
- **Section Path:** `ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) > Population Screening and Risk Factors for Hypertension`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `["All adults >= 18 years should get blood pressure measured at every clinic visit"]`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
POPULATION SCREENING:
- ALL ADULTS >= 18 YEARS SHOULD GET BLOOD PRESSURE MEASURED AT EVERY CLINIC VISIT.
- Population screening BP reading may count as the first reading for diagnosis.

RISK FACTORS FOR HYPERTENSION:
- High salt intake
- Sedentary behavior
- Tobacco and alcohol consumption
- Obesity
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: icmr_htn_001 | PAGE 1] ===
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and 
available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by the treating physician. There will be no indemnity for direct or indirect 
consequences. Kindly visit our web portal (stw.icmr.org.in) for more information. © Indian Council of Medical Research and Department of Health Research, Ministry of Health & Family Welfare, Government of India.
Standard Treatment Workflow (STW)
HYPERTENSION IN ADULTS
ICD-11 BA00
May/2026
PHARMACOTHERAPY
MANAGEMENT OF HYPERTENSION
ACEi:  Angiotensin-converting enzyme inhibitor
ARB:  Angiotensin receptor blocker 
BP: Blood pressure
CCB: Calcium channel blocker
FDC: Fixed-dose combination
ABBREVIATIONS
REFERENCES
   
•
RISK FACTORS 
• High salt 
intake
• Sedentary 
behavior
• Tobacco and 
alcohol 
consumption
• Obesity 
DIAGNOSIS OF HYPERTENSION
• Systolic BP  ≥140 AND/OR Diastolic BP ≥ 
90 mmHg on two diﬀerent clinic visits
• Population screening BP reading may 
count as the ﬁrst reading
• Use the higher category if only Systolic or 
Diastolic BP is high, manage based on 
the higher value
• If Systolic BP is ≥160 AND/OR Diastolic BP 
≥100 measurement of one clinic visit is 
suﬃcient for diagnosing hypertension 
BLOOD PRESSURE CONTROL TARGETS 
• All adults: SBP <140 and DBP <90 
mmHg
• Diabetes mellitus, CKD, or established 
CVD: SBP <130 and DBP <80 mmHg 
(optimal target if tolerated)
• Age ≥80 years: SBP <150 and DBP <90 
mmHg 
• Assess orthostatic BP at every visit of 
adults ≥ 65 years
LIFESTYLE MODIFICATION 
• Advise all patients against tobacco 
and alcohol use
• Limit salt intake to <5g/day
• Use healthy oils, eat more 
fruits/vegetables, prefer ﬁsh/omega-3 
foods such as nuts and seeds
• Physical Activity: 30 minutes daily 
• Weight Management: Keep BMI <23 
kg/m2 and waist circumference: <90 
cm (men) and <80 cm (women)
• BP to be measured at every clinical 
visit
• Evaluate for diabetes (fasting 
plasma glucose or HbA1c) and 
manage accordingly
• Annual evaluations - Serum 
creatinine, Urine (albumin,  sugar, 
creatinine), Lipid proﬁle, 
Fundoscopy
• Additional investigations (if 
required)- ECG, ECHO    
MONITORING OF HYPERTENSION 
HYPERTENSION URGENCY
Systolic BP ≥180 AND/OR Diastolic 
BP ≥120 
with
 Symptoms of target organ damage 
• Visual disturbance, dizziness, 
confusion, headache
• Chest pain
• Breathlessness (worse lying 
down/leg swelling)
• Sudden weakness, speech/ 
swallowing diﬃculty, vision 
problem
Management
• Stabilise ABC and refer to 
emergency care at higher center
PROTOCOL NO 1 ATTACC
PROTOCOL NO 2 AATTCC
If BP is high:*
Prescribe Amlodipine 5mg
After 4 weeks measure BP again. 
If still high:
Add Telmisartan 40mg
After 4 weeks measure BP again. 
If still high:
Increase Telmisartan to 80mg
After 4 weeks measure BP again. 
If still high:
Increase Amlodipine to 10mg
After 4 weeks measure BP again. 
If still high:
Add Chlorthalidone 12.5mg
After 4 weeks measure BP again. 
If still high:
1
2
3
4
5
6
If BP is high:*
Prescribe Amlodipine 5mg
After 4 weeks measure BP again. 
If still high:
Increase to Amlodipine 10mg
After 4 weeks measure BP again. 
If still high:
Add Telmisartan 40mg
After 4 weeks measure BP again. 
If still high:
Increase to Telmisartan 80mg
After 4 weeks measure BP again. 
If still high:
Add Chlorthalidone 12.5mg
After 4 weeks measure BP again. 
If still high:
1
2
3
4
5
6
*High BP  ≥140 /90 mmHg 
At every visit: Check if the patient has been taking medications regularly and 
correctly 
Consider adding drugs of other classes, preferably MRA (eg.Spironolactone)
• Combination therapy (two drugs from two diﬀerent classes) could be the 
default initial pharmacological treatment for most adults with 
hypertension
• Single-pill combinations (SPCs/ﬁxed-dose combinations, FDCs) are 
preferred over multiple pills to improve adherence
• Monotherapy remains appropriate only for (a) low-risk Grade 1 HTN, (b) 
elderly ≥ 80 years, or (c) frail patients
• A CCB or Thiazide/Thiazide-like diuretic should be used with a 
Renin-Angiotensin-Aldosterone System (RAAS) blocker (either an ACEi or 
an ARB)
• Three-drug combination, often a RAAS blocker, CCB, or a 
Thiazide/Thiazide-like diuretic, if blood pressure is not controlled with the 
initial two-drug combination
• β-blockers are appropriate in cases of angina, postmyocardial infarction, 
heart failure (HFrEF or HFpEF with ischemia)
• DO NOT combine two RAAS blockers as it increases the risk of adverse 
eﬀects, including acute kidney injury (AKI)
PHARMACOLOGICAL STRATEGY    
SUGGESTED TREATMENT PROTOCOLS 
• Systolic BP ≥180 AND/OR Diastolic ≥
120 mmHg
        AND
• No signs of acute target-organ 
damage
Management 
• Start oral antihypertensive drugs
• Do NOT use IV medicines
• Reduce BP gradually over 24–48 hours
• Refer/admit if symptoms or organ 
damage suspected
• Follow-up within 1 week
  ALL ADULTS  ≥ 18 YEARS SHOULD GET BLOOD PRESSURE MEASURED AT EVERY CLINIC VISIT
1. Mancia G, Kreutz R, Brunström M, et al. 2023 ESH Guidelines for the management of arterial hypertension. J Hypertens. 2023;41(12):1874–2071. doi:10.1097/HJH.0000000000003480 PMID: 37345492
2. Joseph G, Thanh Pham V, Kragh Andersen P, et al. Cardiovascular events according to blood pressure thresholds recommended by ACC/AHA. Blood Press. 2024;33(1):2380346. 
doi:10.1080/08037051.2024.2380346 PMID: 39018201
3. Gupta R, Maheshwari A, Verma N, Narasingan SN, Tripathi K, Joshi S, Manoria PC, et al. Indian Society of Hypertension (InSH) Consensus Guideline for the Management of Hypertension, 2025. 
Hypertension Journal. 2025;11(4):76–138. doi:10.61081/htnj/25v11i401.
4. Ministry of Health and Family Welfare, Government of India. Training modules on non-communicable diseases. New Delhi: MoHFW; 2025.
5. ICMR-National Institute of Epidemiology. India Hypertension Control Initiative: Training modules. Chennai, 2021.
HFrEF: Heart failure with reduced ejection fraction
HFpEF: Heart Failure with Preserved Ejection
OD: Once Daily
MRA: Mineralocorticoid Receptor Antagonist
RAAS:  Renin Angiotensin-Aldosterone System
CLASSIFICATION
Normal
Elevated BP
Hypertension 
Grade 1
Hypertension 
Grade 2
Hypertension 
Grade 3
ACTION
Reassure and 
encourage healthy 
lifestyle
Lifestyle 
modiﬁcation
Pharmacological
management+ 
Lifestyle 
modiﬁcation
BLOOD PRESSURE LEVELS
Systolic <120 AND 
Diastolic<80
Systolic 120-139 AND/ OR 
Diastolic 80-89
Systolic 140-159 AND/ OR 
Diastolic 90-99
Systolic 160-179 AND/ OR 
Diastolic 100-109
Systolic ≥ 180 AND/ OR 
Diastolic ≥ 110
 RED FLAGS SIGNS
DRUG CLASS
CONTRAINDICATIONS
DOSES
SIDE EFFECTS
ACE inhibitors
ARB
CCB
Diuretics
Beta-blockers
Aldosterone antagonist
Dry cough, angioedema, hyperkalemia 
rise in serum creatinine 
Hypotension, acute renal failure, 
hyperkalemia
Pedal edema, constipation
Glucose intolerance, metabolic syndrome, 
hyponatremia, hypercalcemia, hypokalemia
Depression, fatigue, reduced exercise 
tolerance, hyperglycemia, sexual 
dysfunction
Mastalgia, gynecomastia, sexual 
dysfunction, gout
Hyperkalemia
25 mg OD
Asthma, severe bradycardia, 
A-V block (grade 2 or 3), 
uncontrolled heart failure
5–40 mg OD or BD
2.5–10 mg OD
12.5–25 mg OD
12.5–50 mg OD or BD
50–100 mg OD
2.5–10 mg OD or BD
20–40 mg OD
40–80 mg OD
12.5 mg OD
100–400 mg BD
 50–100 mg OD or BD 
 5 mg OD 
Nebivolol
Spironolactone 
Metoprolol
Labetalol 
Carvedilol 
Hydrochlorothiazide
Chlorthalidone
Telmisartan
Olmesartan
Losartan 
 Ramipril
Enalapril
Amlodipine
DRUG
  Pregnancy,
  Women planning pregnancy, 
prior angioedema to ACEi, 
  Hyperkalemia, 
  Bilateral renal artery stenosis
Pregnancy, Gout
Heart failure
Hypertension is a  SILENT KILLER
as the majority of patients with high BP are asymptomatic! 
Only way to know if BP is high is to measure it accurately!
Department of Health Research
Ministry of Health and Family Welfare, Government of India
```

---

### Sampled ICMR Recommendation #9: `icmr_htn_001_c0011`

- **Document Name:** ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) (`icmr_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 1–1
- **Heading:** Treatment Protocols (ATTACC & AATTCC)
- **Section Path:** `ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) > Treatment Protocols (ATTACC & AATTCC)`
- **Population Tags:** `[]`
- **Drug Class Tags:** `["arb", "ccb", "mra_spironolactone", "thiazide"]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
SUGGESTED TREATMENT PROTOCOLS FOR BLOOD PRESSURE CONTROL:
*High BP >= 140/90 mmHg. At every visit: Check if the patient has been taking medications regularly and correctly.

PROTOCOL NO 1 (ATTACC):
- Step 1: If BP is high, prescribe Amlodipine 5mg. After 4 weeks measure BP again.
- Step 2: If still high, add Telmisartan 40mg. After 4 weeks measure BP again.
- Step 3: If still high, increase Telmisartan to 80mg. After 4 weeks measure BP again.
- Step 4: If still high, increase Amlodipine to 10mg. After 4 weeks measure BP again.
- Step 5: If still high, add Chlorthalidone 12.5mg. After 4 weeks measure BP again.
- Step 6: If still high, consider adding drugs of other classes, preferably MRA (e.g. Spironolactone).

PROTOCOL NO 2 (AATTCC):
- Step 1: If BP is high, prescribe Amlodipine 5mg. After 4 weeks measure BP again.
- Step 2: If still high, increase to Amlodipine 10mg. After 4 weeks measure BP again.
- Step 3: If still high, add Telmisartan 40mg. After 4 weeks measure BP again.
- Step 4: If still high, increase to Telmisartan 80mg. After 4 weeks measure BP again.
- Step 5: If still high, add Chlorthalidone 12.5mg. After 4 weeks measure BP again.
- Step 6: If still high, consider adding drugs of other classes, preferably MRA (e.g. Spironolactone).
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: icmr_htn_001 | PAGE 1] ===
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and 
available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by the treating physician. There will be no indemnity for direct or indirect 
consequences. Kindly visit our web portal (stw.icmr.org.in) for more information. © Indian Council of Medical Research and Department of Health Research, Ministry of Health & Family Welfare, Government of India.
Standard Treatment Workflow (STW)
HYPERTENSION IN ADULTS
ICD-11 BA00
May/2026
PHARMACOTHERAPY
MANAGEMENT OF HYPERTENSION
ACEi:  Angiotensin-converting enzyme inhibitor
ARB:  Angiotensin receptor blocker 
BP: Blood pressure
CCB: Calcium channel blocker
FDC: Fixed-dose combination
ABBREVIATIONS
REFERENCES
   
•
RISK FACTORS 
• High salt 
intake
• Sedentary 
behavior
• Tobacco and 
alcohol 
consumption
• Obesity 
DIAGNOSIS OF HYPERTENSION
• Systolic BP  ≥140 AND/OR Diastolic BP ≥ 
90 mmHg on two diﬀerent clinic visits
• Population screening BP reading may 
count as the ﬁrst reading
• Use the higher category if only Systolic or 
Diastolic BP is high, manage based on 
the higher value
• If Systolic BP is ≥160 AND/OR Diastolic BP 
≥100 measurement of one clinic visit is 
suﬃcient for diagnosing hypertension 
BLOOD PRESSURE CONTROL TARGETS 
• All adults: SBP <140 and DBP <90 
mmHg
• Diabetes mellitus, CKD, or established 
CVD: SBP <130 and DBP <80 mmHg 
(optimal target if tolerated)
• Age ≥80 years: SBP <150 and DBP <90 
mmHg 
• Assess orthostatic BP at every visit of 
adults ≥ 65 years
LIFESTYLE MODIFICATION 
• Advise all patients against tobacco 
and alcohol use
• Limit salt intake to <5g/day
• Use healthy oils, eat more 
fruits/vegetables, prefer ﬁsh/omega-3 
foods such as nuts and seeds
• Physical Activity: 30 minutes daily 
• Weight Management: Keep BMI <23 
kg/m2 and waist circumference: <90 
cm (men) and <80 cm (women)
• BP to be measured at every clinical 
visit
• Evaluate for diabetes (fasting 
plasma glucose or HbA1c) and 
manage accordingly
• Annual evaluations - Serum 
creatinine, Urine (albumin,  sugar, 
creatinine), Lipid proﬁle, 
Fundoscopy
• Additional investigations (if 
required)- ECG, ECHO    
MONITORING OF HYPERTENSION 
HYPERTENSION URGENCY
Systolic BP ≥180 AND/OR Diastolic 
BP ≥120 
with
 Symptoms of target organ damage 
• Visual disturbance, dizziness, 
confusion, headache
• Chest pain
• Breathlessness (worse lying 
down/leg swelling)
• Sudden weakness, speech/ 
swallowing diﬃculty, vision 
problem
Management
• Stabilise ABC and refer to 
emergency care at higher center
PROTOCOL NO 1 ATTACC
PROTOCOL NO 2 AATTCC
If BP is high:*
Prescribe Amlodipine 5mg
After 4 weeks measure BP again. 
If still high:
Add Telmisartan 40mg
After 4 weeks measure BP again. 
If still high:
Increase Telmisartan to 80mg
After 4 weeks measure BP again. 
If still high:
Increase Amlodipine to 10mg
After 4 weeks measure BP again. 
If still high:
Add Chlorthalidone 12.5mg
After 4 weeks measure BP again. 
If still high:
1
2
3
4
5
6
If BP is high:*
Prescribe Amlodipine 5mg
After 4 weeks measure BP again. 
If still high:
Increase to Amlodipine 10mg
After 4 weeks measure BP again. 
If still high:
Add Telmisartan 40mg
After 4 weeks measure BP again. 
If still high:
Increase to Telmisartan 80mg
After 4 weeks measure BP again. 
If still high:
Add Chlorthalidone 12.5mg
After 4 weeks measure BP again. 
If still high:
1
2
3
4
5
6
*High BP  ≥140 /90 mmHg 
At every visit: Check if the patient has been taking medications regularly and 
correctly 
Consider adding drugs of other classes, preferably MRA (eg.Spironolactone)
• Combination therapy (two drugs from two diﬀerent classes) could be the 
default initial pharmacological treatment for most adults with 
hypertension
• Single-pill combinations (SPCs/ﬁxed-dose combinations, FDCs) are 
preferred over multiple pills to improve adherence
• Monotherapy remains appropriate only for (a) low-risk Grade 1 HTN, (b) 
elderly ≥ 80 years, or (c) frail patients
• A CCB or Thiazide/Thiazide-like diuretic should be used with a 
Renin-Angiotensin-Aldosterone System (RAAS) blocker (either an ACEi or 
an ARB)
• Three-drug combination, often a RAAS blocker, CCB, or a 
Thiazide/Thiazide-like diuretic, if blood pressure is not controlled with the 
initial two-drug combination
• β-blockers are appropriate in cases of angina, postmyocardial infarction, 
heart failure (HFrEF or HFpEF with ischemia)
• DO NOT combine two RAAS blockers as it increases the risk of adverse 
eﬀects, including acute kidney injury (AKI)
PHARMACOLOGICAL STRATEGY    
SUGGESTED TREATMENT PROTOCOLS 
• Systolic BP ≥180 AND/OR Diastolic ≥
120 mmHg
        AND
• No signs of acute target-organ 
damage
Management 
• Start oral antihypertensive drugs
• Do NOT use IV medicines
• Reduce BP gradually over 24–48 hours
• Refer/admit if symptoms or organ 
damage suspected
• Follow-up within 1 week
  ALL ADULTS  ≥ 18 YEARS SHOULD GET BLOOD PRESSURE MEASURED AT EVERY CLINIC VISIT
1. Mancia G, Kreutz R, Brunström M, et al. 2023 ESH Guidelines for the management of arterial hypertension. J Hypertens. 2023;41(12):1874–2071. doi:10.1097/HJH.0000000000003480 PMID: 37345492
2. Joseph G, Thanh Pham V, Kragh Andersen P, et al. Cardiovascular events according to blood pressure thresholds recommended by ACC/AHA. Blood Press. 2024;33(1):2380346. 
doi:10.1080/08037051.2024.2380346 PMID: 39018201
3. Gupta R, Maheshwari A, Verma N, Narasingan SN, Tripathi K, Joshi S, Manoria PC, et al. Indian Society of Hypertension (InSH) Consensus Guideline for the Management of Hypertension, 2025. 
Hypertension Journal. 2025;11(4):76–138. doi:10.61081/htnj/25v11i401.
4. Ministry of Health and Family Welfare, Government of India. Training modules on non-communicable diseases. New Delhi: MoHFW; 2025.
5. ICMR-National Institute of Epidemiology. India Hypertension Control Initiative: Training modules. Chennai, 2021.
HFrEF: Heart failure with reduced ejection fraction
HFpEF: Heart Failure with Preserved Ejection
OD: Once Daily
MRA: Mineralocorticoid Receptor Antagonist
RAAS:  Renin Angiotensin-Aldosterone System
CLASSIFICATION
Normal
Elevated BP
Hypertension 
Grade 1
Hypertension 
Grade 2
Hypertension 
Grade 3
ACTION
Reassure and 
encourage healthy 
lifestyle
Lifestyle 
modiﬁcation
Pharmacological
management+ 
Lifestyle 
modiﬁcation
BLOOD PRESSURE LEVELS
Systolic <120 AND 
Diastolic<80
Systolic 120-139 AND/ OR 
Diastolic 80-89
Systolic 140-159 AND/ OR 
Diastolic 90-99
Systolic 160-179 AND/ OR 
Diastolic 100-109
Systolic ≥ 180 AND/ OR 
Diastolic ≥ 110
 RED FLAGS SIGNS
DRUG CLASS
CONTRAINDICATIONS
DOSES
SIDE EFFECTS
ACE inhibitors
ARB
CCB
Diuretics
Beta-blockers
Aldosterone antagonist
Dry cough, angioedema, hyperkalemia 
rise in serum creatinine 
Hypotension, acute renal failure, 
hyperkalemia
Pedal edema, constipation
Glucose intolerance, metabolic syndrome, 
hyponatremia, hypercalcemia, hypokalemia
Depression, fatigue, reduced exercise 
tolerance, hyperglycemia, sexual 
dysfunction
Mastalgia, gynecomastia, sexual 
dysfunction, gout
Hyperkalemia
25 mg OD
Asthma, severe bradycardia, 
A-V block (grade 2 or 3), 
uncontrolled heart failure
5–40 mg OD or BD
2.5–10 mg OD
12.5–25 mg OD
12.5–50 mg OD or BD
50–100 mg OD
2.5–10 mg OD or BD
20–40 mg OD
40–80 mg OD
12.5 mg OD
100–400 mg BD
 50–100 mg OD or BD 
 5 mg OD 
Nebivolol
Spironolactone 
Metoprolol
Labetalol 
Carvedilol 
Hydrochlorothiazide
Chlorthalidone
Telmisartan
Olmesartan
Losartan 
 Ramipril
Enalapril
Amlodipine
DRUG
  Pregnancy,
  Women planning pregnancy, 
prior angioedema to ACEi, 
  Hyperkalemia, 
  Bilateral renal artery stenosis
Pregnancy, Gout
Heart failure
Hypertension is a  SILENT KILLER
as the majority of patients with high BP are asymptomatic! 
Only way to know if BP is high is to measure it accurately!
Department of Health Research
Ministry of Health and Family Welfare, Government of India
```

---

### Sampled ICMR Recommendation #10: `icmr_t2dm_001_c0007`

- **Document Name:** ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11) (`icmr_t2dm_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `both`
- **Indexed For Retrieval:** `True`
- **Page Range:** 1–1
- **Heading:** Screening for Diabetes Mellitus
- **Section Path:** `ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11) > Screening for Diabetes Mellitus`
- **Population Tags:** `["cardiovascular_disease", "pregnancy"]`
- **Drug Class Tags:** `["insulin"]`
- **Applicability Conditions:** `["In pregnant women: screen 1st trimester with FPG; 75g OGTT at 24-28 weeks if normal", "In overweight or obese adults (BMI >= 23 kg/m2) with risk factors"]`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
SCREENING FOR DIABETES MELLITUS:
1. IN PREGNANCY:
- All pregnant women to be screened in 1st trimester with FPG.
- FPG >= 126 mg/dl and/or HbA1c >= 6.5% to be considered pre-existing diabetes.
- FPG between 92–125 mg/dl to be considered as GDM.
- All women with normal screening in 1st trimester to get a 75g oral glucose tolerance test (OGTT) at 24–28 weeks.
- All GDM women to be tested 6 weeks post-partum and once every 3 years.

2. IN AN APPARENTLY NORMAL ADULT:
- In obese or overweight (BMI >= 27.5 or >= 23 kg/m2) with risk factors: first degree relative with diabetes, history of CVD, BP >= 140/90 mmHg, dyslipidemia (TG > 250 mg/dL, HDL < 40 male, < 50 female), physical inactivity, PCOS, insulin resistance (acanthosis nigricans), age > 30 years, previous history of GDM.

3. IN AN ADULT WITH ILLNESS:
- Osmotic symptoms, unexplained weight loss, acute coronary syndrome, deep seated infections (pneumonia, tuberculosis, pyelonephritis), recurrent infections (oral thrush, cellulitis, UTI), non-healing ulcers.
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: icmr_t2dm_001 | PAGE 1] ===
Standard Treatment Workﬂow (STW)
DIABETES MELLITUS TYPE 2
ICD-10-E11
      KEEP LOW THRESHOLD FOR DIAGNOSIS. MAKE SURE TO FOLLOW UP TO MEET TARGETS
ABBREVIATIONS
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and 
are based on expert opinions and available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by 
the treating physician. There will be no indemnity for direct or indirect consequences. Kindly visit the website of DHR for more information: (stw.icmr.org.in) for more information.
©Department of Health Research, Ministry of Health & Family Welfare, Government of India.
Osmotic 
symptoms
ie., polyuria, 
polydipsia and 
polyphagia 
May be asymptomatic
Weight loss
Non healing 
wounds
Paraesthesia
Recurrent 
infections
Blurring of 
vision
DIAGNOSIS
EXAMINATION:
BMI 
waist 
circumference
BP Peripheral 
pulses
Hypertension
Dyslipidaemia CAD CKD
Skin, oral 
cavity, foot 
Fundus 
(dilated) 
examination
ASSESS
INVESTIGATION
• HbA1c 
• Creatinine 
• K+
• Fasting lipid proﬁle
• Urine routine examination 
and spot albumin: creatinine 
ratio#
• LFT/ ALT, AST
• ECG
• Others like Echo, USG 
abdomen as indicated
#These may best be carried 
out after initial glycaemic 
control 
METABOLIC TARGETS
• HbA1c </= 7 .0% (except elderly and 
those with signiﬁcant comorbid 
conditions) where higher target may 
be acceptable
• Pre-prandial capillary plasma 
glucose: 80-130 mg/dl
• Post-prandial capillary plasma 
glucose: <180 mg/dl
• BP=140/90 (130/80 in CKD) LDL: < 100 
mg/dl (< 70mg/dl in CAD)
TREATMENT
• Dietary modiﬁcation
• Avoidance of tobacco and restriction/ 
avoidance of alcohol
• Physical activity
• Pharmacotherapy:
› HbA1c < 8.5%: Monotherapy- Metformin
› HbA1c 8.5-10%: Dual therapy- Metformin 
+ SU’s/TZD/ DPPIVi/SGLT2i /AGI/GLP-1RA
› HbA1c > 10%: Basal Insulin+ Metformin + 
another OAD / triple OAD combination
OR
OR
OR
CO-MORBIDITIES:
SYMPTOMS
SCREENING FOR DIABETES MELLITUS
IN PREGNANCY
• H/O GDM/Pre-existing diabetes
• All pregnant women to be screened in 1st trimester with FPG
• FPG ≥ 126 and/or HbA1c ≥ 6.5% to be considered pre-existing diabetes
• FPG between 92-125 to be considered as GDM
• All those women with normal screening in 1st trimester to get a 75 g-oral 
glucose tolerance test done at 24-28 weeks
• All GDM women to be tested 6 weeks post-partum and once every 3 years
• PREDIABETES: should be tested yearly 
IN AN APPARENTLY NORMAL ADULT
• In obese or overweight (BMI ≥ 27.5 
or ≥ 23 kg/m2) with any of the 
following risk factors
• First degree relative with diabetes
• History of cardiovascular disease
• BP (≥ 140/90 mmHg)
• Dyslipidemia (TG > 250 mg/dL, 
HDL <40 mg/dl in male, <50 mg/dl 
in female
• Physical inactivity
• Polycystic ovary syndrome (PCOS)
• Insulin resistance (acanthosis 
nigricans)
• Adults > 30 years of age
• Previous history of GDM
  IN AN ADULT WITH ILLNESS
• In any adult/adolescent who presents with one of the following 
illness/complaints
• Osmotic symptoms (polyuria, polydipsia, polyphagia, nocturia)
• Unexplained weight loss
• Unexplained depression or dementia
• Acute coronary syndrome
• Deep seated infections (liver abscess, lower lobe pneumonia, tuberculosis, 
pyelonephritis, abscesses, septic arthritis, osteomyelitis)
• Recurrent infections (tinea, oral thrush, onychomycosis, cystitis-urinary 
tract infection, sinusitis, STI, cellulitis, carbuncle)
• Non-healing ulcers (foot ulcers-infected/neuropathic)
• Exogenous/iatrogenic Cushing’s syndrome
Department of Health Research
Ministry of Health and Family Welfare, Government of India
PREDIABETES: 
Impaired fasting glucose: FPG 100-125 mg/dL; Impaired 
glucose tolerance: 140-199 mg/dL; HbA1c 5.7-6.4%
ALT: Alanine transaminase
AST: Aspartate aminotransferase
BMI: Body mass index
BP: Blood pressure
CAD: Coronary artery disease
CGM: Continuous glucose monitor
CKD: Chronic kidney disease
DTR: Deep tendon reﬂex
ECG: Electrocardiogram
FPG: Fasting plasma glucose
GDM: Gestational diabetes mellitus
HDL: High-density lipoprotein
LDL: Low-density lipoprotein
LFT: Liver function test
OAD: Oral antidiabetic drug
OGTT: Oral glucose tolerance test
SMBG: Self-monitoring of blood 
           glucose
TG: Triglyceride
• Endocrinology: for uncontrolled hyperglycemia
• Ophthalmology: at initial evaluation and every year 
• Nephrology: for deranged renal function
• Cardiology: for CAD/HF/arrhythmia
REFERRALS
MONITORING
• Blood glucose; FPG and 2 hours PPG once monthly 
more frequent as required including SMBG or CGM
• HbA1c every 6-12 months ( 3 monthly if uncontrolled)
• Annual monitoring : ECG, urine ACR (albumin 
creatinine ratio),dilated fundoscopy,foot examination
Pin-prick 
sensation, 
monoﬁlament 
test ,vibration, 
DTR
FPG ≥126 
mg/dl 
(after 8hr 
fasting)
2-h plasma
 glucose ≥200
 mg/dl 
during OGTT
HbA1C ≥
6.5%
Diabetes 
symptoms  
+ random 
plasma 
glucose ≥
200 mg/dl
July/ 2022
```

---

### Sampled ICMR Recommendation #11: `icmr_htn_001_c0009`

- **Document Name:** ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) (`icmr_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 1–1
- **Heading:** Hypertension Urgency and Emergency
- **Section Path:** `ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) > Hypertension Urgency and Emergency`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `null`
- **Exceptions:** `["Do not use IV medicines for asymptomatic hypertension urgency"]`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
HYPERTENSION URGENCY & EMERGENCY:
Definition: Systolic BP >= 180 AND/OR Diastolic BP >= 120 mmHg.

Red Flags / Symptoms of target organ damage:
- Visual disturbance, dizziness, confusion, headache, chest pain, breathlessness (worse lying down/leg swelling), sudden weakness, speech/swallowing difficulty, vision problem.
- Management: Stabilise ABC and refer to emergency care at higher center.

Hypertension Urgency (Without acute target-organ damage):
- Management: Start oral antihypertensive drugs. Do NOT use IV medicines. Reduce BP gradually over 24-48 hours. Refer/admit if symptoms or organ damage suspected. Follow-up within 1 week.
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: icmr_htn_001 | PAGE 1] ===
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and 
available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by the treating physician. There will be no indemnity for direct or indirect 
consequences. Kindly visit our web portal (stw.icmr.org.in) for more information. © Indian Council of Medical Research and Department of Health Research, Ministry of Health & Family Welfare, Government of India.
Standard Treatment Workflow (STW)
HYPERTENSION IN ADULTS
ICD-11 BA00
May/2026
PHARMACOTHERAPY
MANAGEMENT OF HYPERTENSION
ACEi:  Angiotensin-converting enzyme inhibitor
ARB:  Angiotensin receptor blocker 
BP: Blood pressure
CCB: Calcium channel blocker
FDC: Fixed-dose combination
ABBREVIATIONS
REFERENCES
   
•
RISK FACTORS 
• High salt 
intake
• Sedentary 
behavior
• Tobacco and 
alcohol 
consumption
• Obesity 
DIAGNOSIS OF HYPERTENSION
• Systolic BP  ≥140 AND/OR Diastolic BP ≥ 
90 mmHg on two diﬀerent clinic visits
• Population screening BP reading may 
count as the ﬁrst reading
• Use the higher category if only Systolic or 
Diastolic BP is high, manage based on 
the higher value
• If Systolic BP is ≥160 AND/OR Diastolic BP 
≥100 measurement of one clinic visit is 
suﬃcient for diagnosing hypertension 
BLOOD PRESSURE CONTROL TARGETS 
• All adults: SBP <140 and DBP <90 
mmHg
• Diabetes mellitus, CKD, or established 
CVD: SBP <130 and DBP <80 mmHg 
(optimal target if tolerated)
• Age ≥80 years: SBP <150 and DBP <90 
mmHg 
• Assess orthostatic BP at every visit of 
adults ≥ 65 years
LIFESTYLE MODIFICATION 
• Advise all patients against tobacco 
and alcohol use
• Limit salt intake to <5g/day
• Use healthy oils, eat more 
fruits/vegetables, prefer ﬁsh/omega-3 
foods such as nuts and seeds
• Physical Activity: 30 minutes daily 
• Weight Management: Keep BMI <23 
kg/m2 and waist circumference: <90 
cm (men) and <80 cm (women)
• BP to be measured at every clinical 
visit
• Evaluate for diabetes (fasting 
plasma glucose or HbA1c) and 
manage accordingly
• Annual evaluations - Serum 
creatinine, Urine (albumin,  sugar, 
creatinine), Lipid proﬁle, 
Fundoscopy
• Additional investigations (if 
required)- ECG, ECHO    
MONITORING OF HYPERTENSION 
HYPERTENSION URGENCY
Systolic BP ≥180 AND/OR Diastolic 
BP ≥120 
with
 Symptoms of target organ damage 
• Visual disturbance, dizziness, 
confusion, headache
• Chest pain
• Breathlessness (worse lying 
down/leg swelling)
• Sudden weakness, speech/ 
swallowing diﬃculty, vision 
problem
Management
• Stabilise ABC and refer to 
emergency care at higher center
PROTOCOL NO 1 ATTACC
PROTOCOL NO 2 AATTCC
If BP is high:*
Prescribe Amlodipine 5mg
After 4 weeks measure BP again. 
If still high:
Add Telmisartan 40mg
After 4 weeks measure BP again. 
If still high:
Increase Telmisartan to 80mg
After 4 weeks measure BP again. 
If still high:
Increase Amlodipine to 10mg
After 4 weeks measure BP again. 
If still high:
Add Chlorthalidone 12.5mg
After 4 weeks measure BP again. 
If still high:
1
2
3
4
5
6
If BP is high:*
Prescribe Amlodipine 5mg
After 4 weeks measure BP again. 
If still high:
Increase to Amlodipine 10mg
After 4 weeks measure BP again. 
If still high:
Add Telmisartan 40mg
After 4 weeks measure BP again. 
If still high:
Increase to Telmisartan 80mg
After 4 weeks measure BP again. 
If still high:
Add Chlorthalidone 12.5mg
After 4 weeks measure BP again. 
If still high:
1
2
3
4
5
6
*High BP  ≥140 /90 mmHg 
At every visit: Check if the patient has been taking medications regularly and 
correctly 
Consider adding drugs of other classes, preferably MRA (eg.Spironolactone)
• Combination therapy (two drugs from two diﬀerent classes) could be the 
default initial pharmacological treatment for most adults with 
hypertension
• Single-pill combinations (SPCs/ﬁxed-dose combinations, FDCs) are 
preferred over multiple pills to improve adherence
• Monotherapy remains appropriate only for (a) low-risk Grade 1 HTN, (b) 
elderly ≥ 80 years, or (c) frail patients
• A CCB or Thiazide/Thiazide-like diuretic should be used with a 
Renin-Angiotensin-Aldosterone System (RAAS) blocker (either an ACEi or 
an ARB)
• Three-drug combination, often a RAAS blocker, CCB, or a 
Thiazide/Thiazide-like diuretic, if blood pressure is not controlled with the 
initial two-drug combination
• β-blockers are appropriate in cases of angina, postmyocardial infarction, 
heart failure (HFrEF or HFpEF with ischemia)
• DO NOT combine two RAAS blockers as it increases the risk of adverse 
eﬀects, including acute kidney injury (AKI)
PHARMACOLOGICAL STRATEGY    
SUGGESTED TREATMENT PROTOCOLS 
• Systolic BP ≥180 AND/OR Diastolic ≥
120 mmHg
        AND
• No signs of acute target-organ 
damage
Management 
• Start oral antihypertensive drugs
• Do NOT use IV medicines
• Reduce BP gradually over 24–48 hours
• Refer/admit if symptoms or organ 
damage suspected
• Follow-up within 1 week
  ALL ADULTS  ≥ 18 YEARS SHOULD GET BLOOD PRESSURE MEASURED AT EVERY CLINIC VISIT
1. Mancia G, Kreutz R, Brunström M, et al. 2023 ESH Guidelines for the management of arterial hypertension. J Hypertens. 2023;41(12):1874–2071. doi:10.1097/HJH.0000000000003480 PMID: 37345492
2. Joseph G, Thanh Pham V, Kragh Andersen P, et al. Cardiovascular events according to blood pressure thresholds recommended by ACC/AHA. Blood Press. 2024;33(1):2380346. 
doi:10.1080/08037051.2024.2380346 PMID: 39018201
3. Gupta R, Maheshwari A, Verma N, Narasingan SN, Tripathi K, Joshi S, Manoria PC, et al. Indian Society of Hypertension (InSH) Consensus Guideline for the Management of Hypertension, 2025. 
Hypertension Journal. 2025;11(4):76–138. doi:10.61081/htnj/25v11i401.
4. Ministry of Health and Family Welfare, Government of India. Training modules on non-communicable diseases. New Delhi: MoHFW; 2025.
5. ICMR-National Institute of Epidemiology. India Hypertension Control Initiative: Training modules. Chennai, 2021.
HFrEF: Heart failure with reduced ejection fraction
HFpEF: Heart Failure with Preserved Ejection
OD: Once Daily
MRA: Mineralocorticoid Receptor Antagonist
RAAS:  Renin Angiotensin-Aldosterone System
CLASSIFICATION
Normal
Elevated BP
Hypertension 
Grade 1
Hypertension 
Grade 2
Hypertension 
Grade 3
ACTION
Reassure and 
encourage healthy 
lifestyle
Lifestyle 
modiﬁcation
Pharmacological
management+ 
Lifestyle 
modiﬁcation
BLOOD PRESSURE LEVELS
Systolic <120 AND 
Diastolic<80
Systolic 120-139 AND/ OR 
Diastolic 80-89
Systolic 140-159 AND/ OR 
Diastolic 90-99
Systolic 160-179 AND/ OR 
Diastolic 100-109
Systolic ≥ 180 AND/ OR 
Diastolic ≥ 110
 RED FLAGS SIGNS
DRUG CLASS
CONTRAINDICATIONS
DOSES
SIDE EFFECTS
ACE inhibitors
ARB
CCB
Diuretics
Beta-blockers
Aldosterone antagonist
Dry cough, angioedema, hyperkalemia 
rise in serum creatinine 
Hypotension, acute renal failure, 
hyperkalemia
Pedal edema, constipation
Glucose intolerance, metabolic syndrome, 
hyponatremia, hypercalcemia, hypokalemia
Depression, fatigue, reduced exercise 
tolerance, hyperglycemia, sexual 
dysfunction
Mastalgia, gynecomastia, sexual 
dysfunction, gout
Hyperkalemia
25 mg OD
Asthma, severe bradycardia, 
A-V block (grade 2 or 3), 
uncontrolled heart failure
5–40 mg OD or BD
2.5–10 mg OD
12.5–25 mg OD
12.5–50 mg OD or BD
50–100 mg OD
2.5–10 mg OD or BD
20–40 mg OD
40–80 mg OD
12.5 mg OD
100–400 mg BD
 50–100 mg OD or BD 
 5 mg OD 
Nebivolol
Spironolactone 
Metoprolol
Labetalol 
Carvedilol 
Hydrochlorothiazide
Chlorthalidone
Telmisartan
Olmesartan
Losartan 
 Ramipril
Enalapril
Amlodipine
DRUG
  Pregnancy,
  Women planning pregnancy, 
prior angioedema to ACEi, 
  Hyperkalemia, 
  Bilateral renal artery stenosis
Pregnancy, Gout
Heart failure
Hypertension is a  SILENT KILLER
as the majority of patients with high BP are asymptomatic! 
Only way to know if BP is high is to measure it accurately!
Department of Health Research
Ministry of Health and Family Welfare, Government of India
```

---

### Sampled ICMR Recommendation #12: `icmr_htn_001_c0006`

- **Document Name:** ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) (`icmr_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `both`
- **Indexed For Retrieval:** `True`
- **Page Range:** 1–1
- **Heading:** Blood Pressure Control Targets
- **Section Path:** `ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) > Blood Pressure Control Targets`
- **Population Tags:** `["cardiovascular_disease", "chronic_kidney_disease", "elderly", "type_2_diabetes"]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `["In patients with diabetes mellitus, CKD, or established CVD: SBP < 130 and DBP < 80 mmHg", "For adults aged >= 80 years: SBP < 150 and DBP < 90 mmHg"]`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
BLOOD PRESSURE CONTROL TARGETS:
- All adults: SBP < 140 and DBP < 90 mmHg.
- Diabetes mellitus, CKD, or established CVD: SBP < 130 and DBP < 80 mmHg (optimal target if tolerated).
- Age >= 80 years: SBP < 150 and DBP < 90 mmHg.
- Assess orthostatic BP at every visit of adults >= 65 years.
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: icmr_htn_001 | PAGE 1] ===
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and 
available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by the treating physician. There will be no indemnity for direct or indirect 
consequences. Kindly visit our web portal (stw.icmr.org.in) for more information. © Indian Council of Medical Research and Department of Health Research, Ministry of Health & Family Welfare, Government of India.
Standard Treatment Workflow (STW)
HYPERTENSION IN ADULTS
ICD-11 BA00
May/2026
PHARMACOTHERAPY
MANAGEMENT OF HYPERTENSION
ACEi:  Angiotensin-converting enzyme inhibitor
ARB:  Angiotensin receptor blocker 
BP: Blood pressure
CCB: Calcium channel blocker
FDC: Fixed-dose combination
ABBREVIATIONS
REFERENCES
   
•
RISK FACTORS 
• High salt 
intake
• Sedentary 
behavior
• Tobacco and 
alcohol 
consumption
• Obesity 
DIAGNOSIS OF HYPERTENSION
• Systolic BP  ≥140 AND/OR Diastolic BP ≥ 
90 mmHg on two diﬀerent clinic visits
• Population screening BP reading may 
count as the ﬁrst reading
• Use the higher category if only Systolic or 
Diastolic BP is high, manage based on 
the higher value
• If Systolic BP is ≥160 AND/OR Diastolic BP 
≥100 measurement of one clinic visit is 
suﬃcient for diagnosing hypertension 
BLOOD PRESSURE CONTROL TARGETS 
• All adults: SBP <140 and DBP <90 
mmHg
• Diabetes mellitus, CKD, or established 
CVD: SBP <130 and DBP <80 mmHg 
(optimal target if tolerated)
• Age ≥80 years: SBP <150 and DBP <90 
mmHg 
• Assess orthostatic BP at every visit of 
adults ≥ 65 years
LIFESTYLE MODIFICATION 
• Advise all patients against tobacco 
and alcohol use
• Limit salt intake to <5g/day
• Use healthy oils, eat more 
fruits/vegetables, prefer ﬁsh/omega-3 
foods such as nuts and seeds
• Physical Activity: 30 minutes daily 
• Weight Management: Keep BMI <23 
kg/m2 and waist circumference: <90 
cm (men) and <80 cm (women)
• BP to be measured at every clinical 
visit
• Evaluate for diabetes (fasting 
plasma glucose or HbA1c) and 
manage accordingly
• Annual evaluations - Serum 
creatinine, Urine (albumin,  sugar, 
creatinine), Lipid proﬁle, 
Fundoscopy
• Additional investigations (if 
required)- ECG, ECHO    
MONITORING OF HYPERTENSION 
HYPERTENSION URGENCY
Systolic BP ≥180 AND/OR Diastolic 
BP ≥120 
with
 Symptoms of target organ damage 
• Visual disturbance, dizziness, 
confusion, headache
• Chest pain
• Breathlessness (worse lying 
down/leg swelling)
• Sudden weakness, speech/ 
swallowing diﬃculty, vision 
problem
Management
• Stabilise ABC and refer to 
emergency care at higher center
PROTOCOL NO 1 ATTACC
PROTOCOL NO 2 AATTCC
If BP is high:*
Prescribe Amlodipine 5mg
After 4 weeks measure BP again. 
If still high:
Add Telmisartan 40mg
After 4 weeks measure BP again. 
If still high:
Increase Telmisartan to 80mg
After 4 weeks measure BP again. 
If still high:
Increase Amlodipine to 10mg
After 4 weeks measure BP again. 
If still high:
Add Chlorthalidone 12.5mg
After 4 weeks measure BP again. 
If still high:
1
2
3
4
5
6
If BP is high:*
Prescribe Amlodipine 5mg
After 4 weeks measure BP again. 
If still high:
Increase to Amlodipine 10mg
After 4 weeks measure BP again. 
If still high:
Add Telmisartan 40mg
After 4 weeks measure BP again. 
If still high:
Increase to Telmisartan 80mg
After 4 weeks measure BP again. 
If still high:
Add Chlorthalidone 12.5mg
After 4 weeks measure BP again. 
If still high:
1
2
3
4
5
6
*High BP  ≥140 /90 mmHg 
At every visit: Check if the patient has been taking medications regularly and 
correctly 
Consider adding drugs of other classes, preferably MRA (eg.Spironolactone)
• Combination therapy (two drugs from two diﬀerent classes) could be the 
default initial pharmacological treatment for most adults with 
hypertension
• Single-pill combinations (SPCs/ﬁxed-dose combinations, FDCs) are 
preferred over multiple pills to improve adherence
• Monotherapy remains appropriate only for (a) low-risk Grade 1 HTN, (b) 
elderly ≥ 80 years, or (c) frail patients
• A CCB or Thiazide/Thiazide-like diuretic should be used with a 
Renin-Angiotensin-Aldosterone System (RAAS) blocker (either an ACEi or 
an ARB)
• Three-drug combination, often a RAAS blocker, CCB, or a 
Thiazide/Thiazide-like diuretic, if blood pressure is not controlled with the 
initial two-drug combination
• β-blockers are appropriate in cases of angina, postmyocardial infarction, 
heart failure (HFrEF or HFpEF with ischemia)
• DO NOT combine two RAAS blockers as it increases the risk of adverse 
eﬀects, including acute kidney injury (AKI)
PHARMACOLOGICAL STRATEGY    
SUGGESTED TREATMENT PROTOCOLS 
• Systolic BP ≥180 AND/OR Diastolic ≥
120 mmHg
        AND
• No signs of acute target-organ 
damage
Management 
• Start oral antihypertensive drugs
• Do NOT use IV medicines
• Reduce BP gradually over 24–48 hours
• Refer/admit if symptoms or organ 
damage suspected
• Follow-up within 1 week
  ALL ADULTS  ≥ 18 YEARS SHOULD GET BLOOD PRESSURE MEASURED AT EVERY CLINIC VISIT
1. Mancia G, Kreutz R, Brunström M, et al. 2023 ESH Guidelines for the management of arterial hypertension. J Hypertens. 2023;41(12):1874–2071. doi:10.1097/HJH.0000000000003480 PMID: 37345492
2. Joseph G, Thanh Pham V, Kragh Andersen P, et al. Cardiovascular events according to blood pressure thresholds recommended by ACC/AHA. Blood Press. 2024;33(1):2380346. 
doi:10.1080/08037051.2024.2380346 PMID: 39018201
3. Gupta R, Maheshwari A, Verma N, Narasingan SN, Tripathi K, Joshi S, Manoria PC, et al. Indian Society of Hypertension (InSH) Consensus Guideline for the Management of Hypertension, 2025. 
Hypertension Journal. 2025;11(4):76–138. doi:10.61081/htnj/25v11i401.
4. Ministry of Health and Family Welfare, Government of India. Training modules on non-communicable diseases. New Delhi: MoHFW; 2025.
5. ICMR-National Institute of Epidemiology. India Hypertension Control Initiative: Training modules. Chennai, 2021.
HFrEF: Heart failure with reduced ejection fraction
HFpEF: Heart Failure with Preserved Ejection
OD: Once Daily
MRA: Mineralocorticoid Receptor Antagonist
RAAS:  Renin Angiotensin-Aldosterone System
CLASSIFICATION
Normal
Elevated BP
Hypertension 
Grade 1
Hypertension 
Grade 2
Hypertension 
Grade 3
ACTION
Reassure and 
encourage healthy 
lifestyle
Lifestyle 
modiﬁcation
Pharmacological
management+ 
Lifestyle 
modiﬁcation
BLOOD PRESSURE LEVELS
Systolic <120 AND 
Diastolic<80
Systolic 120-139 AND/ OR 
Diastolic 80-89
Systolic 140-159 AND/ OR 
Diastolic 90-99
Systolic 160-179 AND/ OR 
Diastolic 100-109
Systolic ≥ 180 AND/ OR 
Diastolic ≥ 110
 RED FLAGS SIGNS
DRUG CLASS
CONTRAINDICATIONS
DOSES
SIDE EFFECTS
ACE inhibitors
ARB
CCB
Diuretics
Beta-blockers
Aldosterone antagonist
Dry cough, angioedema, hyperkalemia 
rise in serum creatinine 
Hypotension, acute renal failure, 
hyperkalemia
Pedal edema, constipation
Glucose intolerance, metabolic syndrome, 
hyponatremia, hypercalcemia, hypokalemia
Depression, fatigue, reduced exercise 
tolerance, hyperglycemia, sexual 
dysfunction
Mastalgia, gynecomastia, sexual 
dysfunction, gout
Hyperkalemia
25 mg OD
Asthma, severe bradycardia, 
A-V block (grade 2 or 3), 
uncontrolled heart failure
5–40 mg OD or BD
2.5–10 mg OD
12.5–25 mg OD
12.5–50 mg OD or BD
50–100 mg OD
2.5–10 mg OD or BD
20–40 mg OD
40–80 mg OD
12.5 mg OD
100–400 mg BD
 50–100 mg OD or BD 
 5 mg OD 
Nebivolol
Spironolactone 
Metoprolol
Labetalol 
Carvedilol 
Hydrochlorothiazide
Chlorthalidone
Telmisartan
Olmesartan
Losartan 
 Ramipril
Enalapril
Amlodipine
DRUG
  Pregnancy,
  Women planning pregnancy, 
prior angioedema to ACEi, 
  Hyperkalemia, 
  Bilateral renal artery stenosis
Pregnancy, Gout
Heart failure
Hypertension is a  SILENT KILLER
as the majority of patients with high BP are asymptomatic! 
Only way to know if BP is high is to measure it accurately!
Department of Health Research
Ministry of Health and Family Welfare, Government of India
```

---

### Sampled ICMR Recommendation #13: `icmr_htn_001_c0010`

- **Document Name:** ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) (`icmr_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 1–1
- **Heading:** Pharmacological Strategy
- **Section Path:** `ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) > Pharmacological Strategy`
- **Population Tags:** `["cardiovascular_disease", "elderly"]`
- **Drug Class Tags:** `["ace_inhibitor", "arb", "beta_blocker", "ccb", "thiazide"]`
- **Applicability Conditions:** `null`
- **Exceptions:** `["DO NOT combine two RAAS blockers as it increases the risk of adverse effects, including acute kidney injury (AKI)"]`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
PHARMACOLOGICAL STRATEGY FOR HYPERTENSION:
- Combination therapy (two drugs from two different classes) could be the default initial pharmacological treatment for most adults with hypertension.
- Single-pill combinations (SPCs/fixed-dose combinations, FDCs) are preferred over multiple pills to improve adherence.
- Monotherapy remains appropriate only for (a) low-risk Grade 1 HTN, (b) elderly >= 80 years, or (c) frail patients.
- A CCB or Thiazide/Thiazide-like diuretic should be used with a Renin-Angiotensin-Aldosterone System (RAAS) blocker (either an ACEi or an ARB).
- Three-drug combination, often a RAAS blocker, CCB, or a Thiazide/Thiazide-like diuretic, if blood pressure is not controlled with the initial two-drug combination.
- Beta-blockers are appropriate in cases of angina, postmyocardial infarction, heart failure (HFrEF or HFpEF with ischemia).
- DO NOT combine two RAAS blockers as it increases the risk of adverse effects, including acute kidney injury (AKI).
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: icmr_htn_001 | PAGE 1] ===
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and 
available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by the treating physician. There will be no indemnity for direct or indirect 
consequences. Kindly visit our web portal (stw.icmr.org.in) for more information. © Indian Council of Medical Research and Department of Health Research, Ministry of Health & Family Welfare, Government of India.
Standard Treatment Workflow (STW)
HYPERTENSION IN ADULTS
ICD-11 BA00
May/2026
PHARMACOTHERAPY
MANAGEMENT OF HYPERTENSION
ACEi:  Angiotensin-converting enzyme inhibitor
ARB:  Angiotensin receptor blocker 
BP: Blood pressure
CCB: Calcium channel blocker
FDC: Fixed-dose combination
ABBREVIATIONS
REFERENCES
   
•
RISK FACTORS 
• High salt 
intake
• Sedentary 
behavior
• Tobacco and 
alcohol 
consumption
• Obesity 
DIAGNOSIS OF HYPERTENSION
• Systolic BP  ≥140 AND/OR Diastolic BP ≥ 
90 mmHg on two diﬀerent clinic visits
• Population screening BP reading may 
count as the ﬁrst reading
• Use the higher category if only Systolic or 
Diastolic BP is high, manage based on 
the higher value
• If Systolic BP is ≥160 AND/OR Diastolic BP 
≥100 measurement of one clinic visit is 
suﬃcient for diagnosing hypertension 
BLOOD PRESSURE CONTROL TARGETS 
• All adults: SBP <140 and DBP <90 
mmHg
• Diabetes mellitus, CKD, or established 
CVD: SBP <130 and DBP <80 mmHg 
(optimal target if tolerated)
• Age ≥80 years: SBP <150 and DBP <90 
mmHg 
• Assess orthostatic BP at every visit of 
adults ≥ 65 years
LIFESTYLE MODIFICATION 
• Advise all patients against tobacco 
and alcohol use
• Limit salt intake to <5g/day
• Use healthy oils, eat more 
fruits/vegetables, prefer ﬁsh/omega-3 
foods such as nuts and seeds
• Physical Activity: 30 minutes daily 
• Weight Management: Keep BMI <23 
kg/m2 and waist circumference: <90 
cm (men) and <80 cm (women)
• BP to be measured at every clinical 
visit
• Evaluate for diabetes (fasting 
plasma glucose or HbA1c) and 
manage accordingly
• Annual evaluations - Serum 
creatinine, Urine (albumin,  sugar, 
creatinine), Lipid proﬁle, 
Fundoscopy
• Additional investigations (if 
required)- ECG, ECHO    
MONITORING OF HYPERTENSION 
HYPERTENSION URGENCY
Systolic BP ≥180 AND/OR Diastolic 
BP ≥120 
with
 Symptoms of target organ damage 
• Visual disturbance, dizziness, 
confusion, headache
• Chest pain
• Breathlessness (worse lying 
down/leg swelling)
• Sudden weakness, speech/ 
swallowing diﬃculty, vision 
problem
Management
• Stabilise ABC and refer to 
emergency care at higher center
PROTOCOL NO 1 ATTACC
PROTOCOL NO 2 AATTCC
If BP is high:*
Prescribe Amlodipine 5mg
After 4 weeks measure BP again. 
If still high:
Add Telmisartan 40mg
After 4 weeks measure BP again. 
If still high:
Increase Telmisartan to 80mg
After 4 weeks measure BP again. 
If still high:
Increase Amlodipine to 10mg
After 4 weeks measure BP again. 
If still high:
Add Chlorthalidone 12.5mg
After 4 weeks measure BP again. 
If still high:
1
2
3
4
5
6
If BP is high:*
Prescribe Amlodipine 5mg
After 4 weeks measure BP again. 
If still high:
Increase to Amlodipine 10mg
After 4 weeks measure BP again. 
If still high:
Add Telmisartan 40mg
After 4 weeks measure BP again. 
If still high:
Increase to Telmisartan 80mg
After 4 weeks measure BP again. 
If still high:
Add Chlorthalidone 12.5mg
After 4 weeks measure BP again. 
If still high:
1
2
3
4
5
6
*High BP  ≥140 /90 mmHg 
At every visit: Check if the patient has been taking medications regularly and 
correctly 
Consider adding drugs of other classes, preferably MRA (eg.Spironolactone)
• Combination therapy (two drugs from two diﬀerent classes) could be the 
default initial pharmacological treatment for most adults with 
hypertension
• Single-pill combinations (SPCs/ﬁxed-dose combinations, FDCs) are 
preferred over multiple pills to improve adherence
• Monotherapy remains appropriate only for (a) low-risk Grade 1 HTN, (b) 
elderly ≥ 80 years, or (c) frail patients
• A CCB or Thiazide/Thiazide-like diuretic should be used with a 
Renin-Angiotensin-Aldosterone System (RAAS) blocker (either an ACEi or 
an ARB)
• Three-drug combination, often a RAAS blocker, CCB, or a 
Thiazide/Thiazide-like diuretic, if blood pressure is not controlled with the 
initial two-drug combination
• β-blockers are appropriate in cases of angina, postmyocardial infarction, 
heart failure (HFrEF or HFpEF with ischemia)
• DO NOT combine two RAAS blockers as it increases the risk of adverse 
eﬀects, including acute kidney injury (AKI)
PHARMACOLOGICAL STRATEGY    
SUGGESTED TREATMENT PROTOCOLS 
• Systolic BP ≥180 AND/OR Diastolic ≥
120 mmHg
        AND
• No signs of acute target-organ 
damage
Management 
• Start oral antihypertensive drugs
• Do NOT use IV medicines
• Reduce BP gradually over 24–48 hours
• Refer/admit if symptoms or organ 
damage suspected
• Follow-up within 1 week
  ALL ADULTS  ≥ 18 YEARS SHOULD GET BLOOD PRESSURE MEASURED AT EVERY CLINIC VISIT
1. Mancia G, Kreutz R, Brunström M, et al. 2023 ESH Guidelines for the management of arterial hypertension. J Hypertens. 2023;41(12):1874–2071. doi:10.1097/HJH.0000000000003480 PMID: 37345492
2. Joseph G, Thanh Pham V, Kragh Andersen P, et al. Cardiovascular events according to blood pressure thresholds recommended by ACC/AHA. Blood Press. 2024;33(1):2380346. 
doi:10.1080/08037051.2024.2380346 PMID: 39018201
3. Gupta R, Maheshwari A, Verma N, Narasingan SN, Tripathi K, Joshi S, Manoria PC, et al. Indian Society of Hypertension (InSH) Consensus Guideline for the Management of Hypertension, 2025. 
Hypertension Journal. 2025;11(4):76–138. doi:10.61081/htnj/25v11i401.
4. Ministry of Health and Family Welfare, Government of India. Training modules on non-communicable diseases. New Delhi: MoHFW; 2025.
5. ICMR-National Institute of Epidemiology. India Hypertension Control Initiative: Training modules. Chennai, 2021.
HFrEF: Heart failure with reduced ejection fraction
HFpEF: Heart Failure with Preserved Ejection
OD: Once Daily
MRA: Mineralocorticoid Receptor Antagonist
RAAS:  Renin Angiotensin-Aldosterone System
CLASSIFICATION
Normal
Elevated BP
Hypertension 
Grade 1
Hypertension 
Grade 2
Hypertension 
Grade 3
ACTION
Reassure and 
encourage healthy 
lifestyle
Lifestyle 
modiﬁcation
Pharmacological
management+ 
Lifestyle 
modiﬁcation
BLOOD PRESSURE LEVELS
Systolic <120 AND 
Diastolic<80
Systolic 120-139 AND/ OR 
Diastolic 80-89
Systolic 140-159 AND/ OR 
Diastolic 90-99
Systolic 160-179 AND/ OR 
Diastolic 100-109
Systolic ≥ 180 AND/ OR 
Diastolic ≥ 110
 RED FLAGS SIGNS
DRUG CLASS
CONTRAINDICATIONS
DOSES
SIDE EFFECTS
ACE inhibitors
ARB
CCB
Diuretics
Beta-blockers
Aldosterone antagonist
Dry cough, angioedema, hyperkalemia 
rise in serum creatinine 
Hypotension, acute renal failure, 
hyperkalemia
Pedal edema, constipation
Glucose intolerance, metabolic syndrome, 
hyponatremia, hypercalcemia, hypokalemia
Depression, fatigue, reduced exercise 
tolerance, hyperglycemia, sexual 
dysfunction
Mastalgia, gynecomastia, sexual 
dysfunction, gout
Hyperkalemia
25 mg OD
Asthma, severe bradycardia, 
A-V block (grade 2 or 3), 
uncontrolled heart failure
5–40 mg OD or BD
2.5–10 mg OD
12.5–25 mg OD
12.5–50 mg OD or BD
50–100 mg OD
2.5–10 mg OD or BD
20–40 mg OD
40–80 mg OD
12.5 mg OD
100–400 mg BD
 50–100 mg OD or BD 
 5 mg OD 
Nebivolol
Spironolactone 
Metoprolol
Labetalol 
Carvedilol 
Hydrochlorothiazide
Chlorthalidone
Telmisartan
Olmesartan
Losartan 
 Ramipril
Enalapril
Amlodipine
DRUG
  Pregnancy,
  Women planning pregnancy, 
prior angioedema to ACEi, 
  Hyperkalemia, 
  Bilateral renal artery stenosis
Pregnancy, Gout
Heart failure
Hypertension is a  SILENT KILLER
as the majority of patients with high BP are asymptomatic! 
Only way to know if BP is high is to measure it accurately!
Department of Health Research
Ministry of Health and Family Welfare, Government of India
```

---

### Sampled WHO Recommendation #14: `who_htn_001_c0013`

- **Document Name:** WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (`who_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 9–9
- **Heading:** 1.	 RECOMMENDATION ON BLOOD PRESSURE THRESHOLD FOR INITIATION OF > PHARMACOLOGICAL TREATMENT
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > ACRONYMS AND ABBREVIATIONS > 1.	 RECOMMENDATION ON BLOOD PRESSURE THRESHOLD FOR INITIATION OF > PHARMACOLOGICAL TREATMENT`
- **Population Tags:** `["cardiovascular_disease"]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
1.	 RECOMMENDATION ON BLOOD PRESSURE THRESHOLD FOR INITIATION OF
PHARMACOLOGICAL TREATMENT
WHO recommends initiation of pharmacological antihypertensive treatment of individuals
with a confirmed diagnosis of hypertension and systolic blood pressure of >=140 mmHg or
diastolic blood pressure of >=90 mmHg.
Strong recommendation, moderate- to high-certainty evidence
WHO recommends pharmacological antihypertensive treatment of individuals with existing
cardiovascular disease and systolic blood pressure of 130-139 mmHg.
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: who_htn_001 | PAGE 9] ===
Executive summary
More people die each year from cardiovascular diseases than from any other cause. Over three 
quarters of heart disease and stroke-related deaths occur in low-income and middle-income countries. 
Hypertension – or elevated blood pressure – is a serious medical condition that significantly increases the 
risk of heart, brain, kidney and other diseases. Hypertension can be defined using specific systolic and 
diastolic blood pressure levels or reported use of antihypertensive medications. An estimated 1.4 billion 
people worldwide have high blood pressure, but just 14% have it under control. However, cost-effective 
treatment options do exist.
In this guideline, the World Health Organization (WHO) provides the most current and relevant 
evidence-based global public health guidance on the initiation of treatment with pharmacological 
agents for hypertension in adults. The recommendations target adult, non-pregnant patients who were 
appropriately diagnosed with hypertension and counselled about life-style modifications. 
The guideline provides new recommendations on the threshold for the initiation of pharmacological 
treatment for hypertension, as well as recommendations on intervals for follow up, target blood 
pressure to be achieved for control, and the cadre of health care workers who may initiate treatment. 
The guideline provides the basis for deciding whether to initiate treatment with monotherapy, dual 
therapy or single-pill combinations, as well as guidance for countries selecting medicines and algorithms 
for hypertension control for their national guidelines for hypertension management.
The guideline was developed in accordance with the WHO Handbook for Guideline Development. In 
brief, the WHO Steering Group, in collaboration with the Guideline Development Group, developed 
key questions and rated outcomes to identify those critical for the development of the guideline. 
Conflicts of interest were handled in line with the current Compliance, Risk Management and Ethics 
(CRE) policy and all members of the GDG were asked to fill in the standard WHO Declaration of Interest 
(DOI) forms, which were reviewed. An overview of systematic reviews of the evidence was used to build 
summary of findings tables according to the Grading of Recommendations, Assessment, Development 
and Evaluations (GRADE) approach. The Guideline Development Group developed recommendations, 
considering the certainty of the evidence; the balance between desirable and undesirable effects; 
resource requirements and cost-effectiveness; health equity; acceptability, patient values and 
preferences, and feasibility.
Recommendations 
1.	 RECOMMENDATION ON BLOOD PRESSURE THRESHOLD FOR INITIATION OF 
PHARMACOLOGICAL TREATMENT
WHO recommends initiation of pharmacological antihypertensive treatment of individuals 
with a confirmed diagnosis of hypertension and systolic blood pressure of ≥140 mmHg or 
diastolic blood pressure of ≥90 mmHg.
Strong recommendation, moderate- to high-certainty evidence
WHO recommends pharmacological antihypertensive treatment of individuals with existing 
cardiovascular disease and systolic blood pressure of 130–139 mmHg.
Strong recommendation, moderate- to high-certainty evidence
EXECUTIVE SUMMARY
vii
```

---

### Sampled WHO Recommendation #15: `who_htn_001_c0048`

- **Document Name:** WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (`who_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 25–25
- **Heading:** 5.	 RECOMMENDATION ON COMBINATION THERAPY
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > 3.5	 Combination therapy > 5.	 RECOMMENDATION ON COMBINATION THERAPY`
- **Population Tags:** `[]`
- **Drug Class Tags:** `["ace_inhibitor", "ccb", "thiazide"]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
5.	 RECOMMENDATION ON COMBINATION THERAPY
For adults with hypertension requiring pharmacological treatment, WHO suggests
combination therapy, preferably with a single-pill combination (to improve adherence and
persistence), as an initial treatment. Antihypertensive medications used in combination
therapy should be chosen from the following three drug classes: diuretics (thiazide or
thiazide-like), angiotensin-converting enzyme inhibitors (ACEis)/angiotensin-receptor
blockers (ARBs), and long-acting dihydropyridine calcium channel blockers (CCBs).
Conditional recommendation, moderate-certainty evidence
Implementation remarks:
[
[
Combination medication therapy may be especially valuable when the baseline BP is
>=20/10 mmHg higher than the target blood pressure.
[
[
Single-pill combination therapy improves medication-taking adherence and persistence and BP
control.
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: who_htn_001 | PAGE 25] ===
Evidence-to-decision considerations
The value of antihypertensive therapy is well accepted by most patients, health care providers, health 
systems, professional societies and government agencies. From a patient’s perspective, preventing 
cardiovascular events is highly valued. However, some individuals who are eligible for antihypertensive 
treatment may evade efforts aimed at treatment or are prescribed a treatment but fail to take/adhere 
to the treatment. The asymptomatic nature of the disease and concern about adverse events are the 
likely driver for this perspective. Interviews of patients in England suggested greater acceptance of 
antihypertensive drug therapy with higher socioeconomic status. 
In one study, as many as 35% of the Caucasians and 20% of the South Asians in the two lowest 
socioeconomic categories told their interviewer that they would not accept antihypertensive drug 
therapy (35). Shahaj et al. (6) synthesized six qualitative and 29 quantitative reviews and identified a 
range of individual and social factors that affect treatment adherence, including familial (lack of support, 
need for separate meals), and environmental (sense of security, local amenities, healthy food availability). 
A review by Fragasso et al. (36) suggested that quality of life on antihypertensive therapy is an important 
issue because clinicians are asked to initiate drug therapy in mostly asymptomatic patients who are 
never happy to become, instead, symptomatic because of side-effects. Therefore, the GDG considered 
that there is important variability in stakeholder values, but overall initiation of HTN medications is likely 
to be feasible and acceptable overall. Considering the ample literature on disparities in adherence to BP 
medication regimes and cardiovascular outcomes based on race or socioeconomic status, treatment was 
judged to reduce health inequities. 
In terms of costs and resource requirements, thiazide-like agents, ACEis/ARBs and long-acting 
dihydropyridine CCBs are available as generic drugs, are simple to manufacture, and should be 
available at low cost globally. Other costs related to workforce requirements, provision of infrastructure, 
laboratory testing, lost work time etc. are real but modest. Numerous modelling studies demonstrate 
cost effectiveness of antihypertensive therapy, which is especially beneficial in LMICs where large 
numbers of adults have untreated HTN, as long as medications are available at low cost. Models were 
available from many countries, including Bangladesh, Ghana and Nigeria (37, 38, 39, 40). 
3.5	 Combination therapy
To develop a recommendation that is practical and implementable by end-users, the evidence-
to-decision frameworks of PICO questions 6, 7 and 8 (see Annex 4) were used to develop one 
recommendation. 
5.	 RECOMMENDATION ON COMBINATION THERAPY
For adults with hypertension requiring pharmacological treatment, WHO suggests 
combination therapy, preferably with a single-pill combination (to improve adherence and 
persistence), as an initial treatment. Antihypertensive medications used in combination 
therapy should be chosen from the following three drug classes: diuretics (thiazide or 
thiazide-like), angiotensin-converting enzyme inhibitors (ACEis)/angiotensin-receptor 
blockers (ARBs), and long-acting dihydropyridine calcium channel blockers (CCBs).
Conditional recommendation, moderate-certainty evidence
Implementation remarks:
[
[
Combination medication therapy may be especially valuable when the baseline BP is 
≥20/10 mmHg higher than the target blood pressure.
[
[
Single-pill combination therapy improves medication-taking adherence and persistence and BP 
control.
RECOMMENDATIONS
13
```

---

### Sampled WHO Recommendation #16: `who_htn_001_c0015`

- **Document Name:** WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (`who_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 10–10
- **Heading:** 2.	 RECOMMENDATION ON LABORATORY TESTING
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > EXECUTIVE SUMMARY > 2.	 RECOMMENDATION ON LABORATORY TESTING`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
2.	 RECOMMENDATION ON LABORATORY TESTING
When starting pharmacological therapy for hypertension, WHO suggests obtaining tests to
screen for comorbidities and secondary hypertension, but only when testing does not delay
or impede starting treatment.
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: who_htn_001 | PAGE 10] ===
GUIDELINE FOR THE PHARMACOLOGICAL TREATMENT OF HYPERTENSION IN ADULTS
WHO suggests pharmacological antihypertensive treatment of individuals without 
cardiovascular disease but with high cardiovascular risk, diabetes mellitus, or chronic kidney 
disease, and systolic blood pressure of 130–139 mmHg.
Conditional recommendation, moderate- to high-certainty evidence 
2.	 RECOMMENDATION ON LABORATORY TESTING
When starting pharmacological therapy for hypertension, WHO suggests obtaining tests to 
screen for comorbidities and secondary hypertension, but only when testing does not delay 
or impede starting treatment.
Conditional recommendation, low-certainty evidence
3.	 RECOMMENDATION ON CARDIOVASCULAR DISEASE RISK ASSESSMENT 
WHO suggests cardiovascular disease risk assessment at or after the initiation of 
pharmacological treatment for hypertension, but only where this is feasible and does not 
delay treatment.
Conditional recommendation, low-certainty evidence
4.	 RECOMMENDATION ON DRUG CLASSES TO BE USED AS FIRST-LINE AGENTS
For adults with hypertension requiring pharmacological treatment, WHO recommends the 
use of drugs from any of the following three classes of pharmacological antihypertensive 
medications as an initial treatment: 
1. thiazide and thiazide-like agents
2. angiotensin-converting enzyme inhibitors (ACEis)/angiotensin-receptor blockers (ARBs)
3. long-acting dihydropyridine calcium channel blockers (CCBs).
Strong recommendation, high-certainty evidence
5.	 RECOMMENDATION ON COMBINATION THERAPY
For adults with hypertension requiring pharmacological treatment, WHO suggests 
combination therapy, preferably with a single-pill combination (to improve adherence and 
persistence), as an initial treatment. Antihypertensive medications used in combination 
therapy should be chosen from the following three drug classes: diuretics (thiazide or 
thiazide-like), angiotensin-converting enzyme inhibitors (ACEis)/angiotensin-receptor 
blockers (ARBs), and long-acting dihydropyridine calcium channel blockers (CCBs).
Conditional recommendation, moderate-certainty evidence
6.	 RECOMMENDATIONS ON TARGET BLOOD PRESSURE
WHO recommends a target blood pressure treatment goal of <140/90 mmHg in all patients 
with hypertension without comorbidities.
Strong recommendation, moderate-certainty evidence
viii
```

---

### Sampled WHO Recommendation #17: `who_htn_001_c0021`

- **Document Name:** WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (`who_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 11–11
- **Heading:** 8.	 RECOMMENDATION ON TREATMENT BY NONPHYSICIAN PROFESSIONALS
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > 7.	 RECOMMENDATIONS ON FREQUENCY OF ASSESSMENT > 8.	 RECOMMENDATION ON TREATMENT BY NONPHYSICIAN PROFESSIONALS`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
8.	 RECOMMENDATION ON TREATMENT BY NONPHYSICIAN PROFESSIONALS
WHO suggests that pharmacological treatment of hypertension can be provided by
nonphysician professionals such as pharmacists and nurses, as long as the following
conditions are met: proper training, prescribing authority, specific management protocols
and physician oversight.
Conditional recommendation, low-certainty evidence
ix
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: who_htn_001 | PAGE 11] ===
WHO recommends a target systolic blood pressure treatment goal of <130 mmHg in patients 
with hypertension and known cardiovascular disease (CVD).
Strong recommendation, moderate-certainty evidence
WHO suggests a target systolic blood pressure treatment goal of <130 mmHg in high-risk 
patients with hypertension (those with high CVD risk, diabetes mellitus, chronic kidney 
disease).
Conditional recommendation, moderate-certainty evidence
7.	 RECOMMENDATIONS ON FREQUENCY OF ASSESSMENT
WHO suggests a monthly follow up after initiation or a change in antihypertensive 
medications until patients reach target.
Conditional recommendation, low-certainty evidence
WHO suggests a follow up every 3–6 months for patients whose blood pressure is under 
control.
Conditional recommendation, low-certainty evidence
8.	 RECOMMENDATION ON TREATMENT BY NONPHYSICIAN PROFESSIONALS
WHO suggests that pharmacological treatment of hypertension can be provided by 
nonphysician professionals such as pharmacists and nurses, as long as the following 
conditions are met: proper training, prescribing authority, specific management protocols 
and physician oversight.
Conditional recommendation, low-certainty evidence
ix
```

---

### Sampled WHO Recommendation #18: `who_htn_001_c0044`

- **Document Name:** WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (`who_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 23–23
- **Heading:** 4.	 RECOMMENDATION ON DRUG CLASSES TO BE USED AS FIRST-LINE AGENTS
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > 3.4	 Drug classes to be used as first-line agents > 4.	 RECOMMENDATION ON DRUG CLASSES TO BE USED AS FIRST-LINE AGENTS`
- **Population Tags:** `["cardiovascular_disease", "chronic_kidney_disease"]`
- **Drug Class Tags:** `["ace_inhibitor", "beta_blocker", "ccb", "thiazide"]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
4.	 RECOMMENDATION ON DRUG CLASSES TO BE USED AS FIRST-LINE AGENTS
For adults with hypertension requiring pharmacological treatment, WHO recommends the
use of drugs from any of the following three classes of pharmacological antihypertensive
medications as an initial treatment:
1. thiazide and thiazide-like agents
2. angiotensin-converting enzyme inhibitors (ACEis)/angiotensin-receptor blockers (ARBs)
3. long-acting dihydropyridine calcium channel blockers (CCBs).
Strong recommendation, high-certainty evidence
Implementation remarks:
[
[
Long-acting antihypertensives are preferred.
[
[
Examples of indications to consider specific agents include diuretics or CCBs in patients over
65 years or those of African descent, beta-blockers in ischaemic heart disease, ACEis/ARBs in
patients with severe proteinuria, diabetes mellitus, heart failure or kidney disease.
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: who_htn_001 | PAGE 23] ===
The GDG deduced that benefits of risk assessment may not all be attributable to risk assessment per 
se, but rather to the various treatments provided for risk factors identified during risk assessment. 
The certainty of evidence across outcome was judged to be very low due to serious concerns about 
the indirectness of evidence. Overall, the desirable effects of risk assessment at or after initiating HTN 
medications outweighed the plausible undesirable effects, particularly when risk assessment was 
deemed not to delay the initiation of treatment.
Evidence-to-decision considerations
There is important uncertainty over the value stakeholders place on conducting a CVD risk assessment 
prior to starting pharmacological treatment, and it was noted that patient perspectives may vary, 
depending on the setting. In low-resource settings, patients may focus more on immediate treatment 
without having to bear additional costs for screening for other risk factors and treating them. Studies 
have also shown that in high-income countries (HICs) such as the United States, people of a lower 
socioeconomic status have lower control of blood pressure and higher CVD risk over the years (25). 
Thus, in low-resource settings, adding one more step before initiating treatment may increase inequities, 
as those patients who have limited access to health care services may suffer delays in treatment or even 
end up not receiving HTN treatment at all. 
In terms of costs, there is no direct evidence of whether treatment of HTN with or without risk 
stratification is more cost effective. The cost of implementation of CVD risk assessment should also 
account for capacity building of health care providers and the time taken to do so for each patient. 
Cost of testing and delay in initiating care can be significant following a CVD risk stratification strategy 
in low-resource settings. Modelling by Gaziano et al. showed significant cost reduction using CVD risk-
stratification before initiation of treatment in low-resource settings. However, screening costs, including 
the cost of obtaining risk-factor information, productivity costs due to work loss, care costs and travel 
time were not included in the analysis (26). 
A meta-analysis showed that proportional relative risk reduction in major CVD events from BP lowering 
did not differ substantially with the presence or absence of previous CVD events, coronary heart disease, 
or cerebrovascular disease. Hence, the absolute benefit of blood pressure lowering would be greatest in 
those with the highest absolute risk of CVD (27). 
3.4	 Drug classes to be used as first-line agents
To develop a recommendation that is practical and implementable by end-users, the evidence-to-decision 
frameworks of PICO questions 4 and 5 (see Annex 4) were used to develop one recommendation. 
4.	 RECOMMENDATION ON DRUG CLASSES TO BE USED AS FIRST-LINE AGENTS
For adults with hypertension requiring pharmacological treatment, WHO recommends the 
use of drugs from any of the following three classes of pharmacological antihypertensive 
medications as an initial treatment: 
1. thiazide and thiazide-like agents
2. angiotensin-converting enzyme inhibitors (ACEis)/angiotensin-receptor blockers (ARBs)
3. long-acting dihydropyridine calcium channel blockers (CCBs).
Strong recommendation, high-certainty evidence
Implementation remarks:
[
[
Long-acting antihypertensives are preferred.
[
[
Examples of indications to consider specific agents include diuretics or CCBs in patients over 
65 years or those of African descent, beta-blockers in ischaemic heart disease, ACEis/ARBs in 
patients with severe proteinuria, diabetes mellitus, heart failure or kidney disease.
RECOMMENDATIONS
11
```

---

### Sampled WHO Recommendation #19: `who_htn_001_c0016`

- **Document Name:** WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (`who_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 10–10
- **Heading:** 3.	 RECOMMENDATION ON CARDIOVASCULAR DISEASE RISK ASSESSMENT
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > 2.	 RECOMMENDATION ON LABORATORY TESTING > 3.	 RECOMMENDATION ON CARDIOVASCULAR DISEASE RISK ASSESSMENT`
- **Population Tags:** `["cardiovascular_disease"]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `None`
- **Last Updated:** `None`

#### Exact Chunk Text

```text
3.	 RECOMMENDATION ON CARDIOVASCULAR DISEASE RISK ASSESSMENT
WHO suggests cardiovascular disease risk assessment at or after the initiation of
pharmacological treatment for hypertension, but only where this is feasible and does not
delay treatment.
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: who_htn_001 | PAGE 10] ===
GUIDELINE FOR THE PHARMACOLOGICAL TREATMENT OF HYPERTENSION IN ADULTS
WHO suggests pharmacological antihypertensive treatment of individuals without 
cardiovascular disease but with high cardiovascular risk, diabetes mellitus, or chronic kidney 
disease, and systolic blood pressure of 130–139 mmHg.
Conditional recommendation, moderate- to high-certainty evidence 
2.	 RECOMMENDATION ON LABORATORY TESTING
When starting pharmacological therapy for hypertension, WHO suggests obtaining tests to 
screen for comorbidities and secondary hypertension, but only when testing does not delay 
or impede starting treatment.
Conditional recommendation, low-certainty evidence
3.	 RECOMMENDATION ON CARDIOVASCULAR DISEASE RISK ASSESSMENT 
WHO suggests cardiovascular disease risk assessment at or after the initiation of 
pharmacological treatment for hypertension, but only where this is feasible and does not 
delay treatment.
Conditional recommendation, low-certainty evidence
4.	 RECOMMENDATION ON DRUG CLASSES TO BE USED AS FIRST-LINE AGENTS
For adults with hypertension requiring pharmacological treatment, WHO recommends the 
use of drugs from any of the following three classes of pharmacological antihypertensive 
medications as an initial treatment: 
1. thiazide and thiazide-like agents
2. angiotensin-converting enzyme inhibitors (ACEis)/angiotensin-receptor blockers (ARBs)
3. long-acting dihydropyridine calcium channel blockers (CCBs).
Strong recommendation, high-certainty evidence
5.	 RECOMMENDATION ON COMBINATION THERAPY
For adults with hypertension requiring pharmacological treatment, WHO suggests 
combination therapy, preferably with a single-pill combination (to improve adherence and 
persistence), as an initial treatment. Antihypertensive medications used in combination 
therapy should be chosen from the following three drug classes: diuretics (thiazide or 
thiazide-like), angiotensin-converting enzyme inhibitors (ACEis)/angiotensin-receptor 
blockers (ARBs), and long-acting dihydropyridine calcium channel blockers (CCBs).
Conditional recommendation, moderate-certainty evidence
6.	 RECOMMENDATIONS ON TARGET BLOOD PRESSURE
WHO recommends a target blood pressure treatment goal of <140/90 mmHg in all patients 
with hypertension without comorbidities.
Strong recommendation, moderate-certainty evidence
viii
```

---

### Sampled NICE Recommendation #20: `nice_htn_001_c0067`

- **Document Name:** NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (`nice_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 21–21
- **Heading:** 1.4.42
- **Section Path:** `NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management > 1.4 Treating and monitoring hypertension > 1.4.42`
- **Population Tags:** `[]`
- **Drug Class Tags:** `["ace_inhibitor", "arb", "ccb", "thiazide"]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `2019`
- **Last Updated:** `2026-02-26`

#### Exact Chunk Text

```text
1.4.42
If hypertension is not controlled in adults taking step 1 treatment of a CCB, offer
the choice of 1 of the following drugs in addition to step 1 treatment:
-  an ACE inhibitor or
-  an ARB or
-  a thiazide-like diuretic. [2019]
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: nice_htn_001 | PAGE 21] ===
1.4.39 
For adults with hypertension already having treatment with bendroflumethiazide 
or hydrochlorothiazide, who have stable, well-controlled blood pressure, continue 
with their current treatment. [2019] 
For a short explanation of why the committee made the 2019 recommendations and 
how they might affect practice, see the rationale and impact section on step 1 
treatment. 
Full details of the evidence and the committee's discussion are in evidence review E: 
step 1 treatment. 
Step 2 treatment 
1.4.40 
Before considering next step treatment for hypertension discuss with the person 
if they are taking their medicine as prescribed and support adherence in line with 
NICE's guideline on medicines adherence. [2019] 
1.4.41 
If hypertension is not controlled in adults taking step 1 treatment of an ACE 
inhibitor or ARB, offer the choice of 1 of the following drugs in addition to step 1 
treatment: 
• a CCB or 
• a thiazide-like diuretic. [2019] 
1.4.42 
If hypertension is not controlled in adults taking step 1 treatment of a CCB, offer 
the choice of 1 of the following drugs in addition to step 1 treatment: 
• an ACE inhibitor or 
• an ARB or 
• a thiazide-like diuretic. [2019] 
1.4.43 
If hypertension is not controlled in adults of Black African or African–Caribbean 
family origin who do not have type 2 diabetes taking step 1 treatment, consider 
an ARB, in preference to an ACE inhibitor, in addition to step 1 treatment. [2019] 
Hypertension in adults: diagnosis and management (NG136)
© NICE 2026. All rights reserved. Subject to Notice of rights (https://www.nice.org.uk/terms-and-
conditions#notice-of-rights).
Page 21 of
52
```

---

### Sampled NICE Recommendation #21: `nice_t2dm_001_c0196`

- **Document Name:** NICE Guideline NG28: Type 2 Diabetes in Adults - Management (`nice_t2dm_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `type_2_diabetes`
- **Indexed For Retrieval:** `True`
- **Page Range:** 113–113
- **Heading:** 1.37.2
- **Section Path:** `NICE Guideline NG28: Type 2 Diabetes in Adults - Management > 1.37 Periodontitis > 1.37.2`
- **Population Tags:** `["type_2_diabetes"]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `2022`
- **Last Updated:** `2026-02-18`

#### Exact Chunk Text

```text
1.37.2
Advise adults with type 2 diabetes to have regular oral health reviews (their oral
healthcare or dental team will tell them how often, in line with NICE's guideline on
dental checks: intervals between oral health reviews). [2022]
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: nice_t2dm_001 | PAGE 113] ===
Complications 
1.37 Periodontitis 
1.37.1 
Advise adults with type 2 diabetes at their annual review that: 
• they are at higher risk of periodontitis 
• if they get periodontitis, managing it can improve their blood glucose control 
and can reduce their risk of hyperglycaemia. [2022] 
1.37.2 
Advise adults with type 2 diabetes to have regular oral health reviews (their oral 
healthcare or dental team will tell them how often, in line with NICE's guideline on 
dental checks: intervals between oral health reviews). [2022] 
1.37.3 
For guidance for oral healthcare and dental teams on how to provide oral health 
advice, see NICE's guideline on oral health promotion. [2022] 
1.37.4 
For adults with type 2 diabetes who have been diagnosed with periodontitis by 
an oral healthcare or dental team, offer dental appointments to manage and treat 
their periodontitis (at a frequency based on their oral health needs). [2022] 
Type 2 diabetes in adults: management (NG28)
© NICE 2026. All rights reserved. Subject to Notice of rights (https://www.nice.org.uk/terms-
and-conditions#notice-of-rights).
Page 113 of
131
```

---

### Sampled NICE Recommendation #22: `nice_t2dm_001_c0087`

- **Document Name:** NICE Guideline NG28: Type 2 Diabetes in Adults - Management (`nice_t2dm_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `type_2_diabetes`
- **Indexed For Retrieval:** `True`
- **Page Range:** 45–45
- **Heading:** 1.15.2
- **Section Path:** `NICE Guideline NG28: Type 2 Diabetes in Adults - Management > 1.15 People with atherosclerotic cardiovascular > 1.15.2`
- **Population Tags:** `[]`
- **Drug Class Tags:** `["glp1_ra", "metformin", "sglt2_inhibitor"]`
- **Applicability Conditions:** `null`
- **Exceptions:** `["1.15.2\nIf metformin is contraindicated or not tolerated, offer:\n-  an SGLT-2 inhibitor, and\n-  subcutaneous semaglutide (Ozempic), up to 1 mg once a week, for its\ncardiovascular, renal and glycaemic benefits."]`
- **Cross References:** `[]`
- **Recommendation Year:** `2026`
- **Last Updated:** `2026-02-18`

#### Exact Chunk Text

```text
1.15.2
If metformin is contraindicated or not tolerated, offer:
-  an SGLT-2 inhibitor, and
-  subcutaneous semaglutide (Ozempic), up to 1 mg once a week, for its
cardiovascular, renal and glycaemic benefits. [2026]
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: nice_t2dm_001 | PAGE 45] ===
1.15 People with atherosclerotic cardiovascular 
disease 
1.15.1 
For adults with type 2 diabetes and atherosclerotic cardiovascular disease, offer: 
• modified-release metformin, and 
• an SGLT-2 inhibitor, and 
• subcutaneous semaglutide (Ozempic), up to 1 mg once a week, for its 
cardiovascular, renal and glycaemic benefits. [2026] 
1.15.2 
If metformin is contraindicated or not tolerated, offer: 
• an SGLT-2 inhibitor, and 
• subcutaneous semaglutide (Ozempic), up to 1 mg once a week, for its 
cardiovascular, renal and glycaemic benefits. [2026] 
Type 2 diabetes in adults: management (NG28)
© NICE 2026. All rights reserved. Subject to Notice of rights (https://www.nice.org.uk/terms-and-
conditions#notice-of-rights).
Page 45 of
131
```

---

### Sampled NICE Recommendation #23: `nice_htn_001_c0075`

- **Document Name:** NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (`nice_htn_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `hypertension`
- **Indexed For Retrieval:** `True`
- **Page Range:** 23–23
- **Heading:** 1.4.50
- **Section Path:** `NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management > 1.4 Treating and monitoring hypertension > 1.4.50`
- **Population Tags:** `[]`
- **Drug Class Tags:** `["thiazide"]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `2019`
- **Last Updated:** `2026-02-26`

#### Exact Chunk Text

```text
1.4.50
When using further diuretic therapy for step 4 treatment of resistant
hypertension, monitor blood sodium and potassium and renal function within
1 month of starting treatment and repeat as needed thereafter. [2019]
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: nice_htn_001 | PAGE 23] ===
• Discuss adherence (see recommendation 1.4.40). [2019] 
1.4.48 
For people with confirmed resistant hypertension, consider adding a fourth 
antihypertensive drug as step 4 treatment or seeking specialist advice. [2019] 
Follow the MHRA safety advice on ACE inhibitors and angiotensin II receptor 
antagonists: not for use in pregnancy, how to use for breastfeeding and 
clarification on breastfeeding. 
1.4.49 
Consider further diuretic therapy with low-dose spironolactone for adults with 
resistant hypertension starting step 4 treatment who have a blood potassium 
level of 4.5 mmol/l or less. Use particular caution in people with a reduced 
estimated glomerular filtration rate because they have an increased risk of 
hyperkalaemia. [2019] 
In March 2019, this was an off-label use of some preparations of spironolactone. 
See NICE's information on prescribing medicines. 
1.4.50 
When using further diuretic therapy for step 4 treatment of resistant 
hypertension, monitor blood sodium and potassium and renal function within 
1 month of starting treatment and repeat as needed thereafter. [2019] 
1.4.51 
Consider an alpha-blocker or beta-blocker for adults with resistant hypertension 
starting step 4 treatment who have a blood potassium level of more than 
4.5 mmol/l. [2019] 
1.4.52 
If blood pressure remains uncontrolled in people with resistant hypertension 
taking the optimal tolerated doses of 4 drugs, seek specialist advice. [2019] 
For a short explanation of why the committee made the 2019 recommendations and 
how they might affect practice, see the rationale and impact section on step 4 
treatment. 
Full details of the evidence and the committee's discussion are in evidence review G: 
step 4 treatment. 
Hypertension in adults: diagnosis and management (NG136)
© NICE 2026. All rights reserved. Subject to Notice of rights (https://www.nice.org.uk/terms-and-
conditions#notice-of-rights).
Page 23 of
52
```

---

### Sampled NICE Recommendation #24: `nice_t2dm_001_c0112`

- **Document Name:** NICE Guideline NG28: Type 2 Diabetes in Adults - Management (`nice_t2dm_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `type_2_diabetes`
- **Indexed For Retrieval:** `True`
- **Page Range:** 65–65
- **Heading:** 1.19.2
- **Section Path:** `NICE Guideline NG28: Type 2 Diabetes in Adults - Management > 1.19 People with frailty > 1.19.2`
- **Population Tags:** `[]`
- **Drug Class Tags:** `["dpp4_inhibitor", "metformin", "sglt2_inhibitor"]`
- **Applicability Conditions:** `null`
- **Exceptions:** `["1.19.2\nIf metformin is contraindicated or not tolerated, assess whether their level of\nfrailty places the person at risk of adverse events from SGLT-2 inhibitors:\n-  if it does not, consider monotherapy with a SGLT-2 inhibitor\n-  if it does, consider monotherapy with a DPP-4 inhibitor."]`
- **Cross References:** `[]`
- **Recommendation Year:** `2026`
- **Last Updated:** `2026-02-18`

#### Exact Chunk Text

```text
1.19.2
If metformin is contraindicated or not tolerated, assess whether their level of
frailty places the person at risk of adverse events from SGLT-2 inhibitors:
-  if it does not, consider monotherapy with a SGLT-2 inhibitor
-  if it does, consider monotherapy with a DPP-4 inhibitor. [2026]
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: nice_t2dm_001 | PAGE 65] ===
How the recommendations might affect practice 
Metformin 
The recommendations about the use of metformin may lead to a change in current 
practice but should not lead to a significant cost or resource impact. The price of 
modified-release metformin can fluctuate but, in December 2025, was lower than the 
cost of standard-release metformin. 
SGLT-2 inhibitors 
The recommendations about the use of SGLT-2 inhibitors should not lead to a change 
in current practice. 
DPP-4 inhibitors, pioglitazone and insulin 
The recommendation about the use of DPP-4 inhibitors, pioglitazone and insulin 
should not reflect a change in current practice. 
1.19 People with frailty 
1.19.1 
For adults with type 2 diabetes and frailty: 
• Offer modified-release metformin. 
• Only offer an SGLT2 inhibitor if the person's level of frailty does not place 
them at risk of adverse events from such a medicine (for example, volume 
depletion or hypotension). [2026] 
1.19.2 
If metformin is contraindicated or not tolerated, assess whether their level of 
frailty places the person at risk of adverse events from SGLT-2 inhibitors: 
• if it does not, consider monotherapy with a SGLT-2 inhibitor 
• if it does, consider monotherapy with a DPP-4 inhibitor. [2026] 
Type 2 diabetes in adults: management (NG28)
© NICE 2026. All rights reserved. Subject to Notice of rights (https://www.nice.org.uk/terms-and-
conditions#notice-of-rights).
Page 65 of
131
```

---

### Sampled NICE Recommendation #25: `nice_t2dm_001_c0214`

- **Document Name:** NICE Guideline NG28: Type 2 Diabetes in Adults - Management (`nice_t2dm_001`)
- **Chunk Type:** `recommendation`
- **Condition:** `type_2_diabetes`
- **Indexed For Retrieval:** `True`
- **Page Range:** 118–118
- **Heading:** 1.42.3
- **Section Path:** `NICE Guideline NG28: Type 2 Diabetes in Adults - Management > 1.42 Erectile dysfunction > 1.42.3`
- **Population Tags:** `["type_2_diabetes"]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `null`
- **Exceptions:** `null`
- **Cross References:** `[]`
- **Recommendation Year:** `2015`
- **Last Updated:** `2026-02-18`

#### Exact Chunk Text

```text
1.42.3
Consider a phosphodiesterase‐5 inhibitor to treat problematic erectile
dysfunction in people with type 2 diabetes. Initially choose the medicine with the
lowest acquisition cost and take into account any contraindications. [2015]
```

#### Full Raw Source Page Text (Uncompressed)

```text
=== [SOURCE PDF: nice_t2dm_001 | PAGE 118] ===
1.42 Erectile dysfunction 
1.42.1 
As part of the type 2 diabetes annual review, offer to discuss erectile dysfunction 
(if relevant). [2015] 
1.42.2 
Assess, educate and support people with type 2 diabetes who have problematic 
erectile dysfunction, addressing contributory factors such as cardiovascular 
disease as well as possible treatment options. [2015] 
1.42.3 
Consider a phosphodiesterase‑5 inhibitor to treat problematic erectile 
dysfunction in people with type 2 diabetes. Initially choose the medicine with the 
lowest acquisition cost and take into account any contraindications. [2015] 
1.42.4 
After discussion, refer people with type 2 diabetes to a service offering other 
medical, surgical or psychological management of erectile dysfunction if 
treatment (including a phosphodiesterase‑5 inhibitor, as appropriate) has been 
unsuccessful. [2015] 
1.43 Eye disease 
1.43.1 
When adults are diagnosed with type 2 diabetes, refer them immediately to the 
local eye screening service. [2009, amended 2020] 
1.43.2 
Encourage adults to attend eye screening, and explain that it will help them to 
keep their eyes healthy and help to prevent problems with their vision. Explain 
that the screening service is effective at identifying problems so that they can be 
treated early. [2009] 
1.43.3 Arrange emergency review by an ophthalmologist for: 
• sudden loss of vision 
• rubeosis iridis 
• pre-retinal or vitreous haemorrhage 
• retinal detachment. [2009] 
Type 2 diabetes in adults: management (NG28)
© NICE 2026. All rights reserved. Subject to Notice of rights (https://www.nice.org.uk/terms-
and-conditions#notice-of-rights).
Page 118 of
131
```

---
