"""
Multilingual translator + romanizer (cleaned, commented)

Recommended installs for best results:
pip install langid deep-translator pykakasi pypinyin transliterate hangul-romanize

Notes:
- langid is used for detection (more stable than langdetect).
- deep-translator.GoogleTranslator does translation (source='auto').
- Some libraries (hangul-romanize, transliterate) are optional; script falls back gracefully.
- Urdu romanization uses an extended manual dictionary + character mapping for readable output.
"""
try:
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate
except Exception:
    transliterate = None
    sanscript = None

import langid
from deep_translator import GoogleTranslator

# optional libs (we try to import; if missing, we fall back gracefully)
try:
    import pykakasi  # Japanese -> romaji
except Exception:
    pykakasi = None

try:
    from pypinyin import lazy_pinyin  # Chinese -> pinyin
except Exception:
    lazy_pinyin = None

try:
    from transliterate import translit, get_available_language_codes  # Russian/Greek etc.
except Exception:
    translit = None
    get_available_language_codes = lambda: []

try:
    from hangul_romanize import Transliter
    from hangul_romanize.rule import academic
    korean_trans = Transliter(academic)
except Exception:
    korean_trans = None


import re

def clean_hinglish(itrans_text: str) -> str:
    """
    Convert academic-style romanization (Harvard-Kyoto/ITRANS) into
    smoother Hinglish (WhatsApp style).
    """
    text = itrans_text

    # Remove weird diacritics and over-markings
    text = text.replace(".N", "n").replace("M", "n").replace("~N", "n")
    text = text.replace(".a", "a").replace(".i", "i").replace(".u", "u")
    text = text.replace(".r", "r")

    replacements = {
        "maiM": "main",
        "tumase": "tumse",
        "pyAra": "pyaar",
        "karatA": "karta",
        "hU.n": "hoon",
        "hU.N": "hoon",
        "tumheM": "tumhe",
        "yAda": "yaad",
        "mujhe": "mujhe",
        "pUrA": "poora",
        "yakIna": "yakeen",
        "tuma": "tum",
        "aisA": "aisa",
        "karate": "karte"
    }
    for k, v in replacements.items():
        text = re.sub(r"\b" + re.escape(k) + r"\b", v, text)

    text = text.lower()
    text = re.sub(r"aa+", "aa", text)
    text = re.sub(r"ii+", "i", text)
    text = re.sub(r"uu+", "u", text)

    return text.strip()


# -------------------------
# LANGUAGE NAME -> CODE MAP
# Accepts both names and short codes
# -------------------------
LANG_MAP = {
    'english': 'en', 'en': 'en',
    'hindi': 'hi', 'hi': 'hi',
    'japanese': 'ja', 'ja': 'ja',
    'korean': 'ko', 'ko': 'ko',
    'spanish': 'es', 'es': 'es',
    'french': 'fr', 'fr': 'fr',
    'turkish': 'tr', 'tr': 'tr',
    'Dutch': 'nl', 'nl': 'nl',
    'german': 'de', 'de': 'de',
    'russian': 'ru', 'ru': 'ru',
    'italian': 'it', 'it': 'it',
    'chinese': 'zh-CN', 'zh': 'zh-CN', 'zh-cn': 'zh-CN', 'zh-tw': 'zh-TW',
    'latin': 'la', 'la': 'la',
    # 'cyrillic' is not a language; map to 'ru' as a practical proxy where needed
    'cyrillic': 'ru', 'sr': 'sr'
}

def normalize_target_lang(inp: str) -> str:
    """Return the translation target language code expected by GoogleTranslator."""
    if not inp:
        return 'en'
    key = inp.strip().lower()
    return LANG_MAP.get(key, key)

