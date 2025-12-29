"""
Gemini LLM client.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

GENAI_API_KEY = os.getenv("GENAI_API_KEY")
MODEL_MAIN = os.getenv("MODEL_MAIN")

if not GENAI_API_KEY:
    raise RuntimeError("GENAI_API_KEY not set in environment")

if not MODEL_MAIN:
    raise RuntimeError("MODEL_MAIN not set in environment")

# --------------------------------------------------
# Configure Gemini
# --------------------------------------------------
genai.configure(api_key=GENAI_API_KEY)

# Initialize model once
_model = genai.GenerativeModel(MODEL_MAIN)

def call_main_llm(prompt: str) -> str:
    response = _model.generate_content(prompt)
    return response.text.strip()
