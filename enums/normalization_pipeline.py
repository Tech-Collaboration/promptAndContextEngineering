from enum import Enum

class NormalizationPipeline(Enum):
    LLM = "llm"
    STORAGE = "storage"
    LIGHT = "light"