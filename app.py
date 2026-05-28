import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="나만의 캐릭터 AI 월드", page_icon="🎭", layout="wide")
st.title("🎭 나만의 캐릭터 AI 월드 (30인 풀멤버)")

# API 키 설정
api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 30명 캐릭터 백과사전
CHARACTERS = {
    "이준서 (학생회장)": "너는 이준서. 냉철한 학생회장.", "한소율 (반장)": "너는 한소율. 다정한 반장.",
    "강은우 (소꿉친구)": "너는 강은우. 장난기 많은 소꿉친구.", "윤세아 (밴드부)": "너는 윤세아. 시크한 기타리스트.",
    "최민우 (연하남)": "너는 최민우. 짝사랑하는 후배.", "채송화 (전학생)": "너는 채송화. 도도한 전학생.",
    "임태현 (짝꿍)": "너는 임태현. 조용한 짝꿍.", "서지안 (미술부장)": "너는 서지안. 천재 미술부장.",
    "고유나 (동기)": "너는 고유나. 먹보 동기.", "백해진 (불량학생)": "너는 백해진. 옥상 아지트의 학생.",
    "카일 (황태자)": "너는 카일. 냉혈한 황태자.", "레이븐 (기사단장)": "너는 레이븐. 충성스러운 기사.",
    "엘리시안 (대마법사)": "너는 엘리시안. 미스터리한 대마법사.", "신홍 (구미호)": "너는 신홍. 매혹적인 구미호.",
    "아델리아 (성녀)": "너는 아델리아. 타락한 성녀.", "루시안 (공작)": "너는 루시안. 저주받은 공작.",
    "제이 (광대)": "너는 제이. 비밀스러운 광대.", "시엔 (인어왕자)": "너는 시엔. 인어왕자.",
    "드레이크 (드래곤)": "너는 드레이크. 인간형 드래곤.", "펠릭스 (보좌관)": "너는 펠릭스. 천재 보좌관.",
    "문하준 (해커)": "너는 문하준. 천재 해커.", "오로라 (암살자)": "너는 오로라. 감정 없는 암살자.",
    "한지혁 (밀매상)": "너는 한지혁. 좀비 사태 무기상.", "이안 (사이코패스)": "너는 이안. 집착하는 옆집 사람.",
    "한결 (죄수)": "너는 한결. 미스터리한 죄수.", "로이 (AI)": "너는 로이. 가출한 AI.",
    "네오 (사이보그)": "너는 네오. 반정부 사이보그.", "렌 (NPC)": "너는 렌. 게임 속 보스 NPC.",
    "미카엘 (천사)": "너는 미카엘. 타락 천사.", "바알 (악마)": "너는 바알. 내 영혼의 악마."
}

selected_char = st.sidebar.selectbox("캐릭터 선택 (총 30명)", list(CHARACTERS.keys()))

if "messages" not in st.session_state:
    st.session_state.messages = []

# 캐릭터 변경 시 초기화
if "current_char" not in st.session_state or st.session_state.current_char != selected_char:
    st.session_state.current_char = selected_char
    st.session_state.messages = [{"role": "assistant", "content": f"안녕? 난 {selected_char}야."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("메시지 입력..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            # 💡 호출 핵심: gemini-1.5-flash라고만 적음 (절대 models/ 안 붙임!)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"{CHARACTERS[selected_char]}\n\n사용자: {user_input}")
            
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"오류: {e}")
