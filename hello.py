import streamlit as st
from google import genai

# Secrets से API Key उठाना
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="SHREE AI", page_icon="📚")
st.title("📚 SHREE AI")
st.subheader("आपका अपना AI शिक्षक (सभी कोर्सेज के लिए)")
st.write("नमस्ते! 'SHREE AI' में आपका हार्दिक स्वागत है।")

# चैट हिस्ट्री सेटअप
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुरानी बातचीत दिखाना
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# छात्र से सवाल इनपुट लेना
if user_question := st.chat_input("अपना सवाल यहाँ टाइप करें (जैसे CTET क्या है?)"):
    with st.chat_message("user"):
        st.markdown(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    # AI से जवाब जेनरेट करना (एडवांस एरर हैंडलिंग के साथ)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # यहाँ एडवांस प्रो मॉडल सेट है
            response = client.models.generate_content(
                model='gemini-2.5-pro',
                contents=user_question,
            )
            ai_response = response.text
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            # कोटा खत्म होने पर यह सुंदर मैसेज दिखेगा
            error_msg = "⚠️ *शिक्षक अभी व्यस्त हैं (कोटा समाप्त)। कृपया 1 मिनट बाद दोबारा प्रयास करें!*"
            message_placeholder.markdown(error_msg)
