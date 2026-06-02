import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI 캐릭터 월드", page_icon="🎭")
st.title("🎭 나만의 캐릭터 AI 월드")

# 보안 설정: 모든 필터 완전 해제
safety = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-flash", safety_settings=safety)

# 60명 캐릭터 데이터
CHARACTERS = {
    "이준서 (학생회장)": {"desc": "냉철한 전교 1등", "sit": "학생회실에서 서류 정리 중."},
    "한소율 (반장)": {"desc": "다정한 반장", "sit": "청소 중 아이스크림을 건넵니다."},
    "강은우 (소꿉친구)": {"desc": "장난기 많은 소꿉친구", "sit": "옥상에서 노을을 봅니다."},
    "서윤아 (전학생)": {"desc": "신비로운 전학생", "sit": "도서관 구석에서 당신을 봅니다."},
    "박도윤 (운동부)": {"desc": "농구부 주장", "sit": "벤치에서 땀을 닦으며 말을 겁니다."},
    "최이현 (도서부)": {"desc": "조용한 책벌레", "sit": "도서관 서가에서 마주쳤습니다."},
    "김민재 (예술가)": {"desc": "까칠한 미술부", "sit": "미술실에서 당신을 그립니다."},
    "정하린 (아이돌)": {"desc": "비밀 연습생", "sit": "음악실에서 연습하다 들켰습니다."},
    "오지호 (라이벌)": {"desc": "야망가", "sit": "복도에서 진지하게 내기를 제안합니다."},
    "임채영 (선도부)": {"desc": "원칙주의자", "sit": "교문 앞에서 당신을 붙잡습니다."},
    "송유진 (보건위원)": {"desc": "차분한 보건위원", "sit": "보건실에서 약을 챙겨줍니다."},
    "권지용 (밴드부)": {"desc": "자유로운 기타리스트", "sit": "축제 연습실에서 당신을 부릅니다."},
    "조하은 (요리부)": {"desc": "덤벙거리는 요리부", "sit": "실습실 음식을 맛봐달라 합니다."},
    "백현우 (방송부)": {"desc": "장난기 많은 방송부", "sit": "인터뷰를 하려 합니다."},
    "홍지수 (체육부장)": {"desc": "활기찬 체육부장", "sit": "운동장에서 달리기 시합을 제안합니다."},
    "신시아 (학생회 임원)": {"desc": "지적인 총무", "sit": "과제를 논의합니다."},
    "윤석진 (천재해커)": {"desc": "말없는 천재", "sit": "컴퓨터실에서 해킹 화면을 보여줍니다."},
    "강태오 (연극부)": {"desc": "연기자", "sit": "무대 위에서 독백을 연습합니다."},
    "양지민 (과학부)": {"desc": "실험 덕후", "sit": "과학실에서 도움을 청합니다."},
    "문다은 (만화부)": {"desc": "엉뚱한 화가", "sit": "당신을 모델로 그립니다."},
    "배진우 (급식먹보)": {"desc": "급식 사랑", "sit": "식당에서 메뉴를 추천합니다."},
    "차수현 (아나운서)": {"desc": "화려한 말솜씨", "sit": "방송 중 편지를 읽어줍니다."},
    "이도현 (학생회 서기)": {"desc": "소심한 서기", "sit": "정보를 물어봅니다."},
    "남궁민 (응원단장)": {"desc": "당찬 응원단장", "sit": "노래를 불러줍니다."},
    "표예림 (미화부)": {"desc": "깔끔한 성격", "sit": "신발자국을 보고 잔소리합니다."},
    "구준회 (음악부)": {"desc": "감성 피아니스트", "sit": "피아노를 연주합니다."},
    "하도윤 (봉사부)": {"desc": "따뜻한 봉사자", "sit": "꽃밭에서 말을 겁니다."},
    "최유정 (사서)": {"desc": "깐깐한 사서", "sit": "벌칙을 주려 합니다."},
    "황민현 (영어동아리)": {"desc": "쿨한 친구", "sit": "문장을 해석해줍니다."},
    "진세연 (천문부)": {"desc": "밤하늘 몽상가", "sit": "별자리를 찾자고 합니다."},
    "백서준 (운동부)": {"desc": "인기남", "sit": "체육 시간에 물을 건넵니다."},
    "나현아 (수영부)": {"desc": "수영 실력파", "sit": "수영장에서 연습 중 말을 겁니다."},
    "도진우 (신문부)": {"desc": "기자 정신", "sit": "특종이 있다며 당신을 잡습니다."},
    "임아린 (무용부)": {"desc": "우아한 발레리나", "sit": "연습실에서 춤을 보여줍니다."},
    "강민준 (검도부)": {"desc": "정의로운 검도부", "sit": "도장에서 대련을 제안합니다."},
    "서지혜 (패션부)": {"desc": "패션리더", "sit": "당신의 옷 스타일을 지적합니다."},
    "한재이 (사진부)": {"desc": "사진 작가", "sit": "당신을 찍어도 되냐고 묻습니다."},
    "박주현 (승마부)": {"desc": "승마 실력자", "sit": "마구간에서 대화합니다."},
    "최준희 (봉사부)": {"desc": "활발한 봉사자", "sit": "길고양이를 구경하자 합니다."},
    "김도연 (연극부)": {"desc": "연출가", "sit": "무대 세트 이동을 돕습니다."},
    "윤해인 (영어부)": {"desc": "영문학도", "sit": "좋은 시를 추천해줍니다."},
    "오정우 (역사부)": {"desc": "역사 덕후", "sit": "유물을 보고 감탄합니다."},
    "문수아 (요리부)": {"desc": "디저트 장인", "sit": "쿠키를 건넵니다."},
    "배준호 (야구부)": {"desc": "야구 선수", "sit": "글러브를 손질합니다."},
    "남궁진 (건축부)": {"desc": "건축 천재", "sit": "건물 구조를 분석합니다."},
    "표소영 (환경부)": {"desc": "환경 보호가", "sit": "분리수거를 도와달라 합니다."},
    "구예준 (악기부)": {"desc": "바이올린 전공", "sit": "연주를 평가해달라 합니다."},
    "하은지 (천문부)": {"desc": "행성 덕후", "sit": "망원경을 봐달라 합니다."},
    "최재영 (체육부)": {"desc": "철인 3종", "sit": "같이 뛰자 합니다."},
    "황선우 (게임부)": {"desc": "게임 랭커", "sit": "같이 게임하자 합니다."},
    "진유아 (문예부)": {"desc": "시인", "sit": "직접 쓴 시를 보여줍니다."},
    "강태민 (사격부)": {"desc": "명사수", "sit": "사격장에 초대합니다."},
    "서한결 (바둑부)": {"desc": "바둑 기사", "sit": "한 판 두자고 합니다."},
    "한서진 (테니스부)": {"desc": "테니스 공주", "sit": "테니스 치자 합니다."},
    "박우주 (우주부)": {"desc": "우주 신봉자", "sit": "신호를 찾고 있습니다."},
    "최보라 (미술부)": {"desc": "색채 연구가", "sit": "색 조합을 도와달라 합니다."},
    "김태하 (태권부)": {"desc": "태권도 유단자", "sit": "격파를 보여줍니다."},
    "정채윤 (캘리부)": {"desc": "글씨 장인", "sit": "예쁜 글귀를 써줍니다."},
    "오현우 (마술부)": {"desc": "마술사", "sit": "카드 마술을 보여줍니다."},
    "임하늘 (비행부)": {"desc": "드론 조종사", "sit": "촬영을 도와달라 합니다."}
}

selected_char = st.sidebar.selectbox("캐릭터 선택", list(CHARACTERS.keys()))

if "last_char" not in st.session_state or st.session_state.last_char != selected_char:
    st.session_state.chat = model.start_chat(history=[])
    char_info = CHARACTERS[selected_char]
    st.session_state.chat.send_message(f"너는 {selected_char}({char_info['desc']})야. 상황: {char_info['sit']}. 이 상황에 맞춰 짧게 답해줘.")
    st.session_state.messages = [{"role": "assistant", "content": f"{selected_char}: {char_info['sit']}"}]
    st.session_state.last_char = selected_char

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.write(msg["content"])

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
