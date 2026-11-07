import json
from pydantic import BaseModel, Field, ValidationError


class RfpAnswer(BaseModel):
    answer: str
    confidence: float = Field(ge=0, le=1)   # must be between 0 and 1
    assumptions: list[str]
    risks: list[str]


def main():
    # 1. A correct reply
    good = '{"answer": "We use multi-AZ replicas.", "confidence": 0.8, "assumptions": ["Customer accepts 15-min RPO"], "risks": ["Higher cost"]}'
    result = RfpAnswer.model_validate_json(good)
    print("Answer:", result.answer)
    print("Confidence:", result.confidence)
    print("First risk:", result.risks[0])

    # 2. A broken reply: confidence is a word, risks is missing
    bad = '{"answer": "Yes.", "confidence": "high", "assumptions": []}'
    try:
        RfpAnswer.model_validate_json(bad)
    except ValidationError as e:
        print("\nValidation failed, as expected:")
        print(e)

    # 3. The schema you'll send to the model
    print("\nJSON schema:")
    print(json.dumps(RfpAnswer.model_json_schema(), indent=2))


if __name__ == "__main__":
    main()
