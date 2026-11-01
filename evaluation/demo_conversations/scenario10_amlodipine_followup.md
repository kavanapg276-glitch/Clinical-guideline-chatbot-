# Scenario 10: Multi-Turn Antihypertensive Follow-Up & Treatment Escalation
**Category**: Follow-Up & Escalation  
**Description**: Patient was started on amlodipine last week; clinic BP today is 145/92 mmHg; clinician asks for next step.  
**Session ID**: `scenario10_amlodipine_followup`  

---

### Turn 1
**Clinician/User**: Patient was started on amlodipine 5 mg last week for Stage 1 hypertension; clinic BP today is 145/92 mmHg.

**Chatbot Action**: `recommendation` | **Abstention**: `False`
**Patient State Summary**: *BP: 145/92 mmHg; Conditions: hypertension; Medications: amlodipine*
**Patient State Delta**: `{"conditions": {"previous": null, "current": ["hypertension"]}, "medications": {"previous": null, "current": ["amlodipine"]}, "vitals": {"previous": null, "current": {"sbp": 145.0, "dbp": 92.0}}}`

**Retrieved Guideline Evidence (Top-5)**:
- `mohfw_htn_001_c0203` (Score: 0.0161): MoHFW STG - Hypertension (Background Document) (p. 87, §4.6.12. If the BP is not controlled despite use of 3 anti-hypertensives in optimal doses, then (Part 4))
- `mohfw_htn_001_c0190` (Score: 0.0149): MoHFW STG - Hypertension (Background Document) (p. 82, §4.6.1 In patients with Grade 1 or Grade 2 hypertension, therapy can be initiated with one)
- `icmr_htn_001_c0011` (Score: 0.0147): ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) (p. 1, §Treatment Protocols (ATTACC & AATTCC))
- `mohfw_htn_001_c0050` (Score: 0.0145): MoHFW STG - Hypertension (Background Document) (p. 20, §4.6 The treatment regimen and the use of combinations: > 4.6.1 In patients with Grade 1 or Grade 2 hypertension, therapy can be initiated with)
- `who_htn_001_c0076` (Score: 0.014): WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (p. 41, §IMPLEMENTATION TOOLS > 6.2	 Drug- and dose-specific protocols (Part 2))

**Response (Sentence-by-Sentence Grounding)**:
### Guideline Recommendation(s)

1. **4.6.12. If the BP is not controlled despite use of 3 anti-hypertensives in optimal doses, then (Part 4)** [MoHFW STG - Hypertension (Background Document), p. 87, §4.6.12. If the BP is not controlled despite use of 3 anti-hypertensives in optimal doses, then (Part 4), 2016]:
   *Reduce dose of amlodipine to 2.5 mg once a day when it is started in low body weight elderly patients, and when amlodipine is added to another antihypertensive medication. § Reduce dose to enalapril 2.5 mg when it is used in elderly (>65 years) and when the patient has been on diuretic therapy. [^1]

2. **4.6.1 In patients with Grade 1 or Grade 2 hypertension, therapy can be initiated with one** [MoHFW STG - Hypertension (Background Document), p. 82, §4.6.1 In patients with Grade 1 or Grade 2 hypertension, therapy can be initiated with one, 2016]:
   4.6.1 In patients with Grade 1 or Grade 2 hypertension, therapy can be initiated with one drug (CCBs, ACE inhibitors, thiazide diuretics) in combination with lifestyle modifications.(Step 1 in table 13) Average initial doses can be 5 mg of amlodipine, 5 mg of enalapril and 12.5 mg of hydrochlorot... [^2]

3. **Treatment Protocols (ATTACC & AATTCC)** [ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), p. 1, §Treatment Protocols (ATTACC & AATTCC), 2026]:
   SUGGESTED TREATMENT PROTOCOLS FOR BLOOD PRESSURE CONTROL: *High BP >= 140/90 mmHg. At every visit: Check if the patient has been taking medications regularly and correctly. PROTOCOL NO 1 (ATTACC): - Step 1: If BP is high, prescribe Amlodipine 5mg. After 4 weeks measure BP again. - Step 2: If stil... [^3]

4. **4.6 The treatment regimen and the use of combinations: > 4.6.1 In patients with Grade 1 or Grade 2 hypertension, therapy can be initiated with** [MoHFW STG - Hypertension (Background Document), p. 20, §4.6 The treatment regimen and the use of combinations: > 4.6.1 In patients with Grade 1 or Grade 2 hypertension, therapy can be initiated with, 2016]:
   4.6 The treatment regimen and the use of combinations: 4.6.1 In patients with Grade 1 or Grade 2 hypertension, therapy can be initiated with one drug (CCBs, ACE inhibitors, thiazide diuretics)   in combination with lifestyle modifications. Average initial doses can be 5 mg of amlodipine, 5 mg of ... [^4]


### Patient Applicability & Context Analysis

- **Recorded Clinic BP (145/92 mmHg)**: Evaluated against threshold criteria in retrieved guideline recommendations [^1].
- **Current Pharmacotherapy (amlodipine)**: Evaluated against step-up or combination protocols in retrieved guidance [^1].

