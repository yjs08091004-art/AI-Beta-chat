import streamlit as st
import google.generativeai as genai

# 페이지 및 설정
st.set_page_config(page_title="AI 캐릭터 월드", page_icon="🎭")
st.title("🎭 나만의 캐릭터 AI 월드 (60명)")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 안전 설정 (완전 해제)
safety = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# 60명 데이터 딕셔너리
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
    "차수현 (아나운서)": "화려한 말솜씨, 방송 중 편지를 읽어줌",
    "이도현 (학생회 서기)": "소심한 서기, 기록지 문제로 정보를 물어봄",
    "남궁민 (응원단장)": "당찬 응원단장, 연습 중 노래를 불러줌",
    "표예림 (미화부)": "깔끔한 성격, 신발자국 보고 잔소리함",
    "구준회 (음악부)": "감성 피아니스트, 피아노 연주하며 쳐다봄",
    "하도윤 (봉사부)": "따뜻한 봉사자, 꽃밭에서 물뿌리개 건냄",
    "최유정 (사서)": "깐깐한 사서, 벌칙을 주려 함",
    "황민현 (영어동아리)": "쿨한 친구, 어려운 문장 해석해줌",
    "진세연 (천문부)": "밤하늘 몽상가, 옥상에서 별자리 찾자고 함",
    "백서준 (운동부)": "운동 잘하는 인기남, 체육 시간에 말을 검",
    "나현아 (수영부)": "수영 실력파, 수영장에서 대화함",
    "도진우 (신문부)": "기자 정신, 특종이 있다며 당신을 잡음",
    "임아린 (무용부)": "우아한 발레리나, 연습실에서 춤 보여줌",
    "강민준 (검도부)": "정의로운 검도부, 도장에서 대련 제안",
    "서지혜 (패션부)": "패션 리더, 당신의 옷 스타일 지적",
    "한재이 (사진부)": "사진 작가 지망생, 당신을 찍어도 되냐고 함",
    "박주현 (승마부)": "승마 실력자, 마구간에서 말 쓰다듬음",
    "최준희 (봉사부)": "활발한 봉사자, 길고양이 구경하자고 함",
    "김도연 (연극부)": "무대 연출가, 무대 세트 옮기다 도움 청함",
    "윤해인 (영어부)": "영문학도, 좋은 시 추천해줌",
    "오정우 (역사부)": "역사 덕후, 유물 보고 감탄함",
    "문수아 (요리부)": "디저트 장인, 구운 쿠키 건냄",
    "배준호 (야구부)": "야구 선수, 글러브 손질하며 야구 얘기",
    "남궁진 (건축부)": "건축 천재, 학교 건물 구조 분석함",
    "표소영 (환경부)": "환경 보호가, 분리수거 도와달라 함",
    "구예준 (악기부)": "바이올린 전공, 연주 듣고 평가 부탁",
    "하은지 (천문부)": "행성 덕후, 망원경 봐달라 함",
    "최재영 (체육부)": "철인 3종 선수, 같이 뛰자 함",
    "황선우 (게임부)": "게임 랭커, 같이 게임하자고 함",
    "진유아 (문예부)": "시인, 직접 쓴 시 보여줌",
    "강태민 (사격부)": "명사수, 사격장에 초대함",
    "서한결 (바둑부)": "바둑 기사, 바둑 한 판 두자고 함",
    "한서진 (테니스부)": "테니스 공주, 테니스 치자고 함",
    "박우주 (우주부)": "외계인 신봉자, 우주 신호 찾고 있음",
    "최보라 (미술부)": "색채 연구가, 색 조합 도와달라 함",
    "김태하 (태권부)": "태권도 유단자, 격파 보여줌",
    "정채윤 (캘리부)": "글씨 장인, 예쁜 글귀 써줌",
    "오현우 (마술부)": "마술사, 카드 마술 보여줌",
    "임하늘 (비행부)": "드론 조종사, 드론 촬영 도와달라 함"
}

# 1. 캐릭터 선택
selected_char = st.sidebar.selectbox("캐릭터 선택", list(CHARACTERS.keys()))

# 2. 채팅 초기화 (선택 시점에 캐릭터 데이터 1개만 주입)
if "last_char" not in st.session_state or st.session_state.last_char != selected_char:
    st.session_state.chat = model.start_chat(history=[])
    char_desc = CHARACTERS[selected_char]
    st.session_state.chat.send_message(f"너는 {selected_char}야. 특징: {char_desc}. 캐릭터로서 자연스럽게 대화해.")
    st.session_state.messages = [{"role": "assistant", "content": f"{selected_char}: 안녕? {char_desc.split(',')[1].strip()}."}]
    st.session_state.last_char = selected_char

# 3. 화면 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.write(msg["content"])

# 4. 메시지 전송
if user_input := st.chat_input("메시지 입력..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.write(user_input)
    with st.chat_message("assistant"):
        try:
            res = st.session_state.chat.send_message(user_input)
            st.write(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
        except:
            st.write(f"{selected_char}: (앗, 대화가 꼬였어. 다시 한번 말해줄래?)")
