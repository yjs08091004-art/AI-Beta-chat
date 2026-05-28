import streamlit as st
import requests

st.set_page_config(page_title="AI 캐릭터 월드", page_icon="🎭")
st.title("🎭 캐릭터 AI 월드")

# API 키 가져오기
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Secrets에 GEMINI_API_KEY가 없습니다!")
    st.stop()

# 캐릭터 정의
CHARACTERS = {
    "이준서 (학생회장)": "너는 이준서야. 전교 1등에 까칠한 학생회장. 츤데레 말투를 써.",
    "한소율 (반장)": "너는 한소율이야. 밝고 다정한 반장. 항상 웃으면서 말해.",
    "루시안 (공작)": "너는 루시안이야. 차갑고 고독한 밤의 공작."
}

selected_char = st.sidebar.selectbox("캐릭터 선택", list(CHARACTERS.keys()))

if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅창 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 메시지 전송 로직 (공식 라이브러리 없이 직접 통신)
if user_input := st.chat_input("메시지 입력..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            # 💡 구글 API 직통 호출 (v1beta 규격)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            # 대화 데이터 구성
            payload = {
                "contents": [{
                    "parts": [{"text": f"System: {CHARACTERS[selected_char]}\nUser: {user_input}"}]
                }]
            }
            
            # 직접 요청 보내기
            response = requests.post(url, json=payload)
            res_data = response.json()
            
            # 답변 파싱
            ai_text = res_data['candidates'][0]['content']['parts'][0]['text']
            
            st.write(ai_text)
            st.session_state.messages.append({"role": "assistant", "content": ai_text})
        except Exception as e:
            st.error(f"통신 에러: {e}")
