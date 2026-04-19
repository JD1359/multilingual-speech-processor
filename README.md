# Multilingual Speech Processor

> Real-time bidirectional speech-to-text and text-to-speech conversion across 10+ languages — built with Python and NLP libraries.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-Natural_Language_Processing-orange?style=flat)
![gTTS](https://img.shields.io/badge/gTTS-Text_to_Speech-blue?style=flat)
![SpeechRecognition](https://img.shields.io/badge/SpeechRecognition-STT-green?style=flat)

---

## Overview

This application provides a complete multilingual speech processing pipeline — converting spoken audio to text (STT) and converting text to spoken audio (TTS) across multiple languages in real time. The system handles language detection automatically and routes to the correct NLP processing pipeline based on detected language.

Built to solve a real accessibility problem: enabling cross-language voice communication for users who speak different languages.

---

## Supported Languages

English · Hindi · Kannada · Tamil · Telugu · Spanish · French · German · Japanese · Chinese (Mandarin)

*(Language support depends on installed NLP models)*

---

## Features

- **Speech-to-Text (STT):** Converts microphone input or audio files to text using `SpeechRecognition` with Google Web Speech API backend
- **Text-to-Speech (TTS):** Converts text to natural-sounding spoken audio using `gTTS` (Google Text-to-Speech)
- **Automatic language detection:** Identifies the spoken or written language without user selection
- **Bidirectional pipeline:** Supports both STT → TTS translation workflow and standalone STT/TTS modes
- **Cross-language support:** Processes input in one language and outputs in another (e.g., speak in Hindi, get English text)
- **Audio file support:** Accepts `.wav`, `.mp3` audio files in addition to live microphone input

---

## Tech Stack

| Component | Library |
|---|---|
| Speech-to-Text | `SpeechRecognition` + Google Web Speech API |
| Text-to-Speech | `gTTS` (Google Text-to-Speech) |
| Language Detection | `langdetect` |
| Audio Processing | `pyaudio`, `pydub` |
| NLP Utilities | `nltk` |

---

## Project Structure

```
multilingual-speech-processor/
├── stt.py              # Speech-to-text pipeline
├── tts.py              # Text-to-speech pipeline
├── detect_language.py  # Automatic language detection
├── pipeline.py         # End-to-end STT → TTS flow
├── main.py             # CLI entry point
├── requirements.txt    # Python dependencies
└── README.md
```

---

## Setup & Run

```bash
# 1. Clone the repo
git clone https://github.com/JD1359/multilingual-speech-processor.git
cd multilingual-speech-processor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run speech-to-text (microphone)
python main.py --mode stt --lang en

# 4. Run text-to-speech
python main.py --mode tts --text "Hello, how are you?" --lang hi

# 5. Run full pipeline (speak → detect → convert → speak back)
python main.py --mode pipeline
```

---

## Example Usage

```bash
# Convert English speech to text
$ python main.py --mode stt --lang en
🎤 Listening... Speak now.
📝 Detected: "What is the weather today?"

# Convert text to Hindi speech
$ python main.py --mode tts --text "नमस्ते, आप कैसे हैं?" --lang hi
🔊 Playing audio...

# Auto-detect and translate pipeline
$ python main.py --mode pipeline
🎤 Listening...
🌐 Detected language: Kannada
📝 Transcribed: "ನೀವು ಹೇಗಿದ್ದೀರಿ?"
🔊 Speaking in English: "How are you?"
```

---

## Architecture

```
Microphone / Audio File
        │
        ▼
SpeechRecognition (STT)
        │
        ▼
Language Detector (langdetect)
        │
        ▼
NLP Processing (nltk — tokenization, normalization)
        │
        ▼
gTTS (Text-to-Speech)
        │
        ▼
Audio Output (speaker / .mp3 file)
```

---

## Key Implementation Challenges

**Language detection accuracy:** Short phrases (< 5 words) often confuse the language detector. Solved by adding a minimum-confidence threshold — falling back to user-specified language when confidence drops below 70%.

**Audio latency:** gTTS requires a network call to Google's API, introducing ~1–2 second latency. For offline use, `pyttsx3` is available as a fallback TTS engine.

**Cross-platform audio:** `pyaudio` requires platform-specific dependencies (PortAudio). Documented setup for macOS, Linux, and Windows in the troubleshooting section.

---

## Future Improvements

- [ ] Add offline STT support using OpenAI Whisper (no internet required)
- [ ] Integrate translation between languages (not just detection)
- [ ] Build a web UI with Flask for browser-based usage
- [ ] Add real-time streaming STT (WebSocket-based)
- [ ] Support regional Indian languages: Bengali, Marathi, Gujarati

---

## Author

**Jayadeep Gopinath**
M.S. Computer Science · Illinois Institute of Technology, Chicago
[LinkedIn](https://linkedin.com/in/jayadeep-g-05b643257) · jg@hawk.illinoistech.edu
