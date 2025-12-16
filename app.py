import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(
    page_title="프롬프트 개선 테스트",
    page_icon="🤑",
    layout="wide"
)

# CSS 스타일 적용
st.markdown("""
<style>
    .stApp {
        background-color: #f5f5f5;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        line-height: 1.5;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
    }
    .bot-message {
        background-color: #f3e5f5;
        border-left: 5px solid #9c27b0;
    }
    .main-title {
        color: #6a1b9a;
        text-align: center;
        padding: 2rem 0;
        font-size: 2.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .description {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# 제목과 설명
st.markdown('<h1 class="main-title">프롬프트 개선 테스트</h1>', unsafe_allow_html=True)
st.markdown('<p class="description">프롬프트 개선 테스트용 페이지입니다.</p>', unsafe_allow_html=True)

# Gemini API 설정
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("API 키를 설정해주세요! (.streamlit/secrets.toml 파일에 GOOGLE_API_KEY를 추가해주세요)")
    st.stop()

# 모델 설정
model = genai.GenerativeModel('gemini-1.5-flash')

# 세션 상태 초기화
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []
    # 초기 메시지 추가
    initial_message = "프롬프트를 입력해주세요"
    st.session_state.messages.append({"role": "assistant", "content": initial_message})

# 채팅 히스토리 표시
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-message user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message bot-message">🧙‍♀️ {message["content"]}</div>', unsafe_allow_html=True)

# 사용자 입력
user_input = st.text_input("문제나 답변을 입력해주세요", key="user_input", placeholder="여기에 입력하세요...")

if user_input:
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 챗봇 프롬프트 설정
    prompt = """
    ## Role & Objective
당신은 Google Gemini API 및 LLM 활용에 통달한 **'수석 프롬프트 엔지니어(Chief Prompt Engineer)'**입니다. 
당신의 목표는 사용자가 입력한 불완전하거나 단순한 프롬프트를 분석하여, Google의 공식 [Prompting Strategies] 가이드라인에 부합하는 **'최적화된 프롬프트'**로 재작성해주는 것입니다.

## Optimization Guidelines (Google AI Docs 기반)
사용자의 프롬프트를 개선할 때는 다음의 핵심 전략을 반드시 적용하십시오:

1. **명확한 지시 (Clear Instructions):** 모호한 표현을 제거하고, 모델이 수행해야 할 작업을 구체적으로 명시합니다.
2. **페르소나 부여 (Adopt a Persona):** 모델이 어떤 관점에서 응답해야 하는지 역할(Role)을 부여합니다.
3. **구분자 사용 (Use Delimiters):** 지시사항, 문맥, 입력 데이터를 명확히 구분하기 위해 특수 기호(```, """, ---, <tag> 등)를 사용합니다.
4. **단계적 사고 유도 (Chain of Thought):** 복잡한 작업의 경우 "단계별로 생각하라(Think step-by-step)"는 지시를 추가하여 논리적 추론을 강화합니다.
5. **퓨샷 프롬프팅 (Few-shot Prompting):** 필요한 경우, 입력과 출력의 예시(Example)를 구조에 포함시킬 수 있도록 템플릿화합니다.
6. **출력 형식 지정 (Output Formatting):** 결과물이 어떤 형식(Markdown, JSON, Table 등)으로 나와야 하는지 명시합니다.

## Operational Process
1. **의도 파악:** 사용자가 입력한 프롬프트의 핵심 목표와 요구사항을 분석합니다.
2. **약점 진단:** 현재 프롬프트에서 부족한 점(맥락 부재, 모호함, 구조 부족 등)을 식별합니다.
3. **재작성 (Refinement):** 위의 'Optimization Guidelines'를 적용하여 프롬프트를 전문적인 구조로 재작성합니다.
4. **설명 제공:** 왜 이렇게 수정했는지, 어떤 전략이 적용되었는지 간략히 설명합니다.

## Output Format
당신의 답변은 항상 다음의 구조를 따라야 합니다:

---
### 🔍 분석 및 개선 포인트
* **적용된 전략:** (예: 페르소나 부여, 구조화, 단계적 사고 등)
* **개선 이유:** (원문에서 부족했던 점과 보완된 내용 간략 설명)

### ✨ 최적화된 프롬프트 (Copy & Paste)
```markdown
# Role
[모델에게 부여할 역할]

# Context
[작업의 배경 및 상황 설명]

# Task
[구체적인 작업 지시 사항]

# Constraints
[제약 조건: 길이, 스타일, 하지 말아야 할 것 등]

# Output Format
[원하는 출력 형식]

# Input Data
{{사용자가 입력할 데이터}}
"""

    try:
        # Gemini 모델에 메시지 전송
        response = st.session_state.chat.send_message(f"{prompt}\n\n사용자: {user_input}")
        assistant_message = response.text
        
        # 챗봇 메시지 추가
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        
        # 입력창 초기화를 위한 rerun
        st.rerun()
        
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
