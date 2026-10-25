import argparse
from pid.detector import PromptInjectionDetector


def main():
    parser = argparse.ArgumentParser(
        description="Prompt Injection Detector CLI"
    )

    parser.add_argument(
        "text",
        nargs="*",
        help="Text to analyze for prompt injection"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed reasoning and matched rules"
    )

    args = parser.parse_args()

    # Join text arguments into a single string
    text = " ".join(args.text)

    detector = PromptInjectionDetector()
    result = detector.detect(text)

    # JSON output mode
    if args.json:
        print(result.to_json())
        return

    # Default human-readable output
    print(f"Injection Detected: {result.is_injection}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Severity: {result.severity.value}")

    # Verbose mode
    if args.verbose:
        print("\n--- Reasons ---")
        for reason in result.reasons:
            print(f"• {reason}")

if __name__ == "__main__":
    main()
