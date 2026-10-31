# Clinical Guideline Chunk Audit Report (v2)

**Generated:** 2026-11-01  
**Milestone:** Phase 1b Chunking Defect Remediation & Verification Gate  
**Audited Samples:** 25 Random Recommendations + 23 ICMR Poster Chunks + 10 Table Chunks + 10 Trap Verifications  

---

## 1. Ten Dedicated Clinical 'Trap' Verifications

| Trap # | Description & Audited Defect | Chunk ID | Verification Evaluation & Output | Status |
|---|---|---|---|---|
| **1** | **Trap 1: Type 1 vs Type 2 Diabetes Disambiguation**<br>NICE 1.4.20 cross-references Type 1 Diabetes; must tag type_1_diabetes, NOT type_2_diabetes. | `nice_htn_001_c0048` | Tagged type_1_diabetes, cleanly omitted type_2_diabetes. | **PASS** |
| **2** | **Trap 2: Negation Handling ('without renal disease')**<br>NICE 1.2.12 annual screening in T2DM without renal disease; must NOT tag chronic_kidney_disease. | `nice_htn_001_c0023` | Tagged type_2_diabetes, negation detected: chronic_kidney_disease omitted. | **PASS** |
| **3** | **Trap 3: Screening Test Mention vs Population Applicability**<br>NICE 1.3.3 general hypertension workup lists HbA1c; must NOT tag type_2_diabetes. | `nice_htn_001_c0028` | Laboratory screening panel recognized: type_2_diabetes omitted. | **PASS** |
| **4** | **Trap 4: Drug Adverse Reaction Mention vs Population**<br>MoHFW 5.3.2 lists hyperglycemia as thiazide side effect; must NOT tag type_2_diabetes. | `mohfw_htn_001_c0106` | Adverse effect detected: type_2_diabetes omitted; condition stays hypertension. | **PASS** |
| **5** | **Trap 5: Pregnancy Contraindications in Drug Table**<br>ICMR HTN drug therapy table must explicitly flag pregnancy contraindication for ACEi, ARBs, and Diuretics. | `icmr_htn_001_c0012` | Tagged pregnancy, exact contraindications preserved in table rows and exceptions. | **PASS** |
| **6** | **Trap 6: Age-80 Target in NICE (<150/90 mmHg)**<br>NICE 1.4.21 explicitly sets target clinic BP < 150/90 mmHg for adults aged 80 and over. | `nice_htn_001_c0049` | Target <150/90 mmHg preserved with elderly population tag. | **PASS** |
| **7** | **Trap 7: General Blood Pressure Target in WHO (<140/90 mmHg)**<br>WHO Recommendation 6 sets general BP target < 140/90 mmHg in patients without comorbidities. | `who_htn_001_c0052` | Target <140/90 mmHg preserved with Moderate certainty evidence. | **PASS** |
| **8** | **Trap 8: Age-80 Target in ICMR (<150/90 mmHg)**<br>ICMR HTN STW explicitly sets SBP < 150 and DBP < 90 mmHg for age >= 80 years. | `icmr_htn_001_c0006` | Target SBP <150 and DBP <90 mmHg preserved with elderly tag. | **PASS** |
| **9** | **Trap 9: MoHFW Diabetes Target (<140/90 adopting JNC 8)**<br>MoHFW STG Background & QuickRef explicitly targets SBP < 140 and DBP < 90 in diabetes. | `mohfw_htn_001_c0062` | Target <140/90 mmHg confirmed across chunks c0062 and c0209 (adopting JNC 8). | **PASS** |
| **10** | **Trap 10: Trailing Section Heading Not Glued**<br>NICE 1.2.12 must NOT contain trailing heading 'Specialist investigations for possible secondary causes...' | `nice_htn_001_c0023` | Trailing section header cleanly stripped into its own boundary. | **PASS** |

---

## 2. Twenty-Five Random Recommendation Chunks Audit (Total: 25)

### Sample 1: `nice_htn_001_c0080` (NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management, pp. 23-23)
- **Chunk Type:** `recommendation` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `1.4.52`
- **Section Path:** `NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management > [IMAGE] > 1.4.52`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `2019` | **Last Updated:** `2026-02-26`

```markdown
--- CHUNK TEXT ---
1.4.52
If blood pressure remains uncontrolled in people with resistant hypertension
taking the optimal tolerated doses of 4 drugs, seek specialist advice. [2019]
For a short explanation of why the committee made the 2019 recommendations and
how they might affect practice, see the rationale and impact section on step 4
treatment.
Full details of the evidence and the committee's discussion are in evidence review G:
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
• Discuss adherence (see recommendation 1.4.40). [2019] 
1.4.48 
For people with confirmed resistant hypertension, consider adding a fourth 
antihypertensive drug as step 4 treatment or seeking specialist advice. [2019] 
Follow the MHRA safety advice on ACE inhibitors and angiotensin II receptor 
antagonists: not for use in pregnancy, how to use for breastfeeding and 
clarification on breastfeedin
...
```
</details>

---

### Sample 2: `who_htn_001_c0069` (WHO Guideline for the Pharmacological Treatment of Hypertension in Adults, pp. 36-36)
- **Chunk Type:** `recommendation` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `5.3	 Evaluation`
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > 5.2	 Implementation and dissemination > 5.3	 Evaluation`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
5.3	 Evaluation
WHO will monitor uptake and implementation of the guideline in national policies and programmes by
reviewing the number of countries that have adapted or endorsed the guideline nationally.
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
GUIDELINE FOR THE PHARMACOLOGICAL TREATMENT OF HYPERTENSION IN ADULTS
5	 Publication, implementation, 
evaluation and research gaps
5.1	 Publication 
This guideline is available to download from the WHO website. Given that an overview of published 
systematic reviews was used for the development of the guideline, all reviews are already published and 
available online. 
5.2	 Implementation and dis
...
```
</details>

---

### Sample 3: `nice_t2dm_001_c0164` (NICE Guideline NG28: Type 2 Diabetes in Adults - Management, pp. 117-117)
- **Chunk Type:** `recommendation` | **Condition:** `both` | **Indexed:** `True`
- **Heading:** `1.40.3`
- **Section Path:** `NICE Guideline NG28: Type 2 Diabetes in Adults - Management > 1.40 Autonomic neuropathy > 1.40.3`
- **Population Tags:** `['type_2_diabetes']`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `2009` | **Last Updated:** `2026-02-18`

```markdown
--- CHUNK TEXT ---
1.40.3
For adults with type 2 diabetes and autonomic neuropathy who are taking
tricyclic antidepressants and antihypertensive medicines, be aware of the
increased likelihood of side effects such as orthostatic hypotension. For guidance
on safe prescribing of antidepressants and managing withdrawal, see NICE's
guideline on medicines associated with dependence or withdrawal symptoms.
[2009]
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
1.39 Painful diabetic neuropathy 
1.39.1 
For guidance on managing painful diabetic peripheral neuropathy in adults with 
type 2 diabetes, see NICE's guideline on neuropathic pain in adults. [2015] 
1.40 Autonomic neuropathy 
1.40.1 
Think about the possibility of contributory sympathetic nervous system damage 
in adults with type 2 diabetes who lose the warning signs of hypoglycaemia. 
[2009, ame
...
```
</details>

---

### Sample 4: `nice_t2dm_001_c0132` (NICE Guideline NG28: Type 2 Diabetes in Adults - Management, pp. 96-96)
- **Chunk Type:** `recommendation` | **Condition:** `type_2_diabetes` | **Indexed:** `True`
- **Heading:** `1.29 People living with obesity > 1.29.1`
- **Section Path:** `NICE Guideline NG28: Type 2 Diabetes in Adults - Management > 1.28 People with early onset type 2 diabetes > 1.29 People living with obesity > 1.29.1`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `2026` | **Last Updated:** `2026-02-18`

```markdown
--- CHUNK TEXT ---
1.29 People living with obesity
1.29.1
If considering medicines primarily for weight management, see information about
medicines for overweight and obesity in NICE's guideline on overweight and
obesity management. [2026]
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
1.29 People living with obesity 
1.29.1 
If considering medicines primarily for weight management, see information about 
medicines for overweight and obesity in NICE's guideline on overweight and 
obesity management. [2026] 
1.29.2 
Consider adding a GLP-1 receptor agonist or tirzepatide for adults with type 2 
diabetes who are living with obesity, if: 
• they have been taking initial therapy for
...
```
</details>

---

### Sample 5: `nice_t2dm_001_c0108` (NICE Guideline NG28: Type 2 Diabetes in Adults - Management, pp. 70-72)
- **Chunk Type:** `recommendation` | **Condition:** `type_2_diabetes` | **Indexed:** `True`
- **Heading:** `1.21.3`
- **Section Path:** `NICE Guideline NG28: Type 2 Diabetes in Adults - Management > 1.21 Preventing diabetic ketoacidosis when taking > 1.21.3`
- **Population Tags:** `['type_2_diabetes']`
- **Drug Class Tags:** `['glp1_ra', 'metformin', 'sglt2_inhibitor']`
- **Applicability Conditions:** `None`
- **Exceptions:** `['In line with current practice, the committee recommended starting with\nmetformin and then adding the SGLT-2 inhibitor without delay once metformin\ntolerability at the highest achievable dose is established, to avoid people remaining on\nmetformin alone for prolonged periods.', "In the\ncommittee's experience there have been multiple instances of avoidable diabetes\nketoacidosis (DKA) resulting in hospital admission.", 'The committee agreed that taking these factors into account was more\nimportant than providing a specific HbA1c threshold from which to avoid prescribing\nSGLT-2 inhibitors.']`
- **Recommendation Year:** `2022` | **Last Updated:** `2026-02-18`

```markdown
--- CHUNK TEXT ---
1.21.3
Advise adults with type 2 diabetes who are taking an SGLT-2 inhibitor that a very
low carbohydrate or ketogenic diet would increase their risk of DKA and so:
-  they should speak with their healthcare professional before starting such a
diet, and
-  their SGLT-2 inhibitor treatment may need to be suspended for the duration
of the diet. [2022]
Why the committee made these recommendations
When starting first-line therapy with metformin and other medicines, the committee
noted the importance of introducing the medicines sequentially. This enables any side
effects and intolerances from the first medicine to be identified before the second is
introduced. In line with current practice, the committee recommended starting with
metformin and then adding the SGLT-2 inhibitor without delay once metformin
tolerability at the highest achievable dose is established, to avoid people remaining on
metformin alone for prolonged periods.
The committee agreed that sudden reductions in HbA1c can increase the risk of
diabetic retinopathy and ischaemic maculopathy, especially with GLP-1 receptor
agonists and tirzepatide. Given this safety concern, they highlighted relevant
recommendations in NICE's guideline on diabetic retinopathy for further guidance for
anyone starting these medicines.
Preventing diabetic ketoacidosis when taking SGLT-2 inhibitors
The committee noted some particularly important safety considerations to take into
account before an adult with type 2 diabetes starts on an SGLT-2 inhibitor. In the
committee's experience there have been multiple instances of avoidable diabetes
ketoacidosis (DKA) resulting in hospital admission. The committee highlighted some
factors that might put someone at higher risk of DKA, but the list is not intended to be
exhaustive. Addressing modifiable risk factors before starting an SGLT-2 inhibitor
could reduce the risk of DKA and make the medicine safer for the person with type 2
diabetes. The committee agreed that taking these factors into account was more
important than providing a specific HbA1c threshold from which to avoid prescribing
SGLT-2 inhibitors.
The committee was aware that adults with type 2 diabetes who are living with
overweight or obesity may wish to try a ketogenic diet to reverse or reduce the
severity of their diabetes or induce remission. However, the committee agreed, based
on their experience, that there may be an increased risk of DKA associated with
SGLT-2 inhibitors and such diets. It is important to tell people about these risks and to
advise them to discuss any planned change to a very low carbohydrate or ketogenic
diet with their healthcare professional first.
Full details of the evidence and the committee's discussion are in evidence review B:
pharmacological therapies with cardiovascular and other benefits in people with
type 2 diabetes.
How the recommendations might affect practice
The recommendations are not expected to significantly increase consultation time or
be a change in practice because these should already form part of the prescribing
process. Checking that the person is not at increased risk of DKA when they are
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
1.21 Preventing diabetic ketoacidosis when taking 
SGLT-2 inhibitors 
1.21.1 
Before starting an SGLT-2 inhibitor, check whether the person may be at 
increased risk of diabetic ketoacidosis (DKA), for example if they: 
• have had a previous episode of DKA 
• are unwell with intercurrent illness 
• are at risk of dehydration or volume depletion 
• are following a very low carbohydrate or ketogenic
...
Why the committee made these recommendations 
When starting first-line therapy with metformin and other medicines, the committee 
noted the importance of introducing the medicines sequentially. This enables any side 
effects and intolerances from the first medicine to be identified before the second is 
introduced. In line with current practice, the committee recommended starting with 
metformin a
...
Full details of the evidence and the committee's discussion are in evidence review B: 
pharmacological therapies with cardiovascular and other benefits in people with 
type 2 diabetes. 
How the recommendations might affect practice 
The recommendations are not expected to significantly increase consultation time or 
be a change in practice because these should already form part of the prescribing
...
```
</details>

---

### Sample 6: `nice_t2dm_001_c0019` (NICE Guideline NG28: Type 2 Diabetes in Adults - Management, pp. 10-10)
- **Chunk Type:** `recommendation` | **Condition:** `type_2_diabetes` | **Indexed:** `True`
- **Heading:** `1.3 Dietary advice > 1.3.1`
- **Section Path:** `NICE Guideline NG28: Type 2 Diabetes in Adults - Management > 1.2 Structured education programmes > 1.3 Dietary advice > 1.3.1`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `2009` | **Last Updated:** `2026-02-18`

```markdown
--- CHUNK TEXT ---
1.3 Dietary advice
1.3.1
Provide individualised and ongoing nutritional advice from a healthcare
professional with specific expertise and competencies in nutrition. [2009]
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
Dietary advice and interventions 
1.3 Dietary advice 
1.3.1 
Provide individualised and ongoing nutritional advice from a healthcare 
professional with specific expertise and competencies in nutrition. [2009] 
1.3.2 
Provide dietary advice in a form sensitive to the person's needs, culture and 
beliefs, being sensitive to their willingness to change and the effects on their 
quality of life. [2009
...
```
</details>

---

