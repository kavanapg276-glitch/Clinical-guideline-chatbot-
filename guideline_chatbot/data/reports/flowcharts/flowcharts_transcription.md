# MoHFW Guideline Flowchart Structured Transcriptions

> [!CAUTION]
> **VERIFICATION STATUS: `needs_review: true` | `indexed_for_retrieval: false`**  
> These structured decision nodes were transcribed from the embedded flowchart drawings of the MoHFW Standard Treatment Guidelines. Per Gate 0 approval directives, **these nodes MUST NOT be indexed for RAG retrieval** until each has been explicitly verified by the human reviewer against the rendered high-resolution page images.

---

## 1. Flowchart Overview & Image Mapping

| Flowchart ID | Source Document | Page | Rendered High-Res Image | Verification Status | RAG Indexing Allowed? |
|---|---|---|---|---|---|
| `fc_mohfw_qr_p40` | MoHFW STG Quick Reference Guide (`6591.pdf`) | p. 40 | [`mohfw_quickref_p40_adult_htn_algorithm.png`](file:///c:/Users/kavan/OneDrive/Desktop/capstone/guideline_chatbot/data/reports/flowcharts/mohfw_quickref_p40_adult_htn_algorithm.png) | `needs_review` | **NO** (Hold until human review) |
| `fc_mohfw_qr_p44` | MoHFW STG Quick Reference Guide (`6591.pdf`) | p. 44 | [`mohfw_quickref_p44_diabetic_htn_algorithm.png`](file:///c:/Users/kavan/OneDrive/Desktop/capstone/guideline_chatbot/data/reports/flowcharts/mohfw_quickref_p44_diabetic_htn_algorithm.png) | `needs_review` | **NO** (Hold until human review) |
| `fc_mohfw_bg_p127` | MoHFW STG Background Document (`5191.pdf`) | p. 127 | [`mohfw_background_p127_screening_diagnosis_flowchart.png`](file:///c:/Users/kavan/OneDrive/Desktop/capstone/guideline_chatbot/data/reports/flowcharts/mohfw_background_p127_screening_diagnosis_flowchart.png) | `needs_review` | **NO** (Hold until human review) |
| `fc_mohfw_qr_p52` | MoHFW STG Quick Reference Guide (`6591.pdf`) | p. 52 | [`mohfw_quickref_p52_pregnancy_htn_algorithm.png`](file:///c:/Users/kavan/OneDrive/Desktop/capstone/guideline_chatbot/data/reports/flowcharts/mohfw_quickref_p52_pregnancy_htn_algorithm.png) | `needs_review` | **NO** (Hold until human review) |

---

## 2. Transcribed Flowchart 1: Physical Activity & Exercise Prescription
- **Source:** MoHFW STG Quick Reference Guide, Page 40 (Ref: 85 - Metkus et al., Circulation 2010; MoHFW STG Annexure 2).
- **Target Condition:** Adult Hypertension (Lifestyle & Non-Pharmacological Management).

```mermaid
flowchart TD
    N1["Adult with diagnosed HTN or high CV risk (BP >= 140/90)"] --> N2{"Pre-exercise symptom & safety check: Chest pain, dyspnea, syncope, heart failure, ACS?"}
    N2 -- Yes --> N3["CONTRAINDICATION: Do not start exercise. Urgent cardiac evaluation & stabilization."]
    N2 -- No --> N4{"Is the patient chronically sedentary?"}
    N4 -- Yes --> N5["Gradual start: 10 min/session moderate activity; build gradually."]
    N4 -- No --> N6["Standard aerobic prescription: >= 30 min/day or >= 150 min/week in >= 10 min bouts (brisk walk 3-4 mph). Avg reduction: -4 SBP / -2.5 DBP."]
    N5 --> N6
    N6 --> N7["Resistance training: Muscle strengthening exercises >= 2 days/week."]
```

### Node Dictionary
- **Node `N1` (Entry):** Adult presenting with diagnosed hypertension or high CVD risk.
- **Node `N2` (Decision/Check):** Clinical safety screen for chest discomfort, jaw pain, palpitations, syncope, dyspnea, decompensated heart failure, or acute coronary syndrome.
- **Node `N3` (Action/Contraindication):** Exercise contraindicated. Urgent referral/workup required before any exercise program.
- **Node `N4` (Decision/Check):** Activity history assessment: chronically sedentary vs active.
- **Node `N5` (Action):** Start with 10 minutes moderate activity per session; gradually titrate upward to prevent acute cardiac events and musculoskeletal trauma.
- **Node `N6` (Action/Prescription):** Moderate-intensity physical activity of 30 mins/day or >= 150 mins/week, 4–7 days/week (brisk walking, cycling).
- **Node `N7` (Action/Prescription):** Resistance muscle-strengthening exercises on at least 2 days per week.

---

## 3. Transcribed Flowchart 2: Adult Hypertension Diagnosis, Stratification & Treatment Pathway
- **Source:** MoHFW STG Quick Reference Guide, Page 44 & Background Document, Page 127 (Ref: 23 - European Guidelines on CVD Prevention / MoHFW Section 7 Management Pathway).
- **Target Condition:** Primary Hypertension in Adults.

```mermaid
flowchart TD
    M1["Confirmed HTN: SBP >= 140 and/or DBP >= 90 mmHg on >= 2 clinic visits"] --> M2["Universal lifestyle modification: Salt < 5 g/day, BMI 18.5-22.9, exercise, stop tobacco"]
    M2 --> M3{"Severity & Risk Stratification: Grade 1 Uncomplicated vs Grade 2/3, TOD, Diabetes, CKD, CAD?"}
    M3 -- Grade 1 Low Risk --> M4{"3-Month Lifestyle Trial: Is BP controlled to < 140/90?"}
    M4 -- Controlled --> M4_OK["Maintain lifestyle & review clinic BP every 3-6 months"]
    M4 -- Uncontrolled --> M5["Step 1 Monotherapy: Age < 60y: ACEi (Enalapril 2.5-5 mg) or ARB (Losartan 25-50 mg) or CCB. Age >= 60y: CCB (Amlodipine 2.5-5 mg) or Thiazide (HCTZ 12.5 mg)."]
    M3 -- Grade 2/3 or High Risk --> M5
    M5 --> M6{"Step 1 Target Check at 4-6 Weeks: BP < 140/90 (<150/90 if >=80y; <130/80 if DM/CKD)?"}
    M6 -- Yes --> M6_OK["Maintain dose & monitor creatinine/electrolytes at 6 months"]
    M6 -- No --> M7["Step 2 Dual Combination: Combine 2 classes: ACEi/ARB + CCB (A + C) OR ACEi/ARB + Thiazide (A + D). NEVER ACEi + ARB."]
    M7 --> M8{"Step 2 Target Check at 4 Weeks: BP at target?"}
    M8 -- Yes --> M6_OK
    M8 -- No --> M9["Step 3 Triple Combination: ACEi/ARB + CCB + Thiazide (A + C + D). Verify adherence."]
    M9 --> M10{"Step 3 Target Check at 4 Weeks: BP at target?"}
    M10 -- Yes --> M6_OK
    M10 -- No --> M11["Step 4 Resistant HTN: Add Spironolactone (MRA 25 mg) or Beta-blocker; refer to District/Specialist."]
```

---

## 4. Transcribed Flowchart 3: Essential Formulary & Renal Safeguards
- **Source:** MoHFW STG Quick Reference Guide, Page 52 (Formulary Summary & Renal Footnote).
- **Target Condition:** Drug safety and dosing boundaries in renal impairment.

```mermaid
flowchart TD
    F1["Antihypertensive Drug Selection: CCB (Amlodipine), ACEi (Enalapril), ARB (Losartan), Thiazide (HCTZ)"] --> F2{"Renal Function Check: Creatinine Clearance < 30 ml/min (approx Serum Cr >= 3.0 mg/dl)?"}
    F2 -- CrCl < 30 ml/min --> F3["CRITICAL WARNING: Avoid Thiazide Diuretics (ineffective at CrCl < 30). Switch to Loop Diuretics (Furosemide). Monitor K+ and Cr closely with ACEi/ARBs."]
    F2 -- CrCl >= 30 ml/min --> F4["Standard Essential Formulary Dosing: HCTZ 12.5 mg once daily (near-maximal BP reduction with minimal metabolic impact); Amlodipine 2.5-5 mg once daily; Enalapril 2.5-5 mg once daily."]
```

### Footnote Citation from Page 52:
> *"Renal impairment: Avoid if creatinine clearance is less than <30 ml/min (approximate serum creatinine 3 mg/dl), when they may be ineffective."*

