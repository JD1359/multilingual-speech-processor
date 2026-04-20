"""
main.py — CLI Entry Point
Multilingual Speech Processor — STT / TTS / Auto-detect Pipeline

Usage:
  python main.py --mode stt --lang english
  python main.py --mode tts --text "Hello world" --lang hindi
  python main.py --mode tts --text "नमस्ते" --lang hi --save output.mp3
  python main.py --mode pipeline --output-lang english
  python main.py --mode pipeline --source file --file speech.wav
  python main.py --mode detect --text "Bonjour, comment allez-vous?"
  python main.py --languages
"""

import argparse
import sys
from stt import speech_to_text_from_mic, speech_to_text_from_file, list_supported_languages as stt_langs
from tts import text_to_speech, list_supported_languages as tts_langs
from detect_language import detect_language_name, detect_all_candidates
from pipeline import run_pipeline


def print_banner():
    print("""
╔══════════════════════════════════════════════════════╗
║      Multilingual Speech Processor v1.0              ║
║      STT · TTS · Auto Language Detection             ║
║      Built by Jayadeep Gopinath                      ║
╚══════════════════════════════════════════════════════╝
""")


def print_languages():
    print("\nSupported Languages:\n")
    langs = stt_langs()
    print(f"  {'Name':<15} {'STT Tag':<12} {'TTS Code':<10}")
    print("  " + "─" * 38)

    tts_map = tts_langs()
    for name, stt_tag in sorted(langs.items()):
        tts_code = tts_map.get(name, "—")
        print(f"  {name.capitalize():<15} {stt_tag:<12} {tts_code:<10}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Multilingual Speech Processor — STT, TTS, and auto-detect pipeline",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("--mode", choices=["stt", "tts", "pipeline", "detect"],
                        help="Mode: stt | tts | pipeline | detect")
    parser.add_argument("--lang", default="english",
                        help="Input language (name or code). Default: english")
    parser.add_argument("--output-lang", default="english",
                        help="Output language for TTS in pipeline mode. Default: english")
    parser.add_argument("--text", type=str,
                        help="Text to convert (for tts and detect modes)")
    parser.add_argument("--source", choices=["mic", "file"], default="mic",
                        help="Audio source for STT/pipeline. Default: mic")
    parser.add_argument("--file", type=str,
                        help="Path to audio file (required if --source file)")
    parser.add_argument("--save", type=str, default=None,
                        help="Save TTS output to this .mp3 file path")
    parser.add_argument("--languages", action="store_true",
                        help="List all supported languages and exit")
    parser.add_argument("--timeout", type=int, default=5,
                        help="Mic listen timeout in seconds. Default: 5")

    args = parser.parse_args()

    print_banner()

    if args.languages:
        print_languages()
        sys.exit(0)

    if not args.mode:
        parser.print_help()
        sys.exit(1)

    # ── STT Mode ─────────────────────────────────────────────────────────
    if args.mode == "stt":
        print(f"Mode: Speech-to-Text | Language: {args.lang}\n")
        if args.source == "file":
            if not args.file:
                print(" --file is required when --source is 'file'")
                sys.exit(1)
            text = speech_to_text_from_file(args.file, language=args.lang)
        else:
            text = speech_to_text_from_mic(language=args.lang, timeout=args.timeout)

        if text:
            print(f"\nTranscription:\n   {text}")
        else:
            print("\n No text recognized.")

    # ── TTS Mode ─────────────────────────────────────────────────────────
    elif args.mode == "tts":
        if not args.text:
            print("--text is required for tts mode")
            sys.exit(1)
        print(f"Mode: Text-to-Speech | Language: {args.lang}\n")
        path = text_to_speech(args.text, language=args.lang, save_path=args.save)
        print(f"\nAudio output: {path}")

    # ── Pipeline Mode ─────────────────────────────────────────────────────
    elif args.mode == "pipeline":
        print(f"Mode: Full Pipeline | Input: auto-detect → Output: {args.output_lang}\n")
        result = run_pipeline(
            input_language="auto",
            output_language=args.output_lang,
            source=args.source,
            audio_file=args.file,
            save_output=args.save
        )
        print(f"\nSummary:")
        print(f"   Transcribed:       {result['transcribed_text']}")
        print(f"   Detected language: {result['detected_language']}")
        print(f"   Output language:   {result['output_language']}")

    # ── Detect Mode ───────────────────────────────────────────────────────
    elif args.mode == "detect":
        if not args.text:
            print("--text is required for detect mode")
            sys.exit(1)
        print(f"Mode: Language Detection\n")
        name = detect_language_name(args.text)
        candidates = detect_all_candidates(args.text)
        print(f"\nDetected: {name}")
        if candidates:
            print(f"\nAll candidates:")
            for c in candidates[:5]:
                bar = "█" * int(c['confidence'] * 20)
                print(f"   {c['name']:<20} {bar:<20} {c['confidence']:.0%}")


if __name__ == "__main__":
    main()
