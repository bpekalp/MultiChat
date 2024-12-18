import streamlit as st
from config import AVALIABLE_MODELS, DEFAULT_MODEL, MODEL_DETAILS
from conversationManager import ConversationManager
from groqCloud import GroqChatInterface


def main():
    st.set_page_config(page_title="MultiChat AI", page_icon="🤖", layout="wide")

    st.title("🤖 MultiChat AI: Birden fazla modelle aynı anda sohbet edin!")

    # Model seçim listesinin model adlarıyla oluşturulması
    modelOptions = [MODEL_DETAILS[model]["displayName"] for model in AVALIABLE_MODELS]

    displayToInternal = {
        MODEL_DETAILS[model]["displayName"]: model for model in AVALIABLE_MODELS
    }

    # Ana sayfanın sütunlara ayırılması
    col1, col2 = st.columns([2, 3])

    with col1:
        # Model seçimi ve ek bilgilerin yazılması
        selectedDisplayName = st.selectbox(
            "AI Modelini Seçin",
            options=modelOptions,
            index=modelOptions.index(MODEL_DETAILS[DEFAULT_MODEL]["displayName"]),
        )

        # Modelin asıl isminin alınması
        selectedModel = displayToInternal[selectedDisplayName]

    with col2:
        # Model bilgilerinin yazılması
        modelInfo = MODEL_DETAILS[selectedModel]
        st.info(f"**{modelInfo['description']}**")
        st.markdown(f"**Model Boyutu:** {modelInfo['size']}")
        st.markdown(f"**Kullanım Alanları:**")
        for case in modelInfo["bestFor"]:
            st.markdown(f"- {case}")

    # Sohbet yönetiminin başlatılması
    if "conversationId" not in st.session_state:
        st.session_state.conversationId = ConversationManager.generateConversationId()
        st.session_state.messages = []

    # Groq Cloud bağlantısının başlatılması
    if (
        "chatInterface" not in st.session_state
        or st.session_state.currentModel != selectedModel
    ):
        st.session_state.chatInterface = GroqChatInterface(model=selectedModel)
        st.session_state.currentModel = selectedModel

    # Sohbet geçmişinin gösterilmesi
    with st.sidebar:
        st.header("Sohbet Geçmişi")

        conversations = ConversationManager.listConversations()

        for conv in conversations:
            convDisplay = f"{conv['id'][:8]} | {MODEL_DETAILS[conv['model']]['displayName']} | {conv['messageCount']} mesaj"

            if st.button(convDisplay, key=conv["id"]):
                loadedConv = ConversationManager.loadConversation(conv["id"])
                if loadedConv:
                    st.session_state.messages = loadedConv["messages"]
                    st.session_state.conversationId = loadedConv["id"]
                    st.session_state.currentModel = loadedConv["model"]
                    st.rerun()

        st.markdown("---")

        # Yeni sohbet ve sohbet geçmişi temizleme
        colNew, colClear = st.columns(2)

        with colNew:
            if st.button("Yeni Sohbet"):
                st.session_state.conversationId = (
                    ConversationManager.generateConversationId()
                )
                st.session_state.messages = []
                st.rerun()

        with colClear:
            if st.button("Geçmişi Temizle"):
                ConversationManager.clearAllConversations()
                st.success("Sohbet geçmişi başarıyla temizlendi.")
                st.rerun()

    # Sohbet ekranı
    # Mesajların gösterilmesi
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Kullanıcı girişi
    if prompt := st.chat_input(f"{selectedDisplayName} ile sohbet edin!"):
        # Kullanıcı mesajının eklenmesi
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Kullanıcı mesajının görüntülenmesi
        with st.chat_message("user"):
            st.markdown(prompt)

        # Yapay zekadan cevap alınması
        with st.chat_message("assistant"):
            placeholder = st.empty()
            try:
                fullResponse = st.session_state.chatInterface.generateResponse(
                    st.session_state.messages
                )
                placeholder.markdown(fullResponse)

            except Exception as e:
                placeholder.error(
                    f"Yanıt oluşturulurken bir hata oluştu. Hata kodu: {e}"
                )
                fullResponse = (
                    f"Üzgünüm. Size şu anda yanıt veremiyorum. Hata kodu: {e}"
                )

        # Yapay zeka cevabının görüntülenmesi
        st.session_state.messages.append({"role": "assistant", "content": fullResponse})

        # Sohbetin kayıt edilmesi
        ConversationManager.saveConversation(
            st.session_state.conversationId, st.session_state.messages, selectedModel
        )


if __name__ == "__main__":
    main()
