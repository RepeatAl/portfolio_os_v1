from engines.engine_runner import run_all_engines


def main():

    print("\n=== PORTFOLIO OS START ===")

    results = run_all_engines()

    print("\n=== FULL SYSTEM OUTPUT ===")

    for key, value in results.items():
        print(f"\n{key.upper()} RESULT:")
        print(value)

    print("\n=== ORCHESTRATION COMPLETE ===")


if __name__ == "__main__":
    main()