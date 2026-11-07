from week3_structured.structured_call import ask_rfp

QUESTION = "Describe your approach to disaster recovery for a managed PostgreSQL database."


def main():
    successes = 0
    for i in range(10):
        try:
            result, usage = ask_rfp(QUESTION)
            successes += 1
            print(f"Run {i + 1}: OK (confidence {result.confidence:.0%})")
        except ValueError as e:
            print(f"Run {i + 1}: FAILED: {e}")
    print(f"\n{successes}/10 valid answers")


if __name__ == "__main__":
    main()