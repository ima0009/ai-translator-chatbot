import os
import tempfile
import requests
from groq import Groq

WHISPER_MODEL = "whisper-large-v3-turbo"
MYMEMORY_URL  = "https://api.mymemory.translated.net/get"

def _get_client():
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        raise RuntimeError("❌ Clé GROQ_API_KEY manquante dans .streamlit/secrets.toml")
    return Groq(api_key=api_key)

class AudioTranslator:
    def translate(self, file, target_lang: str = "en") -> dict:
        filename   = getattr(file, "name", None) or getattr(file, "filename", "audio.mp3")
        extension  = os.path.splitext(filename.lower())[1] or ".mp3"
        file_bytes = file.read() if hasattr(file, "read") else b""

        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        try:
            client = _get_client()
            with open(tmp_path, "rb") as audio_file:
                result = client.audio.transcriptions.create(
                    model           = WHISPER_MODEL,
                    file            = audio_file,
                    response_format = "text"
                )
            transcription = result.strip() if isinstance(result, str) else str(result)
        finally:
            os.unlink(tmp_path)

        if not transcription:
            return {"transcription": "", "translated_text": ""}

        translated = self._translate(transcription, target_lang)
        return {"transcription": transcription, "translated_text": translated}

    def _translate(self, text: str, target_lang: str) -> str:
        try:
            chunks  = [text[i:i+450] for i in range(0, len(text), 450)]
            results = []
            for chunk in chunks:
                response = requests.get(MYMEMORY_URL, params={
                    "q": chunk, "langpair": f"en|{target_lang}"
                }, timeout=10)
                data = response.json()
                if data.get("responseStatus") == 200:
                    results.append(data["responseData"]["translatedText"])
                else:
                    results.append(chunk)
            return " ".join(results)
        except Exception:
            return text
