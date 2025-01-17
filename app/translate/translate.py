from typing import Optional
from googletrans import Translator

class TranslateService:
    def __init__(self):
        self.translator = Translator()

    def translate_text(self, 
                      text: str, 
                      source_language: str, 
                      target_language: str) -> Optional[str]:
        """
        将文本从源语言翻译为目标语言
        
        Args:
            text: 要翻译的文本
            source_language: 源语言代码 (例如 'zh')
            target_language: 目标语言代码 (例如 'en')
            
        Returns:
            翻译后的文本，如果翻译失败则返回 None
        """
        try:
            if source_language == target_language:
                return text
                
            result = self.translator.translate(
                text,
                src=source_language,
                dest=target_language
            )
            return result.text
        except Exception as e:
            print(f"翻译失败: {str(e)}")
            return None 