# -------------------------
# Urdu transliteration helpers (improved dictionary + char fallback)
# -------------------------
# Word-level replacements: common words/phrases to correct human-readable roman Urdu
URDU_WORD_MAP = {
    # Pronouns
    "میں": "main", "تم": "tum", "آپ": "aap", "ہم": "hum",
    "وہ": "woh", "یہ": "yeh", "وہاں": "wahan", "یہاں": "yahan",
    "میرا": "mera", "میری": "meri", "میرے": "mere",
    "ہمارا": "hamara", "ہماری": "hamari", "ہمارے": "hamare",

    # Greetings & basics
    "سلام": "salaam", "ہیلو": "hello", "ہائے": "hi",
    "کیسے": "kaise", "ہوں": "hoon", "ہے": "hai", "ہیں": "hain",
    "ہاں": "haan", "نہیں": "nahin", "ٹھیک": "theek",

    # Common verbs
    "کرنا": "karna", "کرتا": "karta", "کرتی": "karti",
    "جانا": "jana", "جاتا": "jata", "جاتی": "jati",
    "کھانا": "khana", "پینا": "peena", "سونا": "sona",
    "دیکھنا": "dekhna", "آنا": "aana", "دینا": "dena", "لینا": "lena",

    # Time & daily
    "آج": "aaj", "کل": "kal", "اب": "ab", "پھر": "phir",
    "صبح": "subah", "شام": "shaam", "رات": "raat", "دن": "din",
    "ہفتہ": "hafta", "مہینہ": "mahina", "سال": "saal",

    # Feelings
    "پیار": "pyaar", "محبت": "mohabbat", "خوشی": "khushi",
    "غم": "gham", "زندگی": "zindagi", "دل": "dil",
    "دنیا": "duniya", "اللہ": "Allah", "انسان": "insaan",

    # Numbers (1–10)
    "ایک": "ek", "دو": "do", "تین": "teen", "چار": "chaar", "پانچ": "paanch",
    "چھ": "chhay", "سات": "saat", "آٹھ": "aath", "نو": "nau", "دس": "das",

    # OTHERS
    "ٹکنالوجی" : "Technology",
    "ٹول" : "tool",
    "باکس" :"box", "خلا" : "space",
    
}

# Character-level mapping fallback (better than nothing)
URDU_CHAR_MAP = {
    'ا': 'a', 'آ': 'aa',
    'ب': 'b', 'پ': 'p',
    'ت': 't', 'ٹ': 't',
    'ث': 's',
    'ج': 'j', 'چ': 'ch',
    'ح': 'h', 'خ': 'kh',
    'د': 'd', 'ڈ': 'd',
    'ذ': 'z',
    'ر': 'r', 'ڑ': 'r',
    'ز': 'z', 'ژ': 'zh',
    'س': 's', 'ش': 'sh',
    'ص': 's', 'ض': 'z',
    'ط': 't', 'ظ': 'z',
    'ع': "'", 'غ': 'gh',
    'ف': 'f',
    'ق': 'q',
    'ک': 'k', 'گ': 'g',
    'ل': 'l',
    'م': 'm',
    'ن': 'n', 'ں': 'n',
    'و': 'o', 'ؤ': 'o',
    'ہ': 'h', 'ھ': 'h',
    'ی': 'y', 'ے': 'e', 'ئ': 'i',
    'ء': "'", 'ٓ': '', 'ٔ': '',
}


def romanize_urdu_text(text: str) -> str:
    """
    Smart-ish romanization for Urdu:
    - Try word replacements first (gives natural results for common words)
    - Then fall back to character mapping for remaining characters
    """
    # Normalize spacing (split by whitespace)
    words = text.split()
    out_words = []
    for w in words:
        # exact-word map
        if w in URDU_WORD_MAP:
            out_words.append(URDU_WORD_MAP[w])
            continue
        # punctuation-aware: strip common punctuation, map, then reattach
        prefix = ''
        suffix = ''
        core = w
        # preserve punctuation at start/end
        while core and not core[0].isalnum():
            prefix += core[0]; core = core[1:]
        while core and not core[-1].isalnum():
            suffix = core[-1] + suffix; core = core[:-1]
        if not core:
            out_words.append(prefix + suffix)
            continue
        # if whole core in dict
        if core in URDU_WORD_MAP:
            out_words.append(prefix + URDU_WORD_MAP[core] + suffix)
            continue
        # else character-by-character
        roman = []
        for ch in core:
            roman.append(URDU_CHAR_MAP.get(ch, ch))
        out_words.append(prefix + ''.join(roman) + suffix)
    return ' '.join(out_words)

