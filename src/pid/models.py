import json
from dataclasses import dataclass
from enum import Enum
from typing import List


class Severity(Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class DetectionResult:
    is_injection: bool
    confidence: float
    severity: Severity
    reasons: List[str]

    def to_json(self) -> str:
        """Return a JSON-formatted string representation of the detection result."""
        return json.dumps({
            "is_injection": self.is_injection,
            "confidence": self.confidence,
            "severity": self.severity.value,
            "reasons": self.reasons
        }, indent=2)
