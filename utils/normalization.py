import re
import unicodedata
from enums.unicode_mode import UnicodeMode
from enums.normalization_pipeline import NormalizationPipeline

# --- Regex patterns ---

# Matches letters repeated 3 or more times, e.g. "soooo" → captures "o"
ELONGATED_RE = re.compile(r"([a-zA-Z])\1{2,}")

# Matches invisible Unicode characters (zero-width space, joiner, non-joiner, BOM)
ZERO_WIDTH_RE = re.compile(r"[\u200B\u200C\u200D\uFEFF]")

# Matches repeated emoji or high Unicode symbols to collapse emoji storms
EMOJI_RE = re.compile(r"([\U00010000-\U0010ffff])\1+")

# Matches URLs (http(s) and www)
URL_RE = re.compile(r"https?://\S+|www\.\S+")

# Matches email addresses
EMAIL_RE = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")

# Matches long numeric sequences (IDs, phone numbers, etc.)
NUMBER_RE = re.compile(r"\b\d{3,}\b")


# --- Normalization primitives ---

def normalize_unicode(txt: str, mode: UnicodeMode) -> str:
    """
    Normalize Unicode text to a canonical or compatibility form (NFC / NFKC).
    This reduces visually identical but binary-distinct representations.
    """
    return unicodedata.normalize(mode.value, txt)


def remove_zero_width(txt: str) -> str:
    """
    Remove invisible Unicode characters that affect tokenization and matching
    but are not visible to the user (can be used for obfuscation).
    """
    return ZERO_WIDTH_RE.sub("", txt)


def strip_combining_marks(txt: str) -> str:
    """
    Remove Unicode combining marks (category Mn), which strips accents and Zalgo noise.
    Use carefully if accents are semantically meaningful for your use case.
    """
    return "".join(c for c in txt if unicodedata.category(c) != "Mn")


def normalize_elongation(txt: str) -> str:
    """
    Collapse exaggerated letter repetition:
    'soooo' → 'soo', while preserving legitimate doubles like 'cool' or 'book'.
    """
    return ELONGATED_RE.sub(r"\1\1", txt)


def collapse_emoji(txt: str) -> str:
    """
    Reduce repeated emoji or symbols into a single instance:
    '😂😂😂' → '😂'. Helps reduce token noise in informal text.
    """
    return EMOJI_RE.sub(r"\1", txt)


def normalize_punctuation(txt: str) -> str:
    """
    Normalize expressive punctuation:
    '!!!' → '!', '????' → '?', '......' → '.', long dashes → '-'.
    """
    txt = re.sub(r"!{2,}", "!", txt)
    txt = re.sub(r"\?{2,}", "?", txt)
    txt = re.sub(r"\.{3,}", ".", txt)
    txt = re.sub(r"[-—–]{2,}", "-", txt)
    return txt


def normalize_whitespace(txt: str) -> str:
    """
    Collapse multiple whitespace characters into a single space and trim edges.
    """
    return re.sub(r"\s+", " ", txt).strip()


def alias_urls_emails_numbers(txt: str) -> str:
    """
    Replace URLs, emails, and long numeric sequences with placeholder tokens
    (<URL>, <EMAIL>, <NUM>) to reduce token variance while preserving semantics.
    """
    txt = URL_RE.sub("<URL>", txt)
    txt = EMAIL_RE.sub("<EMAIL>", txt)
    txt = NUMBER_RE.sub("<NUM>", txt)
    return txt


# --- Main pipeline ---

def normalize_text(
    txt: str,
    pipeline: NormalizationPipeline,
    *,
    alias_urls: bool = True,
    alias_emails: bool = True,
    alias_numbers: bool = False,
    lowercase: bool = False,
) -> str:
    """
    Normalize text according to a predefined pipeline.

    Pipelines:
    - LLM: aggressive normalization for LLM ingestion and token efficiency
    - LIGHT: gentle cleanup for human readability
    - STORAGE: canonical Unicode only, preserve original semantics as much as possible
    """

    if pipeline == NormalizationPipeline.LLM:
        txt = normalize_unicode(txt, UnicodeMode.COMPATIBILITY)
        txt = remove_zero_width(txt)
        txt = strip_combining_marks(txt)
        txt = normalize_elongation(txt)
        txt = collapse_emoji(txt)
        txt = normalize_punctuation(txt)
        txt = normalize_whitespace(txt)

        if alias_urls or alias_emails or alias_numbers:
            txt = alias_urls_emails_numbers(txt)

        return txt

    elif pipeline == NormalizationPipeline.LIGHT:
        txt = normalize_unicode(txt, UnicodeMode.CANONICAL)
        txt = remove_zero_width(txt)
        txt = normalize_elongation(txt)
        txt = normalize_whitespace(txt)

        if lowercase:
            txt = txt.lower()

        return txt

    elif pipeline == NormalizationPipeline.STORAGE:
        return normalize_unicode(txt, UnicodeMode.CANONICAL)

    else:
        raise ValueError(f"Unknown normalization pipeline: {pipeline}")

def normalize_text_custom(
    txt: str,
    *,
    unicode_mode: UnicodeMode = UnicodeMode.CANONICAL,
    remove_zero_width_flag: bool = True,
    strip_marks: bool = False,
    normalize_elongation_flag: bool = True,
    collapse_emoji_flag: bool = True,
    normalize_punct_flag: bool = True,
    normalize_whitespace_flag: bool = True,
    alias_urls: bool = False,
    alias_emails: bool = False,
    alias_numbers: bool = False,
    lowercase: bool = False,
) -> str:
    """
    User-configurable normalization pipeline for LLM-safe prompt cleanup.
    All operations are semantics-preserving.
    """

    txt = normalize_unicode(txt, unicode_mode)

    if remove_zero_width_flag:
        txt = remove_zero_width(txt)

    if strip_marks:
        txt = strip_combining_marks(txt)

    if normalize_elongation_flag:
        txt = normalize_elongation(txt)

    if collapse_emoji_flag:
        txt = collapse_emoji(txt)

    if normalize_punct_flag:
        txt = normalize_punctuation(txt)

    if normalize_whitespace_flag:
        txt = normalize_whitespace(txt)

    if alias_urls or alias_emails or alias_numbers:
        txt = alias_urls_emails_numbers(txt)

    if lowercase:
        txt = txt.lower()

    return txt




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

    with open('test/output.txt', 'w+') as f:
        f.write("\n===== ORIGINAL =====")
        f.write(text)

        f.write("\n===== LLM PIPELINE =====\n")
        llm_output = normalize_text(text, NormalizationPipeline.LLM)
        f.write(llm_output)

        f.write("\n===== LIGHT PIPELINE =====\n")
        light_output = normalize_text(text, NormalizationPipeline.LIGHT)
        f.write(light_output)

        f.write("\n===== STORAGE PIPELINE =====\n")
        storage_output = normalize_text(text, NormalizationPipeline.STORAGE)
        f.write(storage_output)

        f.write("\n===== Custom Defaukt PIPELINE =====\n")
        cleaned = normalize_text_custom(
            text,
            unicode_mode=UnicodeMode.COMPATIBILITY,
            remove_zero_width_flag=True,
            strip_marks=True,
            normalize_elongation_flag=True,
            collapse_emoji_flag=True,
            normalize_punct_flag=True,
            normalize_whitespace_flag=True,
            alias_emails=True,
            lowercase=False,
        )
        f.write(cleaned)

