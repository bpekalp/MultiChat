import uuid
import json
from pathlib import Path
from typing import List, Dict, Optional
from config import CONVERSATION_STORAGE_PATH, MODEL_DETAILS, DEFAULT_MODEL


class ConversationManager:
    @staticmethod
    def generateConversationId() -> str:
        """UUID kütüphanesiyle benzersiz bir sohbet ID'si oluşturur."""
        return str(uuid.uuid4())

    @staticmethod
    def saveConversation(conversationId: str, messages: List[Dict], model: str):
        """Sohbeti kullanıcının bilgisayarında depolar."""
        conversationFile = CONVERSATION_STORAGE_PATH / f"{conversationId}.json"
        conversationData = {"id": conversationId, "model": model, "messages": messages}

        with open(conversationFile, "w") as file:
            json.dump(conversationData, file, indent=2)

    @staticmethod
    def loadConversation(conversationId: str) -> Optional[Dict]:
        """Yereldeki sohbetleri yükler."""
        conversationFile = CONVERSATION_STORAGE_PATH / f"{conversationId}.json"

        if conversationFile.exists():
            try:
                with open(conversationFile, "r") as file:
                    conversation = json.load(file)

                if conversation.get("model") not in MODEL_DETAILS:
                    conversation["model"] = DEFAULT_MODEL

                return conversation

            except Exception as e:
                print(f"{conversationId} numaralı sohbet yüklenemedi. Hata kodu: {e}")
                return None
        return None

    @staticmethod
    def listConversations() -> List[Dict]:
        """Kayıtlı sohbetleri listeler."""
        conversations = []

        for convFile in CONVERSATION_STORAGE_PATH.glob("*.json"):
            try:
                with open(convFile, "r") as file:
                    conversation = json.load(file)

                model = conversation.get("model", DEFAULT_MODEL)
                if model not in MODEL_DETAILS:
                    model = DEFAULT_MODEL

                conversations.append(
                    {
                        "id": conversation["id"],
                        "model": model,
                        "messageCount": len(conversation["messages"]),
                    }
                )
            except Exception as e:
                print(f"{convFile} işlenemedi. Hata kodu: {e}")

        return conversations

    # @staticmethod
    # def deleteConversation(conversationId: str):
    #     """Belirli sohbeti siler."""
    #     conversationFile = CONVERSATION_STORAGE_PATH / f"{conversationId}.json"

    #     if conversationFile.exists():
    #         try:
    #             conversationFile.unlink()

    #         except Exception as e:
    #             print(f"{conversationFile} silinemedi. Hata kodu: {e}")

    @staticmethod
    def clearAllConversations():
        """Kayıtlı bütün sohbetleri siler."""
        for file in CONVERSATION_STORAGE_PATH.glob("*.json"):
            try:
                file.unlink()

            except Exception as e:
                print(f"{file} silinemedi. Hata kodu: {e}")
