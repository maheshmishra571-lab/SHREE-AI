import streamlit as st
from google import genai
from google.genai import types
from openai import OpenAI

st.set_page_config(page_title="SHREE AI UNIVERSAL", page_icon="🌐", layout="wide")
st.title("🌐 SHREE AI UNIVERSAL")
st.subheader("आपका अपना सर्वज्ञानी AI सहायक (Universal Knowledge Engine)")
st.write("नमस्ते! आप मुझसे किसी भी विषय, परीक्षा, बिज़नेस, या सामान्य ज्ञान से जुड़ा सवाल पूछ सकते हैं।")

# चैट हिस्ट्री सेटअप
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुरानी बातचीत दिखाना
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# यूजर से किसी भी क्षेत्र का सवाल इनपुट लेना
if user_question := st.chat_input("कोई भी सवाल यहाँ टाइप करें (जैसे- होटल मैनेजमेंट, UGC-NET, या कोई भी सामान्य ज्ञान)..."):
    with st.chat_message("user"):
        st.markdown(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    # AI से जवाब जेनरेट करना
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # 1. Google Gemini (सर्वव्यापी ज्ञान के लिए)
        try:
            gemini_key = st.secrets["GEMINI_API_KEY"]
            client = genai.Client(api_key=gemini_key)
            
            # यहाँ हमने AI को हर क्षेत्र का एक्सपर्ट बना दिया है
            config = types.GenerateContentConfig(
                system_instruction=(
                    "आप एक अत्यंत बुद्धिमान, सर्वज्ञानी और अनुभवी यूनिवर्सल AI सहायक हैं। "
                    "आपके पास शिक्षा (CTET, UGC-NET), व्यापार, होटल व प्रॉपर्टी मैनेजमेंट, भारतीय रेलवे, "
                    "मानव अधिकार, इतिहास और विज्ञान समेत हर क्षेत्र का गहरा ज्ञान है। "
                    "यूज़र के सवाल के अनुसार, उस क्षेत्र के विशेषज्ञ की तरह बिल्कुल सटीक, व्यावहारिक "
                    "और उच्च गुणवत्ता (High Ranking) वाला उत्तर बिंदुवार (Bullet Points) हिंदी में दें।"
                ),
                temperature=0.3, # इससे जवाब भटकेगा नहीं, हमेशा सटीक रहेगा
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
            # 2. बैकअप: ChatGPT (Universal Backup)
            try:
                openai_key = st.secrets["OPENAI_API_KEY"]
                openai_client = OpenAI(api_key=openai_key)
                
                response = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system", 
                            "content": "आप एक सर्वज्ञानी और सर्वश्रेष्ठ AI सहायक हैं। किसी भी क्षेत्र के सवाल का सबसे सटीक और तार्किक उत्तर हिंदी में दें।"
                        },
                        {"role": "user", "content": user_question}
                    ],
                    temperature=0.3
                )
                ai_response = response.choices[0].message.content
                message_placeholder.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as openai_error:
                error_msg = "⚠️ *सभी AI विशेषज्ञ अभी व्यस्त हैं। कृपया 1 मिनट बाद दोबारा प्रयास करें!*"
                message_placeholder.markdown(error_msg)
