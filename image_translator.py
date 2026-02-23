import os
import requests
from groq import Groq
from lingua import LanguageDetectorBuilder

_lingua_detector = LanguageDetectorBuilder.from_all_languages().build()
OCR_API_URL = "https://api.ocr.space/parse/image"


def _get_client():
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        raise RuntimeError("Clé GROQ_API_KEY manquante")
    return Groq(api_key=api_key)


def _ocr_extract(file, api_key: str) -> str:
    if hasattr(file, "seek"):
        file.seek(0)
    file_bytes = file.read() if hasattr(file, "read") else b""
    filename   = getattr(file, "name", None) or "image.png"
    response   = requests.post(OCR_API_URL,
        files = {"file": (filename, file_bytes)},
        data  = {"apikey": api_key, "language": "eng", "isOverlayRequired": False},
        timeout = 30)
    result = response.json()
    if result.get("IsErroredOnProcessing"):
        raise RuntimeError(f"OCR erreur : {result.get('ErrorMessage')}")
    parsed = result.get("ParsedResults", [])
    return parsed[0].get("ParsedText", "").strip() if parsed else ""


def _translate_with_groq(text: str, source_lang: str, target_lang: str) -> str:
    client   = _get_client()
    prompt   = f"Translate from {source_lang} to {target_lang}. Return ONLY the translated text:\n\n{text}"
    response = client.chat.completions.create(
        model       = "llama-3.3-70b-versatile",
        messages    = [{"role": "user", "content": prompt}],
        max_tokens  = 2048,
        temperature = 0.1
    )
    return response.choices[0].message.content.strip()


class ImageTranslator:
    def translate(self, file, target_lang: str = "en") -> dict:
        api_key        = os.environ.get("OCR_API_KEY", "helloworld")
        extracted_text = _ocr_extract(file, api_key)
        if not extracted_text:
            return {"extracted_text": "", "translated_text": ""}
        detected    = _lingua_detector.detect_language_of(extracted_text)
        source_lang = detected.iso_code_639_1.name.lower() if detected else "en"
        translated  = _translate_with_groq(extracted_text, source_lang, target_lang)
        return {"extracted_text": extracted_text, "translated_text": translated}