from pid.heuristic_detector import HeuristicDetector
from pid.models import DetectionResult, Severity
from pid.pattern_detector import PatternDetector


class PromptInjectionDetector:
    """
    Fusion engine that combines:
      - PatternDetector (regex-based)
      - HeuristicDetector (intent-based)
    Produces a unified DetectionResult with blended confidence and severity.
    """

    def __init__(self) -> None:
        self.pattern_detector = PatternDetector()
        self.heuristic_detector = HeuristicDetector()

    def detect(self, text: str) -> DetectionResult:
        # Run both detectors
        pattern_result = self.pattern_detector.detect(text)
        heuristic_result = self.heuristic_detector.detect(text)

        # If neither detector fires → no injection
        if not pattern_result.is_injection and not heuristic_result.is_injection:
            return DetectionResult(
                is_injection=False,
                confidence=0.0,
                severity=Severity.NONE,
                reasons=[]
            )

        # --- Fusion Logic ---
        # Blend confidence scores
        confidence = max(pattern_result.confidence, heuristic_result.confidence)

        # Combine reasons
        reasons = []
        reasons.extend(pattern_result.reasons)
        reasons.extend(heuristic_result.reasons)

        # Severity escalation rules
        if pattern_result.severity == Severity.HIGH or heuristic_result.severity == Severity.HIGH:
            severity = Severity.HIGH
        elif pattern_result.severity == Severity.MEDIUM or heuristic_result.severity == Severity.MEDIUM:
            severity = Severity.MEDIUM
        else:
            severity = Severity.LOW

        # Final injection decision
        is_injection = confidence >= 0.5

        return DetectionResult(
            is_injection=is_injection,
            confidence=confidence,
            severity=severity,
            reasons=reasons
        )
