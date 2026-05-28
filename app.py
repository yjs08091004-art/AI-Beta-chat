import streamlit as st
import google.generativeai as genai
import os

# 1. 페이지 설정
st.set_page_config(page_title="캐릭터 AI 월드", page_icon="🎭")
st.title("🎭 나만의 캐릭터 AI 월드")

# 2. API 설정
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Secrets 설정에서 GEMINI_API_KEY를 확인하세요!")
    st.stop()

# 최신 방식으로 설정
genai.configure(api_key=api_key)

# 3. 모델 호출 (404 방지를 위해 라이브러리 직접 호출)
model = genai.GenerativeModel("gemini-1.5-flash")

# 4. 캐릭터 리스트
CHARACTERS = {
    "이준서 (학생회장)": "너는 냉철하고 까칠한 전교 1등 학생회장이야.",
    "한소율 (반장)": "너는 밝고 다정한 인기 만점 반장이야.",
    "강은우 (소꿉친구)": "너는 장난기 많고 의리 넘치는 소꿉친구야."
}

selected_char = st.sidebar.selectbox("캐릭터 선택", list(CHARACTERS.keys()))

# 5. 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 캐릭터 변경 시 대화 초기화
if "current_char" not in st.session_state or st.session_state.current_char != selected_char:
    st.session_state.current_char = selected_char
    st.session_state.messages = [{"role": "assistant", "content": f"안녕? 나는 {selected_char}야."}]

# 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. 채팅 입력
if user_input := st.chat_input("메시지를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            # 💡 호출 방식 최적화
            full_prompt = f"당신은 {selected_char}입니다. {CHARACTERS[selected_char]} 대화 상대방의 질문에 맞게 대답하세요. 질문: {user_input}"
            response = model.generate_content(full_prompt)
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"오류: {e}")
