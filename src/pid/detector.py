from pid.pattern_detector import PatternDetector
from pid.heuristic_detector import HeuristicDetector
from pid.models import DetectionResult, Severity


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

        # If neither detector finds evidence → no injection
        if not pattern_result.reasons and not heuristic_result.reasons:
            return DetectionResult(
                is_injection=False,
                confidence=0.0,
                severity=Severity.NONE,
                reasons=[]
            )

        # --- Fusion Logic ---
        # Blend confidence scores across detectors. Weak signals can add up to
        # a high-confidence injection even when each detector is sub-threshold.
        confidence = min(
            pattern_result.confidence + heuristic_result.confidence,
            1.0,
        )

        # Combine reasons
        reasons = []
        reasons.extend(pattern_result.reasons)
        reasons.extend(heuristic_result.reasons)

        # Severity escalation rules
        if (
            confidence >= 0.8
            or pattern_result.severity == Severity.HIGH
            or heuristic_result.severity == Severity.HIGH
        ):
            severity = Severity.HIGH
        elif (
            confidence >= 0.5
            or pattern_result.severity == Severity.MEDIUM
            or heuristic_result.severity == Severity.MEDIUM
        ):
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