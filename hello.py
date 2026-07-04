import streamlit as st
from google import genai
import openai

st.set_page_config(page_title="SHREE AI PLUS", page_icon="📚")
st.title("📚 SHREE AI PLUS")
st.subheader("आपका अपना एडवांस AI शिक्षक (Gemini + ChatGPT Engine)")
st.write("नमस्ते! 'SHREE AI PLUS' में आपका स्वागत है। यहाँ दोनों बेहतरीन AI मिलकर काम करते हैं।")

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

    # AI से जवाब जेनरेट करना
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # चरण 1: पहले Google Gemini (Flash Engine) से प्रयास करें
        try:
            gemini_key = st.secrets["GEMINI_API_KEY"]
            client = genai.Client(api_key=gemini_key)
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_question,
            )
            ai_response = response.text
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as gemini_error:
            # चरण 2: अगर Gemini में कोई दिक्कत आए, तो तुरंत ChatGPT पर स्विच करें
            try:
                # ध्यान दें: इसके लिए आपके Secrets में OPENAI_API_KEY भी होनी चाहिए
                openai.api_key = st.secrets["OPENAI_API_KEY"]
                
                response = openai.chat.completions.create(
                    model="gpt-4o-mini", # सबसे तेज़ और बेहतरीन मॉडल
                    messages=[{"role": "user", "content": user_question}]
                )
                ai_response = response.choices[0].message.content
                message_placeholder.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as openai_error:
                # अगर दोनों ही इंजन इस समय काम नहीं कर रहे हैं
                error_msg = "⚠️ *सभी AI शिक्षक अभी व्यस्त हैं। कृपया 1 मिनट बाद दोबारा प्रयास करें!*"
                message_placeholder.markdown(error_msg)
