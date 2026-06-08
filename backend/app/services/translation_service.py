from langdetect import detect, detect_langs
from deep_translator import GoogleTranslator
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

# Language code to name mapping
LANGUAGE_NAMES = {
    'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
    'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)', 'ja': 'Japanese', 'ko': 'Korean',
    'ar': 'Arabic', 'hi': 'Hindi', 'bn': 'Bengali', 'pa': 'Punjabi',
    'te': 'Telugu', 'mr': 'Marathi', 'ta': 'Tamil', 'ur': 'Urdu',
    'gu': 'Gujarati', 'kn': 'Kannada', 'ml': 'Malayalam', 'th': 'Thai',
    'vi': 'Vietnamese', 'tr': 'Turkish', 'pl': 'Polish', 'uk': 'Ukrainian',
    'nl': 'Dutch', 'sv': 'Swedish', 'da': 'Danish', 'no': 'Norwegian',
    'fi': 'Finnish', 'el': 'Greek', 'cs': 'Czech', 'ro': 'Romanian',
    'hu': 'Hungarian', 'id': 'Indonesian', 'ms': 'Malay', 'tl': 'Filipino',
    'he': 'Hebrew', 'fa': 'Persian', 'sw': 'Swahili', 'af': 'Afrikaans'
}

class TranslationService:
    def __init__(self):
        self.supported_languages = list(LANGUAGE_NAMES.keys())
    
    def detect_language(self, text: str) -> Tuple[str, str, float]:
        """
        Detect the language of the given text.
        Returns: (language_code, language_name, confidence)
        """
        try:
            if not text or len(text.strip()) < 3:
                return 'en', 'English', 0.0
            
            detected_langs = detect_langs(text)
            if detected_langs:
                top_lang = detected_langs[0]
                lang_code = str(top_lang.lang)
                confidence = top_lang.prob
                lang_name = LANGUAGE_NAMES.get(lang_code, lang_code.upper())
                return lang_code, lang_name, confidence
            
            return 'en', 'English', 0.0
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return 'en', 'English', 0.0
    
    def translate_text(
        self,
        text: str,
        target_language: str = 'en',
        source_language: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Translate text to target language.
        Returns: (translated_text, source_language)
        """
        try:
            if not text or len(text.strip()) == 0:
                return text, source_language or 'en'
            
            # Detect source language if not provided
            if not source_language:
                source_language, _, _ = self.detect_language(text)
            
            # If source and target are the same, return original
            if source_language == target_language:
                return text, source_language
            
            # Handle Chinese variants
            src_lang = 'zh-CN' if source_language in ['zh-cn', 'zh'] else source_language
            tgt_lang = 'zh-CN' if target_language in ['zh-cn', 'zh'] else target_language
            
            translator = GoogleTranslator(source=src_lang, target=tgt_lang)
            translated = translator.translate(text)
            
            return translated, source_language
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text, source_language or 'en'
    
    def translate_to_english(self, text: str, source_language: Optional[str] = None) -> Tuple[str, str]:
        """Translate text to English."""
        return self.translate_text(text, target_language='en', source_language=source_language)
    
    def translate_from_english(self, text: str, target_language: str) -> str:
        """Translate English text to target language."""
        translated, _ = self.translate_text(text, target_language=target_language, source_language='en')
        return translated
    
    def get_language_name(self, lang_code: str) -> str:
        """Get the full name of a language from its code."""
        return LANGUAGE_NAMES.get(lang_code, lang_code.upper())

translation_service = TranslationService()