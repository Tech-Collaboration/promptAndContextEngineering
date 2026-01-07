"""
RuleBasedCompressor
Performs deterministic, semantics-preserving normalization only.
"""

from utils.normalization import normalize_text_custom
from enums.unicode_mode import UnicodeMode


class RuleBasedCompressor:
    def __init__(
        self,
        *,
        normalization_config: dict | None = None,
    ):
        """
        :param normalization_config: Optional overrides passed to normalize_text_custom.
        """
        self.normalization_config = normalization_config or {}

    def compress(self, text: str) -> str:
        original_len = len(text.split())

        normalized = normalize_text_custom(
            text,
            unicode_mode=UnicodeMode.COMPATIBILITY,
            remove_zero_width_flag=True,
            strip_marks=True,
            normalize_elongation_flag=True,
            collapse_emoji_flag=True,
            normalize_punct_flag=True,
            normalize_whitespace_flag=True,
            alias_urls=False,
            alias_emails=False,
            alias_numbers=False,
            lowercase=False,
            **self.normalization_config,
        )

        new_len = len(normalized.split())
        print(f"[RuleBasedCompressor] Words {original_len} → {new_len}")

        return normalized
