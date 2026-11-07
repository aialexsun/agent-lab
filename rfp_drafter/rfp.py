import json
import time
from pathlib import Path
from week3_structured.structured_call import ask_rfp

FOLDER = Path(__file__).parent
QUESTIONS_FILE = FOLDER / "questions.txt"
ANSWERS_FILE = FOLDER / "answers.json"
REVIEW_BELOW = 0.6   # flag answers with lower confidence for human review


def load_questions(path):
    questions = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            questions.append(line)
    return questions


def main():
    questions = load_questions(QUESTIONS_FILE)
    print(f"Loaded {len(questions)} questions\n")

    results = []
    for number, question in enumerate(questions, start=1):
        print(f"[{number}/{len(questions)}] {question}")
        start = time.perf_counter()
        try:
            answer, tokens_in, tokens_out = ask_rfp(question)
            seconds = time.perf_counter() - start
            entry = {
                "question": question,
                **answer.model_dump(),
                "tokens_in": tokens_in,
                "tokens_out": tokens_out,
                "seconds": round(seconds, 1),
            }
            flag = "  <- review" if answer.confidence < REVIEW_BELOW else ""
            print(f"    OK in {seconds:.0f} s, {tokens_out} tokens out, confidence {answer.confidence:.0%}{flag}\n")
        except ValueError as e:
            seconds = time.perf_counter() - start
            entry = {"question": question, "error": str(e), "seconds": round(seconds, 1)}
            print(f"    FAILED after {seconds:.0f} s: {e}\n")
        results.append(entry)

    ANSWERS_FILE.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    ok = [r for r in results if "error" not in r]
    total_seconds = sum(r["seconds"] for r in results)
    total_tokens = sum(r["tokens_out"] for r in ok)
    print(f"Done: {len(ok)}/{len(results)} answered, {total_seconds:.0f} s total, {total_tokens} output tokens")
    print(f"Saved to {ANSWERS_FILE}")


if __name__ == "__main__":
    main()