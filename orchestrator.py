"""
Orchestrator module to coordinate input, LLM call, and output.
"""

from input_handler import get_input_prompt
from utils.llm_client import call_main_llm
from output_handler import print_model_output
from utils.GeminiTokenCounter import GeminiTokenCounter

# Ensure the project directory is on sys.path so local packages (like 'layers') can be imported
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from layers.prompt_compressing_layer import PromptCompressor
    
def main():
    compressor = PromptCompressor()     # instantiate class
    print("==> orchestrator.py started")
    print("==> main started")

    prompt = get_input_prompt()
    compressed_prompt_data = compressor.compress_prompt(prompt)
    output = call_main_llm(compressed_prompt_data["compressed_prompt"])
    print_model_output(output)

if __name__ == "__main__":
    main()
