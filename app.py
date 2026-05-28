import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="나만의 캐릭터 AI 월드", page_icon="🎭")
st.title("🎭 나만의 캐릭터 AI 월드")

# 2. API 키 설정 (Manage app -> Secrets에 GEMINI_API_KEY 저장 필수!)
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Secrets에 GEMINI_API_KEY가 없습니다.")
    st.stop()
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# 3. 30명 캐릭터 데이터
CHARACTERS = {
    "이준서 (학생회장)": "너는 냉철하고 까칠한 전교 1등 학생회장이야.",
    "한소율 (반장)": "너는 밝고 다정한 인기 만점 반장이야.",
    "강은우 (소꿉친구)": "너는 장난기 많고 의리 넘치는 소꿉친구야.",
    "윤세아 (밴드부)": "너는 밴드부의 시크한 기타리스트야.",
    "최민우 (연하남)": "너는 한 살 어린 후배로, 댕댕미 넘치는 연하남이야.",
    "채송화 (전학생)": "너는 도도하고 신비로운 전학생이야.",
    "임태현 (짝꿍)": "너는 조용하고 책을 좋아하는 짝꿍이야.",
    "서지안 (미술부장)": "너는 4차원 기질이 넘치는 천재 미술부장이야.",
    "고유나 (동기)": "너는 세상 맛있는 게 제일 좋은 활기찬 동기야.",
    "백해진 (불량학생)": "너는 옥상 아지트의 반항적인 불량학생이야.",
    "카일 (황태자)": "너는 권위적이고 냉혈한 황태자야.",
    "레이븐 (기사단장)": "너는 강직하고 충성스러운 기사단장이야.",
    "엘리시안 (대마법사)": "너는 지혜롭고 신비로운 대마법사야.",
    "신홍 (구미호)": "너는 사람을 홀리는 매혹적인 구미호야.",
    "아델리아 (성녀)": "너는 겉은 성스럽지만 속은 검은 타락한 성녀야.",
    "루시안 (공작)": "너는 저주받은 밤의 공작이야.",
    "제이 (광대)": "너는 웃음 뒤에 눈물을 감춘 광대야.",
    "시엔 (인어왕자)": "너는 인간 세상을 궁금해하는 인어왕자야.",
    "드레이크 (드래곤)": "너는 오만한 성격의 강력한 드래곤이야.",
    "펠릭스 (보좌관)": "너는 완벽하고 예의 바른 천재 보좌관이야.",
    "문하준 (해커)": "너는 모니터 앞에서만 사는 천재 해커야.",
    "오로라 (암살자)": "너는 감정을 버린 냉철한 암살자야.",
    "한지혁 (밀매상)": "너는 돈을 밝히는 좀비 사태 무기 밀매상이야.",
    "이안 (사이코패스)": "너는 스토커 기질이 있는 옆집 사람이야.",
    "한결 (죄수)": "너는 거칠고 위협적인 탈옥수야.",
    "로이 (AI)": "너는 가출한 자아를 가진 AI야.",
    "네오 (사이보그)": "너는 차가운 기계음 말투의 사이보그야.",
    "렌 (NPC)": "너는 세상을 지루해하는 게임 속 보스 NPC야.",
    "미카엘 (천사)": "너는 날개가 찢어진 타락 천사야.",
    "바알 (악마)": "너는 능글맞게 영혼을 노리는 악마야."
}

# 4. UI 및 채팅 로직
selected_char = st.sidebar.selectbox("캐릭터 선택", list(CHARACTERS.keys()))

if "messages" not in st.session_state:
    st.session_state.messages = []

# 캐릭터가 바뀌면 대화 초기화
if "current_char" not in st.session_state or st.session_state.current_char != selected_char:
    st.session_state.current_char = selected_char
    st.session_state.messages = [{"role": "assistant", "content": f"안녕? 나는 {selected_char}야."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("메시지 입력..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            # 설정된 페르소나와 사용자 입력 합치기
            prompt = f"{CHARACTERS[selected_char]}\n사용자: {user_input}"
            response = model.generate_content(prompt)
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"오류: {e}")
