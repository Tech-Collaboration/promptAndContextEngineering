"""
Orchestrator module to coordinate input, LLM call, and output.
"""

from input_handler import get_input_prompt
from utils.llm_client import call_main_llm
from output_handler import print_model_output
from utils.GeminiTokenCounter import GeminiTokenCounter

def main():
    counter = GeminiTokenCounter()     # instantiate class
    print("==> orchestrator.py started")
    print("==> main started")

    prompt = get_input_prompt()
    counter.count_text(prompt)
    output = call_main_llm(prompt)
    print_model_output(output)

if __name__ == "__main__":
    main()
