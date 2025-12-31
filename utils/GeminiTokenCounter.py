import os
import time
from typing import List, Union

from dotenv import load_dotenv
from google import genai
from google.genai import types
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
# Gemini client
# --------------------------------------------------
client = genai.Client(api_key=GENAI_API_KEY)

class GeminiTokenCounter:
    def __init__(self, model: str = MODEL_MAIN):
        self.client = client
        self.model = model

    # -------------------------------
    # Model info
    # -------------------------------
    def print_model_limits(self):
        info = self.client.models.get(model=self.model)
        print("\n=== Model Context Window ===")
        print(f"Model: {self.model}")
        print(f"Input token limit: {info.input_token_limit}")
        print(f"Output token limit: {info.output_token_limit}")

    # -------------------------------
    # Text token count
    # -------------------------------
    def count_text(self, text: str):
        total = self.client.models.count_tokens(model=self.model, contents=text)
        print("\n=== Text Token Count ===")
        print(f"Text: {text[:80]}{'...' if len(text) > 80 else ''}")
        print(f"Total tokens: {total}")
        return total

    # -------------------------------
    # Chat token count
    # -------------------------------
    def count_chat(self, history: List[types.Content]):
        total = self.client.models.count_tokens(model=self.model, contents=history)
        print("\n=== Chat Token Count ===")
        print(f"Messages: {len(history)}")
        print(f"Total tokens: {total}")
        return total

    # -------------------------------
    # Generate content and print usage
    # -------------------------------
    def generate_with_usage(self, contents: Union[str, list]):
        response = self.client.models.generate_content(
            model=self.model, contents=contents
        )

        print("\n=== Generation Usage ===")
        print(response.usage_metadata)

        return response

    # -------------------------------
    # Image token count
    # -------------------------------
    def count_image(self, prompt: str, image_path: str):
        image = PIL.Image.open(image_path)
        total = self.client.models.count_tokens(
            model=self.model, contents=[prompt, image]
        )

        print("\n=== Image Token Count ===")
        print(f"Prompt: {prompt}")
        print(f"Image: {image_path}")
        print(f"Total tokens: {total}")

        return total

    # -------------------------------
    # Audio / Video token count
    # -------------------------------
    def count_media_file(self, prompt: str, file_path: str):
        uploaded = self.client.files.upload(file=file_path)

        while not uploaded.state or uploaded.state.name != "ACTIVE":
            print("Processing media...")
            time.sleep(3)
            uploaded = self.client.files.get(name=uploaded.name)

        total = self.client.models.count_tokens(
            model=self.model, contents=[prompt, uploaded]
        )

        print("\n=== Media Token Count ===")
        print(f"Prompt: {prompt}")
        print(f"File: {file_path}")
        print(f"Total tokens: {total}")

        return total