### Sample 7: `nice_htn_001_c0068` (NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management, pp. 21-21)
- **Chunk Type:** `recommendation` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `Step 1 treatment > Step 2 treatment > 1.4.40`
- **Section Path:** `NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management > [IMAGE] > Step 1 treatment > Step 2 treatment > 1.4.40`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `2019` | **Last Updated:** `2026-02-26`

```markdown
--- CHUNK TEXT ---
step 1 treatment.
Step 2 treatment
1.4.40
Before considering next step treatment for hypertension discuss with the person
if they are taking their medicine as prescribed and support adherence in line with
NICE's guideline on medicines adherence. [2019]
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
1.4.39 
For adults with hypertension already having treatment with bendroflumethiazide 
or hydrochlorothiazide, who have stable, well-controlled blood pressure, continue 
with their current treatment. [2019] 
For a short explanation of why the committee made the 2019 recommendations and 
how they might affect practice, see the rationale and impact section on step 1 
treatment. 
Full details of the
...
```
</details>

---

### Sample 8: `mohfw_htn_002_c0053` (MoHFW Standard Treatment Guidelines - Hypertension (Quick Reference Guide), pp. 17-17)
- **Chunk Type:** `recommendation` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `4.6.6. The preferred 2 drug combinations are combination of calcium channel blockers with ACE`
- **Section Path:** `MoHFW Standard Treatment Guidelines - Hypertension (Quick Reference Guide) > KEY RECOMMENDATIONS > 4.6.6. The preferred 2 drug combinations are combination of calcium channel blockers with ACE`
- **Population Tags:** `[]`
- **Drug Class Tags:** `['ace_inhibitor', 'ccb', 'thiazide']`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
4.6.6. The preferred 2 drug combinations are combination of calcium channel blockers with ACE
inhibitors, ACE inhibitors with low dose diuretics, and calcium channel blockers with low dose
diuretics.
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
Standard Treatment Guidelines -Hypertension
Page 17
Source: ref. Mancia G, Fagard R, Narkiewicz K, et al. 2013 ESH/ESC guidelines for the management of arterial hypertension: the
Task Force for the Management of Arterial Hypertension of the European Society of Hypertension (ESH) and of the European
Society of Cardiology (ESC). Blood pressure. 2013;22(4):193-278.
KEY RECOMMENDATIONS
4.6
The treatme
...
```
</details>

---

### Sample 9: `nice_htn_001_c0052` (NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management, pp. 17-17)
- **Chunk Type:** `recommendation` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `1.4.24`
- **Section Path:** `NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management > [IMAGE] > 1.4.24`
- **Population Tags:** `['type_2_diabetes']`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `2004` | **Last Updated:** `2026-02-26`

```markdown
--- CHUNK TEXT ---
1.4.24
Provide an annual review of care for adults with hypertension to monitor blood
pressure, provide people with support, and discuss their lifestyle, symptoms and
medication. [2004]
Treatment review when type 2 diabetes is diagnosed
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
For a short explanation of why the committee made the 2019 recommendations and 
how they might affect practice, see the rationale and impact section on monitoring 
treatment and blood pressure targets for people without cardiovascular disease. 
Full details of the evidence and the committee's discussion are in evidence review B: 
monitoring the response to treatment. 
1.4.23 
Use the same blood pr
...
```
</details>

---

### Sample 10: `mohfw_htn_002_c0107` (MoHFW Standard Treatment Guidelines - Hypertension (Quick Reference Guide), pp. 28-29)
- **Chunk Type:** `recommendation` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `4.11.6 Prescribe statins for use in hypertensive patients with overt atherosclerotic`
- **Section Path:** `MoHFW Standard Treatment Guidelines - Hypertension (Quick Reference Guide) > 4.11 Integration with other interventions to reduce cardiovascular risks > 4.11.6 Prescribe statins for use in hypertensive patients with overt atherosclerotic`
- **Population Tags:** `['cardiovascular_disease']`
- **Drug Class Tags:** `['statin']`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
4.11.6 Prescribe statins for use in hypertensive patients with overt atherosclerotic
cardiovascular disease [coronary artery disease including acute coronary
syndromes, history of myocardial infarction, stable angina),
cerebrovascular
disease (stroke or transient ischemic attack), and peripheral arterial disease],
regardless of age.
Quick Reference Guide-Hypertension
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
Quick Reference Guide-Hypertension
Page 28
IV labetalol
20-80 mg IV
5-10 min
Scalp 
tingling,
dizziness, 
nausea,
heart block
Can be used in many
hypertensive
emergencies. Avoid in
acute heart failure
IV nicardipine
5-15  mg per
hour as IV
5-10 min
Tachycardia,
headache, 
nausea,
tachycardia
Can be used in many
hypertensive
emergencies. Avoid in
acute heart failure
IV
nitroglycerine
5-100 µg/min
2
...
Quick Reference Guide-Hypertension
Page 29
4.11.7 Prescribe statins  in hypertensive patients

aged more than 40 years, with LDL –cholesterol more than 190 mg/dl,
where secondary causes have been ruled out

in hypertensive patients  who are diabetic and in the age group of 40-79
years,

in hypertensive patients aged more than 40 years with high
cardiovascular risk (3 or more out of list of 11 c
...
```
</details>

---

### Sample 11: `mohfw_htn_001_c0161` (MoHFW STG - Hypertension (Background Document), pp. 64-65)
- **Chunk Type:** `recommendation` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `3.8  All patients should be asked about tobacco use and advised to stop it. (Part 2)`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 3.6 The level of BP and results of the assessment will influence the following: > 3.8  All patients should be asked about tobacco use and advised to stop it. (Part 2)`
- **Population Tags:** `['cardiovascular_disease']`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
-  Medications may have to be taken lifelong, and monitoring with regular checks of
blood pressure is required to note their efficacy. Taking medications regularly
without BP checks is suboptimal, as is checking BP regularly without regular
intake of medications. Most drugs can be given only once a day and can control
BP with minimal side effects.
Patient education should be given in an empathic and culturally appropriate
manner. It should elicit their views of the disease, and their expectations from
treatment. It can be given by both physicians and non-physician staff.
Assessment of a patient with hypertension has the following 5 components
a. Assessing the lifestyle related and other cardiovascular risk factors in
patients with hypertension and the capability each patient's capacity or
willingness to change these factors; e.g.
b. Assessing the target organ damage related to hypertension.
c. Assessing the presence of associated clinical conditions like diabetes,
kidney disease or symptomatic cardiovascular disease.
d. Assessing the clues to a secondary cause of hypertension.
e. Assessment of overall cardiovascular risk of a patient
       To assess patients for each of the above components the healthcare provider should ask
relevant questions, look for relevant features on physical examination, and carry out
appropriate laboratory investigations, which may be available at that level of care or may
require referral .Some of these assessments can be done at any level of care, while others
are only possible at a community health centre level. The tables below have been made
keeping in mind the resources and level of training of healthcare providers in India and are
not exhaustive.

a. Assessment of lifestyle and other cardiovascular risk factors: This is mentioned in
table 1.
Table 1: Assessment of lifestyle and other cardiovascular risk factors
Table 2: Risk factors for cardiovascular disease
A comprehensive list of risk factors is given in table 2. It is vital to ask every hypertensive
patient about their smoking history, confirm it with a relative, since it is often
underreported, and advise on cessation of tobacco use. Tobacco use is an independent
and powerful predictor of cardiovascular diseases.  The diet with regard to fat and salt
content and exercise pattern should be enquired. On examination, body weight and
height should be measured and the body mass index [weight in kg/ (height in metre)
2]calculated. In laboratory evaluation, the blood glucose should be checked to rule out
undetected diabetes (currently available at CHCs), and the lipid profile should be carried
out whenever feasible. Detection of associated diabetes should be an integral part of
evaluation of hypertension and diabetes care should be integrated with the care of
hypertension.
b. Assessment of target organ damage related to hypertension is described in table 2.
Assess lifestyle factors and other cardiovascular risk factors
  History:                             Smoking history
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
64 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
and 90 mm diastolic. The disease is persistent and although it cannot be cured it 
can be controlled. 
• Healthy living habits (lifestyle modification) like stopping smoking, eating a 
healthy diet lower in salt and saturated fat, exercising losing weight has many 
benefits with no cost. It can reduce blo
...
65 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
 
 
 
 
 
 
 
Table 1: Assessment of lifestyle and other cardiovascular risk factors 
Table 2: Risk factors for cardiovascular disease 
A comprehensive list of risk factors is given in table 2. It is vital to ask every hypertensive 
patient about their smoking history, confirm it with a relative, since it
...
```
</details>

---

