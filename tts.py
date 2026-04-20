from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
import tempfile

# Language name → gTTS language code mapping
LANGUAGE_MAP = {
    "english":    "en",
    "hindi":      "hi",
    "kannada":    "kn",
    "tamil":      "ta",
    "telugu":     "te",
    "spanish":    "es",
    "french":     "fr",
    "german":     "de",
    "japanese":   "ja",
    "chinese":    "zh",
    "mandarin":   "zh",
    "arabic":     "ar",
    "portuguese": "pt",
}


def get_language_code(language: str) -> str:
    """
    Convert a human-readable language name to a gTTS language code.
    Falls back to 'en' if language is not recognized.
    """
    return LANGUAGE_MAP.get(language.lower().strip(), language.lower())


def text_to_speech(text: str, language: str = "en", save_path: str = None) -> str:
    """
    Convert text to speech and either play it or save it to a file.

    Args:
        text:      The text to convert to speech.
        language:  Language name (e.g. 'hindi') or gTTS code (e.g. 'hi').
        save_path: Optional file path to save the .mp3. If None, plays immediately.

    Returns:
        Path to the saved audio file (temp file if save_path not provided).

    Raises:
        ValueError: If text is empty.
        Exception:  If gTTS API call fails (network issue or unsupported language).
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    lang_code = get_language_code(language)

    print(f"Converting to speech [{lang_code}]: {text[:60]}{'...' if len(text) > 60 else ''}")

    tts = gTTS(text=text, lang=lang_code, slow=False)

    # Save to provided path or a temp file
    if save_path:
        tts.save(save_path)
        output_path = save_path
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.save(tmp.name)
            output_path = tmp.name

    print(f"Audio saved to: {output_path}")

    # Auto-play if no save path was specified
    if not save_path:
        _play_audio(output_path)

    return output_path


def _play_audio(file_path: str):
    """Play an audio file using pydub."""
    try:
        audio = AudioSegment.from_mp3(file_path)
        play(audio)
    except Exception as e:
        print(f"Could not play audio automatically: {e}")
        print(f"   Open manually: {file_path}")


def list_supported_languages() -> dict:
    """Return the full language name → code mapping."""
    return LANGUAGE_MAP


if __name__ == "__main__":
    # Quick test
    text_to_speech("Hello! This is a test of the text to speech system.", language="en")
    text_to_speech("नमस्ते, आप कैसे हैं?", language="hindi")