# -------------------------
# Arabic & Persian simple transliteration map (readable approximate)
# These are crude but produce human-readable ascii text (not perfect IPA)
# -------------------------
ARABIC_CHAR_MAP = {
    'ا': 'a', 'ب': 'b', 'ت': 't', 'ث': 'th', 'ج': 'j', 'ح': 'h', 'خ': 'kh',
    'د': 'd', 'ذ': 'dh', 'ر': 'r', 'ز': 'z', 'س': 's', 'ش': 'sh', 'ص': 's',
    'ض': 'd', 'ط': 't', 'ظ': 'z', 'ع': "'", 'غ': 'gh', 'ف': 'f', 'ق': 'q',
    'ک': 'k', 'گ': 'g', 'ل': 'l', 'م': 'm', 'ن': 'n', 'و': 'u', 'ه': 'h',
    'ی': 'y', 'ء': "'", 'أ': 'a', 'إ': 'i', 'ؤ': 'u', 'ئ': 'i', 'ى': 'a',
    'آ': 'aa', 'ة': 'a', 'چ':'che', 'ي' : 'i', 'ك' : 'ek', 'پ' :'p',
}

def romanize_arabic_like(text: str) -> str:
    """Rough transliteration for Arabic/Persian script to readable ASCII."""
    out = []
    for ch in text:
        out.append(ARABIC_CHAR_MAP.get(ch, ch))
    return ''.join(out)

# Hindi Romanization

HINDI_WORD_MAP = {
    # Pronouns
    "मैं": "main", "तुम": "tum", "आप": "aap", "हम": "hum",
    "वह": "vah", "ये": "ye", "यह": "yeh", "वे": "ve",
    "मेरा": "mera", "मेरी": "meri", "मेरे": "mere",
    "हमारा": "hamara", "हमारी": "hamari", "हमारे": "hamare",

    # Greetings & basics
    "नमस्ते": "namaste", "शुभ": "shubh", "प्रणाम": "pranam",
    "कैसे": "kaise", "हो": "ho", "हूँ": "hoon", "हैं": "hain", "है": "hai",
    "हाँ": "haan", "नहीं": "nahin", "ठीक": "theek",

    # Common verbs
    "करना": "karna", "करते": "karte", "करती": "kartii", "कर": "kar",
    "जाना": "jana", "जाता": "jata", "जाती": "jati",
    "खाना": "khana", "पीना": "peena", "सोना": "sona",
    "देखना": "dekhna", "आना": "aana", "देना": "dena", "लेना": "lena",

    # Time & daily
    "आज": "aaj", "कल": "kal", "अब": "ab", "फिर": "phir",
    "सुबह": "subah", "शाम": "shaam", "रात": "raat", "दिन": "din",
    "सप्ताह": "saptah", "महीना": "mahina", "साल": "saal",

    # Feelings
    "प्यार": "pyaar", "प्रेम": "prem", "खुशी": "khushi",
    "दुख": "dukh", "जीवन": "jeevan", "दिल": "dil",
    "दुनिया": "duniya", "भगवान": "bhagwan",

    # Numbers (1–10)
    "एक": "ek", "दो": "do", "तीन": "teen", "चार": "chaar", "पांच": "paanch",
    "छह": "chhah", "सात": "saat", "आठ": "aath", "नौ": "nau", "दस": "das",
}