### Sample 12: `who_htn_001_c0120` (WHO Guideline for the Pharmacological Treatment of Hypertension in Adults, pp. 57-57)
- **Chunk Type:** `recommendation` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `ANNEXES (Part 2)`
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > ANNEXES > ANNEXES (Part 2)`
- **Population Tags:** `['cardiovascular_disease', 'chronic_kidney_disease']`
- **Drug Class Tags:** `['ace_inhibitor', 'arb', 'ccb', 'thiazide']`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
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

<details><summary>Click to view Source Page Text excerpt</summary>

```text
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
Death (all-cause mortality), cardiovascular death (de
...
```
</details>

---

### Sample 13: `who_htn_001_c0075` (WHO Guideline for the Pharmacological Treatment of Hypertension in Adults, pp. 39-41)
- **Chunk Type:** `recommendation` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `IMPLEMENTATION TOOLS > 6.2	 Drug- and dose-specific protocols`
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > 6.1	 Guideline recommendations > IMPLEMENTATION TOOLS > 6.2	 Drug- and dose-specific protocols`
- **Population Tags:** `['pregnancy']`
- **Drug Class Tags:** `['ace_inhibitor', 'arb', 'ccb', 'thiazide']`
- **Applicability Conditions:** `['If  BP is not at goal,\nincrease ARB-CCB (double\nthe dose to Telmisartan 80-\nAmlodipine 10 mg\nonce a day).', 'If BP is not at goal,\nadd a thiazide/thiazide-like\ndiuretic at half-maximal\ndose (hydrochlorothiazide\n25 mg or chlorthalidone\n12.5 mg once a day).', 'If BP is not at goal, increase\nthe thiazide/thiazide-like\ndiuretic (double the dose to\nhydrochlorothiazide 50 mg or\nchlorthalidone 25 mg\nonce a day).', 'If  BP is not at goal,\nrefer to a specialist.']`
- **Exceptions:** `['[\n[ Drugs affecting the renin-angiotensin system (ACEis, ARBs, and aliskiren) have been associated\nwith serious fetal toxicity, including renal and cardiac abnormalities and death; they are\ncontraindicated for use during pregnancy.', 'This protocol is contraindicated for women who are or could become pregnant.', 'with monotherapy\nor free combination therapy)\n[\n[ A CCB, rather than a thiazide-type diuretic or ACEi/ARB, was selected as first-line medication\nif one agent is used, to avoid the need for electrolyte measurements or to alleviate concerns\nregarding potential change in GFR.', '[\n[ Drugs affecting the renin-angiotensin-aldosterone system (ACEis, ARBs, and aliskiren) have been\nassociated with serious fetal toxicity, including renal and cardiac abnormalities and death; they\nare contraindicated for use during pregnancy.']`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
IMPLEMENTATION TOOLS
6.2	 Drug- and dose-specific protocols
Two examples of suggested drug and dose-specific protocols are presented below (Figs 5 and 6). These
should be viewed as examples and other approaches are possible.
Algorithm 1: Initiation of treatment with a single-pill combination
[
[ Beginning treatment with two antihypertensive drugs from different classes is recommended
when baseline BP is >=20/10 mmHg above goal, and should be considered when baseline BP is
>=140/90 mmHg.
[
[ Drugs affecting the renin-angiotensin system (ACEis, ARBs, and aliskiren) have been associated
with serious fetal toxicity, including renal and cardiac abnormalities and death; they are
contraindicated for use during pregnancy.
Fig. 5 Algorithm 1
Start ARB-CCB at
half-maximal doses
(Example*: Telmisartan 40-
Amlodipine 5 mg**
once a day).
Recheck BP in 4-6 weeks;
if BP is at goal, follow up
in 3-6 months.
Recheck BP in 4-6 weeks;
if BP is at goal, follow up
in 3-6 months.
Recheck BP in 4-6 weeks;
if BP is at goal, follow up
in 3-6 months.
Recheck BP in 4-6 weeks;
if BP is at goal, follow up
in 3-6 months.
If  BP is not at goal,
increase ARB-CCB (double
the dose to Telmisartan 80-
Amlodipine 10 mg
once a day).
If BP is not at goal,
add a thiazide/thiazide-like
diuretic at half-maximal
dose (hydrochlorothiazide
25 mg or chlorthalidone
12.5 mg once a day).
If BP is not at goal, increase
the thiazide/thiazide-like
diuretic (double the dose to
hydrochlorothiazide 50 mg or
chlorthalidone 25 mg
once a day).
If  BP is not at goal,
refer to a specialist.
NOTE: Monitor potassium and
kidney function when starting or
changing the dose of ACEi/ARB
or thiazide/thiazide-like diuretic, if
testing is readily available and does
not delay treatment.
This protocol is contraindicated for women who are or could become pregnant. Neither an ACEI or ARB
should be given to pregnant women.
*	 The medications mentioned serve as examples and can be replaced with any two medications from any of the
three drug classes (ACEis/ARBs, CCBs or thiazide/thiazide-like diuretics). Start two individual pills or, if available,
both in a single-pill combination (fixed-dose combination).
**	 Can be replaced with other individual pills or, if available, other single-pill combinations (fixed-dose
combinations).
Algorithm 2: Initiation of treatment not using a single-pill combination (i.e. with monotherapy
or free combination therapy)
[
[ A CCB, rather than a thiazide-type diuretic or ACEi/ARB, was selected as first-line medication
if one agent is used, to avoid the need for electrolyte measurements or to alleviate concerns
regarding potential change in GFR.
[
[ Drugs affecting the renin-angiotensin-aldosterone system (ACEis, ARBs, and aliskiren) have been
associated with serious fetal toxicity, including renal and cardiac abnormalities and death; they
are contraindicated for use during pregnancy.
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
Fig. 4 	An approach for starting treatment not using a single-pill combination (i.e. with monotherapy or 
free combination therapy)
Pharmacological treatment to be initiated under the following circumstances:
[
[
A diagnosis of HTN has already been made.
[
[
Initiation of pharmacological HTN treatment should start no later than four weeks after diagnosis of HTN. 
[
[
If BP level is high or there i
...
GUIDELINE FOR THE PHARMACOLOGICAL TREATMENT OF HYPERTENSION IN ADULTS
6.2	 Drug- and dose-specific protocols
Two examples of suggested drug and dose-specific protocols are presented below (Figs 5 and 6). These 
should be viewed as examples and other approaches are possible.
Algorithm 1: Initiation of treatment with a single-pill combination
[
[ Beginning treatment with two antihypertensive drugs f
...
Algorithm 2: Initiation of treatment not using a single-pill combination (i.e. with monotherapy 
or free combination therapy)
[
[ A CCB, rather than a thiazide-type diuretic or ACEi/ARB, was selected as first-line medication 
if one agent is used, to avoid the need for electrolyte measurements or to alleviate concerns 
regarding potential change in GFR.
[
[ Drugs affecting the renin-angiotensin-al
...
```
</details>

---

### Sample 14: `nice_htn_001_c0059` (NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management, pp. 19-19)
- **Chunk Type:** `recommendation` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `1.4.31`
- **Section Path:** `NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management > [IMAGE] > 1.4.31`
- **Population Tags:** `['cardiovascular_disease', 'type_1_diabetes']`
- **Drug Class Tags:** `['ace_inhibitor', 'arb']`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `2022` | **Last Updated:** `2026-02-26`

```markdown
--- CHUNK TEXT ---
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

<details><summary>Click to view Source Page Text excerpt</summary>

```text
antagonists: not for use in pregnancy, how to use for breastfeeding and 
clarification on breastfeeding. 
1.4.31 
For people with cardiovascular disease: 
• Follow the recommendations for disease-specific indications in the NICE 
guideline on their condition (for example, when prescribing an ACE inhibitor 
or an ARB for secondary prevention of myocardial infarction). Relevant 
recommendations incl
...
```
</details>

---

### Sample 15: `nice_t2dm_001_c0101` (NICE Guideline NG28: Type 2 Diabetes in Adults - Management, pp. 66-68)
- **Chunk Type:** `recommendation` | **Condition:** `type_2_diabetes` | **Indexed:** `True`
- **Heading:** `1.19.3`
- **Section Path:** `NICE Guideline NG28: Type 2 Diabetes in Adults - Management > 1.19 People with frailty > 1.19.3`
- **Population Tags:** `['type_2_diabetes']`
- **Drug Class Tags:** `['glp1_ra', 'sglt2_inhibitor']`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `2026` | **Last Updated:** `2026-02-18`

```markdown
--- CHUNK TEXT ---
1.19.3
Consider reviewing the person's overall diabetes treatment plan to ensure that
they are taking the smallest effective number of medications, at the lowest
effective dosage.
For further guidance on making a treatment plan for people with frailty (including
when associated with multimorbidity), see NICE's guidelines on clinically
assessing and managing multimorbidity, medicines optimisation and shared
decision making. [2026]
Why the committee made these recommendations
Because of concerns about adverse effects and polypharmacy, the committee agreed
that SGLT-2 inhibitors may not be appropriate for some people with frailty and type 2
diabetes.
There was no specific evidence for people with frailty, so the committee could not
recommend a particular method of assessment or cutoff for prescribing SGLT-2
inhibitors. The decision would need to be made based on clinical judgement, taking
into account the needs of each person.
The committee recommended medicines for this group based on:
-  their own expertise
-  common medicine contraindications in this group
-  their knowledge of which medicines were likely to have the most manageable side
effects.
The committee did not recommend GLP-1 receptor agonists and tirzepatide for people
with frailty. However, they agreed that there is no additional safety risk for this
population. Therefore, if a person has a relevant indication and frailty, they can still be
offered a GLP-1 receptor agonists or tirzepatide.
Full details of the evidence and the committee's discussion are in:
-  evidence review E: initial management
-  evidence review F: subsequent management.
How the recommendations might affect practice
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
1.19.3 
Consider reviewing the person's overall diabetes treatment plan to ensure that 
they are taking the smallest effective number of medications, at the lowest 
effective dosage. 
For further guidance on making a treatment plan for people with frailty (including 
when associated with multimorbidity), see NICE's guidelines on clinically 
assessing and managing multimorbidity, medicines optimisa
...
Why the committee made these recommendations 
Because of concerns about adverse effects and polypharmacy, the committee agreed 
that SGLT-2 inhibitors may not be appropriate for some people with frailty and type 2 
diabetes. 
There was no specific evidence for people with frailty, so the committee could not 
recommend a particular method of assessment or cutoff for prescribing SGLT-2 
inhibitors.
...
How the recommendations might affect practice 
Metformin 
The recommendations about the use of metformin may lead to a change in current 
practice but should not lead to a significant cost or resource impact. The price of 
modified-release metformin can fluctuate but, in December 2025, was lower than the 
cost of standard-release metformin. 
DPP-4 inhibitors 
The recommendations about the use of D
...
```
</details>

---

### Sample 16: `nice_t2dm_001_c0118` (NICE Guideline NG28: Type 2 Diabetes in Adults - Management, pp. 77-77)
- **Chunk Type:** `recommendation` | **Condition:** `type_2_diabetes` | **Indexed:** `True`
- **Heading:** `1.24.4`
- **Section Path:** `NICE Guideline NG28: Type 2 Diabetes in Adults - Management > 1.24 Reviewing other medicines > 1.24.4`
- **Population Tags:** `[]`
- **Drug Class Tags:** `['glp1_ra']`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `2026` | **Last Updated:** `2026-02-18`

```markdown
--- CHUNK TEXT ---
1.24.4
Stop GLP-1 receptor agonists or tirzepatide if they do not help the person reach
their individualised glycaemic targets and they are not being taken for their
cardiovascular benefits. [2026]
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
How the recommendation might affect practice 
The recommendations will lead to people taking SGLT-2 inhibitors and GLP-1 receptor 
agonists or tirzepatide for longer. This will initially increase costs. However, the long-
term protective benefits of these medicines will reduce the need to treat future 
cardiovascular and renal problems, which will lead to cost savings. Otherwise, the 
recommendati
...
```
</details>

---

### Sample 17: `mohfw_htn_001_c0260` (MoHFW STG - Hypertension (Background Document), pp. 106-106)
- **Chunk Type:** `recommendation` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `5.7 Community based health workers can be trained to play a critical role in meeting the`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 5.6 Diagnosis and management of hypertension in India, needs to be embedded in the > 5.7 Community based health workers can be trained to play a critical role in meeting the`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
5.7 Community based health workers can be trained to play a critical role in meeting the
challenge of undetected, untreated and uncontrolled hypertension in India. They can
improve detection, promote lifestyle modifications, monitor response and ensure
adherence to therapy. They can also help prevent hypertension by advising appropriate
lifestyle modifications in those who have a high normal BP ( 130-139 mm Hg systolic and
85-89 mm Hg diastolic)
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
106 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
5.7 Community based health workers can be trained to play a critical role in meeting the 
challenge of undetected, untreated and uncontrolled hypertension in India. They can 
improve detection, promote lifestyle modifications, monitor response and ensure 
adherence to therapy. They can also help prevent
...
```
</details>

---

### Sample 18: `mohfw_t2dm_001_c0019` (MoHFW Standard Treatment Guidelines - Endocrinology (Diabetes Mellitus), pp. 19-20)
- **Chunk Type:** `recommendation` | **Condition:** `type_2_diabetes` | **Indexed:** `True`
- **Heading:** `Alpha glucosidase inhibitors > DPP-4 Inhibitors (Part 4)`
- **Section Path:** `MoHFW Standard Treatment Guidelines - Endocrinology (Diabetes Mellitus) > -  ECG > Alpha glucosidase inhibitors > DPP-4 Inhibitors (Part 4)`
- **Population Tags:** `[]`
- **Drug Class Tags:** `['insulin', 'metformin', 'sulfonylurea']`
- **Applicability Conditions:** `None`
- **Exceptions:** `['Sick day guidelines: The objective of these guidelines is to avoid hospitalisation during situations\nlike acute diarrhoea, vomiting febrile illness.', 'All diabetics should be taught these simple\nrules or a handout may be given mentioning- In any febrile illness or whenever there is poor intake\nof food and water due to any illness dehydration and ketosis must be avoided .Never omit your\nmedication -insulin or OAD.']`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
Hypoglycemia: more common in following situations
Patients who are older, have renal or liver disease
Have a long duration of diabetes, autonomic neuropathy, hypopituitarism
Regularly miss meals, erratic meal pattern
unusual exercise
Take greater than the prescribed dose of their medication
Concomitant medication - Levofloxacin*, beta blockers,
* hyperglycemia is more common with Levofloxacin though rarely hypoglycemia can occur.

Diabetes Education: Educating the patient for lifestyle modifications, hypoglycemia, insulin
therapy, foot care, benefits of quitting smoking and tobacco, reducing alcohol helps in achieving
the targets of therapy.

Sick day guidelines: The objective of these guidelines is to avoid hospitalisation during situations
like acute diarrhoea, vomiting febrile illness. And if at all it is required the patient is able to prevent
DKA or other diabetes related acute complications. All diabetics should be taught these simple
rules or a handout may be given mentioning- In any febrile illness or whenever there is poor intake
of food and water due to any illness dehydration and ketosis must be avoided .Never omit your
medication -insulin or OAD. Infact sometimes a higher dose is required when we are sick even
when we are not eating. Blood glucose and urine ketones must be checked frequently -every 4-6
hourly. Type 1 diabetics may require monitoring 2-4 hourly. Try to eat small amounts of
carbohydrates every 2-4 hourly ,soft food or liquids are easier to take .!00-120ml of fluid every
hour (carbohydrate free if glucose is >250 and with carbohydrates if glucose is less than 250. Fluids
and carbohydrates are required to maintain hydration and calorie requirement and preventing
hypoglycemia. Dehydration and worsening ketosis are ominous signs . Physician must be consulted
if nausea or vomiting persists with ketosis .If blood glucose is persisting more than 300 on two
consecutive times .If breathing becomes rapid or laboured, fever >100 degree F persisting more
than 24 hours, persisting diarrhoea or vomiting or pain abdomen. Inability to take fluids for more
than 4 hours due to vomiting drowsiness or altered sensorium or anyother unexplained symptoms.
Drug treatment adjustments during sickdays- stop metformin, and preferably other OADs except
sulphonylureas, increase or decrease sulphonylureas according to the glucose readings. Addition of
short acting insulin may be required to OADs.In situations where patient is already on insulin, long
acting or intermediate insulin should be continued in the same doses. Dose of short acting insulin
can be adjusted by measuring sugars 4-6 hourly.Premixed insulins should be supplimented by short
acting insulins usually 20-25 %extra or more dose of insulin is required in addition to the usual
dose of insulin.However if vomiting or diarrhoea persists hypoglycemia can occur.

Prevention of diabetes: Identify the high risk population .Fasting glucose and OGTT should  be
used for identifying IFG and IGT.No drug is recommended for the prevention of diabetes.MF and
Acarbose can be used in IGT and IFG.Lifestyle measures mentioned in section 2.3 should be
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
19
 
Most of these patients will be on insulin which preferably should be given as bolus -basal therapy 
i.e.3-4 boluses of short acting insulin and a bedtime dose of NPH or long acting insulin. Stable 
patients who are eating well can be managed with 2-3 time insulin (premixed or split mixed)In all 
hemodynamically compromised situations, acute myocardial infarction, stroke, high dose steroid 
th
...
20
 
short acting insulin may be required to OADs.In situations where patient is already on insulin, long 
acting or intermediate insulin should be continued in the same doses. Dose of short acting insulin 
can be adjusted by measuring sugars 4-6 hourly.Premixed insulins should be supplimented by short 
acting insulins usually 20-25 %extra or more dose of insulin is required in addition to the usu
...
```
</details>

---

### Sample 19: `who_htn_001_c0071` (WHO Guideline for the Pharmacological Treatment of Hypertension in Adults, pp. 36-37)
- **Chunk Type:** `recommendation` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `5.5	 Research gaps`
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > 5.4	 Future updating of the guideline > 5.5	 Research gaps`
- **Population Tags:** `['cardiovascular_disease', 'chronic_kidney_disease']`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
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

<details><summary>Click to view Source Page Text excerpt</summary>

```text
GUIDELINE FOR THE PHARMACOLOGICAL TREATMENT OF HYPERTENSION IN ADULTS
5	 Publication, implementation, 
evaluation and research gaps
5.1	 Publication 
This guideline is available to download from the WHO website. Given that an overview of published 
systematic reviews was used for the development of the guideline, all reviews are already published and 
available online. 
5.2	 Implementation and dis
...
[
[ There is a need for periodic analysis of trials in order to capture effects of changes over time in 
background epidemiology of CVD, non-BP treatments, competing risks, etc.
[
[ More evidence is needed in LICs, MICs and other non-North American/European countries.
[
[ An assessment of the feasibility, resource needs, and costs of intensive treatment in real clinical 
practice is needed. The re
...
```
</details>

---

### Sample 20: `mohfw_htn_002_c0075` (MoHFW Standard Treatment Guidelines - Hypertension (Quick Reference Guide), pp. 24-24)
- **Chunk Type:** `recommendation` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `4.8.4.2`
- **Section Path:** `MoHFW Standard Treatment Guidelines - Hypertension (Quick Reference Guide) > GRADE 3 HYPERTENSION (SBP > =180, DBP > =110) > 4.8.4.2`
- **Population Tags:** `['cardiovascular_disease']`
- **Drug Class Tags:** `['ace_inhibitor', 'arb']`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
4.8.4.2
In patients with a history of stroke or TIA, initiation of drug treatment should be
considered even with Grade 1 hypertension, and a systolic BP of less than 140 mm Hg
should be targeted. An ACE inhibitor/ARB is considered an initial drug.
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
Quick Reference Guide-Hypertension
Page 24
4.8.3.4 Use of ACE inhibitors and Thiazide or thiazide like diuretics should be used as
other antihypertensive agents, and in the presence of volume overload, loop
diuretics like frusemide may be used.
4.8.4
Cerebrovascular disease:
4.8.4.1
Prevention of stroke can occur with all classes of antihypertensive drugs if BP is
effectively controlled.
4.8.4.2
I
...
```
</details>

---

### Sample 21: `nice_t2dm_001_c0080` (NICE Guideline NG28: Type 2 Diabetes in Adults - Management, pp. 49-50)
- **Chunk Type:** `recommendation` | **Condition:** `type_2_diabetes` | **Indexed:** `True`
- **Heading:** `recommendation on monitoring because it is covered by MHRA drug safety updates.`
- **Section Path:** `NICE Guideline NG28: Type 2 Diabetes in Adults - Management > 1.15 People with atherosclerotic cardiovascular > recommendation on monitoring because it is covered by MHRA drug safety updates.`
- **Population Tags:** `['cardiovascular_disease']`
- **Drug Class Tags:** `['glp1_ra', 'metformin', 'sglt2_inhibitor']`
- **Applicability Conditions:** `['When\ncompared in health economic evaluation, adding subcutaneous semaglutide to an\nSGLT-2 inhibitor and metformin was cost effective.', 'When\ncompared with placebo in clinical trials, GLP-1 receptor agonists, including\nsemaglutide also showed cardiovascular benefits, regardless of other treatment\nreceived.']`
- **Exceptions:** `['Because of this, the committee agreed that people with atherosclerotic\ncardiovascular disease should receive therapy combining an SGLT-2 inhibitor and\nsubcutaneous semaglutide if metformin is contraindicated or not tolerated.']`
- **Recommendation Year:** `None` | **Last Updated:** `2026-02-18`

```markdown
--- CHUNK TEXT ---
recommendation on monitoring because it is covered by MHRA drug safety updates.
See MHRA guidance on GLP-1 receptor agonists: reminder of the potential side
effects and to be aware of the potential for misuse, GLP-1 receptor agonists and dual
GLP-1/GIP receptor agonists: strengthened warnings on acute pancreatitis, including
necrotising and fatal cases and semaglutide (Wegovy, Ozempic and Rybelsus): risk of
non-arteritic anterior ischemic optic neuropathy (NAION) for more details.
The committee made the decision to recommend this medicine in combination with
metformin and an SGLT-2 inhibitor based on:
-  evidence they had from a pooled analysis
-  their own clinical experience.
The evidence in the pooled network meta-analysis came from a review that looked at
the cost and clinical effectiveness of adding subsequent therapies to previous
treatment. It showed clinical benefits from GLP-1 receptor agonists, but most studies
in the evidence review did not give separate results based on the number or type of
other treatments received. A small number of studies specifically included triple
therapy combining GLP-1 receptor agonists, SGLT-2 inhibitors and metformin. When
compared in health economic evaluation, adding subcutaneous semaglutide to an
SGLT-2 inhibitor and metformin was cost effective.
The evidence for combination therapy with metformin and SGLT-2 inhibitors showed
that the cardiovascular benefits came from the SGLT-2 inhibitors alone. This was clear
because people receiving metformin and placebo did not get the same benefits. When
compared with placebo in clinical trials, GLP-1 receptor agonists, including
semaglutide also showed cardiovascular benefits, regardless of other treatment
received. Because of this, the committee agreed that people with atherosclerotic
cardiovascular disease should receive therapy combining an SGLT-2 inhibitor and
subcutaneous semaglutide if metformin is contraindicated or not tolerated.
Full details of the evidence and the committee's discussion are in:
-  evidence review E: initial management
-  evidence review F: subsequent management.
How the recommendations might affect practice
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
agonists and tirzepatide, and a potential for misuse. However, they did not make a 
recommendation on monitoring because it is covered by MHRA drug safety updates. 
See MHRA guidance on GLP-1 receptor agonists: reminder of the potential side 
effects and to be aware of the potential for misuse, GLP-1 receptor agonists and dual 
GLP-1/GIP receptor agonists: strengthened warnings on acute pancreatit
...
How the recommendations might affect practice 
Metformin 
The recommendations about the use of metformin may lead to a change in current 
practice but should not lead to a significant cost or resource impact. The price of 
modified-release metformin can fluctuate but, in December 2025, was lower than the 
cost of standard-release metformin. 
SGLT-2 inhibitors were recommended by NICE in 2022. They
...
```
</details>

---

### Sample 22: `mohfw_htn_001_c0158` (MoHFW STG - Hypertension (Background Document), pp. 62-62)
- **Chunk Type:** `recommendation` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `3.5   The overall risk of cardiovascular events can be assessed from these assessments as`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 3.4   The risk factors, target organ damage and associated clinical conditions can be > 3.5   The overall risk of cardiovascular events can be assessed from these assessments as`
- **Population Tags:** `['cardiovascular_disease', 'chronic_kidney_disease']`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
3.5   The overall risk of cardiovascular events can be assessed from these assessments as
follows:
Level of blood pressure: Grade 2 Hypertension even in isolation confers
moderate risk (20-30% risk of CV event over 10 years), while Grade 3
hypertension confers high risk (Over 30% risk of CV event over 10 years).

Risk factors: Presence of 3 or more risk factors confers moderate to high
risk even in a patient with Grade 1 hypertension, while even fewer risk
factors increase risk in Grade 2 hypertension.
TOD/Diabetes/CKD/Clinical cardiovascular disease: Presence of any target
organ damage, diabetes, chronic kidney disease or clinical cardiovascular
disease confers high to very high risk on patients.
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
62 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
smoking cessation) is to be reinforced by all cadres of health workers. 
Screening for hyperlipidemia can be suggested and carried out in 
patients at PHC/CHC especially in those who are obese, or have family 
history of premature coronary artery disease, or have existing 
cardiovascular disease. 
3.4.2 P
...
```
</details>

---

### Sample 23: `nice_t2dm_001_c0105` (NICE Guideline NG28: Type 2 Diabetes in Adults - Management, pp. 69-69)
- **Chunk Type:** `recommendation` | **Condition:** `type_2_diabetes` | **Indexed:** `True`
- **Heading:** `1.20.2`
- **Section Path:** `NICE Guideline NG28: Type 2 Diabetes in Adults - Management > 1.20 Introducing medicines in a stepwise manner > 1.20.2`
- **Population Tags:** `['type_2_diabetes']`
- **Drug Class Tags:** `['glp1_ra', 'metformin', 'sglt2_inhibitor']`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `2026` | **Last Updated:** `2026-02-18`

```markdown
--- CHUNK TEXT ---
1.20.2
When an adult with type 2 diabetes starts initial therapy with metformin and one
or more other medicines:
-  introduce the medicines one at a time, starting with metformin and checking
tolerability
-  if using an SGLT-2 inhibitor, start this as soon as metformin is at the
maximum tolerated dose
-  if using a GLP-1 receptor agonist or tirzepatide, start this as soon as the
SGLT-2 inhibitor is at the maximum tolerated dose.
For guidance on how to prevent any negative impact on the person's eyes
from starting blood glucose lowering treatment, see the section on effects of
a rapid reduction in HbA1c in NICE's guideline on diabetic retinopathy. [2022,
amended 2026]
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
How to introduce medicines 
Recommendations in this section that cover dipeptidyl peptidase-4 (DPP-4) 
inhibitors, glucagonlike peptide-1 (GLP-1) receptor agonists, sulfonylureas and 
sodium–glucose cotransporter-2 (SGLT-2) inhibitors refer to each of these groups of 
medicines at class level. 
For GLP-1 receptor agonists, at the time of publication (February 2026) this only 
includes liraglutide,
...
```
</details>

---

### Sample 24: `mohfw_htn_001_c0192` (MoHFW STG - Hypertension (Background Document), pp. 82-82)
- **Chunk Type:** `recommendation` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `4.6.2 In patients with Grade 3 hypertension, the therapy should be initiated with two`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 4.5 Key recommendation: Classes of antihypertensive drugs & preferred choices > 4.6.2 In patients with Grade 3 hypertension, the therapy should be initiated with two`
- **Population Tags:** `[]`
- **Drug Class Tags:** `['ace_inhibitor', 'ccb', 'thiazide']`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
4.6.2 In patients with Grade 3 hypertension, the therapy should be initiated with two
drugs, in combination with lifestyle modifications (Step 2 in table 13). The
combinations can be calcium channel blocker (amlodipine) + ACE inhibitor (enalapril)
or calcium channel blocker (amlodipine) + thiazide diuretic (hydrochlorothiazide) or
ACE inhibitor (enalapril) + thiazide diuretic (hydrochlorothiazide).
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
82 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
4.6Key recommendation: The treatment regimen and the use of combinations: 
 
4.6.1 In patients with Grade 1 or Grade 2 hypertension, therapy can be initiated with one 
drug (CCBs, ACE inhibitors, thiazide diuretics) in combination with lifestyle 
modifications.(Step 1 in table 13) Average initial doses ca
...
```
</details>

---

### Sample 25: `mohfw_htn_002_c0106` (MoHFW Standard Treatment Guidelines - Hypertension (Quick Reference Guide), pp. 28-28)
- **Chunk Type:** `recommendation` | **Condition:** `both` | **Indexed:** `True`
- **Heading:** `4.11.5 The use of low dose aspirin in patients with diabetes without cardiovascular or`
- **Section Path:** `MoHFW Standard Treatment Guidelines - Hypertension (Quick Reference Guide) > 4.11 Integration with other interventions to reduce cardiovascular risks > 4.11.5 The use of low dose aspirin in patients with diabetes without cardiovascular or`
- **Population Tags:** `[]`
- **Drug Class Tags:** `['antiplatelet']`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
4.11.5 The use of low dose aspirin in patients with diabetes without cardiovascular or
cerebrovascular disease is not recommended in view of the uncertain risk-benefit
ratio.
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
Quick Reference Guide-Hypertension
Page 28
IV labetalol
20-80 mg IV
5-10 min
Scalp 
tingling,
dizziness, 
nausea,
heart block
Can be used in many
hypertensive
emergencies. Avoid in
acute heart failure
IV nicardipine
5-15  mg per
hour as IV
5-10 min
Tachycardia,
headache, 
nausea,
tachycardia
Can be used in many
hypertensive
emergencies. Avoid in
acute heart failure
IV
nitroglycerine
5-100 µg/min
2
...
```
</details>

---

## 3. All ICMR Poster Chunks Audit (High-Fidelity) (Total: 23)

### Sample 1: `icmr_htn_001_c0001` (ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), pp. 1-1)
- **Chunk Type:** `front_matter` | **Condition:** `hypertension` | **Indexed:** `False`
- **Heading:** `STW Metadata & Title`
- **Section Path:** `ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) > STW Metadata & Title`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
Standard Treatment Workflow (STW): HYPERTENSION IN ADULTS
ICD-11 BA00 | Printed Date: May/2026
Indian Council of Medical Research (ICMR) and Department of Health Research (DHR), MoHFW, Government of India.
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and 
available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by the treating physician. There will
...
```
</details>

---

### Sample 2: `icmr_htn_001_c0002` (ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), pp. 1-1)
- **Chunk Type:** `front_matter` | **Condition:** `hypertension` | **Indexed:** `False`
- **Heading:** `Abbreviations`
- **Section Path:** `ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) > Abbreviations`
- **Population Tags:** `['cardiovascular_disease']`
- **Drug Class Tags:** `['ace_inhibitor', 'arb', 'ccb', 'mra_spironolactone']`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
ABBREVIATIONS:
- ACEi: Angiotensin-converting enzyme inhibitor
- ARB: Angiotensin receptor blocker
- BP: Blood pressure
- CCB: Calcium channel blocker
- FDC: Fixed-dose combination
- HFrEF: Heart failure with reduced ejection fraction
- HFpEF: Heart failure with preserved ejection
- MRA: Mineralocorticoid receptor antagonist
- RAAS: Renin-angiotensin-aldosterone system
- OD: Once daily
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and 
available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by the treating physician. There will
...
```
</details>

---

### Sample 3: `icmr_htn_001_c0003` (ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), pp. 1-1)
- **Chunk Type:** `recommendation` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `Risk Factors`
- **Section Path:** `ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) > Risk Factors`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
RISK FACTORS FOR HYPERTENSION:
- High salt intake
- Sedentary behavior
- Tobacco and alcohol consumption
- Obesity

All adults >= 18 years should get blood pressure measured at every clinic visit.
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and 
available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by the treating physician. There will
...
```
</details>

---

### Sample 4: `icmr_htn_001_c0004` (ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), pp. 1-1)
- **Chunk Type:** `definition` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `Diagnosis of Hypertension`
- **Section Path:** `ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) > Diagnosis of Hypertension`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `['If Systolic BP >= 160 AND/OR Diastolic BP >= 100 measurement of one clinic visit is sufficient for diagnosing hypertension']`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
DIAGNOSIS OF HYPERTENSION:
- Systolic BP >= 140 AND/OR Diastolic BP >= 90 mmHg on two different clinic visits.
- Population screening BP reading may count as the first reading.
- Use the higher category if only Systolic or Diastolic BP is high; manage based on the higher value.
- If Systolic BP >= 160 AND/OR Diastolic BP >= 100 mmHg, measurement of one clinic visit is sufficient for diagnosing hypertension.
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and 
available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by the treating physician. There will
...
```
</details>

---

### Sample 5: `icmr_htn_001_c0005` (ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), pp. 1-1)
- **Chunk Type:** `table` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `Blood Pressure Classification`
- **Section Path:** `ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) > Blood Pressure Classification`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
### BLOOD PRESSURE LEVELS & CLASSIFICATION

| Classification | Blood Pressure Levels | Action |
| --- | --- | --- |
| Normal | Systolic < 120 AND Diastolic < 80 mmHg | Reassure and encourage healthy lifestyle |
| Elevated BP | Systolic 120-139 AND/OR Diastolic 80-89 mmHg | Lifestyle modification |
| Hypertension Grade 1 | Systolic 140-159 AND/OR Diastolic 90-99 mmHg | Pharmacological management + Lifestyle modification |
| Hypertension Grade 2 | Systolic 160-179 AND/OR Diastolic 100-109 mmHg | Pharmacological management + Lifestyle modification |
| Hypertension Grade 3 | Systolic >= 180 AND/OR Diastolic >= 110 mmHg | Pharmacological management + Lifestyle modification |
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and 
available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by the treating physician. There will
...
```
</details>

---

### Sample 6: `icmr_htn_001_c0006` (ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), pp. 1-1)
- **Chunk Type:** `recommendation` | **Condition:** `both` | **Indexed:** `True`
- **Heading:** `Blood Pressure Control Targets`
- **Section Path:** `ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) > Blood Pressure Control Targets`
- **Population Tags:** `['cardiovascular_disease', 'chronic_kidney_disease', 'elderly', 'type_2_diabetes']`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `['In patients with diabetes mellitus, CKD, or established CVD: SBP < 130 and DBP < 80 mmHg', 'For adults aged >= 80 years: SBP < 150 and DBP < 90 mmHg']`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
BLOOD PRESSURE CONTROL TARGETS:
- All adults: SBP < 140 and DBP < 90 mmHg.
- Diabetes mellitus, CKD, or established CVD: SBP < 130 and DBP < 80 mmHg (optimal target if tolerated).
- Age >= 80 years: SBP < 150 and DBP < 90 mmHg.
- Assess orthostatic BP at every visit of adults >= 65 years.
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and 
available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by the treating physician. There will
...
```
</details>

---

### Sample 7: `icmr_htn_001_c0007` (ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), pp. 1-1)
- **Chunk Type:** `other` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `Lifestyle Modification`
- **Section Path:** `ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) > Lifestyle Modification`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
LIFESTYLE MODIFICATION FOR HYPERTENSION:
- Advise all patients against tobacco and alcohol use.
- Limit salt intake to < 5g/day.
- Use healthy oils, eat more fruits/vegetables, prefer fish/omega-3 foods such as nuts and seeds.
- Physical Activity: 30 minutes daily.
- Weight Management: Keep BMI < 23 kg/m2 and waist circumference: < 90 cm (men) and < 80 cm (women).
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and 
available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by the treating physician. There will
...
```
</details>

---

### Sample 8: `icmr_htn_001_c0008` (ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), pp. 1-1)
- **Chunk Type:** `monitoring` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `Monitoring of Hypertension`
- **Section Path:** `ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) > Monitoring of Hypertension`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
MONITORING OF HYPERTENSION:
- BP to be measured at every clinical visit.
- Evaluate for diabetes (fasting plasma glucose or HbA1c) and manage accordingly.
- Annual evaluations: Serum creatinine, Urine (albumin, sugar, creatinine), Lipid profile, Fundoscopy.
- Additional investigations (if required): ECG, ECHO.
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and 
available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by the treating physician. There will
...
```
</details>

---

### Sample 9: `icmr_htn_001_c0009` (ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), pp. 1-1)
- **Chunk Type:** `recommendation` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `Hypertension Urgency and Emergency`
- **Section Path:** `ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) > Hypertension Urgency and Emergency`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `['Do not use IV medicines for asymptomatic hypertension urgency']`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
HYPERTENSION URGENCY & EMERGENCY:
Definition: Systolic BP >= 180 AND/OR Diastolic BP >= 120 mmHg.

Red Flags / Symptoms of target organ damage:
- Visual disturbance, dizziness, confusion, headache, chest pain, breathlessness (worse lying down/leg swelling), sudden weakness, speech/swallowing difficulty, vision problem.
- Management: Stabilise ABC and refer to emergency care at higher center.

Hypertension Urgency (Without acute target-organ damage):
- Management: Start oral antihypertensive drugs. Do NOT use IV medicines. Reduce BP gradually over 24-48 hours. Refer/admit if symptoms or organ damage suspected. Follow-up within 1 week.
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and 
available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by the treating physician. There will
...
```
</details>

---

### Sample 10: `icmr_htn_001_c0010` (ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), pp. 1-1)
- **Chunk Type:** `recommendation` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `Pharmacological Strategy`
- **Section Path:** `ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) > Pharmacological Strategy`
- **Population Tags:** `['cardiovascular_disease', 'elderly']`
- **Drug Class Tags:** `['ace_inhibitor', 'arb', 'beta_blocker', 'ccb', 'thiazide']`
- **Applicability Conditions:** `None`
- **Exceptions:** `['DO NOT combine two RAAS blockers as it increases the risk of adverse effects, including acute kidney injury (AKI)']`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
PHARMACOLOGICAL STRATEGY FOR HYPERTENSION:
- Combination therapy (two drugs from two different classes) could be the default initial pharmacological treatment for most adults with hypertension.
- Single-pill combinations (SPCs/fixed-dose combinations, FDCs) are preferred over multiple pills to improve adherence.
- Monotherapy remains appropriate only for (a) low-risk Grade 1 HTN, (b) elderly >= 80 years, or (c) frail patients.
- A CCB or Thiazide/Thiazide-like diuretic should be used with a Renin-Angiotensin-Aldosterone System (RAAS) blocker (either an ACEi or an ARB).
- Three-drug combination, often a RAAS blocker, CCB, or a Thiazide/Thiazide-like diuretic, if blood pressure is not controlled with the initial two-drug combination.
- Beta-blockers are appropriate in cases of angina, postmyocardial infarction, heart failure (HFrEF or HFpEF with ischemia).
- DO NOT combine two RAAS blockers as it increases the risk of adverse effects, including acute kidney injury (AKI).
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and 
available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by the treating physician. There will
...
```
</details>

---

### Sample 11: `icmr_htn_001_c0011` (ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), pp. 1-1)
- **Chunk Type:** `recommendation` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `Treatment Protocols (ATTACC & AATTCC)`
- **Section Path:** `ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) > Treatment Protocols (ATTACC & AATTCC)`
- **Population Tags:** `[]`
- **Drug Class Tags:** `['arb', 'ccb', 'mra_spironolactone', 'thiazide']`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
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

<details><summary>Click to view Source Page Text excerpt</summary>

```text
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and 
available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by the treating physician. There will
...
```
</details>

---

### Sample 12: `icmr_htn_001_c0012` (ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), pp. 1-1)
- **Chunk Type:** `table` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `Drug Therapy Table: Doses, Contraindications & Side Effects`
- **Section Path:** `ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) > Drug Therapy Table: Doses, Contraindications & Side Effects`
- **Population Tags:** `['pregnancy']`
- **Drug Class Tags:** `['ace_inhibitor', 'arb', 'beta_blocker', 'ccb', 'mra_spironolactone', 'thiazide']`
- **Applicability Conditions:** `None`
- **Exceptions:** `['Pregnancy is a strict contraindication for ACE inhibitors, ARBs, and Diuretics', 'Heart failure is contraindicated for initial CCB', 'Asthma and A-V block are contraindicated for Beta-blockers']`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
### ANTIHYPERTENSIVE DRUG THERAPY: DOSES, CONTRAINDICATIONS & SIDE EFFECTS

| Drug Class | Drug | Doses | Contraindications | Side Effects |
| --- | --- | --- | --- | --- |
| CCB | Amlodipine | 2.5–10 mg OD | Heart failure | Pedal edema, constipation |
| ACE inhibitors | Enalapril | 5–40 mg OD or BD | Pregnancy, Women planning pregnancy, prior angioedema to ACEi, Hyperkalemia, Bilateral renal artery stenosis | Dry cough, angioedema, hyperkalemia, rise in serum creatinine |
| ACE inhibitors | Ramipril | 2.5–10 mg OD or BD | Pregnancy, Women planning pregnancy, prior angioedema to ACEi, Hyperkalemia, Bilateral renal artery stenosis | Dry cough, angioedema, hyperkalemia, rise in serum creatinine |
| ARB | Losartan | 50–100 mg OD | Pregnancy, Women planning pregnancy, Hyperkalemia, Bilateral renal artery stenosis | Hypotension, acute renal failure, hyperkalemia |
| ARB | Olmesartan | 20–40 mg OD | Pregnancy, Women planning pregnancy, Hyperkalemia, Bilateral renal artery stenosis | Hypotension, acute renal failure, hyperkalemia |
| ARB | Telmisartan | 40–80 mg OD | Pregnancy, Women planning pregnancy, Hyperkalemia, Bilateral renal artery stenosis | Hypotension, acute renal failure, hyperkalemia |
| Diuretics | Chlorthalidone | 12.5–25 mg OD | Pregnancy, Gout | Glucose intolerance, metabolic syndrome, hyponatremia, hypercalcemia, hypokalemia |
| Diuretics | Hydrochlorothiazide | 12.5 mg OD | Pregnancy, Gout | Glucose intolerance, metabolic syndrome, hyponatremia, hypercalcemia, hypokalemia |
| Beta-blockers | Carvedilol | 12.5–50 mg OD or BD | Asthma, severe bradycardia, A-V block (grade 2 or 3), uncontrolled heart failure | Depression, fatigue, reduced exercise tolerance, hyperglycemia, sexual dysfunction |
| Beta-blockers | Labetalol | 100–400 mg BD | Asthma, severe bradycardia, A-V block (grade 2 or 3), uncontrolled heart failure | Depression, fatigue, reduced exercise tolerance, hyperglycemia, sexual dysfunction |
| Beta-blockers | Metoprolol | 50–100 mg OD or BD | Asthma, severe bradycardia, A-V block (grade 2 or 3), uncontrolled heart failure | Depression, fatigue, reduced exercise tolerance, hyperglycemia, sexual dysfunction |
| Beta-blockers | Nebivolol | 5 mg OD | Asthma, severe bradycardia, A-V block (grade 2 or 3), uncontrolled heart failure | Depression, fatigue, reduced exercise tolerance, hyperglycemia, sexual dysfunction |
| Aldosterone antagonist | Spironolactone | 25 mg OD | Hyperkalemia | Mastalgia, gynecomastia, sexual dysfunction, gout |
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and 
available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by the treating physician. There will
...
```
</details>

---

### Sample 13: `icmr_htn_001_c0013` (ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), pp. 1-1)
- **Chunk Type:** `reference` | **Condition:** `hypertension` | **Indexed:** `False`
- **Heading:** `References`
- **Section Path:** `ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) > References`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
REFERENCES:
1. Mancia G, Kreutz R, Brunström M, et al. 2023 ESH Guidelines for the management of arterial hypertension. J Hypertens. 2023;41(12):1874–2071.
2. Joseph G, Thanh Pham V, Kragh Andersen P, et al. Cardiovascular events according to blood pressure thresholds recommended by ACC/AHA. Blood Press. 2024;33(1):2380346.
3. Gupta R, Maheshwari A, Verma N, Narasingan SN, Tripathi K, Joshi S, Manoria PC, et al. Indian Society of Hypertension (InSH) Consensus Guideline for the Management of Hypertension, 2025. Hypertension Journal. 2025;11(4):76–138.
4. Ministry of Health and Family Welfare, Government of India. Training modules on non-communicable diseases. New Delhi: MoHFW; 2025.
5. ICMR-National Institute of Epidemiology. India Hypertension Control Initiative: Training modules. Chennai, 2021.
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and 
available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by the treating physician. There will
...
```
</details>

---

### Sample 14: `icmr_t2dm_001_c0001` (ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11), pp. 1-1)
- **Chunk Type:** `front_matter` | **Condition:** `type_2_diabetes` | **Indexed:** `False`
- **Heading:** `STW Metadata & Title`
- **Section Path:** `ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11) > STW Metadata & Title`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
Standard Treatment Workflow (STW): DIABETES MELLITUS TYPE 2
ICD-10-E11 | Printed Date: July/ 2022
Department of Health Research, Ministry of Health & Family Welfare, Government of India.
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
Standard Treatment Workﬂow (STW)
DIABETES MELLITUS TYPE 2
ICD-10-E11
      KEEP LOW THRESHOLD FOR DIAGNOSIS. MAKE SURE TO FOLLOW UP TO MEET TARGETS
ABBREVIATIONS
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and 
are based on expert opinions and available scientiﬁc
...
```
</details>

---

### Sample 15: `icmr_t2dm_001_c0002` (ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11), pp. 1-1)
- **Chunk Type:** `front_matter` | **Condition:** `type_2_diabetes` | **Indexed:** `False`
- **Heading:** `Abbreviations`
- **Section Path:** `ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11) > Abbreviations`
- **Population Tags:** `['cardiovascular_disease', 'chronic_kidney_disease', 'pregnancy']`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
ABBREVIATIONS:
- ALT: Alanine transaminase
- AST: Aspartate aminotransferase
- BMI: Body mass index
- BP: Blood pressure
- CAD: Coronary artery disease
- CGM: Continuous glucose monitor
- CKD: Chronic kidney disease
- DTR: Deep tendon reflex
- ECG: Electrocardiogram
- FPG: Fasting plasma glucose
- GDM: Gestational diabetes mellitus
- HDL: High-density lipoprotein
- LDL: Low-density lipoprotein
- LFT: Liver function test
- OAD: Oral antidiabetic drug
- OGTT: Oral glucose tolerance test
- SMBG: Self-monitoring of blood glucose
- TG: Triglyceride
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
Standard Treatment Workﬂow (STW)
DIABETES MELLITUS TYPE 2
ICD-10-E11
      KEEP LOW THRESHOLD FOR DIAGNOSIS. MAKE SURE TO FOLLOW UP TO MEET TARGETS
ABBREVIATIONS
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and 
are based on expert opinions and available scientiﬁc
...
```
</details>

---

### Sample 16: `icmr_t2dm_001_c0003` (ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11), pp. 1-1)
- **Chunk Type:** `definition` | **Condition:** `both` | **Indexed:** `True`
- **Heading:** `Symptoms and Clinical Examination`
- **Section Path:** `ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11) > Symptoms and Clinical Examination`
- **Population Tags:** `['cardiovascular_disease', 'chronic_kidney_disease']`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
CLINICAL PRESENTATION & EXAMINATION IN TYPE 2 DIABETES:
- Symptoms: Osmotic symptoms (polyuria, polydipsia, polyphagia), weight loss, non-healing wounds, paraesthesia, recurrent infections, blurring of vision. Note: Many patients may be asymptomatic.
- Examination: BMI, waist circumference, BP, peripheral pulses, skin, oral cavity, foot, and dilated fundus examination.
- Assess Co-morbidities: Hypertension, Dyslipidaemia, CAD, CKD.
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
Standard Treatment Workﬂow (STW)
DIABETES MELLITUS TYPE 2
ICD-10-E11
      KEEP LOW THRESHOLD FOR DIAGNOSIS. MAKE SURE TO FOLLOW UP TO MEET TARGETS
ABBREVIATIONS
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and 
are based on expert opinions and available scientiﬁc
...
```
</details>

---

### Sample 17: `icmr_t2dm_001_c0004` (ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11), pp. 1-1)
- **Chunk Type:** `definition` | **Condition:** `type_2_diabetes` | **Indexed:** `True`
- **Heading:** `Diagnostic Criteria for Diabetes Mellitus`
- **Section Path:** `ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11) > Diagnostic Criteria for Diabetes Mellitus`
- **Population Tags:** `['type_2_diabetes']`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
### DIAGNOSTIC CRITERIA FOR TYPE 2 DIABETES MELLITUS

| Investigation / Parameter | Diagnostic Threshold |
| --- | --- |
| Fasting Plasma Glucose (FPG) | >= 126 mg/dl (after 8hr fasting) |
| 2-hour Plasma Glucose during OGTT | >= 200 mg/dl (using 75g glucose) |
| Glycated Haemoglobin (HbA1c) | >= 6.5% |
| Random Plasma Glucose | >= 200 mg/dl in presence of classic diabetes symptoms |
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
Standard Treatment Workﬂow (STW)
DIABETES MELLITUS TYPE 2
ICD-10-E11
      KEEP LOW THRESHOLD FOR DIAGNOSIS. MAKE SURE TO FOLLOW UP TO MEET TARGETS
ABBREVIATIONS
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and 
are based on expert opinions and available scientiﬁc
...
```
</details>

---

### Sample 18: `icmr_t2dm_001_c0005` (ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11), pp. 1-1)
- **Chunk Type:** `definition` | **Condition:** `type_2_diabetes` | **Indexed:** `True`
- **Heading:** `Prediabetes Diagnostic Criteria`
- **Section Path:** `ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11) > Prediabetes Diagnostic Criteria`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
### PREDIABETES DIAGNOSTIC CRITERIA

| Category | Laboratory Criteria |
| --- | --- |
| Impaired Fasting Glucose (IFG) | Fasting Plasma Glucose 100–125 mg/dL |
| Impaired Glucose Tolerance (IGT) | 2-hour plasma glucose 140–199 mg/dL |
| Prediabetes HbA1c | HbA1c 5.7%–6.4% |

Prediabetes patients should be tested yearly for progression to diabetes.
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
Standard Treatment Workﬂow (STW)
DIABETES MELLITUS TYPE 2
ICD-10-E11
      KEEP LOW THRESHOLD FOR DIAGNOSIS. MAKE SURE TO FOLLOW UP TO MEET TARGETS
ABBREVIATIONS
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and 
are based on expert opinions and available scientiﬁc
...
```
</details>

---

### Sample 19: `icmr_t2dm_001_c0006` (ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11), pp. 1-1)
- **Chunk Type:** `recommendation` | **Condition:** `both` | **Indexed:** `True`
- **Heading:** `Screening for Diabetes Mellitus`
- **Section Path:** `ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11) > Screening for Diabetes Mellitus`
- **Population Tags:** `['cardiovascular_disease', 'pregnancy']`
- **Drug Class Tags:** `['insulin']`
- **Applicability Conditions:** `['In pregnant women: screen 1st trimester with FPG; 75g OGTT at 24-28 weeks if normal', 'In overweight or obese adults (BMI >= 23 kg/m2) with risk factors']`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
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

<details><summary>Click to view Source Page Text excerpt</summary>

```text
Standard Treatment Workﬂow (STW)
DIABETES MELLITUS TYPE 2
ICD-10-E11
      KEEP LOW THRESHOLD FOR DIAGNOSIS. MAKE SURE TO FOLLOW UP TO MEET TARGETS
ABBREVIATIONS
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and 
are based on expert opinions and available scientiﬁc
...
```
</details>

---

### Sample 20: `icmr_t2dm_001_c0007` (ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11), pp. 1-1)
- **Chunk Type:** `table` | **Condition:** `both` | **Indexed:** `True`
- **Heading:** `Metabolic Targets in Type 2 Diabetes`
- **Section Path:** `ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11) > Metabolic Targets in Type 2 Diabetes`
- **Population Tags:** `['cardiovascular_disease', 'chronic_kidney_disease', 'elderly']`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `['In CKD patients: target BP < 130/80 mmHg', 'In CAD patients: target LDL < 70 mg/dl', 'In elderly patients: higher HbA1c target may be acceptable']`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
### METABOLIC TARGETS IN TYPE 2 DIABETES

| Clinical Parameter | Target Goal |
| --- | --- |
| HbA1c | </= 7.0% (except elderly and significant comorbid conditions where higher target may be acceptable) |
| Pre-prandial capillary plasma glucose | 80–130 mg/dl |
| Post-prandial capillary plasma glucose | < 180 mg/dl |
| Blood Pressure | < 140/90 mmHg (< 130/80 mmHg in CKD) |
| LDL Cholesterol | < 100 mg/dl (< 70 mg/dl in CAD) |
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
Standard Treatment Workﬂow (STW)
DIABETES MELLITUS TYPE 2
ICD-10-E11
      KEEP LOW THRESHOLD FOR DIAGNOSIS. MAKE SURE TO FOLLOW UP TO MEET TARGETS
ABBREVIATIONS
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and 
are based on expert opinions and available scientiﬁc
...
```
</details>

---

### Sample 21: `icmr_t2dm_001_c0008` (ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11), pp. 1-1)
- **Chunk Type:** `table` | **Condition:** `type_2_diabetes` | **Indexed:** `True`
- **Heading:** `Stratified Glycemic Pharmacotherapy`
- **Section Path:** `ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11) > Stratified Glycemic Pharmacotherapy`
- **Population Tags:** `[]`
- **Drug Class Tags:** `['dpp4_inhibitor', 'glp1_ra', 'insulin', 'metformin', 'sglt2_inhibitor', 'sulfonylurea']`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
### STRATIFIED PHARMACOTHERAPY BY HBA1C STRATUM

| HbA1c Stratum | Recommended Pharmacotherapy Protocol |
| --- | --- |
| HbA1c < 8.5% | Monotherapy — Metformin |
| HbA1c 8.5%–10.0% | Dual therapy — Metformin + Sulfonylureas (SUs) / Thiazolidinediones (TZD) / DPP-4 inhibitors (DPPIVi) / SGLT2 inhibitors (SGLT2i) / Alpha-glucosidase inhibitors (AGI) / GLP-1 Receptor Agonists (GLP-1RA) |
| HbA1c > 10.0% | Basal Insulin + Metformin + another Oral Antidiabetic Drug (OAD) OR Triple OAD combination |
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
Standard Treatment Workﬂow (STW)
DIABETES MELLITUS TYPE 2
ICD-10-E11
      KEEP LOW THRESHOLD FOR DIAGNOSIS. MAKE SURE TO FOLLOW UP TO MEET TARGETS
ABBREVIATIONS
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and 
are based on expert opinions and available scientiﬁc
...
```
</details>

---

### Sample 22: `icmr_t2dm_001_c0009` (ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11), pp. 1-1)
- **Chunk Type:** `other` | **Condition:** `type_2_diabetes` | **Indexed:** `True`
- **Heading:** `Lifestyle Modification`
- **Section Path:** `ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11) > Lifestyle Modification`
- **Population Tags:** `['type_2_diabetes']`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
LIFESTYLE MANAGEMENT IN TYPE 2 DIABETES:
- Dietary modification: calorie control, complex carbohydrates, reduced refined sugars and saturated fats.
- Avoidance of tobacco and restriction/avoidance of alcohol.
- Regular physical activity: at least 150 minutes per week of moderate-intensity aerobic physical activity.
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
Standard Treatment Workﬂow (STW)
DIABETES MELLITUS TYPE 2
ICD-10-E11
      KEEP LOW THRESHOLD FOR DIAGNOSIS. MAKE SURE TO FOLLOW UP TO MEET TARGETS
ABBREVIATIONS
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and 
are based on expert opinions and available scientiﬁc
...
```
</details>

---

### Sample 23: `icmr_t2dm_001_c0010` (ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11), pp. 1-1)
- **Chunk Type:** `monitoring` | **Condition:** `both` | **Indexed:** `True`
- **Heading:** `Monitoring and Referrals`
- **Section Path:** `ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11) > Monitoring and Referrals`
- **Population Tags:** `['cardiovascular_disease', 'chronic_kidney_disease']`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
MONITORING AND SPECIALIST REFERRALS:
- Blood glucose: FPG and 2 hours PPG once monthly (more frequent as required including SMBG or CGM).
- HbA1c: every 6–12 months (3 monthly if uncontrolled).
- Annual monitoring: ECG, urine ACR (albumin creatinine ratio), dilated fundoscopy, foot examination (pin-prick sensation, monofilament test, vibration, DTR).

Specialist Referrals:
- Endocrinology: for uncontrolled hyperglycemia.
- Ophthalmology: at initial evaluation and every year.
- Nephrology: for deranged renal function.
- Cardiology: for CAD / heart failure / arrhythmia.
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
Standard Treatment Workﬂow (STW)
DIABETES MELLITUS TYPE 2
ICD-10-E11
      KEEP LOW THRESHOLD FOR DIAGNOSIS. MAKE SURE TO FOLLOW UP TO MEET TARGETS
ABBREVIATIONS
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and 
are based on expert opinions and available scientiﬁc
...
```
</details>

---

## 4. Ten Tabular Chunks Audit (Total: 10)

### Sample 1: `mohfw_htn_001_c0121` (MoHFW STG - Hypertension (Background Document), pp. 40-40)
- **Chunk Type:** `table` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `INTRODUCTION > NICE`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > DEVELOPMENT OF GUIDELINE > INTRODUCTION > NICE`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `['If high\nrisk population, request to define\nit and also document the evidence\non which recommendation is\nbased\n\n| SNo .']`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
INTRODUCTION
NICE
What population is recommended
for targeted   screening? If high
risk population, request to define
it and also document the evidence
on which recommendation is
based

| SNo . | Comment | Response |
| --- | --- | --- |
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
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
Su
...
```
</details>

---

### Sample 2: `who_htn_001_c0029` (WHO Guideline for the Pharmacological Treatment of Hypertension in Adults, pp. 17-17)
- **Chunk Type:** `table` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `2.5	 Certainty of evidence and strength of recommendations`
- **Section Path:** `WHO Guideline for the Pharmacological Treatment of Hypertension in Adults > 2.4	 Reviews of evidence > 2.5	 Certainty of evidence and strength of recommendations`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `['When making\nrecommendations, GRADE defines the certainty of a body of evidence as "the extent of our confidence\nthat the estimates of an effect are adequate to support a particular decision or recommendation" (5).', 'When there were systematic reviews\naddressing the relative effects in specific subpopulations, separate evidence profiles were constructed\nfor each subpopulation.']`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
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
| High | Weareveryconfidentthatthetrueeffectliesclosetothatoftheestimate ofeffect . |
| Moderate | Wearemoderatelyconfidentintheeffectestimate (Thetrueeffectislikelyto . beclosetotheestimateofeffect butthereisapossibilitythatitissubstantially , different) . |
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

<details><summary>Click to view Source Page Text excerpt</summary>

```text
2.5	 Certainty of evidence and strength of recommendations 
The GDG rated the certainty of evidence and developed the recommendations using the GRADE 
(Grading of Recommendations Assessment, Development and Evaluation) approach (4). When making 
recommendations, GRADE defines the certainty of a body of evidence as “the extent of our confidence 
that the estimates of an effect are adequate to suppo
...
```
</details>

---

### Sample 3: `icmr_t2dm_001_c0007` (ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11), pp. 1-1)
- **Chunk Type:** `table` | **Condition:** `both` | **Indexed:** `True`
- **Heading:** `Metabolic Targets in Type 2 Diabetes`
- **Section Path:** `ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11) > Metabolic Targets in Type 2 Diabetes`
- **Population Tags:** `['cardiovascular_disease', 'chronic_kidney_disease', 'elderly']`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `['In CKD patients: target BP < 130/80 mmHg', 'In CAD patients: target LDL < 70 mg/dl', 'In elderly patients: higher HbA1c target may be acceptable']`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
### METABOLIC TARGETS IN TYPE 2 DIABETES

| Clinical Parameter | Target Goal |
| --- | --- |
| HbA1c | </= 7.0% (except elderly and significant comorbid conditions where higher target may be acceptable) |
| Pre-prandial capillary plasma glucose | 80–130 mg/dl |
| Post-prandial capillary plasma glucose | < 180 mg/dl |
| Blood Pressure | < 140/90 mmHg (< 130/80 mmHg in CKD) |
| LDL Cholesterol | < 100 mg/dl (< 70 mg/dl in CAD) |
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
Standard Treatment Workﬂow (STW)
DIABETES MELLITUS TYPE 2
ICD-10-E11
      KEEP LOW THRESHOLD FOR DIAGNOSIS. MAKE SURE TO FOLLOW UP TO MEET TARGETS
ABBREVIATIONS
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and 
are based on expert opinions and available scientiﬁc
...
```
</details>

---

### Sample 4: `mohfw_htn_001_c0202` (MoHFW STG - Hypertension (Background Document), pp. 84-86)
- **Chunk Type:** `table` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `4.6.12. If the BP is not controlled despite use of 3 anti-hypertensives in optimal doses, then (Part 2)`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 4.5 Key recommendation: Classes of antihypertensive drugs & preferred choices > 4.6.12. If the BP is not controlled despite use of 3 anti-hypertensives in optimal doses, then (Part 2)`
- **Population Tags:** `['cardiovascular_disease', 'chronic_kidney_disease']`
- **Drug Class Tags:** `['ace_inhibitor', 'arb', 'beta_blocker', 'ccb', 'thiazide']`
- **Applicability Conditions:** `None`
- **Exceptions:** `['of CCB with ARBs/ACE inhibitors or diuretics with ARBs/ACE\ninhibitors are preferred, while combinations of ACE inhibitors with ARBs, and diuretics with\nbeta-blockers are avoidable.']`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
| Calcium channel blockers | Yes | Nil: no effect on lipids glucose , , electrolytes | Nil | Low in public procurement system |
| ACEinhibitors | Yes (may require BD dosing) | No effect on lipid glucose , . Potassium , serum creatinine may rise in some patients | Effectdecreased byNSAIDS | Low in public procurement system |
| Thiazide diuretics | Yes | Small rise in glucose , cholesterol , hypokalemia in higherdoses | Effectdecreased byNSAIDs . | Low in public procurement system |

Table 12 : Comparison of 3 first line anti-hypertensive drugs

Table 13 mentions the 3 initial drugs and their 6 combinations, which can be prescribed. In
general the therapy can be started at half the maximal dose-e.g. 5 mg of amlodipine, 12.5
mg of hydrochlorothiazide, and 5 mg of Enalapril or 50 mg of Losartan. On review after 2-4
weeks if BP control has not been achieved, then a second drug from one of the classes that
has not been used (CCB, diuretic, ACE inhibitor, ARB), and the patient reviewed again for BP
control. The doses of drugs to be used as initial or add-on therapy is mentioned in table 5

Certain combinations e.g. of CCB with ARBs/ACE inhibitors or diuretics with ARBs/ACE
inhibitors are preferred, while combinations of ACE inhibitors with ARBs, and diuretics with
beta-blockers are avoidable. The combination of ACE inhibitors with ARBs has an increased
risk of end-stage renal failure and stroke as documented in trial settings, (69) and is advised
against by all guidelines.(18-21)The combination of thiazide and beta-blockers is also effective
but since both these drugs can elevate blood glucose concentration, the combination should
be used with caution in those with a higher risk of developing diabetes (obese, positive
family history, glucose intolerance).(24, 68)

If the BP is not at goal even after optimal doses of 2 drugs and with regular adherence, then
a 3rd drug may be added. According to most guidelines the preferred 3 drug combination is
of a calcium channel blocker along with ACE inhibitor and a diuretic. (CCB+ACE Inhibitor
+diuretic).
Table 13: Initial drug therapy, preferred drug combinations and combinations to be avoided

| Initialdrug | Preferred combination (as initial or add on therapy) | Combinationsforusein Limitedsettings | Combinations to be avoided |
| --- | --- | --- | --- |
| CCB | CCB+ACEInhibitor* | CCB (dihydropyridines)+ beta-blocker [use in patients with HT and coronary artery disease] | CCB (verapamil/diltiazem) +beta-blocker |
|  | CCB+thiazidediuretic |  |  |
| Diuretic | Thiazide diuretic +ACE Inhibitor* |  | Diuretic + beta- blocker |
|  | ThiazideDiuretic+CCB |  |  |
| ACEinhibitor | ACEInhibitor*+diuretic | ACE Inhibitor + mineralocorticoid antagonist(potential for hyperkalemia) | ACEInhibitor*+ARB |
|  | ACEInhibitor*+CCB |  |  |
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
84 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
with diabetes. If patients have diabetes with proteinuria, or CKD, ACE inhibitors are 
indicated but may require monitoring of serum creatinine and potassium after initiation 
of therapy. 
 
Once 
a 
day 
dosing  
Requirement 
for 
laboratory 
monitoring: 
effect 
on 
glucose, lipids, 
electrolytes  
 Dru
...
85 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
of a calcium channel blocker along with ACE inhibitor and a diuretic. (CCB+ACE Inhibitor 
+diuretic).
...
86 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
Table 13: Initial drug therapy, preferred drug combinations and combinations to be avoided 
 
Initial drug  
Preferred 
combination 
(as initial or add on 
therapy) 
Combinations for use in 
Limited settings 
Combinations to be 
avoided 
CCB  
CCB + ACE Inhibitor*  
CCB 
(dihydropyridines)+ 
beta-blocker
...
```
</details>

---

### Sample 5: `mohfw_htn_001_c0143` (MoHFW STG - Hypertension (Background Document), pp. 55-58)
- **Chunk Type:** `table` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `1.7 All persons who are screened for hypertension should be advised lifestyle measures`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 1.5 At least 2 readings should be taken at each visit with an interval of at least 1 minute > 1.7 All persons who are screened for hypertension should be advised lifestyle measures`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
1.7 All persons who are screened for hypertension should be advised lifestyle measures
including maintaining a daily salt intake appropriate to their occupation, advice on
diet and exercise in case the person is obese,  stopping use of tobacco and
moderating consumption of alcohol to reduce their blood pressure and to reduce
their overall risk of cardiovascular complications.

Implementation:
The health care staff will need to be trained not only in the measurement of BP using a
standardised procedure, but also to interpret the measurements of normal or elevated
BP readings and take appropriate actions. This will be facilitated by the availability of
key messages for the detection, assessment and management of hypertension in a
flyer and quick reference guide.

Suggested response to BP readings:

| InitialBPreadingonscreening |  | AdviceandRecommendationsforFollowup |
| --- | --- | --- |
| SBPmmHg | DBPmmHg |  |
| <<130 | <<85 | Advise lifestyle modifications esp smoking weight . , reductionifpossible:Recheckin2years |
| 130 139 - | 85 89 - | Adviselifestylemodifications:Recheckin1year |
| 140 159 - | 90 99 - | Recheck BP within 1 -2 weeks Advise lifestyle . modifications Refer to nearest health facility within 1 . monthfordiagnosis assessment , . |
| 160 179 - | 100 109 - | Recheck BP within 1 week Advise lifestyle modifications . . Refer to nearest health facility for confirmation of diagnosisandinitiationoftreatment . |
| >180 | >110 | Check for any symptoms/signs of any acute target organ damage (assess symptoms and signs referred to in the mnemonic 'ABCDEFG'mentioned in pathway on assessment and management of hypertensive crisis) In . casesofacutetargetorgandamage treatashypertensive , emergency Refer to PHC/CHC for evaluation and . treatment immediately after confirming elevated readings in this range Initiate therapy before referral if . , seenatPHC . |

  TABLE 3: SUGGESTED RESPONSE TO INITIAL BP READINGS :Adapted from references (29,
47)

Rationale:

There is no evidence from randomised controlled trials regarding the appropriate
rescreening intervals for people screened for hypertension.(47) Recently the US
Preventive Services Task Force published recommendations regarding rescreening
intervals. The weighted mean incidence of hypertension over rescreening intervals
varying between 1 and 5 years was found to range between 2.5% and 13.8%
respectively. In studies persons with even a single risk factor like high normal BP (SBP
130-139 mm and DBP 85-89mm), persons who are obese or overweight , and those with
age >40 years are at greater than 20% risk of developing hypertension within the next 3-
5 years, and therefore such persons should be screened annually for hypertension.
The intervals suggested for confirmation and evaluation at a source of care have been
adapted from the recommendations of the JNC 7.(29)
KEY RECOMMENDATION: DIAGNOSIS AND CLASSIFICATION OF HYPERTENSION
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
55 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
Rescreening, reassessment, and referral of individuals found to have normal or elevated 
BP on screening by allied health staff 
1.6. 
Depending on the BP readings, the person may be advised review up on an 
annual or 2 yearly basis, or referral (immediate or deferred) for diagnosis or 
treatment of hyper
...
56 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
moderating consumption of alcohol to reduce their blood pressure and to reduce 
their overall risk of cardiovascular complications. 
Implementation: 
The health care staff will need to be trained not only in the measurement of BP using a 
standardised procedure, but also to interpret the measurements of n
...
57 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
respectively. In studies persons with even a single risk factor like high normal BP (SBP 
130-139 mm and DBP 85-89mm), persons who are obese or overweight , and those with 
age >40 years are at greater than 20% risk of developing hypertension within the next 3-
5 years, and therefore such persons should b
...
58 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
KEY RECOMMENDATION: DIAGNOSIS AND CLASSIFICATION OF HYPERTENSION 
 
2.1 Diagnosis of hypertension should be made at primary health centres and 
facilities above that level using validated and calibrated BP measurement devices 
and following the standardised BP measurement procedure. 
2.2 Diagnosis of hype
...
```
</details>

---

### Sample 6: `mohfw_htn_002_c0101` (MoHFW Standard Treatment Guidelines - Hypertension (Quick Reference Guide), pp. 27-28)
- **Chunk Type:** `table` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `4.10.7 If BP reduction over few hours is required in view of imminent cardiovascular events,`
- **Section Path:** `MoHFW Standard Treatment Guidelines - Hypertension (Quick Reference Guide) > 4.10 Hypertensive urgencies: > 4.10.7 If BP reduction over few hours is required in view of imminent cardiovascular events,`
- **Population Tags:** `[]`
- **Drug Class Tags:** `['ace_inhibitor', 'beta_blocker', 'thiazide']`
- **Applicability Conditions:** `None`
- **Exceptions:** `['acute left ventricular failure |\nQuick Reference Guide-Hypertension\n\n| IVlabetalol | 20 -80mgIV | 5 -10min | Scalp tingling , dizziness nausea , , heartblock | Can be used in many hypertensive emergencies Avoid in .', 'acuteheartfailure |\n| --- | --- | --- | --- | --- |\n| IVnicardipine | 5 -15 mg per hourasIV | 5 -10min | Tachycardia , headache nausea , , tachycardia | Can be used in many hypertensive emergencies Avoid in .']`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
4.10.7 If BP reduction over few hours is required in view of imminent cardiovascular events,
then oral frusemide, oral clonidine can be used. These can be followed by long term
therapy with CCBs, ACE inhibitors or diuretics.

| Hypertensiveemergencies |  |
| --- | --- |
| Cardiacconditions | Acuteleftventricularfailure |
|  | Acutemyocardialinfarction |
| Renalconditions | Acuteglomerulonephritis |
|  | Renovascularhypertension |
| Cerebrovascularconditions | Hypertensiveencephalopathy |
|  | Cerebralinfarction |
|  | Intracerebralhemorrhage |
|  | Subarachnoidhemorrhage |
|  | Headinjury |
| Acceleratedhypertensionwithexudates and/orpapilledema |  |
| Obstetricconditions | Eclampsia |
| Surgicalconditions | Postoperativehypertension |
|  | Severeburns |
| Excesscatecholamines | Pheochromocytoma |
|  | Abrupt withdrawal of clonidine beta-blockers , |

and/or papilledema
Obstetric conditions
Eclampsia
Surgical conditions
Postoperative hypertension
Severe burns
Excess catecholamines
Pheochromocytoma
Abrupt withdrawal of clonidine, beta-blockers
Table 14: Conditions presenting as hypertensive emergencies

| Drug | Dose | Onset of action | Adverseeffects | Comments |
| --- | --- | --- | --- | --- |
| IVFrusemide | 20 -40 mg in 1 -2min | 5 -15min | Hypovolemia , hypokalemia | May be used in combination with other drugs to maintain their efficacy Indicated in . acute left ventricular failure |
Quick Reference Guide-Hypertension

| IVlabetalol | 20 -80mgIV | 5 -10min | Scalp tingling , dizziness nausea , , heartblock | Can be used in many hypertensive emergencies Avoid in . acuteheartfailure |
| --- | --- | --- | --- | --- |
| IVnicardipine | 5 -15 mg per hourasIV | 5 -10min | Tachycardia , headache nausea , , tachycardia | Can be used in many hypertensive emergencies Avoid in . acuteheartfailure |
| IV nitroglycerine | 5 -100μg/min | 2 -5min | Headache vomiting , , methemoglobinemia , tolerance | Useful in myocardial ischemia with hypertension |

Table 15: Selected intravenous drugs useful in management of hypertensive emergencies
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
Quick Reference Guide-Hypertension
Page 27
sublingual nifedipine. This aggressive reduction of BP in a patient with severe asymptomatic
hypertension may cause fall of BP below the threshold of autoregulation in vascular beds, and
cause serious cerebral and cardiac complications related to ischemia.
4.10.6 Re-institution of therapy or intensification of therapy by increasing the dose of drugs or
ad
...
Quick Reference Guide-Hypertension
Page 28
IV labetalol
20-80 mg IV
5-10 min
Scalp 
tingling,
dizziness, 
nausea,
heart block
Can be used in many
hypertensive
emergencies. Avoid in
acute heart failure
IV nicardipine
5-15  mg per
hour as IV
5-10 min
Tachycardia,
headache, 
nausea,
tachycardia
Can be used in many
hypertensive
emergencies. Avoid in
acute heart failure
IV
nitroglycerine
5-100 µg/min
2
...
```
</details>

---

### Sample 7: `icmr_htn_001_c0012` (ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), pp. 1-1)
- **Chunk Type:** `table` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `Drug Therapy Table: Doses, Contraindications & Side Effects`
- **Section Path:** `ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) > Drug Therapy Table: Doses, Contraindications & Side Effects`
- **Population Tags:** `['pregnancy']`
- **Drug Class Tags:** `['ace_inhibitor', 'arb', 'beta_blocker', 'ccb', 'mra_spironolactone', 'thiazide']`
- **Applicability Conditions:** `None`
- **Exceptions:** `['Pregnancy is a strict contraindication for ACE inhibitors, ARBs, and Diuretics', 'Heart failure is contraindicated for initial CCB', 'Asthma and A-V block are contraindicated for Beta-blockers']`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
### ANTIHYPERTENSIVE DRUG THERAPY: DOSES, CONTRAINDICATIONS & SIDE EFFECTS

| Drug Class | Drug | Doses | Contraindications | Side Effects |
| --- | --- | --- | --- | --- |
| CCB | Amlodipine | 2.5–10 mg OD | Heart failure | Pedal edema, constipation |
| ACE inhibitors | Enalapril | 5–40 mg OD or BD | Pregnancy, Women planning pregnancy, prior angioedema to ACEi, Hyperkalemia, Bilateral renal artery stenosis | Dry cough, angioedema, hyperkalemia, rise in serum creatinine |
| ACE inhibitors | Ramipril | 2.5–10 mg OD or BD | Pregnancy, Women planning pregnancy, prior angioedema to ACEi, Hyperkalemia, Bilateral renal artery stenosis | Dry cough, angioedema, hyperkalemia, rise in serum creatinine |
| ARB | Losartan | 50–100 mg OD | Pregnancy, Women planning pregnancy, Hyperkalemia, Bilateral renal artery stenosis | Hypotension, acute renal failure, hyperkalemia |
| ARB | Olmesartan | 20–40 mg OD | Pregnancy, Women planning pregnancy, Hyperkalemia, Bilateral renal artery stenosis | Hypotension, acute renal failure, hyperkalemia |
| ARB | Telmisartan | 40–80 mg OD | Pregnancy, Women planning pregnancy, Hyperkalemia, Bilateral renal artery stenosis | Hypotension, acute renal failure, hyperkalemia |
| Diuretics | Chlorthalidone | 12.5–25 mg OD | Pregnancy, Gout | Glucose intolerance, metabolic syndrome, hyponatremia, hypercalcemia, hypokalemia |
| Diuretics | Hydrochlorothiazide | 12.5 mg OD | Pregnancy, Gout | Glucose intolerance, metabolic syndrome, hyponatremia, hypercalcemia, hypokalemia |
| Beta-blockers | Carvedilol | 12.5–50 mg OD or BD | Asthma, severe bradycardia, A-V block (grade 2 or 3), uncontrolled heart failure | Depression, fatigue, reduced exercise tolerance, hyperglycemia, sexual dysfunction |
| Beta-blockers | Labetalol | 100–400 mg BD | Asthma, severe bradycardia, A-V block (grade 2 or 3), uncontrolled heart failure | Depression, fatigue, reduced exercise tolerance, hyperglycemia, sexual dysfunction |
| Beta-blockers | Metoprolol | 50–100 mg OD or BD | Asthma, severe bradycardia, A-V block (grade 2 or 3), uncontrolled heart failure | Depression, fatigue, reduced exercise tolerance, hyperglycemia, sexual dysfunction |
| Beta-blockers | Nebivolol | 5 mg OD | Asthma, severe bradycardia, A-V block (grade 2 or 3), uncontrolled heart failure | Depression, fatigue, reduced exercise tolerance, hyperglycemia, sexual dysfunction |
| Aldosterone antagonist | Spironolactone | 25 mg OD | Hyperkalemia | Mastalgia, gynecomastia, sexual dysfunction, gout |
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and 
available scientiﬁc evidence. There may be variations in the management of an individual patient based on his/her speciﬁc condition, as decided by the treating physician. There will
...
```
</details>

---

### Sample 8: `mohfw_htn_001_c0117` (MoHFW STG - Hypertension (Background Document), pp. 33-34)
- **Chunk Type:** `table` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `5 AGREE II Instrument http://www.agreetrust.org/`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > DEVELOPMENT OF GUIDELINE > 5 AGREE II Instrument http://www.agreetrust.org/`
- **Population Tags:** `[]`
- **Drug Class Tags:** `[]`
- **Applicability Conditions:** `None`
- **Exceptions:** `None`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
5 AGREE II Instrument http://www.agreetrust.org/
couldbe adopted fully to suit our requirements. For example, the NICE guideline had
many recommendations applicable to our setting but considered ambulatory blood
pressure monitoring as the gold standard for diagnosis. The assessments recommended
for hypertensives varied between guidelines and different cardiovascular risk estimation
tools were in use which were based on data on cohorts of the local population e.g.
QRISK2 in UK, SCORE in Europe, pooled cohort equation based tool in USA. Therefore for
each issue mentioned in the scope document we searched all the evidence based
guidelines for recommendations and selected them on the basis of the suitability to our
settings in terms of contexts, resources and our priorities.

4. Adaptation and adoption of recommendations:

The clinical sub-group decided in the meeting to adapt recommendations in existing
evidence based guidelines by paraphrasing them & paying close attention to the
integrity of the recommendation, rather than quote verbatim. This decision was taken
for a number of reasons explained here. As mentioned in the preceding paragraph we
selected recommendations from a number of guidelines for the purpose of our STG. The
different guidelines had differing purpose, different target audiences, and differing
presentation and linguistic styles. While NICE guidelines used a user-friendly format in
terms of language, other guidelines made recommendations with mention of strength of
evidence.
Also the population, the healthcare setting and the resources available, the assessment
tools and therapies available are different in the Indian context. For these reasons and in
order to harmonise these different formats and linguistic styles, and have a uniformity
of presentation in our STG, we decided to adapt existing evidence based guidelines. The
quotation of recommendations verbatim would have also involved intellectual property
related issues.
The table below outlines some key recommendations in these guidelines, their source
and some comments related to their adaptation.

Key recommendation
Source guideline(s)
Comment
All adults above the age of 18
years
should
undergo
opportunistic
screening
for
hypertension
by
healthcare
providers at every point of
contact with health services.

| Keyrecommendation | Sourceguideline(s) | Comment |
| --- | --- | --- |
| All adults above the age of 18 years should undergo opportunistic screening for hypertension by healthcare providers at every point of contactwithhealthservices . | US Preventive Services Task Force Screening for . high blood pressure: US Preventive Services Task Force recommendation statement . | Adapted We added the . component of opportunistic screening and screening by both physicians as well as non-physician staff . |
| Screening of hypertension should be done using an automated BP instrument or any other validated device , using a standardised BP measurementprocedure . | NICE European society of , Cardiologyguidelines | Adopted . |
| Depending upon the readings | Joint National Committee | Adapted . |
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
33 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
been developed, reviewed, or revised within the past five years.  The NGC entry criteria 
are similar to the AGREE II Instrument criteria5. 
 
Three of these guidelines were listed on the National Guidelines Clearinghouse , viz:  
Hypertension: Clinical management of primary hypertension in adults NICE gu
...
34 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
couldbe adopted fully to suit our requirements. For example, the NICE guideline had 
many recommendations applicable to our setting but considered ambulatory blood 
pressure monitoring as the gold standard for diagnosis. The assessments recommended 
for hypertensives varied between guidelines and differen
...
```
</details>

---

### Sample 9: `mohfw_htn_001_c0246` (MoHFW STG - Hypertension (Background Document), pp. 98-100)
- **Chunk Type:** `table` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `4.11.7 If BP reduction over few hours is required in view of imminent cardiovascular events,`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 4.11 Hypertensive urgencies: > 4.11.7 If BP reduction over few hours is required in view of imminent cardiovascular events,`
- **Population Tags:** `['cardiovascular_disease']`
- **Drug Class Tags:** `['ace_inhibitor', 'beta_blocker', 'thiazide']`
- **Applicability Conditions:** `None`
- **Exceptions:** `['Avoid\n|  |  |  |  | inacuteheartfailure |\n| --- | --- | --- | --- | --- |\n| IVNicardipine | 5 -15 mg per hourasIV | 5 -10min | Tachycardia , headache nausea , , tachycardia | Can be used in many hypertensive emergencies Avoid .']`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
4.11.7 If BP reduction over few hours is required in view of imminent cardiovascular events,
then oral frusemide, oral clonidine can be used. These can be followed by long term
therapy with CCBs, ACE inhibitors or diuretics.
Background:
Severe elevations of BP can be asymptomatic and can occur in those with undiagnosed,
uncontrolled hypertension or in hypertensive patients who were on therapy but were
non-adherent or have stopped some agents like beta-blockers or clonidine suddenly.
Such asymptomatic severe elevation of BP termed "hypertensive urgencies" demand
reduction of BP over hours and days. Severe hypertension may be associated with lifethreatening events involving cardiac, cerebral or renal systems, in which case the term
"hypertensive emergency" is used and BP is reduced appropriately over minutes to
hours.  Appropriate management of hypertension in these situations can prevent
morbidity and mortality, while inappropriate management which includes sudden
excessive reduction of BP may result in serious complications.
Implementation:
Physicians will need to be trained in the clinical and laboratory assessment of severe
hypertension and to distinguish between hypertensive urgency and an emergency
Patients with hypertensive emergencies have symptoms, signs, and laboratory
abnormalities suggestive of cardiac, cerebral, renal complications, listed in the table
below, and will need care at a secondary/tertiary care facility. However treatment
should not be delayed and the patient should be referred after an initial reduction of BP.
        The healthcare facility will need to keep stock of certain essential medicines for the
management of hypertensive urgencies and emergencies. These are indicated in the
table below. A minimum list would contain IV frusemide, IV labetalol, and IV
nitroglycerine.
 Rationale:There is no good quality evidence from randomised controlled trials to guide the
management of patients with acute severe hypertension with/without complications,
and current recommendations The  and are based on the Seventh Report.(29)
Hypertensive emergencies
Cardiac conditions
Acute left ventricular failure
Acute myocardial infarction
Renal conditions
Acute glomerulonephritis
Renovascular hypertension
Cerebrovascular conditions
Hypertensive encephalopathy
Cerebral infarction
Intracerebral hemorrhage
Subarachnoid hemorrhage
Head injury
Accelerated hypertension with exudates
and/or papilledema

Obstetric conditions
Eclampsia
Surgical conditions
Postoperative hypertension
Severe burns
Excess catecholamine
Pheochromocytoma
Abrupt withdrawal of clonidine, betablockers

Table16: Conditions presenting as hypertensive emergencies
Drug
Dose
Onset
of
action
Adverse effects
Comments
IV Frusemide
20-40 mg in
1-2 min
5-15 min
Hypovolemia,
hypokalemia
May
be
used
in
combination
with
other
drugs
to
maintain
their
efficacy. Indicated in
acute left ventricular
failure
IV labetalol
20-80 mg IV
5-10 min
Scalp
tingling,
dizziness,
nausea,
heart block
Can be used in many
hypertensive
emergencies. Avoid
|  |  |  |  | inacuteheartfailure |
| --- | --- | --- | --- | --- |
| IVNicardipine | 5 -15 mg per hourasIV | 5 -10min | Tachycardia , headache nausea , , tachycardia | Can be used in many hypertensive emergencies Avoid . inacuteheartfailure |
| IV Nitroglycerine | 5 100 - μg/min | 2 -5min | Headache vomiting , , methemoglobinemia , tolerance | Useful in myocardial ischemia with hypertension |
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
98 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
4.11.2. Hypertensive urgencies may occur in patients with chronic hypertension in a number 
of situations. This includes non-adherence to therapy, after sudden withdrawal of beta-
blocker or clonidine therapy, after ingestion of large quantity of salt, or due to anxiety. 
4.11.3  There is no benefit from
...
99 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
        Patients with hypertensive emergencies have symptoms, signs, and laboratory 
abnormalities suggestive of cardiac, cerebral, renal complications, listed in the table 
below, and will need care at a secondary/tertiary care facility. However treatment 
should not be delayed and the patient should be
...
100 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
in acute heart failure
IV Nicardipine
5-15  mg per 
hour as IV 
5-10 min
Tachycardia, 
headache, 
nausea, 
tachycardia 
Can be used in many 
hypertensive 
emergencies. Avoid 
in acute heart failure 
IV 
Nitroglycerine 
5-100 
µg/min 
2-5 min
Headache, vomiting, 
methemoglobinemia, 
tolerance 
Useful in m
...
```
</details>

---

### Sample 10: `mohfw_htn_001_c0189` (MoHFW STG - Hypertension (Background Document), pp. 78-79)
- **Chunk Type:** `table` | **Condition:** `hypertension` | **Indexed:** `True`
- **Heading:** `4.5.7`
- **Section Path:** `MoHFW STG - Hypertension (Background Document) > 4.5 Key recommendation: Classes of antihypertensive drugs & preferred choices > 4.5.7`
- **Population Tags:** `['cardiovascular_disease', 'elderly']`
- **Drug Class Tags:** `['ace_inhibitor', 'arb', 'beta_blocker', 'ccb', 'mra_spironolactone', 'thiazide']`
- **Applicability Conditions:** `None`
- **Exceptions:** `['Implementation:\n\nIn a general patient where hypertension is the only or main condition, any of the 4 classes of\ndrugs can be used as initial therapy, except in the case of elderly patients  with isolated\nsystolic hypertension, where a calcium channel blocker or diuretic would be preferred.']`
- **Recommendation Year:** `None` | **Last Updated:** `None`

```markdown
--- CHUNK TEXT ---
4.5.7
Angiotensin receptor blockers have a mode of action, efficacy and indications
similar to ACE inhibitors, but are currently more expensive than them.  They
should therefore be used in the place of ACE inhibitors, in case there are side
effects with ACE inhibitors like cough, angioedema.
Background:
Current guidelines suggest that all the 4 drug classes of antihypertensive drugs-thiazide
diuretics, calcium channel blockers, ACE inhibitors, Angiotensin receptors blockers for
initiation as well as add-on agents to control BP.(20) Beta-blockers are not considered first
line drugs in most guidelines, but  may be used in patients with hypertension and associated
coronary artery disease or heart failure. Many patients will require combination of drugs for
control of hypertension.

Implementation:

In a general patient where hypertension is the only or main condition, any of the 4 classes of
drugs can be used as initial therapy, except in the case of elderly patients  with isolated
systolic hypertension, where a calcium channel blocker or diuretic would be preferred.  In
case hypertension is associated with other clinical conditions detected during assessment of
a patient with hypertension- diabetes, hypertension associated with previous myocardial
infarction or stroke, heart failure, angina, and then some drugs would be preferred as
mentioned in table 9. Consideration should also be given to the compelling and possible
contraindications to the use of each class of these drugs before initiation of therapy,
mentioned in table 10.
Clinical condition
Drug to be preferred as
first drugs

| Clinicalcondition | Drugtobepreferredas firstdrugs | Seconddrugif neededtoachieve BPcontrol | Thirddrugifneededto achieveBPcontrol |
| --- | --- | --- | --- |
| Isolatedsystolic hypertension(elderly) | CCB/ThiazideDiuretic CCB | ACEInhibitor* | Thiazidediuretic+ACE Inhibitor*+CCB |
| Hypertensionand diabetes | ACEinhibitor* | CCBorthiazide diuretic | ACEinhibitor*+CCB+ thiazidediuretic |
| Hypertensionandchronic kidneydisease(definedas albuminuriaoraneGFR< 60ml/min/173m2for>3 . months) | ACEinhibitor*where closeclinicaland biochemical monitoringispossible . OtherwiseCCB maybe preferable | CCBorthiazide diuretic(loop diureticifeGFRis below30ml/min) | ACEinhibitor* +CCB+thiazidediuretic |
| Hypertensionand previousmyocardial infarction | BB ACEInhibitor* , | CCBordiuretic |  |
| Hypertensionassociated withheartfailure | Thiazide/loopdiuretic , ACE Inhibitor* | BB | Spironolactone |
| Hypertensionassociated withpreviousstroke | ACEinhibitor* | DiureticorCCB | ACEInhibitor*+CCB+ diuretic |

Table 10:  Clinical conditions which may be associated in a patient with hypertension and
the drugs to be preferred

*Angiotensin receptor blockers (ARBs) may be used for this indication if there is intolerance to ACE inhibitors
(cough, angioedema)Abbreviations: ACE inhibitor: angiotensin converting enzyme inhibitor; CCB, calcium
channel blocker; BB, beta-blocker.Notes: Examples of representative drugs: ACE inhibitors - Enalapril, Calcium
channel blockers-Amlodipine, Thiazide diuretic- Hydrochlorothiazide, Beta-blocker- Atenolol

§ Source: adapted from ref.(21)

Angiotensin converting enzyme inhibitors (ACE inhibitors) and Angiotensin receptor blockers
(ARBs) both act by targeting the renin-angiotensin system. Both are generally well tolerated,
have similar indications and contraindications for their use, although ACE inhibitors have a
more robust evidence base with regard to reduction of cardiovascular mortality.(62) ARBs are
```

<details><summary>Click to view Source Page Text excerpt</summary>

```text
78 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
pressure, and on outcomes, although beta-blockers have been associated 
with lesser protection against strokes. All combinations of drugs are not 
however similarly efficacious, and some are preferred. 
 4.5.3.     The different classes of drugs have differing side effect profiles and 
requirements for mo
...
79 
Screening, Diagnosis, Assessment, and Management of Primary Hypertension- Full Document  
line drugs in most guidelines, but  may be used in patients with hypertension and associated 
coronary artery disease or heart failure. Many patients will require combination of drugs for 
control of hypertension. 
Implementation:  
In a general patient where hypertension is the only or main condition, an
...
```
</details>

---
