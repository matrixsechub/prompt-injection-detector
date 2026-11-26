from dataclasses import dataclass


@dataclass
class DetectorConfig:
    threshold: float = 0.6
    enable_pattern_matching: bool = True
    enable_heuristics: bool = True
    enable_ml: bool = False
    max_text_length: int = 10000
    case_sensitive: bool = False

    def __post_init__(self) -> None:
        if not 0.0 <= self.threshold <= 1.0:
            raise ValueError("Threshold must be between 0.0 and 1.0")
        if self.max_text_length <= 0:
            raise ValueError("max_text_length must be positive")
