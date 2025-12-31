"""
LLMCompressor
Handles prompt compression using a smaller Gemini model.
"""

from utils.llm_compression_client import call_compression_llm

class LLMCompressor:
    def compress(self, text: str) -> str:
        compressed = call_compression_llm(text)
        print(f"[LLMCompressor] Compressed from {len(text.split())} → {len(compressed.split())} words")
        return compressed
