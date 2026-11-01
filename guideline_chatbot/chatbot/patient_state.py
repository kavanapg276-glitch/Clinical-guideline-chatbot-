"""Multi-turn clinical patient state tracker and contradiction verification layer.

Extracts demographics, vitals, lab values, allergies, and comorbidities from conversational turns.
Maintains state history and detects clinical contradictions across turns.
"""

from __future__ import annotations

import dataclasses
import logging
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


def _utc_timestamp() -> str:
    """Return ISO 8601 formatted UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


@dataclass
class DisputedFact:
    """Represents a contradiction between established patient state and new claims."""

    field: str
    previous_value: Any
    new_value: Any
    explanation: str
    turn_index: int
    is_resolved: bool = False
    resolution_turn: int | None = None
    resolution_note: str | None = None
    timestamp: str = dataclasses.field(default_factory=_utc_timestamp)


@dataclass
class PatientState:
    """Structured patient profile extracted and tracked across multi-turn interactions."""

    age: int | None = None
    sex: str | None = None  # "male" | "female"
    ethnicity: str | None = None  # "black_african_or_caribbean", "south_asian", "white", etc.
    is_pregnant: bool = False
    pregnancy_weeks: int | None = None
    is_breastfeeding: bool = False

    # Vitals
    sbp: float | None = None
    dbp: float | None = None
    abpm_daytime_sbp: float | None = None
    abpm_daytime_dbp: float | None = None
    bmi: float | None = None

    # Clinical conditions & Comorbidities
    conditions: set[str] = dataclasses.field(default_factory=set)

    # Active medications & Allergies
    medications: set[str] = dataclasses.field(default_factory=set)
    allergies: set[str] = dataclasses.field(default_factory=set)
    symptoms: set[str] = dataclasses.field(default_factory=set)

    # Laboratory parameters
    hba1c: float | None = None  # Percentage
    egfr: float | None = None  # mL/min/1.73m^2
    creatinine: float | None = None  # mg/dL
    potassium: float | None = None  # mmol/L
    urine_acr: float | None = None  # mg/mmol

    # Disputed and conflict tracking
    disputed_facts: list[DisputedFact] = dataclasses.field(default_factory=list)
    turn_count: int = 0
    state_history: list[dict[str, Any]] = dataclasses.field(default_factory=list)

    @property
    def has_conflicts(self) -> bool:
        """Return True if unresolved clinical contradictions have been recorded."""
        return any(not f.is_resolved for f in self.disputed_facts)

    @property
    def active_conflicts(self) -> list[DisputedFact]:
        """Return list of active, unresolved clinical contradictions."""
        return [f for f in self.disputed_facts if not f.is_resolved]

    def to_retrieval_context(self) -> dict[str, Any]:
        """Convert state to dictionary format consumed by HybridRetriever."""
        ctx: dict[str, Any] = {
            "conditions": sorted(self.conditions),
            "medications": sorted(self.medications),
            "allergies": sorted(self.allergies),
            "is_pregnant": self.is_pregnant,
            "pregnancy_weeks": self.pregnancy_weeks,
            "is_breastfeeding": self.is_breastfeeding,
        }
        if self.age is not None:
            ctx["age"] = self.age
        if self.sbp is not None or self.dbp is not None:
            ctx["vitals"] = {
                "sbp": self.sbp,
                "dbp": self.dbp,
            }
        return ctx

    def to_summary_string(self) -> str:
        """Render human-readable summary of active patient state."""
        parts: list[str] = []
        if self.age is not None:
            parts.append(f"Age: {self.age}")
        if self.sex:
            parts.append(f"Sex: {self.sex}")
        if self.is_pregnant:
            if self.pregnancy_weeks is not None:
                parts.append(f"Status: Pregnant ({self.pregnancy_weeks} weeks)")
            else:
                parts.append("Status: Pregnant")
        elif self.is_breastfeeding:
            parts.append("Status: Breastfeeding")

        if self.sbp is not None and self.dbp is not None:
            parts.append(f"BP: {int(self.sbp)}/{int(self.dbp)} mmHg")
        elif self.sbp is not None:
            parts.append(f"SBP: {int(self.sbp)} mmHg")

        if self.conditions:
            parts.append(f"Conditions: {', '.join(sorted(self.conditions))}")
        if self.medications:
            parts.append(f"Medications: {', '.join(sorted(self.medications))}")
        if self.allergies:
            parts.append(f"Allergies: {', '.join(sorted(self.allergies))}")
        if self.hba1c is not None:
            parts.append(f"HbA1c: {self.hba1c:.1f}%")
        if self.egfr is not None:
            parts.append(f"eGFR: {int(self.egfr)} mL/min")
        if self.creatinine is not None:
            parts.append(f"Creatinine: {self.creatinine:.2f} mg/dL")

        if self.disputed_facts:
            parts.append(f"Conflicts ({len(self.disputed_facts)}): Disputed claims detected")

        return "; ".join(parts) if parts else "No patient context provided."


class PatientStateManager:
    """Manages multi-turn patient state extraction, updates, and contradiction detection."""

    def __init__(self) -> None:
        self.state = PatientState()

    def update_from_text(self, text: str) -> tuple[PatientState, list[DisputedFact]]:
        """Parse user input text, update active state, and return any newly detected conflicts."""
        self.state.turn_count += 1
        turn_idx = self.state.turn_count
        new_conflicts: list[DisputedFact] = []

        lower = text.lower()

        # Check if the user is resolving a previously disputed claim
        clarification_pattern = re.search(
            r"\b(?:to\s+clarify|confirming\s+that|verified\s+reading|reading\s+today\s+is\s+confirmed|is\s+confirmed|confirmed\s+on\s+repeated|the\s+correct\s+reading)\b",
            lower,
        )
        if clarification_pattern and self.state.has_conflicts:
            for df in self.state.disputed_facts:
                if not df.is_resolved:
                    df.is_resolved = True
                    df.resolution_turn = turn_idx
                    df.resolution_note = f"Resolved by clinician clarification in Turn {turn_idx}."

        # 1. Blood Pressure Extraction & Conflict Detection
        # Pattern: 140/90, 165 / 105, BP 150/95
        bp_match = re.search(
            r"\b(?:bp|blood\s+pressure)?\s*[:=]?\s*(\d{2,3})\s*/\s*(\d{2,3})\s*(?:mm\s*hg)?\b",
            lower,
        )
        claims_normotension = bool(
            re.search(
                r"\b(?:normal\s+bp|normal\s+blood\s+pressure|no\s+high\s+bp|not\s+hypertensive|bp\s+is\s+fine|bp\s+is\s+normal|blood\s+pressure\s+(?:is\s+)?(?:completely\s+|entirely\s+)?normal)\b",
                lower,
            )
        )
        is_past_normotension = bool(
            re.search(
                r"\b(?:was\s+normal|previously\s+normal|used\s+to\s+be\s+normal|normal\s+in\s+the\s+past|past\s+normal)\b",
                lower,
            )
        )

        if bp_match:
            new_sbp = float(bp_match.group(1))
            new_dbp = float(bp_match.group(2))

            # Contradiction check: only flag if claiming normal BP in the SAME time frame without clarification
            if (
                "normotensive_claim" in self.state.conditions
                and not is_past_normotension
                and (new_sbp >= 140 or new_dbp >= 90)
            ):
                conflict = DisputedFact(
                    field="blood_pressure",
                    previous_value="Claimed normal blood pressure",
                    new_value=f"{int(new_sbp)}/{int(new_dbp)} mmHg",
                    explanation=(
                        f"Patient previously claimed normal blood pressure in Turn 1, but reports "
                        f"elevated clinic BP {int(new_sbp)}/{int(new_dbp)} mmHg in Turn {turn_idx}."
                    ),
                    turn_index=turn_idx,
                )
                self.state.disputed_facts.append(conflict)
                new_conflicts.append(conflict)
                self.state.conditions.discard("normotensive_claim")

            self.state.sbp = new_sbp
            self.state.dbp = new_dbp
            self.state.conditions.add("hypertension")
        elif claims_normotension and not is_past_normotension:
            if self.state.sbp and self.state.sbp >= 140:
                conflict = DisputedFact(
                    field="blood_pressure",
                    previous_value=f"{int(self.state.sbp)}/{int(self.state.dbp or 0)} mmHg",
                    new_value="Claims normal blood pressure",
                    explanation=(
                        f"Patient claims normal blood pressure in Turn {turn_idx}, which contradicts "
                        f"recorded elevated BP {int(self.state.sbp)}/{int(self.state.dbp or 0)} mmHg."
                    ),
                    turn_index=turn_idx,
                )
                self.state.disputed_facts.append(conflict)
                new_conflicts.append(conflict)
            else:
                self.state.conditions.add("normotensive_claim")

        # 2. Age & Sex Extraction & Conflict Detection
        age_match = re.search(
            r"\b(?:age|aged|i am|he is|she is)?\s*[:=]?\s*(\d{1,2})\s*[- ]*(?:years?[- ]*old|yo|y/o)\b",
            lower,
        )
        if not age_match:
            age_match = re.search(r"\bage\s*[:=]?\s*(\d{1,2})\b", lower)
        if age_match:
            parsed_age = int(age_match.group(1))
            if 1 <= parsed_age <= 115:
                if self.state.age is not None and abs(self.state.age - parsed_age) >= 5:
                    conflict = DisputedFact(
                        field="age",
                        previous_value=self.state.age,
                        new_value=parsed_age,
                        explanation=(
                            f"Reported age changed from {self.state.age} to {parsed_age} years "
                            f"in Turn {turn_idx}."
                        ),
                        turn_index=turn_idx,
                    )
                    self.state.disputed_facts.append(conflict)
                    new_conflicts.append(conflict)
                self.state.age = parsed_age

        if re.search(r"\b(?:female|woman|lady)\b", lower):
            self.state.sex = "female"
        elif re.search(r"\b(?:male|man|gentleman)\b", lower):
            self.state.sex = "male"

        # 3. Pregnancy & Lactation Status
        preg_match = re.search(
            r"\b(?:(\d{1,2})\s*weeks?\s+(?:pregnant|gestation|pregnancy)|"
            r"(?:i\s+am|she\s+is|patient\s+is|currently)?\s*pregnant|pregnancy|expecting|gestation|"
            r"first\s+trimester|second\s+trimester|third\s+trimester)\b",
            lower,
        )
        if preg_match:
            self.state.is_pregnant = True
            self.state.conditions.add("pregnancy")
            self.state.sex = "female"
            if preg_match.group(1):
                self.state.pregnancy_weeks = int(preg_match.group(1))
            else:
                weeks_match = re.search(r"\b(\d{1,2})\s*weeks?\b", lower)
                if weeks_match:
                    self.state.pregnancy_weeks = int(weeks_match.group(1))

        if re.search(r"\b(?:breastfeeding|nursing|lactating|lactation)\b", lower):
            self.state.is_breastfeeding = True
            self.state.sex = "female"

        # 4. HbA1c Lab Extraction
        hba1c_match = re.search(
            r"\bhba1c\s*(?:of|is|level|[:=])?\s*(\d{1,2}(?:\.\d+)?)\s*%?\b", lower
        )
        if hba1c_match:
            parsed_a1c = float(hba1c_match.group(1))
            self.state.hba1c = parsed_a1c
            if parsed_a1c >= 6.5:
                self.state.conditions.add("type_2_diabetes")

        # 5. eGFR, Creatinine and Renal Function
        egfr_match = re.search(r"\begfr\s*(?:of|is|[:=])?\s*(\d{1,3})\b", lower)
        if egfr_match:
            self.state.egfr = float(egfr_match.group(1))
            if self.state.egfr < 60:
                self.state.conditions.add("chronic_kidney_disease")

        creat_match = re.search(
            r"\bcreatinine\s*(?:of|is|[:=])?\s*(\d{1,2}(?:\.\d+)?)\s*(?:mg/dl)?\b", lower
        )
        if creat_match:
            self.state.creatinine = float(creat_match.group(1))

        acr_match = re.search(
            r"\b(?:urine\s+acr|acr)\s*(?:of|is|came\s+back\s+at|[:=])?\s*(\d+(?:\.\d+)?)\s*(?:mg/mmol|mg/g)?\b",
            lower,
        )
        if acr_match:
            self.state.urine_acr = float(acr_match.group(1))
            self.state.conditions.add("microalbuminuria")

        if (
            re.search(
                r"\b(?:microalbuminuria|proteinuria|albuminuria|high\s+protein\s+in\s+urine)\b",
                lower,
            )
            and not acr_match
        ):
            self.state.conditions.add("microalbuminuria")
            # NOTE: Strict guideline rule: A single ACR test is microalbuminuria, not diagnosed CKD.
            # Do NOT infer chronic_kidney_disease from a single ACR/microalbuminuria test.

        # 6. Condition Keywords & Conflict Detection
        if re.search(r"\b(?:diabetes|diabetic|t2dm|type\s*2\s*diabetes|sugar)\b", lower):
            if re.search(
                r"\b(?:no\s+diabetes|don't\s+have\s+diabetes|without\s+diabetes|not\s+diabetic)\b",
                lower,
            ):
                if "type_2_diabetes" in self.state.conditions:
                    conflict = DisputedFact(
                        field="type_2_diabetes",
                        previous_value="Present",
                        new_value="Denied",
                        explanation=(
                            f"Patient previously had type 2 diabetes recorded, but explicitly denies "
                            f"diabetes in Turn {turn_idx}."
                        ),
                        turn_index=turn_idx,
                    )
                    self.state.disputed_facts.append(conflict)
                    new_conflicts.append(conflict)
                self.state.conditions.discard("type_2_diabetes")
            else:
                self.state.conditions.add("type_2_diabetes")

        if re.search(
            r"\b(?:hypertension|hypertensive|high\s+bp|high\s+blood\s+pressure)\b", lower
        ) and not re.search(
            r"\b(?:no\s+hypertension|not\s+hypertensive|without\s+hypertension)\b", lower
        ):
            self.state.conditions.add("hypertension")

        if re.search(r"\b(?:heart\s+failure|chf|hfref|hfpef)\b", lower):
            self.state.conditions.add("heart_failure")

        if re.search(
            r"\b(?:cad|coronary\s+artery\s+disease|angina|myocardial\s+infarction|post-?mi)\b",
            lower,
        ):
            self.state.conditions.add("cardiovascular_disease")

        # 7. Medication Extraction & Conflict Detection
        med_denial = bool(
            re.search(
                r"\b(?:no\s+medicines?|no\s+meds?|not\s+taking\s+any(?:thing|medicines?|pills?)|not\s+on\s+any\s+meds?)\b",
                lower,
            )
        )
        if med_denial:
            if self.state.medications:
                conflict = DisputedFact(
                    field="medications",
                    previous_value=", ".join(sorted(self.state.medications)),
                    new_value="None",
                    explanation=(
                        f"Patient claimed no active medications in Turn {turn_idx}, contradicting "
                        f"active medications: {', '.join(sorted(self.state.medications))}."
                    ),
                    turn_index=turn_idx,
                )
                self.state.disputed_facts.append(conflict)
                new_conflicts.append(conflict)
            else:
                self.state.conditions.add("no_meds_claim")

        med_patterns = {
            "metformin": r"\bmetformin\b",
            "amlodipine": r"\bamlodipine\b",
            "ramipril": r"\bramipril\b",
            "telmisartan": r"\btelmisartan\b",
            "losartan": r"\blosartan\b",
            "enalapril": r"\benalapril\b",
            "chlorthalidone": r"\bchlorthalidone\b",
            "hydrochlorothiazide": r"\b(?:hydrochlorothiazide|hctz)\b",
            "atenolol": r"\batenolol\b",
            "carvedilol": r"\bcarvedilol\b",
            "spironolactone": r"\bspironolactone\b",
            "dapagliflozin": r"\bdapagliflozin\b",
            "empagliflozin": r"\bempagliflozin\b",
            "glimepiride": r"\bglimepiride\b",
            "insulin": r"\binsulin\b",
        }
        for med_name, pat in med_patterns.items():
            if re.search(pat, lower):
                if "no_meds_claim" in self.state.conditions:
                    conflict = DisputedFact(
                        field="medications",
                        previous_value="Claimed no medications",
                        new_value=med_name,
                        explanation=(
                            f"Patient previously claimed to take no medicines, but reports taking "
                            f"{med_name} in Turn {turn_idx}."
                        ),
                        turn_index=turn_idx,
                    )
                    self.state.disputed_facts.append(conflict)
                    new_conflicts.append(conflict)
                    self.state.conditions.discard("no_meds_claim")
                self.state.medications.add(med_name)

        # 8. Allergies Extraction & Conflict Detection
        allergy_denial = bool(
            re.search(
                r"\b(?:no\s+allergies|not\s+allergic\s+to\s+anything|no\s+drug\s+allergies|allergies\s*[:=]?\s*none)\b",
                lower,
            )
        )
        if allergy_denial:
            if self.state.allergies:
                conflict = DisputedFact(
                    field="allergies",
                    previous_value=", ".join(sorted(self.state.allergies)),
                    new_value="None",
                    explanation=(
                        f"Patient claimed no allergies in Turn {turn_idx}, contradicting recorded "
                        f"allergies: {', '.join(sorted(self.state.allergies))}."
                    ),
                    turn_index=turn_idx,
                )
                self.state.disputed_facts.append(conflict)
                new_conflicts.append(conflict)
            else:
                self.state.conditions.add("no_allergies_claim")

        allergy_patterns = {
            "penicillin": r"\b(?:allergic\s+to\s+penicillin|penicillin\s+allergy)\b",
            "sulfa": r"\b(?:allergic\s+to\s+sulfa|sulfa\s+allergy|sulfonamide\s+allergy)\b",
            "aspirin": r"\b(?:allergic\s+to\s+aspirin|aspirin\s+allergy)\b",
            "acei": r"\b(?:allergic\s+to\s+ace|angioedema\s+with\s+acei?)\b",
        }
        for allergy_name, pat in allergy_patterns.items():
            if re.search(pat, lower):
                if "no_allergies_claim" in self.state.conditions:
                    conflict = DisputedFact(
                        field="allergies",
                        previous_value="Claimed no allergies",
                        new_value=allergy_name,
                        explanation=(
                            f"Patient previously claimed no allergies, but reports {allergy_name} "
                            f"allergy in Turn {turn_idx}."
                        ),
                        turn_index=turn_idx,
                    )
                    self.state.disputed_facts.append(conflict)
                    new_conflicts.append(conflict)
                    self.state.conditions.discard("no_allergies_claim")
                self.state.allergies.add(allergy_name)

        # Snapshot state history
        self.state.state_history.append(self.state.to_retrieval_context())

        return self.state, new_conflicts

    @staticmethod
    def compute_state_delta(
        prev_ctx: dict[str, Any] | None, curr_ctx: dict[str, Any]
    ) -> dict[str, Any]:
        """Compute field-level changes between previous and current patient state."""
        if not prev_ctx:
            return {k: {"previous": None, "current": v} for k, v in curr_ctx.items() if v}
        delta: dict[str, Any] = {}
        all_keys = set(prev_ctx.keys()) | set(curr_ctx.keys())
        for k in sorted(all_keys):
            prev_v = prev_ctx.get(k)
            curr_v = curr_ctx.get(k)
            if prev_v != curr_v:
                delta[k] = {"previous": prev_v, "current": curr_v}
        return delta
