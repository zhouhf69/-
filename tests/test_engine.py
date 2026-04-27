from app.engine import evaluate_case
from app.models import CaseInput, PatientFact


def test_evaluate_case_triggers_rules():
    case = CaseInput(
        patient_id="p1",
        encounter_id="e1",
        facts=[
            PatientFact(key="eGFR", value=25, source="his"),
            PatientFact(key="glucose", value=3.2, source="his"),
            PatientFact(key="age", value=70, source="his"),
            PatientFact(key="systolic_bp", value=150, source="his"),
        ],
    )

    resp = evaluate_case(case)

    ids = {x.id for x in resp.triggered}
    assert "renal_dose_check" in ids
    assert "hypoglycemia_risk" in ids
    assert "simple_cv_risk_index" in resp.scores
