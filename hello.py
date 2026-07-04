import streamlit as st
from google import genai

# दोनों टीचर्स (Flash और Pro) के लिए क्लाइंट सेटअप
@st.cache_resource
def get_genai_client():
    API_KEY = st.secrets["GEMINI_API_KEY"]
    return genai.Client(api_key=API_KEY)

client = get_genai_client()

st.set_page_config(page_title="SHREE AI", page_icon="📚")
st.title("📚 SHREE AI")
st.subheader("आपका अपना AI शिक्षक (Dual-Engine System)")
st.write("नमस्ते! 'SHREE AI' में आपका हार्दिक स्वागत है। यहाँ दो AI टीचर्स मिलकर आपके सवालों का जवाब देते हैं।")

# चैट हिस्ट्री सेटअप
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुरानी बातचीत दिखाना
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# छात्र से सवाल इनपुट लेना
if user_question := st.chat_input("अपना सवाल यहाँ टाइप करें..."):
    with st.chat_message("user"):
        st.markdown(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    # AI टीचर्स से जवाब जेनरेट करना
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # चरण 1: पहले "प्राइमरी AI शिक्षक" (Flash) से जवाब लेने का प्रयास
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_question,
            )
            ai_response = response.text
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e_flash:
            # चरण 2: अगर पहला शिक्षक व्यस्त है, तो तुरंत "सीनियर AI शिक्षक" (Pro) को काम पर लगाएं
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-pro',
                    contents=user_question,
                )
                ai_response = response.text
                message_placeholder.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e_pro:
                # अगर दोनों ही टीचर्स का कोटा इस समय फुल है
                error_msg = "⚠️ *दोनों AI शिक्षक अभी व्यस्त हैं। कृपया 1 मिनट का इंतज़ार करें और दोबारा प्रयास करें!*"
                message_placeholder.markdown(error_msg)
