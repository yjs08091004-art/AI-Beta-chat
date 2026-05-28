import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI 캐릭터 월드", page_icon="🎭")
st.title("🎭 캐릭터 AI 월드")

# API 키 설정
api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 캐릭터 설정
CHARACTERS = {
    "이준서": "너는 이준서야. 까칠한 학생회장.",
    "한소율": "너는 한소율이야. 다정한 반장.",
    "루시안": "너는 루시안이야. 차가운 공작."
}

selected_char = st.sidebar.selectbox("캐릭터 선택", list(CHARACTERS.keys()))

if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅창 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 메시지 전송 로직
if user_input := st.chat_input("메시지 입력..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            # 모델 설정 (가장 표준적인 호출 방식)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # 대화 기록과 시스템 명령 합치기
            chat = model.start_chat(history=[])
            prompt = f"System: {CHARACTERS[selected_char]}\nUser: {user_input}"
            
            # 응답 받기
            response = chat.send_message(prompt)
            
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"대화 오류: {e}")
