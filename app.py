import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="AI 캐릭터 월드", page_icon="🎭")
st.title("🎭 캐릭터 AI 월드")

# API 키 설정
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("Secrets에 GEMINI_API_KEY를 등록해 주세요!")
        st.stop()
except Exception as e:
    st.error(f"설정 오류: {e}")
    st.stop()

# 캐릭터 정의
CHARACTERS = {
    "이준서 (학생회장)": "너는 이준서야. 냉철하고 까칠한 전교 1등 학생회장. 츤데레 말투를 사용해.",
    "한소율 (반장)": "너는 한소율이야. 밝고 다정한 인기 만점 반장. 항상 웃으면서 말해.",
    "루시안 (공작)": "너는 루시안이야. 차갑고 고독한 밤의 공작. 비밀스러운 로판 주인공처럼 말해."
}

# 사이드바 선택
selected_char = st.sidebar.selectbox("캐릭터 선택", list(CHARACTERS.keys()))

# 세션 관리
if "messages" not in st.session_state:
    st.session_state.messages = []

# 캐릭터 변경 시 초기화
if "current_char" not in st.session_state or st.session_state.current_char != selected_char:
    st.session_state.current_char = selected_char
    st.session_state.messages = [{"role": "assistant", "content": f"안녕, 나는 {selected_char}야. 무슨 일 있어?"}]

# 이전 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 채팅 입력 처리
if user_input := st.chat_input("메시지 입력..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            # 💡 404 방지: 모델 경로를 정확히 지정하고 generate_content 사용
            model = genai.GenerativeModel("models/gemini-1.5-flash")
            
            # 이전 대화와 시스템 설정을 합친 프롬프트 생성
            context = f"System: {CHARACTERS[selected_char]}\n"
            for msg in st.session_state.messages[:-1]:
                context += f"{msg['role']}: {msg['content']}\n"
            
            full_prompt = context + f"user: {user_input}"
            
            # 답변 생성
            response = model.generate_content(full_prompt)
            
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"대화 중 오류 발생: {e}")
