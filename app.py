import streamlit as st
import requests

st.set_page_config(page_title="AI 캐릭터 월드", page_icon="🎭")
st.title("🎭 캐릭터 AI 월드")

# API 키 가져오기
api_key = st.secrets.get("GEMINI_API_KEY")

# 캐릭터 정의 (일단 3명으로 확실하게 테스트!)
CHARACTERS = {
    "이준서": "너는 이준서야. 까칠한 전교 1등 학생회장.",
    "한소율": "너는 한소율이야. 밝고 다정한 반장.",
    "루시안": "너는 루시안이야. 차가운 공작."
}

selected_char = st.sidebar.selectbox("캐릭터 선택", list(CHARACTERS.keys()))

if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화창 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 채팅 입력 및 API 호출
if user_input := st.chat_input("메시지 입력..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            # 💡 중요: 구글 API 호출 주소와 규격을 최신형으로 교체
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            headers = {"Content-Type": "application/json"}
            
            # 구글이 요구하는 정확한 JSON 형식
            payload = {
                "contents": [{
                    "role": "user",
                    "parts": [{"text": f"System: {CHARACTERS[selected_char]}\nUser: {user_input}"}]
                }]
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                res_data = response.json()
                # candidates 구조를 타는 올바른 파싱
                ai_text = res_data['candidates'][0]['content']['parts'][0]['text']
                st.write(ai_text)
                st.session_state.messages.append({"role": "assistant", "content": ai_text})
            else:
                st.error(f"서버 응답 오류 (상태 코드 {response.status_code}): {response.text}")
                
        except Exception as e:
            st.error(f"통신 중 예외 발생: {str(e)}")
