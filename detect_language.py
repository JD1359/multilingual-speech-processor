from langdetect import detect, detect_langs, LangDetectException


# langdetect code → human-readable name
LANG_CODE_TO_NAME = {
    "en": "English",
    "hi": "Hindi",
    "kn": "Kannada",
    "ta": "Tamil",
    "te": "Telugu",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ja": "Japanese",
    "zh-cn": "Chinese (Simplified)",
    "zh-tw": "Chinese (Traditional)",
    "ar": "Arabic",
    "pt": "Portuguese",
    "ru": "Russian",
    "ko": "Korean",
    "it": "Italian",
}

# Minimum confidence to trust the detection
CONFIDENCE_THRESHOLD = 0.70


def detect_language(text: str, fallback: str = "en") -> str:
    """
    Detect the language of the given text.

    Args:
        text:     Input text to detect.
        fallback: Language code to return if detection confidence is too low.

    Returns:
        Detected language code (e.g. 'en', 'hi', 'kn').
        Returns fallback if text is too short or confidence is below threshold.
    """
    if not text or len(text.strip()) < 5:
        print(f"Text too short for reliable detection. Using fallback: {fallback}")
        return fallback

    try:
        results = detect_langs(text)

        # Results are sorted by confidence (highest first)
        best = results[0]
        lang_code = best.lang
        confidence = best.prob

        print(f" Detected: {lang_code} (confidence: {confidence:.0%})")

        if confidence < CONFIDENCE_THRESHOLD:
            print(f"Confidence below {CONFIDENCE_THRESHOLD:.0%}. Using fallback: {fallback}")
            return fallback

        return lang_code

    except LangDetectException as e:
        print(f"Language detection failed: {e}. Using fallback: {fallback}")
        return fallback


def detect_language_name(text: str, fallback: str = "en") -> str:
    """
    Detect language and return its human-readable name.

    Returns:
        e.g. 'Hindi', 'English', 'Kannada'
    """
    code = detect_language(text, fallback)
    return LANG_CODE_TO_NAME.get(code, code.upper())


def detect_all_candidates(text: str) -> list:
    """
    Return all detected language candidates with confidence scores.

    Returns:
        List of dicts: [{'lang': 'en', 'confidence': 0.98}, ...]
    """
    if not text or len(text.strip()) < 5:
        return []

    try:
        results = detect_langs(text)
        return [
            {
                "lang": r.lang,
                "name": LANG_CODE_TO_NAME.get(r.lang, r.lang.upper()),
                "confidence": round(r.prob, 4)
            }
            for r in results
        ]
    except LangDetectException:
        return []


if __name__ == "__main__":
    tests = [
        "Hello, how are you doing today?",
        "नमस्ते, आप कैसे हैं?",
        "ನೀವು ಹೇಗಿದ್ದೀರಿ?",
        "Bonjour, comment allez-vous?",
        "こんにちは、お元気ですか？",
        "Hi",  # too short — should fall back
    ]

    for t in tests:
        print(f"\nText: {t}")
        name = detect_language_name(t)
        print(f"Language: {name}")
        candidates = detect_all_candidates(t)
        if candidates:
            print(f"All candidates: {candidates[:3]}")
