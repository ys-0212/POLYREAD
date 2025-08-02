# PolyOCR: A Robust Multilingual OCR-to-Speech Pipeline with Language Detection and Translation 

## Table of Contents 
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Key Components](#key-components)
  - [1. Optical Character Recognition (OCR)](#1-optical-character-recognition-ocr)
  - [2. Language Detection](#2-language-detection)
  - [3. Translation Module](#3-translation-module)
  - [4. Text-to-Speech (TTS) Synthesis](#4-text-to-speech-tts-synthesis)
  - [Language-Specific Tuning and Script Adaptation](#language-specific-tuning-and-script-adaptation)
  - [UI/UX and Web Deployment](#uiux-and-web-deployment)
- [Installation and Usage](#installation-and-usage)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [Team](#team)
- [License](#license)

## Overview 

*PolyOCR* is a robust and modular OCR-to-speech pipeline tailored to extract, understand, and vocalize text from images across multiple languages and scripts. It unifies:

-  *OCR* (via PaddleOCR)
-  *Language Detection* (via Langdetect)
-  *Translation* (via Googletrans)
-  *Speech Synthesis* (via pyttsx3)

This end-to-end system bridges linguistic gaps, enabling document accessibility and cross-language communication in real-time.

## Features 

-  *Smart Image Preprocessing*: Automatic resizing, noise removal, and normalization for better OCR performance.
-  *Multilingual OCR*: Detects and reads 10 languages using PaddleOCR.
-  *Accurate Language Identification*: Powered by RoBERTa.
-  *Seamless Translation*: Converts text to English (or others) with NMT via Google Translate.
-  *Offline Text-to-Speech*: Converts any text into clear, offline-playable audio using pyttsx3.
-  *Handwritten Text Support*: Recognizes cursive writing styles.
-  *Fully Modular Architecture*: Swap or modify components with ease.
-  *Intuitive Web UI*: Drag-and-drop upload, visual overlays, inline playback, and download options.


## System Architecture 

> *Input Image → Preprocessing → OCR_1 → Language Detection → OCR_2 → Raw Text Output → Translation → TTS → Audio Output*

Each module is independently tunable and replaceable, enabling future flexibility and customization.

## Key Components 

### 1. Optical Character Recognition (OCR) 
-  *PaddleOCR (PP-OCRv4)*.

### 2. Language Detection 
-  *RoBERTo*.
  
### 3. Translation Module 
-  *Googletrans API* 

### 4. Text-to-Speech (TTS) Synthesis 
-  *pyttsx3* 



## UI/UX and Web Deployment 
-  Dark & Light Modes
-  Drag-and-drop image upload
-  Bounding box overlays for OCR
-  Complete Raw Text Ouput Box
-  A line-by-line text output view with Hover-enabled boxes that reveal coordinate information 
-  A live translation module providing real-time results per selected segment
-  Inline audio playback and download options

## Installation and Usage 

### Prerequisites 
- Python 3.10

### Setup 
```bash
git clone https://github.com/your-username/PolyOCR.git
cd PolyOCR
python -m venv venv
.\venv\Scripts\activate #windows
pip install -r requirements.txt
```

For CPU users
```bash
#install pytorch version 2.3.0
pip install torch==2.3.0+cpu torchvision==0.18.0+cpu torchaudio==2.3.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
```

For GPU users
```bash
#install pytorch version 2.3.0 cu121
pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu121
```

Then open your browser at localhost:8000 and upload an image.



## Team 

- Yogendra
- Rishabh
- Ayushi
- Shreya
- Sujith

## License 

Licensed under the *MIT License*. See [LICENSE](LICENSE) for full details.
