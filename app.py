import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="AI 캐릭터 월드", page_icon="🏫")
st.title("🏫 여고의 유일한 남학생")

# 2. API 및 모델 설정 (가장 상단에 배치하여 에러 방지)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# 3. 데이터 구조: 여기서 에러가 나는 것을 방지하기 위해 딕셔너리를 더 짧게 작성
CHARACTERS = {
    "이준서": "학생회장", "한소율": "반장", "강은우": "소꿉친구", "서윤아": "전학생", "박도윤": "농구부",
    "최이현": "책벌레", "김민재": "미술부", "정하린": "연습생", "오지호": "라이벌", "임채영": "선도부",
    "송유진": "보건위원", "권지용": "기타리스트", "조하은": "요리부", "백현우": "방송부", "홍지수": "체육부장",
    "신시아": "총무", "윤석진": "해커", "강태오": "연극부", "양지민": "과학부", "문다은": "화가",
    "배진우": "급식먹보", "차수현": "아나운서", "이도현": "서기", "남궁민": "응원단장", "표예림": "미화부",
    "구준회": "피아니스트", "하도윤": "봉사자", "최유정": "사서", "황민현": "영어부", "진세연": "천문부",
    "백서준": "운동부", "나현아": "수영부", "도진우": "신문부", "임아린": "발레리나", "강민준": "검도부",
    "서지혜": "패션리더", "한재이": "사진작가", "박주현": "승마부", "최준희": "봉사부", "김도연": "연출가",
    "지수": "여고생", "민아": "여고생", "연우": "여고생", "채린": "여고생", "서희": "여고생",
    "하윤": "여고생", "지안": "여고생", "윤서": "여고생", "다은": "여고생", "수아": "여고생",
    "아린": "여고생", "은지": "여고생", "채윤": "여고생", "현우": "여고생", "도희": "여고생",
    "세아": "여고생", "해인": "여고생", "수민": "여고생", "소영": "여고생", "보라": "여고생"
}

# 4. 캐릭터 선택
selected_name = st.sidebar.selectbox("캐릭터 선택", list(CHARACTERS.keys()))

# 5. 세션 관리: 캐릭터 변경 시에만 딱 1번만 프롬프트 전송
if "last_name" not in st.session_state or st.session_state.last_name != selected_name:
    st.session_state.chat = model.start_chat(history=[])
    role = CHARACTERS[selected_name]
    # 모델에 "딱 이 캐릭터 정보"만 전달하여 데이터 과부하 방지
    prompt = f"너는 여고생 {selected_name}({role})야. 우리 학교는 여고인데, 유일한 남학생인 나와 대화하고 있어. 나를 보면 신기해하고 호기심을 보여줘."
    st.session_state.chat.send_message(prompt)
    st.session_state.messages = [{"role": "assistant", "content": f"{selected_name}: 어? 여기 여고인데 남학생이 있네? 신기하다!"}]
    st.session_state.last_name = selected_name

# 6. 채팅 화면 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.write(msg["content"])

# 7. 메시지 입력 및 전송
if user_input := st.chat_input("메시지 입력..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.write(user_input)
    
    with st.chat_message("assistant"):
        try:
            # chat 세션을 통해 모델 응답 생성
            res = st.session_state.chat.send_message(user_input)
            st.write(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
        except Exception as e:
            st.error("대화 생성 중 오류가 발생했습니다. 다시 시도해주세요.")
