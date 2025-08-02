# PolyOCR: A Robust Multilingual OCR-to-Speech Pipeline with Language Detection and Translation 🧠🗣

## Table of Contents 📚
- [Overview 🌍](#overview-🌍)
- [Features 🌟](#features-🌟)
- [System Architecture 🏗](#system-architecture-🏗)
- [Key Components 🧩](#key-components-🧩)
  - [1. Optical Character Recognition (OCR) 👁](#1-optical-character-recognition-ocr-👁)
  - [2. Language Detection 🌐](#2-language-detection-🌐)
  - [3. Translation Module 🌍](#3-translation-module-🌍)
  - [4. Text-to-Speech (TTS) Synthesis 🔊](#4-text-to-speech-tts-synthesis-🔊)
- [Accomplished Enhancements (Previously Future Work) ✅](#accomplished-enhancements-previously-future-work-✅)
  - [Language-Specific Tuning and Script Adaptation ✨](#language-specific-tuning-and-script-adaptation-✨)
  - [Enhanced UI/UX and Web Deployment 🖥](#enhanced-uiux-and-web-deployment-🖥)
  - [Real-Time Camera Input Integration 📸](#real-time-camera-input-integration-📸)
  - [Handwritten Text Support 📝](#handwritten-text-support-📝)
  - [Model Switching Interface 🎛](#model-switching-interface-🎛)
- [Installation and Usage 🧰](#installation-and-usage-🧰)
  - [Prerequisites 🔧](#prerequisites-🔧)
  - [Setup 🚀](#setup-🚀)
  - [Running the Application ▶](#running-the-application-▶)
- [Evaluation and Performance 📈](#evaluation-and-performance-📈)
- [Team 🤝](#team-🤝)
- [License 📄](#license-📄)

## Overview 🌍

*PolyOCR* is a robust and modular OCR-to-speech pipeline tailored to extract, understand, and vocalize text from images across multiple languages and scripts. It unifies:

- 📖 *OCR* (via PaddleOCR)
- 🧠 *Language Detection* (via Langdetect)
- 🌐 *Translation* (via Googletrans)
- 🔊 *Speech Synthesis* (via pyttsx3)

This end-to-end system bridges linguistic gaps, enabling document accessibility and cross-language communication in real-time.

## Features 🌟

- 🖼 *Smart Image Preprocessing*: Automatic resizing, noise removal, and normalization for better OCR performance.
- 🌏 *Multilingual OCR*: Detects and reads over 80 languages using PaddleOCR.
- 🌐 *Accurate Language Identification*: Powered by Langdetect, supports 55+ languages.
- 🧭 *Seamless Translation*: Converts text to English (or others) with NMT via Google Translate.
- 🔉 *Offline Text-to-Speech*: Converts any text into clear, offline-playable audio using pyttsx3.
- 📷 *Live Camera Input*: Enables real-time text detection and translation from your webcam.
- ✍ *Handwritten Text Support*: Recognizes cursive and historical writing styles.
- ⚙ *Fully Modular Architecture*: Swap or modify components with ease.
- 🖥 *Intuitive Web UI*: Drag-and-drop upload, visual overlays, inline playback, and download options.
- 🔁 *OCR Mode Selector*: Switch between General OCR, PP-Structure, or ChatOCR based on input.

## System Architecture 🏗

> *Input Image → Preprocessing → OCR → Language Detection → Translation → TTS → Output*

Each module is independently tunable and replaceable, enabling future flexibility and customization.

## Key Components 🧩

### 1. Optical Character Recognition (OCR) 👁
- ✅ *PaddleOCR (PP-OCRv4)* ensures multilingual, CPU-efficient text extraction.
- 🧱 *DBNet*: Detects complex, curved, or rotated text regions.
- 🔠 *SVTR-LCNet*: Recognizes multilingual scripts, even under poor lighting or resolution.

### 2. Language Detection 🌐
- 🧠 *Langdetect* uses Naive Bayes with character n-grams.
- Supports noisy, short input with 55+ languages.

### 3. Translation Module 🌍
- 🔄 *Googletrans API* for language translation with Neural Machine Translation.
- 🧹 Handles chunking, normalization, and code formatting for long inputs.

### 4. Text-to-Speech (TTS) Synthesis 🔊
- 💻 *pyttsx3* for lightweight, platform-independent speech output.
- 🎵 Exports audio in .mp3 or .wav format with offline capability.

## Accomplished Enhancements (Previously Future Work) ✅

### Language-Specific Tuning and Script Adaptation ✨
- ✏ Normalizes regional scripts for clarity.
- 🧩 Improves translation coherence.
- 🧠 Adds punctuation and pronunciation refinements.

### Enhanced UI/UX and Web Deployment 🖥
- 🌙 Dark & Light Modes
- 🖱 Drag-and-drop image upload
- 🔲 Bounding box overlays for OCR
- 🎧 Inline audio playback and download options

### Real-Time Camera Input Integration 📸
- 👁 Read signboards, notes, and menus live
- ⚙ Optimized for low-latency frame capture and streaming

### Handwritten Text Support 📝
- 📖 Recognizes cursive and unconstrained handwriting
- 🏛 Supports old manuscripts, notes, and form parsing

### Model Switching Interface 🎛
- 🔁 Select between OCR modes per document type
- 🧾 Better results for structured layouts and tables

## Installation and Usage 🧰

### Prerequisites 🔧
- Python 3.x
- Libraries: paddlepaddle, PaddleOCR, langdetect, googletrans, pyttsx3

### Setup 🚀
bash
git clone https://github.com/your-username/PolyOCR.git
cd PolyOCR
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt



Then open your browser at http://127.0.0.1:5000 and upload an image or use your webcam.

## Evaluation and Performance 📈

| Metric                | Value                         |
|-----------------------|-------------------------------|
| OCR Accuracy (H-mean) | ~69.2% (on RRC dataset)       |
| Lang Detection        | High accuracy (major scripts) |
| Translation           | Manual fluency verification   |
| TTS Latency           | ~3.2 seconds (mid-range CPU)  |

## Team 🤝

- Yogendra
- Rishabh
- Ayushi
- Shreya
- Sujith

## License 📄

Licensed under the *MIT License*. See [LICENSE](LICENSE) for full details.
