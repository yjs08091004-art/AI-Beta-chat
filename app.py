import streamlit as st
import requests

st.set_page_config(page_title="AI 캐릭터 월드", page_icon="🎭")
st.title("🎭 캐릭터 AI 월드")

api_key = st.secrets.get("GEMINI_API_KEY")

CHARACTERS = {
    "이준서": "너는 이준서야. 까칠한 전교 1등 학생회장.",
    "한소율": "너는 한소율이야. 밝고 다정한 반장.",
    "루시안": "너는 루시안이야. 차가운 공작."
}

selected_char = st.sidebar.selectbox("캐릭터 선택", list(CHARACTERS.keys()))

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("메시지 입력..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            # 💡 모델을 gemini-pro로 변경 (가장 에러 적음)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
            
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{
                    "role": "user",
                    "parts": [{"text": f"System: {CHARACTERS[selected_char]}\nUser: {user_input}"}]
                }]
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                res_data = response.json()
                ai_text = res_data['candidates'][0]['content']['parts'][0]['text']
                st.write(ai_text)
                st.session_state.messages.append({"role": "assistant", "content": ai_text})
            else:
                st.error(f"오류 발생: {response.text}")
                
        except Exception as e:
            st.error(f"통신 에러: {str(e)}")
