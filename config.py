import os
from pathlib import Path

# Groq Cloud için API keyin yüklenmesi
# Eğer mevcut değilse boş string atanır
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Sohbet geçmişi için dosya yolunun belirtilmesi
CONVERSATION_STORAGE_PATH = Path.home() / ".chatbotConversations"
CONVERSATION_STORAGE_PATH.mkdir(exist_ok=True)

# Sohbet edilebilen modellerin tanımlanması
MODEL_DETAILS = {
    "gemma2-9b-it": {
        "displayName": "Gemma 2 9B Instruct",
        "description": "Google Gemma modelinin daha gelişmiş versiyonudur.",
        "size": "9 milyar parametreyle eğitilmiştir.",
        "bestFor": [
            "Daha ileri düzeyde muhakeme",
            "Birden fazla dilde görevler",
            "Yönerge takip etme",
        ],
    },
    "llama3-groq-70b-8192-tool-use-preview": {
        "displayName": "Llama 3 70B Tool Use (Preview)",
        "description": "Meta'nın araç entegrasyonu yeteneğine sahip gelişmiş dil modelidir.",
        "size": "70 milyar parametreyle eğitilmiştir.",
        "bestFor": [
            "Karmaşık düzeyde muhakeme",
            "Araç kullanımı",
            "İleri düzey problem çözme",
        ],
    },
    "llama3-groq-8b-8192-tool-use-preview": {
        "displayName": "Llama 3 8B Tool Use (Preview)",
        "description": "Meta Llama 3 modelinin daha hafif versiyonudur. Daha az parametreyle eğitilmiştir.",
        "size": "8 milyar parametreyle eğitilmiştir.",
        "bestFor": ["Daha hızlı cevaplar", "Hafif işler", "Araç kullanımı"],
    },
    "llama-3.1-70b-versatile": {
        "displayName": "Llama 3.1 70B Versatile",
        "description": "Meta'nın en son Llama modelidir. Llama 3'e göre daha geniş kapasitesi vardır.",
        "size": "70 milyar parametreyle eğitilmiştir.",
        "bestFor": [
            "Genel kullanım",
            "Karmaşık düzeyde muhakeme",
            "Çok yönlü uygulamalar",
        ],
    },
    "mixtral-8x7b-32768": {
        "displayName": "Mixtral 8x7B",
        "description": "Mistral'in yüksek performanslı MoE (mixture-of-experts) modelidir. MoE, bir yapay zekanın alt yapay zekalara bölünerek oluşturulması, verilen görevleri ilgili alt yapay zekaların bir araya gelerek yapmasını ifade eder.",
        "size": "8x7 milyar parametreyle eğitilmiştir.",
        "bestFor": [
            "Birden fazla dilde görevler",
            "Muhakeme yeteneği",
            "Kod yazımı",
        ],
    },
}

# Model isimlerinin listelenmesi
AVALIABLE_MODELS = list(MODEL_DETAILS.keys())

# Varsayılan modelin ilk model olarak işaretlenmesi
DEFAULT_MODEL = AVALIABLE_MODELS[0]
