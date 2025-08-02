"""
server.py  – PolyRead backend (single-model version)

Features
────────
• POST /api/ocr        → run_ocr()  → {text, lines, image}
• POST /api/translate  → translate_text()  → {translated}
• POST /api/tts        → synthesize()  → audio file
• POST /api/detect-language → language_detection() → {detectedLanguage, score}
• GET  /               → serves index.html + all static assets
"""
import logging, sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

import os
import uuid
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, UploadFile, File, Request, HTTPException, status, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from ocr_module import run_ocr,run_ocr_2
from translate_and_tts_module import translate_text_input, synthesize_tts
from language_detection_module import language_detection

# ── FastAPI app setup ──────────────────────────────────────────
app = FastAPI(title="PolyRead API", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],                   # tweak in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

# static directory (index.html, app.js, css, images …)
STATIC_DIR = Path(__file__).parent / "static"
OUTPUT_IMG_NAME = "detected_output_with_labels.jpg"
OUTPUT_IMG_PATH = STATIC_DIR / OUTPUT_IMG_NAME

# DEFINE the TextPayload class before it's used
# This tells FastAPI what the request body for language detection should look like.
class TextPayload(BaseModel):
    text: str

# ── helper: safe temp file save ────────────────────────────────
def _save_upload_tmp(upload: UploadFile) -> Path:
    suffix = Path(upload.filename).suffix or ".bin"
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(upload.file, tmp)
        return Path(tmp.name)

# ─────────────────────────  API ROUTES  ────────────────────────

@app.post("/api/ocr")
async def ocr_endpoint(request: Request, file: UploadFile = File(...), lang: str | None = Form(None)):
    tmp_path = _save_upload_tmp(file)
    print(f"Language {lang}")
    try:
        if lang is None or lang == "":
            raw_lines, _ = run_ocr(str(tmp_path))

        else:
            raw_lines, _ = run_ocr_2(str(tmp_path), lang)
        # Change the image URL to point to your new endpoint
        img_url = "/api/output-image"

    finally:
        tmp_path.unlink(missing_ok=True)

    # Extract just the text from the list of dictionaries
    all_text = [line['text'] for line in raw_lines]
        
    return {
        "text": "\n".join(all_text),
        "lines": raw_lines,  # Send the full data structure
        "image": img_url,
    }

@app.get("/api/output-image")
async def get_output_image():
    if not OUTPUT_IMG_PATH.is_file():
        raise HTTPException(status_code=404, detail="Output image not found.")
    return FileResponse(OUTPUT_IMG_PATH)

# The endpoint now correctly uses the defined TextPayload
@app.post("/api/detect-language")
async def detect_language_endpoint(payload: TextPayload):
    """
    Receives text and returns the detected language.
    Payload: { "text": "..." }
    """
    try:
        # The language_detection function returns a list like: [{'label': 'eng', 'score': 0.99}]
        result = language_detection(payload.text)
        if not result:
            raise HTTPException(status_code=500, detail="Language detection returned an empty result.")
        lang_map= {
        'en': 'English',
        'fr': 'French',
        'hi': 'Hindii',
        'zh': 'Chinese',
        'de': 'German',
        'ja': 'Japanese',
        'te': 'Telugu',
        'es': 'Spanish',
        'ar': 'Arabic',
        'ru': 'Russian'
        }
        top_result = result[0]
        final_result = lang_map[top_result['label']]
        return {"detectedLanguage": final_result}
    except Exception as e:
        logging.error(f"Error in language detection endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/translate")
async def translate_endpoint(payload: dict):
    """
    Payload: { "text": "...", "target": "en" }
    """
    text = payload.get("text")
    #  Changed "target_lang" to "target" to match the frontend request
    tgt = payload.get("target") 
    
    if not text or not tgt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            # Updated the error detail for clarity
            detail="Both 'text' and 'target' are required."
        )
    
    try:
        # The actual translation logic remains the same
        _, _, translated = await translate_text_input(text, tgt)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error during translation: {str(exc)}"
        ) from exc

    #  Changed the response key from "translated" to "translatedText"
    return {"translatedText": translated}



@app.post("/api/tts")
async def tts_endpoint(payload: dict):
    text = payload.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="text required")
    try:
        path = synthesize_tts(text)
        return FileResponse(path, media_type="audio/mpeg", filename="speech.mp3")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {e}")

# ── serve static files (index.html, app.js, etc.) ──────────────
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

# ── ROUTE AUDIT – prints once at startup ───────────────────────
@app.on_event("startup")
async def show_routes() -> None:
    print("\n=== FastAPI ROUTES ===")
    for r in app.routes:
        if hasattr(r, "methods"):
            methods = ",".join(r.methods)
            print(f"{methods:<14} {r.path}")
    print("=== END ROUTES ===\n")