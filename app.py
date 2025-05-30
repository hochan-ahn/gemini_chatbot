import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

try:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

if not GOOGLE_API_KEY:
    st.error("GEMINI_API_KEY 환경 변수가 설정되지 않았습니다. .streamlit/secrets.toml 또는 환경 변수를 확인해주세요.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

if "chat_model" not in st.session_state:
    st.session_state.chat_model = genai.GenerativeModel('gemini-1.5-flash')
    st.session_state.messages = []
    st.session_state.chat_session = st.session_state.chat_model.start_chat(history=[])

st.title("✨ 기본적인 챗봇 프레임워크")
st.markdown(
    """
    이 챗봇은 Google Gemini API(`gemini-1.5-flash` 모델)와 Streamlit을 기반으로 만들어진 **기본적인 채팅 프레임워크**입니다.
    대화 컨텍스트를 유지하며 질문에 답변합니다.
    """
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"])

if prompt := st.chat_input("메시지를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "parts": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("생각 중..."):
        try:
            response = st.session_state.chat_session.send_message(prompt)
            model_response_text = response.text
            st.session_state.messages.append({"role": "model", "parts": model_response_text})
            with st.chat_message("model"):
                st.markdown(model_response_text)
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
            st.session_state.messages.append({"role": "model", "parts": f"오류가 발생했습니다: {e}"})

if st.button("새로운 대화 시작"):
    st.session_state.messages = []
    st.session_state.chat_session = st.session_state.chat_model.start_chat(history=[])
    st.success("새로운 대화를 시작합니다.")
    st.rerun()
