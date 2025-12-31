"""
RuleBasedCompressor
Performs deterministic text cleanup to reduce token count
without changing semantic meaning.
"""

import re

class RuleBasedCompressor:
    def compress(self, text: str) -> str:
        original_len = len(text.split())

        # Remove polite or redundant phrases
        text = re.sub(r"\b(please|kindly|could you|would you|I would like you to)\b", "", text, flags=re.I)
        text = re.sub(r"\b(make sure to|ensure that)\b", "ensure", text, flags=re.I)
        text = re.sub(r"\b(provide me with)\b", "provide", text, flags=re.I)
        text = re.sub(r"\s+", " ", text).strip()

        new_len = len(text.split())
        print(f"[RuleBasedCompressor] Words {original_len} → {new_len}")
        return text
