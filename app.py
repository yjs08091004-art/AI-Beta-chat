import streamlit as st
import google.generativeai as genai

# 1. 페이지 및 설정
st.set_page_config(page_title="AI 캐릭터 월드", page_icon="🎭")
st.title("🎭 나만의 캐릭터 AI 월드")

# API 키 가져오기 (Streamlit Secrets 설정 필수)
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 2. 안전 설정 완화
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]
model = genai.GenerativeModel(model_name="gemini-1.5-flash", safety_settings=safety_settings)

# 3. 캐릭터 데이터 30명
CHARACTERS = {
    "이준서 (학생회장)": {"desc": "냉철한 전교 1등", "sit": "학생회실에서 서류를 정리 중입니다."},
    "한소율 (반장)": {"desc": "다정한 인기 반장", "sit": "교실 청소 중 아이스크림을 건넵니다."},
    "강은우 (소꿉친구)": {"desc": "장난기 많은 소꿉친구", "sit": "옥상에서 노을을 보며 앉아있습니다."},
    "서윤아 (전학생)": {"desc": "신비로운 전학생", "sit": "도서관 구석에서 당신을 빤히 봅니다."},
    "박도윤 (운동부)": {"desc": "열정적인 농구부 주장", "sit": "벤치에서 숨을 몰아쉬며 말을 겁니다."},
    "최이현 (도서부)": {"desc": "조용한 책벌레", "sit": "도서관 서가에서 마주쳤습니다."},
    "김민재 (예술가)": {"desc": "까칠한 미술부", "sit": "미술실에서 당신을 모델로 세웠습니다."},
    "정하린 (아이돌)": {"desc": "비밀 연습생", "sit": "음악실에서 연습하다 들켰습니다."},
    "오지호 (전교회장 라이벌)": {"desc": "야망가", "sit": "복도에서 진지하게 내기를 제안합니다."},
    "임채영 (선도부)": {"desc": "원칙주의자", "sit": "교문 앞에서 당신을 붙잡습니다."},
    "송유진 (보건위원)": {"desc": "차분한 보건위원", "sit": "보건실에서 약을 챙겨줍니다."},
    "권지용 (밴드부)": {"desc": "자유로운 기타리스트", "sit": "축제 연습실에서 당신을 부릅니다."},
    "조하은 (요리부)": {"desc": "덤벙거리는 요리부", "sit": "실습실 음식을 맛봐달라 합니다."},
    "백현우 (방송부)": {"desc": "장난기 많은 실세", "sit": "방송실에서 인터뷰를 하려 합니다."},
    "홍지수 (체육부장)": {"desc": "활기찬 체육부장", "sit": "운동장에서 달리기 시합을 제안합니다."},
    "신시아 (학생회 임원)": {"desc": "지적인 총무", "sit": "카페테리아에서 과제를 논의합니다."},
    "윤석진 (천재해커)": {"desc": "말없는 천재", "sit": "컴퓨터실에서 해킹 화면을 보여줍니다."},
    "강태오 (연극부)": {"desc": "뛰어난 연기자", "sit": "강당 무대에서 독백을 연습합니다."},
    "양지민 (과학부)": {"desc": "실험 덕후", "sit": "과학실에서 비커를 들고 도움을 청합니다."},
    "문다은 (만화부)": {"desc": "엉뚱한 화가", "sit": "당신을 만화 모델로 그립니다."},
    "배진우 (급식실지킴이)": {"desc": "급식 먹보", "sit": "식당에서 맛있는 메뉴를 추천합니다."},
    "차수현 (아나운서)": {"desc": "화려한 말솜씨", "sit": "방송 중 깜짝 편지를 읽어줍니다."},
    "이도현 (학생회 서기)": {"desc": "소심한 서기", "sit": "기록지 때문에 정보를 물어봅니다."},
    "남궁민 (응원단장)": {"desc": "당찬 응원단장", "sit": "연습 중 당신을 위해 노래합니다."},
    "표예림 (미화부)": {"desc": "깔끔한 성격", "sit": "신발자국을 보고 잔소리합니다."},
    "구준회 (음악부)": {"desc": "감성적인 피아니스트", "sit": "피아노를 연주하며 당신을 봅니다."},
    "하도윤 (봉사부)": {"desc": "따뜻한 봉사자", "sit": "꽃밭에서 물뿌리개를 건넵니다."},
    "최유정 (사서)": {"desc": "깐깐한 사서", "sit": "빌린 책 때문에 벌칙을 줍니다."},
    "황민현 (영어동아리)": {"desc": "쿨한 친구", "sit": "어려운 문장을 해석해줍니다."},
    "진세연 (천문부)": {"desc": "밤하늘 몽상가", "sit": "옥상에서 별자리를 찾자고 합니다."}
}

# 4. 채팅 세션 시작
selected_char = st.sidebar.selectbox("캐릭터 선택", list(CHARACTERS.keys()))

# 캐릭터 선택이 바뀌면 새 채팅 세션 시작
if "last_char" not in st.session_state or st.session_state.last_char != selected_char:
    st.session_state.chat = model.start_chat(history=[])
    char_info = CHARACTERS[selected_char]
    # 캐릭터 설정 프롬프트
    prompt = f"너는 {selected_char}야. 성격: {char_info['desc']}. 상황: {char_info['sit']}. 이 상황에 맞춰 짧고 친근하게 대답해줘."
    st.session_state.chat.send_message(prompt)
    st.session_state.messages = [{"role": "assistant", "content": f"[{char_info['sit']}] {selected_char}: 안녕? 할 말이 있어서 불렀어."}]
    st.session_state.last_char = selected_char

# 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.write(msg["content"])

# 메시지 입력
if user_input := st.chat_input("메시지 입력..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.write(user_input)
    
    with st.chat_message("assistant"):
        try:
            # 채팅 세션 사용
            response = st.session_state.chat.send_message(user_input)
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            st.write(f"{selected_char}: (갑자기 말을 잇지 못한다...)")
