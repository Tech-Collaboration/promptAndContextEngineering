"""
Orchestrator module to coordinate input, LLM call, and output.
"""

from input_handler import get_input_prompt
from llm_client import call_main_llm
from output_handler import print_model_output

def main():
    print("==> orchestrator.py started")
    print("==> main started")

    prompt = get_input_prompt()
    output = call_main_llm(prompt)
    print_model_output(output)

if __name__ == "__main__":
    main()
