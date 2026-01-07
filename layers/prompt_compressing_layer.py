"""
PromptCompressor
Combines rule-based, Lingua, and LLM-based compression with token counting.
"""

import datetime
from compressors.rule_based_compression_layer import RuleBasedCompressor
from compressors.llm_compression import LLMCompressor
from compressors.lingua_compression_layer import LinguaCompressor
from utils.GeminiTokenCounter import GeminiTokenCounter
from evaluation.result import CompressionResult
from evaluation.similarity import semantic_similarity

print(">>> prompt_compressing_layer.py file loaded")

class PromptCompressor:
    def __init__(self, use_llm: bool = True, show_tokens: bool = True):
        print("[PromptCompressor] Initializing...")

        self.use_llm = use_llm
        self.show_tokens = show_tokens

        print("[PromptCompressor] Initializing RuleBasedCompressor...")
        self.rule = RuleBasedCompressor()

        print("[PromptCompressor] Initializing LLMCompressor...")
        self.llm = LLMCompressor()

        print("[PromptCompressor] Initializing LinguaCompressor...")
        self.lingua = LinguaCompressor()   # loads model lazily inside class

        print("[PromptCompressor] Initializing GeminiTokenCounter...")
        self.counter = GeminiTokenCounter()

        print("[PromptCompressor] Initialization complete.")


    def _count_tokens(self, text: str, label: str):
        """Wrapper to conditionally show token counts."""
        return self.counter.count_text(text, operation=label) if self.show_tokens else 0


    def compress_prompt(self, prompt_text: str) -> CompressionResult:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("\n🔹 Starting Compression Pipeline 🔹")

        # Stage 1 – Original
        tokens_before = self._count_tokens(prompt_text, "before compression")

        # Stage 2 – Rule-based cleanup
        rule_output = self.rule.compress(prompt_text)
        tokens_after_rule = self._count_tokens(rule_output, "after rule-based compression")

        # Stage 3 – Lingua compression
        lingua_output = self.lingua.compress(rule_output)
        tokens_after_lingua = self._count_tokens(lingua_output, "after lingua compression")

        # Stage 4 – Optional LLM rewrite
        if self.use_llm:
            final_output = self.llm.compress(lingua_output)
        else:
            final_output = lingua_output

        tokens_after_final = self._count_tokens(final_output, "after compression")

        savings = round(((tokens_before - tokens_after_final) / tokens_before) * 100, 2)

        input_sim = semantic_similarity(prompt_text, final_output)

        print(f"\n [PromptCompressor] Token reduction: {tokens_before} → {tokens_after_final} ({savings}% saved)\n")

        return CompressionResult(
            timestamp=timestamp,
            original_prompt=prompt_text,
            rule_output=rule_output,
            lingua_output=lingua_output,
            final_output=final_output,
            tokens_before=tokens_before,
            tokens_after_rule=tokens_after_rule,
            tokens_after_lingua=tokens_after_lingua,
            tokens_after_final=tokens_after_final,
            used_llm=self.use_llm,
            savings_pct=savings,
            input_similarity=input_sim,
        )