### Missing Patient Information & Recommended Workup

- **Renal Function (eGFR / Serum Creatinine)**: Referenced in retrieved dosing criteria and contraindication exceptions.
- **Serum Potassium and Electrolytes**: Required prior to RAAS blocker or diuretic initiation per retrieved drug guidance.
- **Urine Albumin-to-Creatinine Ratio (ACR)**: Required to screen for renal target-organ damage and microalbuminuria.

### General Clinical Rationale

*General Clinical Rationale — Not a Formal Guideline Recommendation*:
Stepwise blood pressure and glycemic management provides synergistic protection against microvascular and macrovascular events. Treatment decisions should be individualized based on tolerability and target organ evaluation. [^1]

*Research Prototype Disclaimer: For evaluation and research purposes only. This software is not an approved medical device and does not replace certified clinical judgment.*

**Citation Verification**: Citations Verified: 4/4 (100.0% valid). Unverified: 0

---

### Turn 2
**Clinician/User**: Since blood pressure remains above target at 145/92 mmHg on monotherapy, what is the recommended next step?

**Chatbot Action**: `recommendation` | **Abstention**: `False`
**Patient State Summary**: *BP: 145/92 mmHg; Conditions: hypertension; Medications: amlodipine*

**Retrieved Guideline Evidence (Top-5)**:
- `mohfw_htn_001_c0204` (Score: 0.0157): MoHFW STG - Hypertension (Background Document) (p. 87, §Use dose of 25 mg in patients less than 50 kg (Canadian labelling))
- `nice_htn_001_c0069` (Score: 0.0153): NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (p. 22, §Step 3 treatment > 1.4.44)
- `who_htn_001_c0019` (Score: 0.0152): WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (p. 10, §6.	 RECOMMENDATIONS ON TARGET BLOOD PRESSURE)
- `who_htn_001_c0052` (Score: 0.0152): WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (p. 27, §RECOMMENDATIONS > 3.6	 Target blood pressure > 6.	 RECOMMENDATION ON TARGET BLOOD PRESSURES)
- `icmr_htn_001_c0011` (Score: 0.015): ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) (p. 1, §Treatment Protocols (ATTACC & AATTCC))

**Response (Sentence-by-Sentence Grounding)**:
### Guideline Recommendation(s)

1. **Use dose of 25 mg in patients less than 50 kg (Canadian labelling)** [MoHFW STG - Hypertension (Background Document), p. 87, §Use dose of 25 mg in patients less than 50 kg (Canadian labelling), 2016]:
   # Use dose of 25 mg in patients less than 50 kg (Canadian labelling) Rationale: Use of initial monotherapy: Most of the evidence based guidelines like CHEP, ESC/ESH recommend therapy with a single drug in the case of grade 1 hypertension(19, 21), and with a combination of 2 drugs in patients with... [^1]

2. **Step 3 treatment > 1.4.44** [NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management, p. 22, §Step 3 treatment > 1.4.44, 2019/2022]:
   Step 3 treatment 1.4.44 Before considering next step treatment for hypertension: -  review the person's medications to ensure they are being taken at the optimal tolerated doses and -  discuss adherence (see recommendation 1.4.40). [2019] [^2]

3. **6.	 RECOMMENDATIONS ON TARGET BLOOD PRESSURE** [WHO Guideline for the Pharmacological Treatment of Hypertension in Adults, p. 10, §6.	 RECOMMENDATIONS ON TARGET BLOOD PRESSURE, 2021]:
   6.	 RECOMMENDATIONS ON TARGET BLOOD PRESSURE WHO recommends a target blood pressure treatment goal of <140/90 mmHg in all patients with hypertension without comorbidities. Strong recommendation, moderate-certainty evidence viii WHO recommends a target systolic blood pressure treatment goal of <13... [^3]

4. **RECOMMENDATIONS > 3.6	 Target blood pressure > 6.	 RECOMMENDATION ON TARGET BLOOD PRESSURES** [WHO Guideline for the Pharmacological Treatment of Hypertension in Adults, p. 27, §RECOMMENDATIONS > 3.6	 Target blood pressure > 6.	 RECOMMENDATION ON TARGET BLOOD PRESSURES, 2021]:
   RECOMMENDATIONS 3.6	 Target blood pressure 6.	 RECOMMENDATION ON TARGET BLOOD PRESSURES WHO recommends a target blood pressure treatment goal of <140/90 mmHg in all patients with hypertension without comorbidities. Strong recommendation, moderate-certainty evidence WHO recommends a target systoli... [^4]


### Patient Applicability & Context Analysis

- **Recorded Clinic BP (145/92 mmHg)**: Evaluated against threshold criteria in retrieved guideline recommendations [^1].
- **Current Pharmacotherapy (amlodipine)**: Evaluated against step-up or combination protocols in retrieved guidance [^1].

### Missing Patient Information & Recommended Workup

- **Renal Function (eGFR / Serum Creatinine)**: Referenced in retrieved dosing criteria and contraindication exceptions.
- **Glycemic Status (HbA1c / Fasting Glucose)**: Referenced in retrieved criteria to assess diabetic comorbidity and glycemic control.

