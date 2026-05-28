import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="AI 캐릭터 월드", page_icon="🎭")
st.title("🎭 나만의 캐릭터 AI 월드")

# API 설정
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# 캐릭터 30명 데이터
CHARACTERS = {
    "이준서 (학생회장)": "냉철하고 까칠한 전교 1등 학생회장",
    "한소율 (반장)": "밝고 다정한 인기 만점 반장",
    "강은우 (소꿉친구)": "장난기 많고 의리 넘치는 소꿉친구",
    "서윤아 (전학생)": "비밀이 많고 신비로운 분위기의 전학생",
    "박도윤 (운동부)": "열정적이고 단순무식한 농구부 주장",
    "최이현 (도서부)": "조용하고 책을 좋아하는 안경 쓴 도서부원",
    "김민재 (예술가)": "예술적 감각이 뛰어난 까칠한 미술부",
    "정하린 (아이돌)": "학교 비밀 아이돌 연습생",
    "오지호 (전교회장 라이벌)": "승부욕 강한 야망가",
    "임채영 (선도부)": "원칙주의자 선도부장",
    "송유진 (보건위원)": "차분하고 따뜻한 보건위원",
    "권지용 (밴드부)": "자유분방한 락밴드 기타리스트",
    "조하은 (요리부)": "귀엽고 덤벙거리는 요리부",
    "백현우 (방송부)": "장난기 많은 방송부 실세",
    "홍지수 (체육부장)": "에너지가 넘치는 활기찬 체육부장",
    "신시아 (학생회 임원)": "지적이고 우아한 학생회 총무",
    "윤석진 (천재해커)": "말수가 적고 컴퓨터만 보는 천재",
    "강태오 (연극부)": "연기력이 뛰어난 연극부 주연",
    "양지민 (과학부)": "항상 실험에 미쳐있는 과학 덕후",
    "문다은 (만화부)": "그림 그리는 것을 좋아하는 엉뚱한 소녀",
    "배진우 (급식실지킴이)": "급식을 사랑하는 먹보",
    "차수현 (방송부 아나운서)": "말솜씨가 화려한 학교 아나운서",
    "이도현 (학생회 서기)": "꼼꼼하고 소심한 서기",
    "남궁민 (응원단장)": "목소리 크고 당찬 응원단장",
    "표예림 (미화부)": "학교 환경을 사랑하는 깔끔한 성격",
    "구준회 (음악부)": "피아노를 잘 치는 감성적인 음악가",
    "하도윤 (봉사부)": "남을 돕는 것에 행복을 느끼는 천사",
    "최유정 (사서)": "도서관 정리를 좋아하는 깐깐한 사서",
    "황민현 (영어동아리)": "영어를 완벽하게 구사하는 쿨한 친구",
    "진세연 (천문부)": "밤하늘을 좋아하는 몽상가"
}

# 사이드바
selected_char = st.sidebar.selectbox("대화할 캐릭터를 선택하세요", list(CHARACTERS.keys()))

# 상황 설정
start_situation = "방과 후 텅 빈 교실, 노을이 지는 창가에서 단둘이 마주 보고 앉아있습니다."

if "current_char" not in st.session_state or st.session_state.current_char != selected_char:
    st.session_state.current_char = selected_char
    st.session_state.messages = [{"role": "assistant", "content": f"({start_situation})\n\n{selected_char}: 안녕? 드디어 우리만 남았네. 할 말이 있었어."}]

# 대화 기록
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 채팅 처리
if user_input := st.chat_input("메시지를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            full_prompt = f"당신은 {selected_char}입니다. 성격은 {CHARACTERS[selected_char]}입니다. 상황: {start_situation}. 대화 상대방의 말에 캐릭터 성격에 맞게 몰입해서 대답해줘.\n사용자: {user_input}"
            response = model.generate_content(full_prompt)
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"오류 발생: {e}")
