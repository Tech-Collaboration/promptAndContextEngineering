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
    Rewrite or summarize a long instruction + content block more efficiently.
    - Detects and separates 'instruction' and 'content' sections.
    - Compresses only the content while preserving task context.
    """

    # 1️ Detect if the prompt has an instruction part
    split_marker = "Now, here is the text to summarize:"
    if split_marker in prompt:
        instruction, content = prompt.split(split_marker, 1)
        instruction = instruction.strip()
        content = content.strip()
    else:
        instruction, content = "", prompt.strip()

    # 2️ Build a more explicit system directive
    system_prompt = (
        "Your task is to compress and rewrite the TEXT CONTENT concisely "
        "while preserving its full meaning, structure, and key details. "
        "Do NOT rewrite or remove any meta-instructions. "
        "Only shorten the content below the separator.\n\n"
        "--- TEXT CONTENT START ---\n"
        f"{content}\n"
        "--- TEXT CONTENT END ---"
    )

    # 3️ Generate the rewritten text
    response = _model.generate_content([system_prompt])

    rewritten = response.text.strip()

    # 4️ Reattach instruction if present
    if instruction:
        return f"{instruction}\n\n{split_marker}\n{rewritten}"
    return rewritten