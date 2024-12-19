import os
from groq import Groq
from config import AVALIABLE_MODELS, DEFAULT_MODEL
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class GroqChatInterface:
    def __init__(self, apiKey: Optional[str] = None, model: str = DEFAULT_MODEL):

        # API keyi yükle
        if apiKey is None:
            apiKey = os.getenv("GROQ_API_KEY")

        if not apiKey:
            raise ValueError("apiKey yok.")

        try:
            self.client = Groq(api_key=apiKey)

        except Exception as e:
            print(f"Groq istemcisi başlatılırken hata oluştu. Hata kodu: {e}")
            raise

        self.model = model if model in AVALIABLE_MODELS else DEFAULT_MODEL

    def generateResponse(self, messages: List[Dict]) -> str:
        """Groq Cloud bağlantısıyla bir cevap üretir."""

        try:
            chatCompletion = self.client.chat.completions.create(
                messages=messages, model=self.model
            )

            return chatCompletion.choices[0].message.content

        except Exception as e:
            return f"Cevap üretirken hata oluştu. Hata kodu: {str(e)}"

    def switchModel(self, model: str):
        """Mevcut modeli değiştirir."""

        if model in AVALIABLE_MODELS:
            self.model = model

        else:
            raise ValueError(
                f"Model geçerli değil! Şu modellerden birini seçin: {AVALIABLE_MODELS}"
            )
