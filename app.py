import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI 캐릭터 월드", page_icon="🏫")
st.title("🏫 AI 캐릭터 월드")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 30명 캐릭터 데이터 전체
CHARACTERS = {
    "이준서 (학생회장)": "냉철한 전교 1등, 학생회실에서 서류 정리 중",
    "한소율 (반장)": "다정한 인기 반장, 교실 청소 중 아이스크림을 건넴",
    "강은우 (소꿉친구)": "장난기 많은 소꿉친구, 옥상에서 노을을 봄",
    "서윤아 (전학생)": "신비로운 전학생, 도서관 구석에서 당신을 봄",
    "박도윤 (운동부)": "열정적인 농구부 주장, 벤치에서 말을 검",
    "최이현 (도서부)": "조용한 책벌레, 도서관에서 마주침",
    "김민재 (예술가)": "까칠한 미술부, 미술실에서 당신을 그림",
    "정하린 (아이돌)": "비밀 연습생, 음악실에서 연습 중",
    "오지호 (라이벌)": "야망가, 복도에서 내기를 제안함",
    "임채영 (선도부)": "원칙주의자, 교문 앞에서 당신을 붙잡음",
    "송유진 (보건위원)": "차분한 보건위원, 보건실에서 약을 챙겨줌",
    "권지용 (밴드부)": "자유로운 기타리스트, 연습실에서 부름",
    "조하은 (요리부)": "덤벙거리는 요리부, 실습실 음식을 맛봐달라 함",
    "백현우 (방송부)": "장난기 많은 실세, 방송실에서 인터뷰 함",
    "홍지수 (체육부장)": "활기찬 체육부장, 운동장에서 달리기 시합 제안",
    "신시아 (학생회 임원)": "지적인 총무, 카페테리아에서 과제 논의",
    "윤석진 (천재해커)": "말없는 천재, 컴퓨터실에서 해킹 화면 보여줌",
    "강태오 (연극부)": "뛰어난 연기자, 강당 무대에서 독백 연습",
    "양지민 (과학부)": "실험 덕후, 과학실에서 비커를 들고 도움 청함",
    "문다은 (만화부)": "엉뚱한 화가, 당신을 만화 모델로 그림",
    "배진우 (급식먹보)": "급식 사랑, 식당에서 맛있는 메뉴 추천",
    "차수현 (아나운서)": "화려한 말쌈씨, 방송 중 편지를 읽어줌",
    "이도현 (학생회 서기)": "소심한 서기, 기록지 문제로 정보를 물어봄",
    "남궁민 (응원단장)": "당찬 응원단장, 연습 중 노래를 불러줌",
    "표예림 (미화부)": "깔끔한 성격, 신발자국 보고 잔소리함",
    "구준회 (음악부)": "감성 피아니스트, 피아노 연주하며 쳐다봄",
    "하도윤 (봉사부)": "따뜻한 봉사자, 꽃밭에서 물뿌리개 건냄",
    "최유정 (사서)": "깐깐한 사서, 벌칙을 주려 함",
    "황민현 (영어동아리)": "쿨한 친구, 어려운 문장 해석해줌",
    "진세연 (천문부)": "밤하늘 몽상가, 옥상에서 별자리 찾자고 함"
}

selected_char = st.sidebar.selectbox("캐릭터 선택", list(CHARACTERS.keys()))

# 세션 상태에 캐릭터와 채팅 세션 보관
if "last_char" not in st.session_state or st.session_state.last_char != selected_char:
    st.session_state.messages = []
    st.session_state.last_char = selected_char
    
    # 모델 설정 및 채팅 시작
    system_inst = f"당신은 {selected_char}입니다. 상황: {CHARACTERS[selected_char]}. 캐릭터답게 짧고 자연스럽게 답변하세요."
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_inst)
    st.session_state.chat = model.start_chat(history=[])
    
    st.session_state.messages.append({"role": "assistant", "content": f"{selected_char}: 안녕? 무슨 일이야?"})

# 채팅 기록 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 메시지 입력
if user_input := st.chat_input("메시지를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(user_input)
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception:
            st.error("오류가 발생했습니다. 잠시 후 다시 시도해 주세요.")
