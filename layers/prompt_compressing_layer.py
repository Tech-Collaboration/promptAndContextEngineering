"""
PromptCompressor
Combines rule-based and LLM-based compression with token counting.
"""

import datetime
from compressors.rule_based_compression_layer import RuleBasedCompressor
from compressors.llm_compression import LLMCompressor
from utils.GeminiTokenCounter import GeminiTokenCounter

class PromptCompressor:
    def __init__(self, use_llm: bool = True):
        self.use_llm = use_llm
        self.rule = RuleBasedCompressor()
        self.llm = LLMCompressor()
        self.counter = GeminiTokenCounter()

    def compress_prompt(self, prompt_text: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Count before
        tokens_before = self.counter.count_text(prompt_text)

        # Apply rule-based cleanup
        rule_output = self.rule.compress(prompt_text)

        # Optional LLM rewrite
        if self.use_llm:
            compressed_output = self.llm.compress(rule_output)
        else:
            compressed_output = rule_output

        # Count after
        tokens_after = self.counter.count_text(compressed_output)
        savings = round(((tokens_before - tokens_after) / tokens_before) * 100, 2)

        print(f"[PromptCompressor] Token reduction: {tokens_before} → {tokens_after} ({savings}% saved)")

        return {
            "timestamp": timestamp,
            "original_prompt": prompt_text,
            "compressed_prompt": compressed_output,
            "tokens_before": tokens_before,
            "tokens_after": tokens_after,
            "savings_pct": savings,
        }
