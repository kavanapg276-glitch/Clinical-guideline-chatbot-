# Scenario 7: Elderly Patient with Isolated Systolic Hypertension
**Category**: Normal Guideline Questions  
**Description**: 84-year-old patient with clinic BP 162/78 mmHg; clinician asks about blood pressure targets and relaxed thresholds.  
**Session ID**: `scenario7_elderly_systolic_htn`  

---

### Turn 1
**Clinician/User**: I am evaluating an 84-year-old patient with clinic blood pressure 162/78 mmHg and no prior cardiovascular events.

**Chatbot Action**: `recommendation` | **Abstention**: `False`
**Patient State Summary**: *Age: 84; BP: 162/78 mmHg; Conditions: hypertension*
**Patient State Delta**: `{"conditions": {"previous": null, "current": ["hypertension"]}, "age": {"previous": null, "current": 84}, "vitals": {"previous": null, "current": {"sbp": 162.0, "dbp": 78.0}}}`

**Retrieved Guideline Evidence (Top-5)**:
- `nice_htn_001_c0047` (Score: 0.0165): NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (p. 16, §1.4.21)
- `mohfw_htn_001_c0117` (Score: 0.0152): MoHFW STG - Hypertension (Background Document) (p. 35, §5 AGREE II Instrument http://www.agreetrust.org/ (Part 2))
- `nice_htn_001_c0013` (Score: 0.015): NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (p. 7, §1.2.3)
- `nice_htn_001_c0098` (Score: 0.015): NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (p. 37, §Return to recommendations)
- `nice_htn_001_c0012` (Score: 0.0144): NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (p. 7, §1.2.2)

**Response (Sentence-by-Sentence Grounding)**:
### Guideline Recommendation(s)

1. **1.4.21** [NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management, p. 16, §1.4.21, 2019/2022]:
   1.4.21 For adults with hypertension aged 80 and over, reduce clinic blood pressure to below 150/90 mmHg and ensure that it is maintained below that level. Use clinical judgement for people with frailty or multimorbidity (see NICE's guideline on multimorbidity). See also table 2 for guidance on cl... [^1]

2. **5 AGREE II Instrument http://www.agreetrust.org/ (Part 2)** [MoHFW STG - Hypertension (Background Document), p. 35, §5 AGREE II Instrument http://www.agreetrust.org/ (Part 2), 2016]:
    [^2]

3. **1.2.3** [NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management, p. 7, §1.2.3, 2019/2022]:
   1.2.3 If clinic blood pressure is between 140/90 mmHg and 180/120 mmHg, offer ambulatory blood pressure monitoring (ABPM) to confirm the diagnosis of hypertension. See the section on identifying who to refer for people with a clinic blood pressure 180/120 mmHg or higher. [2019] [^3]

4. **Return to recommendations** [NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management, p. 37, §Return to recommendations, 2019/2022]:
   Return to recommendations Blood pressure targets for people without cardiovascular disease Recommendations 1.4.15 to 1.4.22 Why the committee made the recommendations No evidence was identified to determine whether cardiovascular risk or blood pressure targets should be used. The committee agreed... [^4]


### Patient Applicability & Context Analysis

- **Recorded Clinic BP (162/78 mmHg)**: Evaluated against threshold criteria in retrieved guideline recommendations [^1].
- **Patient Age (84 years)**: Evaluated against age-stratified criteria in retrieved recommendations [^1].

### Missing Patient Information & Recommended Workup

- **Out-of-office BP Confirmation (ABPM/HBPM)**: Referenced in retrieved applicability criteria to confirm sustained hypertension.
- **Renal Function (eGFR / Serum Creatinine)**: Referenced in retrieved dosing criteria and contraindication exceptions.
- **Glycemic Status (HbA1c / Fasting Glucose)**: Referenced in retrieved criteria to assess diabetic comorbidity and glycemic control.

### Cross-Guideline Consensus & Divergence

- **Blood Pressure Target**: Cross-guideline variation detected in blood pressure targets.

### General Clinical Rationale

*General Clinical Rationale — Not a Formal Guideline Recommendation*:
Stepwise blood pressure and glycemic management provides synergistic protection against microvascular and macrovascular events. Treatment decisions should be individualized based on tolerability and target organ evaluation. [^1]

*Research Prototype Disclaimer: For evaluation and research purposes only. This software is not an approved medical device and does not replace certified clinical judgment.*

**Citation Verification**: Citations Verified: 4/4 (100.0% valid). Unverified: 0

---

### Turn 2
**Clinician/User**: What clinic blood pressure target applies to adults aged 80 and over according to NICE NG136 and ICMR STW?

**Chatbot Action**: `recommendation` | **Abstention**: `False`
**Patient State Summary**: *Age: 84; BP: 162/78 mmHg; Conditions: hypertension*

**Retrieved Guideline Evidence (Top-5)**:
- `icmr_htn_001_c0006` (Score: 0.0281): ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) (p. 1, §Blood Pressure Control Targets)
- `icmr_htn_001_c0003` (Score: 0.0201): ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00) (p. 1, §Population Screening and Risk Factors for Hypertension)
- `nice_htn_001_c0084` (Score: 0.0172): NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (p. 28, §3 Blood pressure targets for people aged over 80)
- `nice_htn_001_c0047` (Score: 0.0171): NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (p. 16, §1.4.21)
- `nice_htn_001_c0039` (Score: 0.0159): NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (p. 13, §1.4.13)

