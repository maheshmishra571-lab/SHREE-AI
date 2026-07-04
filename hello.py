import streamlit as st
from google import genai
from google.genai import types
from openai import OpenAI

st.set_page_config(page_title="SHREE AI PLUS", page_icon="📚", layout="wide")
st.title("📚 SHREE AI PLUS")
st.subheader("सुपर-फ़ास्ट AI शिक्षक (High-Quality Engine)")
st.write("नमस्ते! यहाँ आपको सबसे तेज़ और सबसे सटीक जवाब मिलेंगे।")

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
        
        # 1. पहले Google Gemini (Flash 2.5) से प्रयास करें - यह सबसे तेज़ है
        try:
            gemini_key = st.secrets["GEMINI_API_KEY"]
            client = genai.Client(api_key=gemini_key)
            
            # रैंकिंग बढ़ाने के लिए प्रोम्प्ट निर्देश देना
            config = types.GenerateContentConfig(
                system_instruction="आप एक अत्यंत ज्ञानी और अनुभवी शिक्षक हैं। छात्र के प्रश्नों का उत्तर बहुत ही स्पष्ट, सटीक, उच्च गुणवत्ता (High Ranking) और बिंदुवार (Bullet Points) हिंदी में दें।",
                temperature=0.3, # कम टेम्परेचर से सटीक जवाब आते हैं
            )
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_question,
                config=config
            )
            ai_response = response.text
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as gemini_error:
            # 2. बैकअप: अगर Gemini व्यस्त है, तो तुरंत ChatGPT (gpt-4o-mini) पर जाएँ
            try:
                openai_key = st.secrets["OPENAI_API_KEY"]
                openai_client = OpenAI(api_key=openai_key)
                
                response = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "आप एक सर्वश्रेष्ठ शिक्षक हैं। सटीक और उच्च गुणवत्ता वाला उत्तर हिंदी में दें।"},
                        {"role": "user", "content": user_question}
                    ],
                    temperature=0.3
                )
                ai_response = response.choices[0].message.content
                message_placeholder.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as openai_error:
                error_msg = "⚠️ *सभी AI शिक्षक अभी व्यस्त हैं। कृपया 1 मिनट बाद दोबारा प्रयास करें!*"
                message_placeholder.markdown(error_msg)
