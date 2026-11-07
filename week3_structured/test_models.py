import pytest
from pydantic import ValidationError
from week3_structured.models import RfpAnswer


def test_valid_answer():
    a = RfpAnswer.model_validate_json('{"answer": "x", "confidence": 0.5, "assumptions": [], "risks": []}')
    assert a.confidence == 0.5


def test_confidence_above_one_is_rejected():
    with pytest.raises(ValidationError):
        RfpAnswer.model_validate_json('{"answer": "x", "confidence": 1.5, "assumptions": [], "risks": []}')