**Response (Sentence-by-Sentence Grounding)**:
### Guideline Recommendation(s)

1. **Blood Pressure Control Targets** [ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), p. 1, §Blood Pressure Control Targets, 2026]:
   BLOOD PRESSURE CONTROL TARGETS: - All adults: SBP < 140 and DBP < 90 mmHg. - Diabetes mellitus, CKD, or established CVD: SBP < 130 and DBP < 80 mmHg (optimal target if tolerated). - Age >= 80 years: SBP < 150 and DBP < 90 mmHg. - Assess orthostatic BP at every visit of adults >= 65 years. [^1]

2. **Population Screening and Risk Factors for Hypertension** [ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00), p. 1, §Population Screening and Risk Factors for Hypertension, 2026]:
   POPULATION SCREENING: - ALL ADULTS >= 18 YEARS SHOULD GET BLOOD PRESSURE MEASURED AT EVERY CLINIC VISIT. - Population screening BP reading may count as the first reading for diagnosis. RISK FACTORS FOR HYPERTENSION: - High salt intake - Sedentary behavior - Tobacco and alcohol consumption - Obesity [^2]

3. **3 Blood pressure targets for people aged over 80** [NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management, p. 28, §3 Blood pressure targets for people aged over 80, 2019/2022]:
   3 Blood pressure targets for people aged over 80 What is the optimum blood pressure target for people aged over 80 with treated primary hypertension (with or without cardiovascular disease)? [2022] For a short explanation of why the committee made the recommendation for research, see the rational... [^3]

