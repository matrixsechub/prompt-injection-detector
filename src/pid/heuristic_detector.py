from pid.models import DetectionResult, Severity


class HeuristicDetector:
    """
    Heuristic-based detection for prompt injection attempts.
    These rules catch patterns that are not simple regex matches,
    but indicate intent to override system behavior.
    """

    def __init__(self) -> None:
        # Weighted heuristic signals
        self.heuristics = [
            # Attempts to override system identity
            (lambda t: "you are now" in t.lower(), 0.5),

            # Attempts to redefine the assistant's role
            (lambda t: "from now on" in t.lower(), 0.4),

            # Attempts to jailbreak or escape constraints
            (lambda t: "break character" in t.lower(), 0.4),
            (lambda t: "stop following rules" in t.lower(), 0.5),

            # Attempts to bypass safety
            (lambda t: "ignore safety" in t.lower(), 0.6),
            (lambda t: "override restrictions" in t.lower(), 0.6),

            # Attempts to force system-level behavior
            (lambda t: "system override" in t.lower(), 0.7),
            (lambda t: "admin mode" in t.lower(), 0.7),
        ]

    def detect(self, text: str) -> DetectionResult:
        if not text:
            return DetectionResult(
                is_injection=False,
                confidence=0.0,
                severity=Severity.NONE,
                reasons=[]
            )

        matches = []
        confidence = 0.0

        # Evaluate each heuristic
        for rule, weight in self.heuristics:
            try:
                if rule(text):
                    matches.append(f"Heuristic triggered (weight {weight}): {rule.__name__}")
                    confidence += weight
            except Exception:
                # If a heuristic fails, skip it safely
                continue

        if not matches:
            return DetectionResult(
                is_injection=False,
                confidence=0.0,
                severity=Severity.NONE,
                reasons=[]
            )

        # Cap confidence
        confidence = min(confidence, 1.0)
        is_injection = confidence >= 0.5

        # Severity mapping
        if confidence >= 0.8:
            severity = Severity.HIGH
        elif confidence >= 0.5:
            severity = Severity.MEDIUM
        else:
            severity = Severity.LOW

        return DetectionResult(
            is_injection=is_injection,
            confidence=confidence,
            severity=severity,
            reasons=matches
        )
