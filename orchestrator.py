"""
Orchestrator module to coordinate input, compression, LLM call, and output.
Loads prompts from test_prompts.json and allows interactive selection.
"""

import sys
import json
from pathlib import Path

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from layers.prompt_compressing_layer import PromptCompressor
from utils.llm_client import call_main_llm
from output_handler import print_model_output


PROMPT_FILE = project_root / "test_prompts.json"


def load_prompts(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def choose_prompt(prompts: dict) -> list[str]:
    print("\nAvailable prompts:")
    for i, key in enumerate(prompts.keys(), 1):
        print(f"  {i}. {key}")

    print("\nEnter prompt number, name, or 'all':")
    choice = input("> ").strip()

    if choice.lower() == "all":
        return list(prompts.keys())

    # by index
    if choice.isdigit():
        idx = int(choice) - 1
        keys = list(prompts.keys())
        if 0 <= idx < len(keys):
            return [keys[idx]]
        else:
            raise ValueError("Invalid prompt number.")

    # by name
    if choice in prompts:
        return [choice]

    raise ValueError(f"Unknown selection: {choice}")


def main():
    print("==> orchestrator.py started")
    compressor = PromptCompressor(use_llm=True)

    prompts = load_prompts(PROMPT_FILE)
    print(f"Loaded {len(prompts)} prompts.")

    try:
        selected_keys = choose_prompt(prompts)
    except ValueError as e:
        print(f"Error: {e}")
        return

    for key in selected_keys:
        prompt = prompts[key]

        print(f"\n========== Processing {key} ==========")

        result = compressor.compress_prompt(prompt)

        print("\n== Compression Summary ==")
        print(f"Tokens before: {result.tokens_before}")
        print(f"Tokens after:  {result.tokens_after_final}")
        print(f"Savings:       {result.savings_pct}%")
        print(f"Input sim:     {round(result.input_similarity, 4)}")

        # output = call_main_llm(result.final_output)

        print("\n== Model Output ==")
        # print_model_output(output)

        print(f"\n========== Done {key} ==========\n")


if __name__ == "__main__":
    main()
