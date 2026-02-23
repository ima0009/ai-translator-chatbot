import os
from groq import Groq

def _get_client():
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        raise RuntimeError("Clé GROQ_API_KEY manquante dans .streamlit/secrets.toml")
    return Groq(api_key=api_key)


def _translate_with_groq(text: str, source_lang: str, target_lang: str) -> str:
    """Traduction via Groq Llama 3.3 70B."""
    client = _get_client()
    prompt = f"Translate the following text from {source_lang} to {target_lang}. Return ONLY the translated text, no explanation:\n\n{text}"
    response = client.chat.completions.create(
        model    = "llama-3.3-70b-versatile",
        messages = [{"role": "user", "content": prompt}],
        max_tokens = 2048,
        temperature = 0.1
    )
    return response.choices[0].message.content.strip()


class TextTranslator:
    def translate(self, text: str, source_lang: str = "fr", target_lang: str = "en") -> str:
        if not text.strip():
            return ""
        if source_lang == target_lang:
            return text
        return _translate_with_groq(text, source_lang, target_lang)