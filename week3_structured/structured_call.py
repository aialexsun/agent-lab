from openai import OpenAI
from pydantic import ValidationError
from config import client, MODEL
from week3_structured.models import RfpAnswer


SYSTEM = (
    "You are a senior cloud presales architect. Answer RFP questions concisely and honestly. "
    "Reply only with JSON with exactly these fields: "
    "answer: plain prose, 3-6 sentences, no JSON, no lists, no headings inside it; "
    "confidence: a number from 0 to 1; "
    "assumptions: 2-4 short strings; "
    "risks: 2-4 short strings. /no_think" # add "/no_think" at the end of this string for qwen models to save tokens and reduce answer time
)


def ask_rfp(question):
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": question},
    ]
    schema = {
        "type": "json_schema",
        "json_schema": {"name": "rfp_answer", "schema": RfpAnswer.model_json_schema()},
    }

    for attempt in range(2):          # first try + one retry
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.6,          # low = more consistent
            max_tokens=800,
            response_format=schema,
        )
        text = response.choices[0].message.content
        try:
            return RfpAnswer.model_validate_json(text), response.usage
        except ValidationError as e:
            print(f"Attempt {attempt + 1} invalid, retrying...")
            print(" Finish reason:", response.choices[0].finish_reason)
            print(" Error:", e)
            print(" Raw reply(first 500 chars):", repr(text[:500]))
            messages.append({"role": "assistant", "content": text})
            messages.append({"role": "user", "content": f"That JSON was invalid: {e}. Return corrected JSON only."})

    raise ValueError("The model did not return valid JSON after a retry")


def main():
    question = input("RFP question: ")
    result, usage = ask_rfp(question)
    print("\nANSWER:\n" + result.answer)
    print(f"\nCONFIDENCE: {result.confidence:.0%}")
    print("ASSUMPTIONS:")
    for item in result.assumptions:
        print(" -", item)
    print("RISKS:")
    for item in result.risks:
        print(" -", item)
    print(f"\nTokens: {usage.prompt_tokens} in, {usage.completion_tokens} out")


if __name__ == "__main__":
    main()