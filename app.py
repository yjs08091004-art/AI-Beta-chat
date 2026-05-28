import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="캐릭터 AI 월드", page_icon="🎭")
st.title("🎭 나만의 캐릭터 AI 월드")

# 2. API 설정 (Secrets 확인)
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Secrets 설정에서 GEMINI_API_KEY를 먼저 입력하세요!")
    st.stop()

# 3. 모델 호출 (404 방지를 위해 라이브러리 직접 호출)
genai.configure(api_key=api_key)
# 'models/'를 붙이지 마세요!
model = genai.GenerativeModel("gemini-1.5-flash")

# 4. 캐릭터 데이터
CHARACTERS = {
    "이준서 (학생회장)": "너는 냉철하고 까칠한 전교 1등 학생회장이야.",
    "한소율 (반장)": "너는 밝고 다정한 인기 만점 반장이야.",
    "강은우 (소꿉친구)": "너는 장난기 많고 의리 넘치는 소꿉친구야."
    # 나머지 27명은 나중에 딕셔너리에 추가하면 돼!
}

# 5. UI 로직
selected_char = st.sidebar.selectbox("캐릭터 선택", list(CHARACTERS.keys()))

if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 기록 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. 채팅 처리
if user_input := st.chat_input("메시지 입력..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            # 💡 모델 호출 부분
            prompt = f"{CHARACTERS[selected_char]}\n사용자: {user_input}"
            response = model.generate_content(prompt)
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"오류: {e}")
