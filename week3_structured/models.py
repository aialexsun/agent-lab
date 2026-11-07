from pydantic import BaseModel, Field


class RfpAnswer(BaseModel):
    answer: str = Field(max_length=1200, description="Concise answer in 3-6 sentences, written as a senior cloud presales architect")
    confidence: float = Field(ge=0, le=1, description="How confident you are in the answer, from 0 to 1")
    assumptions: list[str] = Field(max_length=5, description="Assumptions the answer depends on")
    risks: list[str] = Field(max_length=5, description="Risks or caveats the customer should know about")