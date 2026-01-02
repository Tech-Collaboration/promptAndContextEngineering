@staticmethod 
def should_use_llm_rewrite(tokens_before, tokens_after_lingua, redundancy_factor=0.85):
    compression_ratio = tokens_after_lingua / tokens_before
    # If Lingua removed less than 15% → it's probably dense text
    # If Lingua removed >15% → it's verbose → use rewrite
    print(f"[conditionUtil] Compression ratio: {compression_ratio:.2f}")
    return compression_ratio > redundancy_factor
