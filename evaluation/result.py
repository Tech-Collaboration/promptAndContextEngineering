from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class CompressionResult:
    timestamp: str
    original_prompt: str
    rule_output: str
    lingua_output: str
    final_output: str

    tokens_before: int
    tokens_after_rule: int
    tokens_after_lingua: int
    tokens_after_final: int

    used_llm: bool
    savings_pct: float

    input_similarity: Optional[float] = None
    output_similarity: Optional[float] = None
    metadata: Dict = None
