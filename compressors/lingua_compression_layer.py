"""
LLM-Lingua Compression Layer
----------------------------
Performs token-importance-based compression using Microsoft's LLMLingua.
This is extractive (not generative) pruning — keeps the most important parts
of the prompt based on model scoring.
"""

import sys
from llmlingua import PromptCompressor
from utils.GeminiTokenCounter import GeminiTokenCounter
print(">>> lingua_compression_layer.py file loaded")

class LinguaCompressor:
    def __init__(self, model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0", ratio: float = 0.5):
        self.model_name = model_name
        self.ratio = ratio
        self.available = False
        self.compressor = None
        self.counter = GeminiTokenCounter()

    def _load(self):
        if self.compressor:
            return
        try:
            print(f"[Lingua] Loading {self.model_name} on CPU...")
            self.compressor = PromptCompressor(
                model_name=self.model_name,
                device_map="cpu",
                model_config={
                                "torch_dtype": "float32",
                                "low_cpu_mem_usage": True
            }
            )
            self.available = True
            print(f"[Lingua] Ready (target ratio={self.ratio})")
        except Exception as e:
            print(f"[Lingua] Error loading model: {e}", file=sys.stderr)
            self.available = False

    def compress(self, text: str) -> str:
        if not self.available:
            self._load()
        if not self.available:
            return text
        try:
            compressed_result = self.compressor.compress_prompt(text)
            # New API returns a dict
            if isinstance(compressed_result, dict):
                compressed = compressed_result.get("compressed_prompt", text)
            else:
                compressed = compressed_result

            before = self.counter.count_text(text, ("before Lingua compression"))
            after = self.counter.count_text(compressed, ("after Lingua compression"))
            print(f"[Lingua] Compressed {before} → {after} tokens ({round((before - after) / before * 100, 2)}% saved)")
            return compressed
        except Exception as e:
            print(f"[Lingua] Error during compression: {e}", file=sys.stderr)
            return text

