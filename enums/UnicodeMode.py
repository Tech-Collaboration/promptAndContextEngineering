from enum import Enum

class UnicodeMode(Enum):
    CANONICAL = "NFC"
    COMPATIBILITY = "NFKC"