HINDI_CHAR_MAP = {
    # Vowels
    'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ee',
    'उ': 'u', 'ऊ': 'oo', 'ऋ': 'ri', 'ॠ': 'ri',
    'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
    'ॐ': 'om',

    # Consonants
    'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'n',
    'च': 'ch', 'छ': 'chh', 'ज': 'j', 'झ': 'jh', 'ञ': 'n',
    'ट': 't', 'ठ': 'th', 'ड': 'd', 'ढ': 'dh', 'ण': 'n',
    'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
    'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm',
    'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v',

    # Sibilants + aspirates
    'श': 'sh', 'ष': 'sh', 'स': 's', 'ह': 'h',

    # Conjuncts / special
    'क्ष': 'ksh', 'त्र': 'tr', 'ज्ञ': 'gy',

    # Nukta letters (borrowed sounds)
    'क़': 'q', 'ख़': 'kh', 'ग़': 'gh', 'ज़': 'z', 'ड़': 'r', 'ढ़': 'rh',
    'फ़': 'f', 'झ़': 'zh',

    # Signs / diacritics
    'ं': 'n', 'ँ': 'n', 'ः': 'h', '़': '', '्': '',
    'ौ': 'au', 'ै': 'ai', 'ॉ': 'o', 'ॆ': 'e', 'ॊ': 'o',
}

def romanize_hindi_text(text: str) -> str:
    """
    Romanization for Hindi:
    - Check HINDI_WORD_MAP first
    - Else use character-by-character mapping
    """
    words = text.split()
    out_words = []
    for w in words:
        if w in HINDI_WORD_MAP:
            out_words.append(HINDI_WORD_MAP[w])
            continue
        roman = []
        for ch in w:
            roman.append(HINDI_CHAR_MAP.get(ch, ch))
        out_words.append(''.join(roman))
    return ' '.join(out_words)
# -------------------------
# Rome/romanize dispatcher
# -------------------------
def romanize_text(text: str, lang_code: str) -> str:
    """
    Return a romanized/transliterated version of text according to lang_code.
    Falls back to reasonable defaults if optional libs aren't installed.
    """
    if not text:
        return text

    # Normalize code forms
    lc = (lang_code or '').lower()

    # Japanese -> using pykakasi if available
    # Japanese -> romaji using new pykakasi API
    if lc.startswith('ja') or lc == 'japanese':
        if pykakasi:
           kakasi = pykakasi.kakasi()
           result = kakasi.convert(text)
           return " ".join([item['hepburn'] for item in result])
        else:
           return text
  # no pykakasi: return original

    # Chinese -> pinyin
    if lc.startswith('zh'):
        if lazy_pinyin:
            try:
                return ' '.join(lazy_pinyin(text))
            except Exception:
                return text
        return text

    # Korean -> hangul-romanize if available
    if lc.startswith('ko') or lc == 'korean':
        if korean_trans:
            try:
                return korean_trans.translit(text)
            except Exception:
                return text
        return text

    # Urdu -> our improved dictionary-based romanizer
    if lc == 'ur' or lc == 'urdu':
        return romanize_urdu_text(text)

    # Hindi -> try transliterate library (Devanagari -> Latin)
    if lc == 'hi' or lc == 'hindi':
       if transliterate and sanscript:
          try:
              raw = transliterate(text, sanscript.DEVANAGARI, sanscript.ITRANS)
              return clean_hinglish(raw)  # 👈 scrub output into Hinglish
          except Exception:
              return romanize_hindi_text(text)  # fallback
       else:
          return romanize_hindi_text(text)
  
    # Arabic / Persian -> our simple char-map fallback
    if lc in ('ar', 'arabic', 'fa', 'persian', 'farsi'):
        return romanize_arabic_like(text)

    # Russian / Serbian / other cyrillic -> transliterate if available
    if lc in ('ru', 'sr', 'cyrillic', 'russian'):
        if translit:
            try:
                return translit(text, 'ru', reversed=True)
            except Exception:
                return text
        return text

    # Greek
    if lc in ('el', 'greek'):
        if translit:
            try:
                return translit(text, 'el', reversed=True)
            except Exception:
                return text
        return text

    # Latin-based languages: return as-is (already readable)
    if lc in ('en', 'fr', 'es', 'it', 'la', 'de', 'pt', 'spanish', 'french', 'italian', 'latin'):
        return text

    # Default fallback: return original
    return text

