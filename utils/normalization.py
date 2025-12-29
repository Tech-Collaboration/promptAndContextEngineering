import re
import unicodedata
from enums.UnicodeMode import UnicodeMode
from enums.NormalizationPipeline import NormalizationPipeline


# Match letters repeated 3 or more times (e.g., "soooo", "coooool")
# Group captures the letter, \1{2,} means "repeat that same letter at least 2 more times"
ELONGATED_RE = re.compile(r"([a-zA-Z])\1{2,}")

# Match invisible Unicode characters that can affect matching but not appearance
# Includes zero-width space, joiner, non-joiner, and BOM
ZERO_WIDTH_RE = re.compile(r"[\u200B\u200C\u200D\uFEFF]")

# Match repeated emoji (or any high Unicode symbol) so we can collapse emoji storms
EMOJI_RE = re.compile(r"([\U00010000-\U0010ffff])\1+")

def normalize_unicode(txt: str, mode: UnicodeMode) -> str:
    """
    Normalize Unicode text into a standard form.
    NFC preserves character distinctions; NFKC collapses compatibility variants.
    """
    return unicodedata.normalize(mode.value, txt)

def normalize_elongation(txt: str) -> str:
    """
    Reduce exaggerated character repetition.
    Collapses 3+ repeated letters into 2 (soooo -> soo, coooool -> cool).
    Keeps legitimate double letters intact (cool, book).
    """
    return ELONGATED_RE.sub(r"\1\1", txt)

def remove_zero_width(txt: str) -> str:
    """
    Remove invisible Unicode characters that break string matching and can be used for obfuscation.
    """
    return ZERO_WIDTH_RE.sub("", txt)

def strip_combining_marks(txt: str) -> str:
    """
    Remove all Unicode combining marks (category Mn).
    This strips accents and Zalgo-style corruption.
    Use carefully if accents are semantically important.
    """
    return "".join(c for c in txt if unicodedata.category(c) != "Mn")

def normalize_punctuation(txt: str) -> str:
    """
    Collapse expressive punctuation:
    '!!!' -> '!'
    '???' -> '!'
    '......' -> '.'
    Multiple dashes -> '-'
    """
    txt = re.sub(r"!{2,}", "!", txt)
    txt = re.sub(r"\?{2,}", "?", txt)
    txt = re.sub(r"\.{3,}", ".", txt)
    txt = re.sub(r"[-—–]{2,}", "-", txt)
    return txt

def collapse_emoji(txt: str) -> str:
    """
    Reduce repeated emoji or symbols into a single instance.
    '😂😂😂' -> '😂', '🔥🔥' -> '🔥'
    Helps reduce token noise in informal text.
    """
    return EMOJI_RE.sub(r"\1", txt)

def normalize_text(txt: str, pipeline: NormalizationPipeline) -> str:
    """
    Run a predefined normalization pipeline on the input text.

    Pipelines:
    - LLM: aggressive normalization for model ingestion
    - STORAGE: minimal normalization for preserving fidelity
    - LIGHT: moderate cleanup for human-readable text
    """

    if pipeline == NormalizationPipeline.LLM:
        txt = normalize_unicode(txt, UnicodeMode.COMPATIBILITY)
        txt = remove_zero_width(txt)
        txt = strip_combining_marks(txt)
        txt = normalize_elongation(txt)
        txt = collapse_emoji(txt)
        txt = normalize_punctuation(txt)
        return txt

    elif pipeline == NormalizationPipeline.STORAGE:
        # Only normalize Unicode canonically, preserve all semantics
        return normalize_unicode(txt, UnicodeMode.CANONICAL)

    elif pipeline == NormalizationPipeline.LIGHT:
        txt = normalize_unicode(txt, UnicodeMode.CANONICAL)
        txt = remove_zero_width(txt)
        txt = normalize_elongation(txt)
        return txt

    else:
        raise ValueError(f"Unknown normalization pipeline: {pipeline}")

if __name__ == "__main__":
    text = """Sooooo coooool!!! I looooove this — reaaally 😄😄
        Here’s a fancy quote: “can’t”, and here is decomposed: can\u0301t  
        Café vs Cafe\u0301, naïve vs nai\u0308ve
        
        Zalgo text: H̴̲̬̯̍͌́e̶̞͂̎l̴͉̑̕l̵͕͗͘o̶̹̍̈́
        
        Legit doubles: cool, book, coffee, better, happy
        
        Elongated emotion: yesssss, noooooo, pleaaaseeee, goooood
        
        Mixed symbols: !!!!! ?????? ...... --- —— –
        
        Zero-width here: he​llo wo​rld (look carefully)
        
        Emoji storm: 😂😂😂🔥🔥🔥
        
        Accents:
        e\u0301 vs é
        o\u0308 vs ö
        a\u030a vs å
        
        Full-width text: Ｆｕｌｌｗｉｄｔｈ Ｔｅｘｔ １２３
        
        Random junk: asdjkl@@@### $$$$ %%%
        
        URLs and emails:
        https://example.com/test
        user.name+test@gmail.com
        
        End of teeeext.
    """

    with open('test/output.txt','w+') as f:

        f.write("\n===== ORIGINAL =====")
        f.write(text)

        f.write("\n===== LLM PIPELINE =====")
        llm_output = normalize_text(text, NormalizationPipeline.LLM)
        f.write(llm_output)

        f.write("\n===== LIGHT PIPELINE =====")
        light_output = normalize_text(text, NormalizationPipeline.LIGHT)
        f.write(light_output)

        f.write("\n===== STORAGE PIPELINE =====")
        storage_output = normalize_text(text, NormalizationPipeline.STORAGE)
        f.write(storage_output)