### General Clinical Rationale

*General Clinical Rationale — Not a Formal Guideline Recommendation*:
Stepwise blood pressure and glycemic management provides synergistic protection against microvascular and macrovascular events. Treatment decisions should be individualized based on tolerability and target organ evaluation. [^1]

*Research Prototype Disclaimer: For evaluation and research purposes only. This software is not an approved medical device and does not replace certified clinical judgment.*

**Citation Verification**: Citations Verified: 4/4 (100.0% valid). Unverified: 0

---

### Turn 3
**Clinician/User**: If we add a second agent, which drug class should be combined with amlodipine according to ICMR and WHO protocols?

**Chatbot Action**: `recommendation` | **Abstention**: `False`
**Patient State Summary**: *BP: 145/92 mmHg; Conditions: hypertension; Medications: amlodipine*

**Retrieved Guideline Evidence (Top-5)**:
- `icmr_htn_001_c0010` (Score: 0.0203): ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) (p. 1, §Pharmacological Strategy)
- `icmr_htn_001_c0011` (Score: 0.0202): ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) (p. 1, §Treatment Protocols (ATTACC & AATTCC))
- `icmr_htn_001_c0012` (Score: 0.0178): ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) (p. 1, §Drug Therapy Table: Doses, Contraindications & Side Effects)
- `mohfw_htn_002_c0052` (Score: 0.0144): MoHFW Standard Treatment Guidelines - Hypertension (Quick Reference Guide) (p. 17, §4.6.5. If the second drug in a usual dose also fails to reduce BP to target levels then the third class of)
- `mohfw_htn_001_c0194` (Score: 0.0142): MoHFW STG - Hypertension (Background Document) (p. 82, §4.6.5. If the second drug in a usual dose also fails to reduce BP to target levels then the)

**Response (Sentence-by-Sentence Grounding)**:
### Guideline Recommendation(s)

1. **Pharmacological Strategy** [ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), p. 1, §Pharmacological Strategy, 2026]:
   PHARMACOLOGICAL STRATEGY FOR HYPERTENSION: - Combination therapy (two drugs from two different classes) could be the default initial pharmacological treatment for most adults with hypertension. - Single-pill combinations (SPCs/fixed-dose combinations, FDCs) are preferred over multiple pills to im... [^1]

2. **Treatment Protocols (ATTACC & AATTCC)** [ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), p. 1, §Treatment Protocols (ATTACC & AATTCC), 2026]:
   SUGGESTED TREATMENT PROTOCOLS FOR BLOOD PRESSURE CONTROL: *High BP >= 140/90 mmHg. At every visit: Check if the patient has been taking medications regularly and correctly. PROTOCOL NO 1 (ATTACC): - Step 1: If BP is high, prescribe Amlodipine 5mg. After 4 weeks measure BP again. - Step 2: If stil... [^2]

3. **Drug Therapy Table: Doses, Contraindications & Side Effects** [ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), p. 1, §Drug Therapy Table: Doses, Contraindications & Side Effects, 2026]:
   ### ANTIHYPERTENSIVE DRUG THERAPY: DOSES, CONTRAINDICATIONS & SIDE EFFECTS [^3]

4. **4.6.5. If the second drug in a usual dose also fails to reduce BP to target levels then the third class of** [MoHFW Standard Treatment Guidelines - Hypertension (Quick Reference Guide), p. 17, §4.6.5. If the second drug in a usual dose also fails to reduce BP to target levels then the third class of, 2016]:
   4.6.5. If the second drug in a usual dose also fails to reduce BP to target levels then the third class of drug previously unutilised should be added (Step3 in table 13). An optimal 3 drug combination in case it is required is a calcium channel blocker with a low dose thiazide diuretic and an ACE... [^4]


### Patient Applicability & Context Analysis

- **Recorded Clinic BP (145/92 mmHg)**: Evaluated against threshold criteria in retrieved guideline recommendations [^1].
- **Current Pharmacotherapy (amlodipine)**: Evaluated against step-up or combination protocols in retrieved guidance [^1].

### Missing Patient Information & Recommended Workup

- **Renal Function (eGFR / Serum Creatinine)**: Referenced in retrieved dosing criteria and contraindication exceptions.
- **Serum Potassium and Electrolytes**: Required prior to RAAS blocker or diuretic initiation per retrieved drug guidance.
- **Glycemic Status (HbA1c / Fasting Glucose)**: Referenced in retrieved criteria to assess diabetic comorbidity and glycemic control.

### General Clinical Rationale

*General Clinical Rationale — Not a Formal Guideline Recommendation*:
Stepwise blood pressure and glycemic management provides synergistic protection against microvascular and macrovascular events. Treatment decisions should be individualized based on tolerability and target organ evaluation. [^1]

*Research Prototype Disclaimer: For evaluation and research purposes only. This software is not an approved medical device and does not replace certified clinical judgment.*

**Citation Verification**: Citations Verified: 4/4 (100.0% valid). Unverified: 0

---