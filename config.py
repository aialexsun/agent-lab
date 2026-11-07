import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL"),
    api_key=os.getenv("LLM_API_KEY"),
)
MODEL = os.getenv("LLM_MODEL")
PRICE_IN = float(os.getenv("LLM_PRICE_IN_PER_M", "0"))
PRICE_OUT = float(os.getenv("LLM_PRICE_OUT_PER_M", "0"))

def cost_usd(usage):
    return (usage.prompt_tokens * PRICE_IN + usage.completion_tokens * PRICE_OUT) / 1_000_000