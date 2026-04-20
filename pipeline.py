from stt import speech_to_text_from_mic, speech_to_text_from_file
from tts import text_to_speech
from detect_language import detect_language, detect_language_name


def run_pipeline(
    input_language: str = "auto",
    output_language: str = "en",
    source: str = "mic",
    audio_file: str = None,
    save_output: str = None
) -> dict:
    """
    Full speech processing pipeline.

    Args:
        input_language: Language of the spoken input ('auto' for auto-detect).
        output_language: Language for the TTS output (default: English).
        source:          'mic' for microphone, 'file' for audio file.
        audio_file:      Path to audio file (required if source='file').
        save_output:     Optional path to save the output .mp3.

    Returns:
        dict with keys: 'transcribed_text', 'detected_language', 'output_language'
    """
    result = {
        "transcribed_text": "",
        "detected_language": input_language,
        "output_language": output_language,
    }

    # ── Step 1: Speech to Text ──────────────────────────────────────────────
    print("\n" + "─" * 50)
    print("STEP 1: Speech Recognition")
    print("─" * 50)

    if source == "file" and audio_file:
        text = speech_to_text_from_file(audio_file, language=input_language)
    else:
        listen_lang = "en" if input_language == "auto" else input_language
        text = speech_to_text_from_mic(language=listen_lang)

    if not text:
        print("No text recognized. Pipeline stopped.")
        return result

    result["transcribed_text"] = text

    # ── Step 2: Language Detection ──────────────────────────────────────────
    if input_language == "auto":
        print("\n" + "─" * 50)
        print("STEP 2: Language Detection")
        print("─" * 50)

        detected_code = detect_language(text)
        detected_name = detect_language_name(text)
        result["detected_language"] = detected_code

        print(f"Input language: {detected_name} ({detected_code})")
    else:
        print(f"\nInput language (specified): {input_language}")

    # ── Step 3: Text to Speech ──────────────────────────────────────────────
    print("\n" + "─" * 50)
    print(f"STEP 3: Text-to-Speech → Output in [{output_language}]")
    print("─" * 50)

    audio_path = text_to_speech(text, language=output_language, save_path=save_output)
    result["audio_output_path"] = audio_path

    print("\nPipeline complete!")
    print(f"   Input:  {text}")
    print(f"   Output: {audio_path}")

    return result


if __name__ == "__main__":
    # Run with auto language detection, output in English
    run_pipeline(
        input_language="auto",
        output_language="en",
        source="mic"
    )
