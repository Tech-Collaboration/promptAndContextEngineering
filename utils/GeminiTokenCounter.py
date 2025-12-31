import os
import time
from typing import List, Union

from dotenv import load_dotenv
import google.generativeai as genai
import PIL.Image

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
# Gemini configuration
# --------------------------------------------------
genai.configure(api_key=GENAI_API_KEY)


class GeminiTokenCounter:
    def __init__(self, model: str = MODEL_MAIN):
        self.model_name = model
        self.model = genai.GenerativeModel(model)

    # -------------------------------
    # Model info
    # -------------------------------
    def print_model_limits(self):
        info = genai.get_model(self.model_name)
        print("\n=== Model Context Window ===")
        print(f"Model: {self.model_name}")
        print(f"Input token limit : {info.input_token_limit}")
        print(f"Output token limit: {info.output_token_limit}")

    # -------------------------------
    # Text token count
    # -------------------------------
    def count_text(self, text: str):
        total = self.model.count_tokens(text)
        print("\n=== Text Token Count ===")
        print(f"Text: {text[:80]}{'...' if len(text) > 80 else ''}")
        print(f"Total tokens: {total.total_tokens}")
        return total.total_tokens

    # -------------------------------
    # Chat token count
    # -------------------------------
    def count_chat(self, history: List[dict]):
        total = self.model.count_tokens(history)
        print("\n=== Chat Token Count ===")
        print(f"Messages: {len(history)}")
        print(f"Total tokens: {total.total_tokens}")
        return total.total_tokens

    # -------------------------------
    # Generate content and print usage
    # -------------------------------
    def generate_with_usage(self, contents: Union[str, list]):
        response = self.model.generate_content(contents)
        print("\n=== Generation Usage ===")
        print(response.usage_metadata)
        return response

    # -------------------------------
    # Image token count
    # -------------------------------
    def count_image(self, prompt: str, image_path: str):
        image = PIL.Image.open(image_path)
        total = self.model.count_tokens([prompt, image])
        print("\n=== Image Token Count ===")
        print(f"Prompt: {prompt}")
        print(f"Image: {image_path}")
        print(f"Total tokens: {total.total_tokens}")
        return total.total_tokens

    # -------------------------------
    # Audio / Video token count
    # -------------------------------
    def count_media_file(self, prompt: str, file_path: str):
        uploaded = genai.upload_file(file_path)

        while not getattr(uploaded.state, "name", None) == "ACTIVE":
            print("Processing media...")
            time.sleep(3)
            uploaded = genai.get_file(uploaded.name)

        total = self.model.count_tokens([prompt, uploaded])
        print("\n=== Media Token Count ===")
        print(f"Prompt: {prompt}")
        print(f"File: {file_path}")
        print(f"Total tokens: {total.total_tokens}")
        return total.total_tokens
