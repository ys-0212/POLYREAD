import re
import asyncio
from googletrans import Translator
import pyttsx3
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from tempfile import NamedTemporaryFile
from pathlib import Path


translator = Translator(service_urls=['translate.googleapis.com'])

# Normalize language codes for googletrans compatibility
LANG_CODE_MAP = {
    "zh": "zh-CN",
    "jp": "ja",
    "kr": "ko"
}
model = AutoModelForSequenceClassification.from_pretrained("model")
tokenizer = AutoTokenizer.from_pretrained("model")
clf = pipeline("text-classification", model=model, tokenizer=tokenizer)
def language_detection(text):
    result = clf(text)

    return result

def normalize_lang_code(lang):
    return LANG_CODE_MAP.get(lang.lower(), lang)

# Language detection with CJK script disambiguation
async def translate_text_input(text, target_lang='en'):
    # Return immediately for empty or whitespace-only input
    if not text or text.isspace():
        return None, 0, ""

    lang_detection_result = language_detection(text)

    # Check if language detection returned a valid result
    if not lang_detection_result:
        print("Language detection returned an empty result.")
        # Fallback to googletrans as a last resort
        try:
            detection = translator.detect(text)
            lang_code = detection.lang
            confidence = detection.confidence
        except Exception as e:
            print(f"Fallback language detection failed: {e}")
            return None, 0, "[ Translation failed: could not detect language ]"
    else:
        lang_code = lang_detection_result[0]['label']
        confidence = lang_detection_result[0]['score']

    lang_code = normalize_lang_code(lang_code)
    cleaned = clean_text(text, lang_code)
    full_translation = ""

    for chunk in chunk_text(cleaned):
        try:
            translated = await translator.translate(chunk, dest=target_lang)
            full_translation += translated.text + " "
        except Exception as e:
            full_translation += f"[ Translation error: {e} ] "

    return lang_code, confidence, full_translation.strip()

# Clean text per script
def clean_text(text, lang):
    if lang in ['hi', 'mr', 'bn', 'gu', 'pa', 'ne']:
        return re.sub(r'[^ऀ-ॿঀ-৿਀-੿\s।.,!?]', '', text)
    elif lang in ['ta', 'te']:
        return re.sub(r'[^஀-௿ఀ-౿\s।.,!?]', '', text)
    elif lang == 'kn':
        return re.sub(r'[^ಀ-೿\s।.,!?]', '', text)
    elif lang == 'ml':
        return re.sub(r'[^ഀ-ൿ\s।.,!?]', '', text)
    elif lang == 'si':
        return re.sub(r'[^඀-෿\s।.,!?]', '', text)
    elif lang == 'zh-CN' or lang == 'zh':
        return re.sub(r'[^一-鿿。，！？]', '', text)
    elif lang == 'ja':
        return text  # Japanese cleaning can be more complex; skipping
    elif lang == 'ko':
        return re.sub(r'[^가-힯\s.,!?]', '', text)
    elif lang in ['ar', 'ur']:
        return re.sub(r'[^؀-ۿ\s،؟]', '', text)
    elif lang in ['ru', 'uk', 'sr']:
        return re.sub(r'[^Ѐ-ӿ\s.,!?]', '', text)
    elif lang == 'el':
        return re.sub(r'[^Ͱ-Ͽ\s.,!?]', '', text)
    elif lang == 'he':
        return re.sub(r'[^֐-׿\s.,!?]', '', text)
    elif lang == 'th':
        return re.sub(r'[^฀-๿\s.,!?]', '', text)
    elif lang in ['de', 'es', 'nl', 'it', 'fr', 'en', 'vi', 'pl', 'cs', 'tr', 'id', 'ro']:
        return re.sub(r"[^a-zA-ZÀ-ÿĀ-žŒœẞßÇçÑñÄäÖöÜüẞẞ\s.,!?¿¡'-]", '', text)
    else:
        return re.sub(r'[^\w\s.,!?]', '', text)

# Chunk text to avoid API limit issues
def chunk_text(text, max_len=300):
    words = text.split()
    chunks = []
    current_chunk = []
    current_len = 0
    for word in words:
        if current_len + len(word) + 1 > max_len:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_len = len(word) + 1
        else:
            current_chunk.append(word)
            current_len += len(word) + 1
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

# Text-to-Speech that saves to a file
def synthesize_tts(text: str) -> Path:
    """Synthesizes text to speech and saves it to a temporary MP3 file."""
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 150)
    
    # Create a temporary file to save the speech.
    # We use delete=False to keep the file open until the server sends it.
    with NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        output_path = Path(tmp_file.name)
        
    # Save the speech to the designated temporary file
    engine.save_to_file(text, str(output_path))
    engine.runAndWait()
    
    return output_path

# Example Usage
if __name__ == "__main__":
    input_text = """请您爱护和保护我们的美丽环境。"""
    lang, confidence, translated_text = asyncio.run(translate_text_input(input_text))
    print(f"\nDetected Language: {lang} (Confidence: {confidence})")
    print(f"Translated Text: {translated_text}")
    
    # This part would now save a file instead of speaking directly.
    # To test, you would check your temp directory for the mp3 file.
    print("\nSynthesizing speech to a temporary file...")
    audio_file = synthesize_tts(translated_text)
    print(f" Speech saved to: {audio_file}")