# -------------------------
# Language detection with confidence and ASCII-short-text fallback
# -------------------------
def detect_language_safely(text: str) -> str:
    """
    Use langid to classify language. If confidence is low and text is ASCII,
    assume English. This cuts down on strange short-text misclassifications.
    """
    if not text or not text.strip():
        return 'unknown'
    lang, conf = langid.classify(text)
    # if confidence low and text is mostly ASCII letters/punct, prefer English
    if conf < 0.90:
        # if all characters are ASCII and many English-looking words, assume en
        num_ascii = sum(1 for ch in text if ord(ch) < 128)
        if num_ascii / max(1, len(text)) > 0.9:
            # simple heuristic: presence of common English words
            lowers = text.lower()
            english_signals = ['the ', ' and ', ' how ', ' you', ' is ', ' are ', ' hello', ' hi ']
            if any(sig in lowers for sig in english_signals):
                return 'en'
    return lang

# -------------------------
# Main translate + romanize
# -------------------------
def translate_and_romanize(text: str, target_lang_code: str):
    """
    - Detect source language (safe)
    - Translate using GoogleTranslator (deep-translator)
    - Romanize translated text if needed according to target_lang_code
    Returns (src_lang, translated_text, romanized_text)
    """
    src = detect_language_safely(text)
    # Use normalized target lang (e.g., 'urdu' -> 'ur')
    tgt = normalize_target_lang(target_lang_code)

    try:
        translated = GoogleTranslator(source='auto', target=tgt).translate(text)
    except Exception as e:
        translated = f"(translation error: {e})"

    roman = romanize_text(translated, tgt)
    return src, translated, roman

# -------------------------
# CLI loop
# -------------------------
def prompt_loop():
    print("Multilingual translator — supports: urdu, japanese, persian, chinese, english, russian, latin, french, spanish, italian, korean, arabic, hindi, cyrillic, greek.")
    print("Type text, choose a target language (name or code). Libraries optional; script will try fallbacks.")
    while True:
        text = input("\nEnter text: ").strip()
        if not text:
            print("No text entered. Try again.")
            continue

        target_input = input("Translate into which language (name or code, e.g. 'ur' or 'Russian'): ").strip()
        if not target_input:
            target_input = 'en'
        src_lang, translated, roman = translate_and_romanize(text, target_input)

        print(f"\nDetected Language (heuristic): {src_lang}")
        print(f"Translated ({normalize_target_lang(target_input)}): {translated}")
        print(f"Romanized: {roman}\n")

        again = input("Do you want to translate more? (yes/no): ").strip().lower()
        if again not in ('yes', 'y'):
            print("Exiting translator. Bye.")
            break


from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
# React build path
REACT_BUILD_DIR = os.path.join(os.path.dirname(__file__), "../translator-ui/build")

app = Flask(__name__, static_folder=REACT_BUILD_DIR, static_url_path="/")
CORS(app)

# Serve React frontend
@app.route("/")
def serve_react():
    return send_from_directory(app.static_folder, "index.html")

# API endpoint
@app.route("/api/translate", methods=["POST"])
def translate_api():
    data = request.get_json()
    text = data.get("text", "")
    target = data.get("target", "en")

    if not text.strip():
        return jsonify({
            "source_lang": "-",
            "translated": "",
            "romanized": ""
        })

    src_lang, translated, romanized = translate_and_romanize(text, target)

    return jsonify({
        "source_lang": src_lang,
        "translated": translated,
        "romanized": romanized
    })

# For React Router — serve index.html for all other paths
@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True)
