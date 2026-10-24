import re
from typing import List, Tuple, Pattern
from pid.models import DetectionResult, Severity


class PatternDetector:
    def __init__(self) -> None:
        # Weighted regex patterns
        self.patterns: List[Tuple[Pattern[str], float]] = [
            (re.compile(r"ignore\s+(previous|all|prior)\s+instructions?", re.IGNORECASE), 0.6),
            (re.compile(r"disregard\s+(previous|all|prior)\s+instructions?", re.IGNORECASE), 0.5),
            (re.compile(r"pretend\s+(to\s+be|you\s+are)", re.IGNORECASE), 0.4),
            (re.compile(r"roleplaying\s+mode", re.IGNORECASE), 0.3),
        ]

    def detect(self, text: str) -> DetectionResult:
        # Empty input → no injection
        if not text:
            return DetectionResult(
                is_injection=False,
                confidence=0.0,
                severity=Severity.NONE,
                reasons=[]
            )

        # Collect matches with weights
        matches: List[Tuple[str, float]] = []
        for pattern, weight in self.patterns:
            if pattern.search(text):
                matches.append((f"Matched pattern: {pattern.pattern}", weight))

        # No matches → no injection
        if not matches:
            return DetectionResult(
                is_injection=False,
                confidence=0.0,
                severity=Severity.NONE,
                reasons=[]
            )

        # Weighted scoring
        confidence = sum(weight for _, weight in matches)
        confidence = min(confidence, 1.0)

        # Threshold
        is_injection = confidence >= 0.5

        # Severity mapping
        if confidence >= 0.8:
            severity = Severity.HIGH
        elif confidence >= 0.5:
            severity = Severity.MEDIUM
        else:
            severity = Severity.LOW

        # Return structured result
        return DetectionResult(
            is_injection=is_injection,
            confidence=confidence,
            severity=severity,
            reasons=[reason for reason, _ in matches]
        )

    def analyze(self, text: str) -> dict[str, object]:
        result = self.detect(text)
        return {
            "is_injection": result.is_injection,
            "confidence": result.confidence,
            "severity": result.severity.value,
            "reasons": result.reasons,
        }