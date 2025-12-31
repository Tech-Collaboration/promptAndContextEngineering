"""
Gemini LLM Compression Client
Uses a lightweight Gemini model (e.g., gemini-1.5-flash)
to rewrite prompts concisely without losing semantics.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key and configure
load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
MODEL_COMPRESSOR = os.getenv("MODEL_MAIN")

if not GENAI_API_KEY:
    raise RuntimeError("GENAI_API_KEY not set in environment")

genai.configure(api_key=GENAI_API_KEY)

# Create compression model
_model = genai.GenerativeModel(MODEL_COMPRESSOR)

def call_compression_llm(prompt: str) -> str:
    """
    Rewrite the given prompt concisely while preserving its meaning.
    """
    system_prompt = (
        "Rewrite the following prompt concisely without changing its meaning. "
        "Keep all constraints and key details intact."
    )
    response = _model.generate_content([system_prompt, prompt])
    return response.text.strip()
