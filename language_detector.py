from lingua import Language, LanguageDetectorBuilder

_detector = LanguageDetectorBuilder.from_all_languages().build()

LINGUA_TO_ISO = {
    Language.FRENCH:     "fr",
    Language.ENGLISH:    "en",
    Language.SPANISH:    "es",
    Language.GERMAN:     "de",
    Language.ITALIAN:    "it",
    Language.ARABIC:     "ar",
    Language.RUSSIAN:    "ru",
    Language.CHINESE:    "zh",
    Language.JAPANESE:   "ja",
    Language.PORTUGUESE: "pt",
    Language.DUTCH:      "nl",
    Language.KOREAN:     "ko",
    Language.TURKISH:    "tr",
    Language.POLISH:     "pl",
}

class LanguageDetector:
    def detect(self, text: str) -> str:
        if not text.strip():
            return "fr"
        result = _detector.detect_language_of(text)
        if result is None:
            return "fr"
        return LINGUA_TO_ISO.get(result, "fr")
