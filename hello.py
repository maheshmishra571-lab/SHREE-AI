import streamlit as st
from google import genai

# आपकी वर्किंग API Key
API_KEY = "AIzaSyBBRyroI02aSSPSIF0URTVs4M_Ys3zURWo"

# Gemini क्लाइंट सेटअप
client = genai.Client(api_key=API_KEY)

# वेबसाइट का नाम और डिज़ाइन सेट करना
st.set_page_config(page_title="SHREE AI", page_icon="📚", layout="centered")
st.title("📚 SHREE AI")
st.subheader("आपका अपना AI शिक्षक (सभी कोर्सेज के लिए)")
st.write("नमस्ते! 'SHREE AI' में आपका हार्दिक स्वागत है|")

# चैट हिस्ट्री (याददाश्त) को स्टोर करने के लिए
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुरानी बातचीत को स्क्रीन पर दिखाना
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# छात्र से सवाल इनपुट लेना
if user_question := st.chat_input("अपना सवाल यहाँ टाइप करें... (जैसे: CTET क्या है?)"):
    
    # छात्र का सवाल स्क्रीन पर दिखाना
    with st.chat_message("user"):
        st.markdown(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    # AI से जवाब मांगना
    with st.chat_message("assistant"):
        with st.spinner("Waiting For Response..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_question,
                    config={
                        'system_instruction': "तुम 'SHREE AI' के एक बेहद बुद्धिमान शिक्षक हो। तुम्हारा काम हर कोर्स (जैसे CTET, UGC-NET, B.Ed आदि) के छात्रों के प्रश्नों का सटीक और आसान हिंदी में उत्तर देना है।"
                    }
                )
                ai_response = response.text
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"कुछ गड़बड़ हुई: {e}")