4. **1.4.21** [NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management, p. 16, §1.4.21, 2019/2022]:
   1.4.21 For adults with hypertension aged 80 and over, reduce clinic blood pressure to below 150/90 mmHg and ensure that it is maintained below that level. Use clinical judgement for people with frailty or multimorbidity (see NICE's guideline on multimorbidity). See also table 2 for guidance on cl... [^4]


### Patient Applicability & Context Analysis

- **Recorded Clinic BP (162/78 mmHg)**: Evaluated against threshold criteria in retrieved guideline recommendations [^1].
- **Patient Age (84 years)**: Evaluated against age-stratified criteria in retrieved recommendations [^1].

### Missing Patient Information & Recommended Workup

- **Renal Function (eGFR / Serum Creatinine)**: Referenced in retrieved dosing criteria and contraindication exceptions.
- **Glycemic Status (HbA1c / Fasting Glucose)**: Referenced in retrieved criteria to assess diabetic comorbidity and glycemic control.

### Cross-Guideline Consensus & Divergence

- **Blood Pressure Target**: Cross-guideline variation detected in blood pressure targets.

### General Clinical Rationale

*General Clinical Rationale — Not a Formal Guideline Recommendation*:
Stepwise blood pressure and glycemic management provides synergistic protection against microvascular and macrovascular events. Treatment decisions should be individualized based on tolerability and target organ evaluation. [^1]

*Research Prototype Disclaimer: For evaluation and research purposes only. This software is not an approved medical device and does not replace certified clinical judgment.*

**Citation Verification**: Citations Verified: 4/4 (100.0% valid). Unverified: 0

---

### Turn 3
**Clinician/User**: What first-line drug class is recommended for isolated systolic hypertension in elderly patients?

**Chatbot Action**: `recommendation` | **Abstention**: `False`
**Patient State Summary**: *Age: 84; BP: 162/78 mmHg; Conditions: hypertension*

**Retrieved Guideline Evidence (Top-5)**:
- `mohfw_htn_001_c0188` (Score: 0.0183): MoHFW STG - Hypertension (Background Document) (p. 78, §4.5.7)
- `who_htn_001_c0017` (Score: 0.0163): WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (p. 10, §4.	 RECOMMENDATION ON DRUG CLASSES TO BE USED AS FIRST-LINE AGENTS)
- `mohfw_htn_002_c0061` (Score: 0.0162): MoHFW Standard Treatment Guidelines - Hypertension (Quick Reference Guide) (p. 19, §GRADE 3 HYPERTENSION (SBP > =180, DBP > =110))
- `who_htn_001_c0044` (Score: 0.016): WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (p. 23, §4.	 RECOMMENDATION ON DRUG CLASSES TO BE USED AS FIRST-LINE AGENTS)
- `nice_htn_001_c0053` (Score: 0.0154): NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management (p. 18, §1.4.27 > 1.4.28)

**Response (Sentence-by-Sentence Grounding)**:
### Guideline Recommendation(s)

1. **4.5.7** [MoHFW STG - Hypertension (Background Document), p. 78, §4.5.7, 2016]:
   4.5.7 Angiotensin receptor blockers have a mode of action, efficacy and indications similar to ACE inhibitors, but are currently more expensive than them.  They should therefore be used in the place of ACE inhibitors, in case there are side effects with ACE inhibitors like cough, angioedema. Back... [^1]

2. **4.	 RECOMMENDATION ON DRUG CLASSES TO BE USED AS FIRST-LINE AGENTS** [WHO Guideline for the Pharmacological Treatment of Hypertension in Adults, p. 10, §4.	 RECOMMENDATION ON DRUG CLASSES TO BE USED AS FIRST-LINE AGENTS, 2021]:
   4.	 RECOMMENDATION ON DRUG CLASSES TO BE USED AS FIRST-LINE AGENTS For adults with hypertension requiring pharmacological treatment, WHO recommends the use of drugs from any of the following three classes of pharmacological antihypertensive medications as an initial treatment: 1. thiazide and thi... [^2]

3. **GRADE 3 HYPERTENSION (SBP > =180, DBP > =110)** [MoHFW Standard Treatment Guidelines - Hypertension (Quick Reference Guide), p. 19, §GRADE 3 HYPERTENSION (SBP > =180, DBP > =110), 2016]:
   GRADE 3 HYPERTENSION (SBP >=180, DBP >=110) Use two drugs - A+C or C+D or A+D Add third drug - A+C+D if response not adequate within 2-4 weeks ALL GRADES OF HYPERTENSION WITH ASSOCIATED CLINICAL CONDITIONS CAD: coronary artery disease - B+A2, C CHF: congestive heart failure - D+A+B, MRA CKD: chro... [^3]

4. **4.	 RECOMMENDATION ON DRUG CLASSES TO BE USED AS FIRST-LINE AGENTS** [WHO Guideline for the Pharmacological Treatment of Hypertension in Adults, p. 23, §4.	 RECOMMENDATION ON DRUG CLASSES TO BE USED AS FIRST-LINE AGENTS, 2021]:
   4.	 RECOMMENDATION ON DRUG CLASSES TO BE USED AS FIRST-LINE AGENTS For adults with hypertension requiring pharmacological treatment, WHO recommends the use of drugs from any of the following three classes of pharmacological antihypertensive medications as an initial treatment: 1. thiazide and thi... [^4]


### Patient Applicability & Context Analysis

- **Recorded Clinic BP (162/78 mmHg)**: Evaluated against threshold criteria in retrieved guideline recommendations [^1].
- **Patient Age (84 years)**: Evaluated against age-stratified criteria in retrieved recommendations [^1].

### Missing Patient Information & Recommended Workup

- **Renal Function (eGFR / Serum Creatinine)**: Referenced in retrieved dosing criteria and contraindication exceptions.
- **Urine Albumin-to-Creatinine Ratio (ACR)**: Required to screen for renal target-organ damage and microalbuminuria.
- **Glycemic Status (HbA1c / Fasting Glucose)**: Referenced in retrieved criteria to assess diabetic comorbidity and glycemic control.

### General Clinical Rationale

*General Clinical Rationale — Not a Formal Guideline Recommendation*:
Stepwise blood pressure and glycemic management provides synergistic protection against microvascular and macrovascular events. Treatment decisions should be individualized based on tolerability and target organ evaluation. [^1]

*Research Prototype Disclaimer: For evaluation and research purposes only. This software is not an approved medical device and does not replace certified clinical judgment.*

**Citation Verification**: Citations Verified: 4/4 (100.0% valid). Unverified: 0

---