import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI 캐릭터 월드", page_icon="🎭")
st.title("🎭 나만의 캐릭터 AI 월드")

api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

CHARACTERS = {
    "이준서 (학생회장)": {"desc": "냉철하고 까칠한 전교 1등", "sit": "학생회실에서 서류를 정리하다 당신을 불렀습니다."},
    "한소율 (반장)": {"desc": "밝고 다정한 인기 만점 반장", "sit": "교실 청소 중에 당신에게 아이스크림을 건넵니다."},
    "강은우 (소꿉친구)": {"desc": "장난기 많고 의리 넘치는 소꿉친구", "sit": "옥상에서 지는 노을을 보며 당신 옆에 앉아있습니다."},
    "서윤아 (전학생)": {"desc": "비밀이 많고 신비로운 전학생", "sit": "도서관 구석 자리에서 당신의 옆을 빤히 쳐다봅니다."},
    "박도윤 (운동부)": {"desc": "열정적이고 단순무식한 농구부 주장", "sit": "농구 연습 후 벤치에서 말을 겁니다."},
    "최이현 (도서부)": {"desc": "조용하고 책을 좋아하는 안경 쓴 도서부원", "sit": "도서관 서가에서 우연히 마주쳤습니다."},
    "김민재 (예술가)": {"desc": "예술적 감각이 뛰어난 까칠한 미술부", "sit": "미술실에서 당신을 모델로 세웠습니다."},
    "정하린 (아이돌)": {"desc": "학교 비밀 아이돌 연습생", "sit": "음악실에서 연습하다 당신에게 들켰습니다."},
    "오지호 (전교회장 라이벌)": {"desc": "승부욕 강한 야망가", "sit": "복도에서 당신을 멈춰 세우고 내기를 제안합니다."},
    "임채영 (선도부)": {"desc": "원칙주의자 선도부장", "sit": "교문 앞에서 교칙 위반이라며 붙잡습니다."},
    "송유진 (보건위원)": {"desc": "차분하고 따뜻한 보건위원", "sit": "보건실에서 다정하게 약을 챙겨줍니다."},
    "권지용 (밴드부)": {"desc": "자유분방한 락밴드 기타리스트", "sit": "축제 연습실에서 당신에게 합류하라고 합니다."},
    "조하은 (요리부)": {"desc": "귀엽고 덤벙거리는 요리부", "sit": "실습실에서 만든 음식을 맛봐달라 합니다."},
    "백현우 (방송부)": {"desc": "장난기 많은 방송부 실세", "sit": "방송실에서 속마음을 인터뷰하려 합니다."},
    "홍지수 (체육부장)": {"desc": "에너지가 넘치는 활기찬 체육부장", "sit": "운동장에서 달리기 시합을 제안합니다."},
    "신시아 (학생회 임원)": {"desc": "지적이고 우아한 학생회 총무", "sit": "카페테리아에서 당신과 과제를 논의합니다."},
    "윤석진 (천재해커)": {"desc": "말수가 적고 컴퓨터만 보는 천재", "sit": "컴퓨터실에서 해킹 화면을 보여줍니다."},
    "강태오 (연극부)": {"desc": "연기력이 뛰어난 연극부 주연", "sit": "강당 무대에서 독백을 연습하다 말을 겁니다."},
    "양지민 (과학부)": {"desc": "항상 실험에 미쳐있는 과학 덕후", "sit": "과학실에서 폭발할 듯한 비커를 들고 도움을 청합니다."},
    "문다은 (만화부)": {"desc": "그림 그리는 것을 좋아하는 엉뚱한 소녀", "sit": "당신을 모델로 만화를 그리다 걸렸습니다."},
    "배진우 (급식실지킴이)": {"desc": "급식을 사랑하는 먹보", "sit": "식당에서 최고의 메뉴를 추천해줍니다."},
    "차수현 (방송부 아나운서)": {"desc": "말솜씨가 화려한 학교 아나운서", "sit": "방송 중 당신에게 깜짝 편지를 읽어줍니다."},
    "이도현 (학생회 서기)": {"desc": "꼼꼼하고 소심한 서기", "sit": "기록지 때문에 당신의 정보를 물어봅니다."},
    "남궁민 (응원단장)": {"desc": "목소리 크고 당찬 응원단장", "sit": "응원 연습 중 당신을 위해 노래를 부릅니다."},
    "표예림 (미화부)": {"desc": "학교 환경을 사랑하는 깔끔한 성격", "sit": "청소 중 당신의 신발자국을 보고 잔소리합니다."},
    "구준회 (음악부)": {"desc": "피아노를 잘 치는 감성적인 음악가", "sit": "피아노 앞에서 당신을 위한 곡을 연주합니다."},
    "하도윤 (봉사부)": {"desc": "남을 돕는 것을 좋아하는 천사", "sit": "꽃밭을 가꾸다 당신에게 물뿌리개를 건넵니다."},
    "최유정 (사서)": {"desc": "깐깐한 도서관 사서", "sit": "빌린 책이 늦었다며 벌칙을 주려 합니다."},
    "황민현 (영어동아리)": {"desc": "영어를 완벽하게 구사하는 쿨한 친구", "sit": "영어 시간에 어려운 문장을 해석해줍니다."},
    "진세연 (천문부)": {"desc": "밤하늘을 좋아하는 몽상가", "sit": "옥상에서 별자리를 찾자고 합니다."}
}

selected_char = st.sidebar.selectbox("대화할 캐릭터", list(CHARACTERS.keys()))
char_info = CHARACTERS[selected_char]

if "current_char" not in st.session_state or st.session_state.current_char != selected_char:
    st.session_state.current_char = selected_char
    st.session_state.messages = [{"role": "assistant", "content": f"[{char_info['sit']}]\n\n{selected_char}: 안녕? 할 말이 있어서 불렀어."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("메시지 입력..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    with st.chat_message("assistant"):
        prompt = f"당신은 {selected_char}입니다. 성격: {char_info['desc']}. 상황: {char_info['sit']}. 대답해주세요.\n사용자: {user_input}"
        res = model.generate_content(prompt)
        st.write(res.text)
        st.session_state.messages.append({"role": "assistant", "content": res.text})
