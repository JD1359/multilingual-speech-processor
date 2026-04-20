import speech_recognition as sr
import os


# Language name → BCP-47 language tag (used by Google Speech API)
LANGUAGE_MAP = {
    "english":    "en-US",
    "hindi":      "hi-IN",
    "kannada":    "kn-IN",
    "tamil":      "ta-IN",
    "telugu":     "te-IN",
    "spanish":    "es-ES",
    "french":     "fr-FR",
    "german":     "de-DE",
    "japanese":   "ja-JP",
    "chinese":    "zh-CN",
    "mandarin":   "zh-CN",
    "arabic":     "ar-SA",
    "portuguese": "pt-BR",
}


def get_language_tag(language: str) -> str:
    """
    Convert a human-readable language name to a BCP-47 tag.
    Falls back to 'en-US' if language is not found.
    """
    return LANGUAGE_MAP.get(language.lower().strip(), "en-US")


def speech_to_text_from_mic(language: str = "en", timeout: int = 5, phrase_limit: int = 10) -> str:
    """
    Listen to the microphone and convert speech to text.

    Args:
        language:     Language name or BCP-47 tag.
        timeout:      Seconds to wait for speech to start.
        phrase_limit: Max seconds to record a single phrase.

    Returns:
        Transcribed text string.

    Raises:
        sr.UnknownValueError:   If speech was not intelligible.
        sr.RequestError:        If Google API is unreachable.
        sr.WaitTimeoutError:    If no speech detected within timeout.
    """
    recognizer = sr.Recognizer()
    lang_tag = get_language_tag(language)

    # Calibrate for ambient noise before recording
    with sr.Microphone() as source:
        print("Calibrating for ambient noise... (1 second)")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print(f"Listening... Speak now [{lang_tag}]")

        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
        except sr.WaitTimeoutError:
            print("No speech detected within timeout.")
            return ""

    return _recognize(recognizer, audio, lang_tag)


def speech_to_text_from_file(file_path: str, language: str = "en") -> str:
    """
    Convert speech in an audio file to text.

    Args:
        file_path: Path to a .wav or .aiff audio file.
        language:  Language name or BCP-47 tag.

    Returns:
        Transcribed text string.

    Raises:
        FileNotFoundError: If the audio file does not exist.
        ValueError:        If the file format is not supported.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    recognizer = sr.Recognizer()
    lang_tag = get_language_tag(language)

    print(f"Loading audio file: {file_path}")

    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)

    return _recognize(recognizer, audio, lang_tag)


def _recognize(recognizer: sr.Recognizer, audio: sr.AudioData, lang_tag: str) -> str:
    """
    Internal helper — send audio to Google Web Speech API and return text.
    """
    try:
        print(f"Transcribing [{lang_tag}]...")
        text = recognizer.recognize_google(audio, language=lang_tag)
        print(f"Transcribed: {text}")
        return text

    except sr.UnknownValueError:
        print("Could not understand the audio. Please speak clearly.")
        return ""

    except sr.RequestError as e:
        print(f"Google API error: {e}")
        print("   Check your internet connection.")
        return ""


def list_supported_languages() -> dict:
    """Return the full language name → BCP-47 tag mapping."""
    return LANGUAGE_MAP


if __name__ == "__main__":
    # Quick mic test
    result = speech_to_text_from_mic(language="english")
    if result:
        print(f"\nResult: {result}")
