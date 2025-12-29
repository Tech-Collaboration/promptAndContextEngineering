import unicodedata
import re

#Normalize to NFC Form
def unicode_normalization(txt: str):
    return unicodedata.normalize('NFC', txt)

def elongated_word_normalization(txt: str):
    ELONGATED_RE = re.compile(r"([a-zA-Z])\1{2,}", re.IGNORECASE)
    return ELONGATED_RE.sub(r"\1\1", txt)


if __name__ == "main":
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

    unicodeNormalized = unicode_normalization(text)
    print(unicodeNormalized)

    elongatedWordNormalized = elongated_word_normalization(text)
    print(elongatedWordNormalized)

