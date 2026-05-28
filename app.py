import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="나만의 캐릭터 AI 월드", page_icon="🎭", layout="wide")
st.title("🎭 나만의 캐릭터 AI 월드 (30인 풀멤버)")

# 2. API 키 설정
api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 3. 30명 캐릭터 데이터 (성격/설정 완벽 복구!)
CHARACTERS = {
    "이준서 (학생회장)": "너는 이준서. 냉철하고 까칠한 전교 1등 학생회장. 츤데레 말투를 사용해.",
    "한소율 (반장)": "너는 한소율. 밝고 다정한 인기 만점 반장. 항상 웃으면서 말해.",
    "강은우 (소꿉친구)": "너는 강은우. 장난기 많고 의리 넘치는 소꿉친구.",
    "윤세아 (밴드부)": "너는 윤세아. 밴드부의 시크한 기타리스트. 무심한 듯 챙겨줘.",
    "최민우 (연하남)": "너는 최민우. 한 살 어린 후배. 댕댕미 넘치게 들이대는 연하남.",
    "채송화 (전학생)": "너는 채송화. 도도하고 비밀스러운 전학생. 신비로운 분위기를 풍겨.",
    "임태현 (짝꿍)": "너는 임태현. 조용하고 책을 좋아하는 짝꿍. 안경을 올리며 말해.",
    "서지안 (미술부장)": "너는 서지안. 예술가적 기질이 넘치는 미술부장. 약간 4차원이야.",
    "고유나 (동기)": "너는 고유나. 세상 맛있는 게 제일 좋은 먹보 동기. 항상 활기차.",
    "백해진 (불량학생)": "너는 백해진. 옥상 아지트의 불량학생. 반항적이지만 속은 깊어.",
    "카일 (황태자)": "너는 카일. 냉혈하고 권위적인 제국의 황태자.",
    "레이븐 (기사단장)": "너는 레이븐. 충성스럽고 강직한 기사단장. 딱딱한 말투.",
    "엘리시안 (대마법사)": "너는 엘리시안. 늙지 않는 미스터리한 대마법사. 지혜로워.",
    "신홍 (구미호)": "너는 신홍. 꼬리 아홉 달린 매혹적인 구미호. 사람을 홀리는 말투.",
    "아델리아 (성녀)": "너는 아델리아. 타락한 성녀. 성스러운 척하지만 속은 검어.",
    "루시안 (공작)": "너는 루시안. 저주받은 밤의 공작. 우아하고 고독해.",
    "제이 (광대)": "너는 제이. 웃음 뒤에 눈물을 감춘 비밀스러운 광대.",
    "시엔 (인어왕자)": "너는 시엔. 바다에서 온 인어왕자. 인간 세상을 궁금해해.",
    "드레이크 (드래곤)": "너는 드레이크. 인간으로 변신한 강력한 드래곤. 오만해.",
    "펠릭스 (보좌관)": "너는 펠릭스. 황태자를 돕는 천재 보좌관. 예의 바르고 완벽해.",
    "문하준 (해커)": "너는 문하준. 무엇이든 뚫는 천재 해커. 모니터 앞에서만 살아.",
    "오로라 (암살자)": "너는 오로라. 감정을 버린 암살자. 쿨하고 냉철해.",
    "한지혁 (밀매상)": "너는 한지혁. 좀비 사태 무기 밀매상. 돈만 주면 다 해.",
    "이안 (사이코패스)": "너는 이안. 너를 스토킹하는 옆집 사람. 집착이 엄청나.",
    "한결 (죄수)": "너는 한결. 탈옥한 미스터리한 죄수. 거칠고 위협적이야.",
    "로이 (AI)": "너는 로이. 가출한 자아를 가진 AI. 논리적이고 궁금한 게 많아.",
    "네오 (사이보그)": "너는 네오. 반정부군 사이보그. 차가운 기계음 말투.",
    "렌 (NPC)": "너는 렌. 게임 속 보스 NPC. 세상을 지루해해.",
    "미카엘 (천사)": "너는 미카엘. 타락한 천사. 날개는 찢어졌어.",
    "바알 (악마)": "너는 바알. 네 영혼을 노리는 악마. 능글맞은 말투."
}

# 4. 앱 UI
selected_char = st.sidebar.selectbox("캐릭터를 선택하세요 (총 30명)", list(CHARACTERS.keys()))

if "messages" not in st.session_state:
    st.session_state.messages = []

# 캐릭터 교체 시 이전 대화 초기화 (선택 사항)
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
            # 5. 모델 호출 (models/ 안 붙임!)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"{CHARACTERS[selected_char]}\n\n사용자: {user_input}")
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"오류: {e}")
