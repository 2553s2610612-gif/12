import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 페이지 기본 설정
st.set_page_config(
    page_title="장서희 장군님의 군막(軍幕) 상담소", 
    page_icon="⚔️", 
    layout="centered"
)

# 🎨 밝은 화면 + 장군님 답변 빨간색 처리를 위한 커스텀 CSS
st.markdown("""
<style>
    /* 전체 배경을 밝고 깨끗하게 변경 */
    .stApp {
        background-color: #ffffff;
        color: #111111;
    }
    /* 제목 스타일 (강렬한 대장군 느낌) */
    h1 {
        color: #cc0000 !important;
        font-family: 'Malgun Gothic', sans-serif;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        color: #555555;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    /* 🔴 장군님(AI)의 답변 글씨를 빨간색으로 강제 지정 */
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        color: #cc0000 !important;
        font-weight: bold;
        background-color: #fff0f0; /* 살짝 붉은 기가 도는 밝은 배경으로 강조 */
        border-left: 5px solid #cc0000;
    }
    /* 사용자 입력 글씨는 차분한 검은색 */
    .stChatMessage[data-testid="stChatMessageUser"] {
        color: #222222 !important;
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

st.write("<h1>⚔️ 장서희 장군님의 군막(軍幕)</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>\"고민이란 전장의 적군과 같다. 단호하게 목을 베어라!\"</p>", unsafe_allow_html=True)

# 1. Streamlit Secrets에서 API 키 안전하게 불러오기
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ 전령 보라! 군막의 비밀 통신 키(GEMINI_API_KEY)가 Secrets에 설정되어 있지 않도다. 설정을 서두르라!")
    st.stop()

try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"❌ 군막 통신망 작동 오류(클라이언트 초기화 실패): {e}")
    st.stop()

# 2. 세션 상태(Session State) 초기화 - 대화 기록 누적을 막기 위해 1개의 세트만 저장하도록 설계
if "current_user_msg" not in st.session_state:
    st.session_state.current_user_msg = ""
if "current_ai_msg" not in st.session_state:
    st.session_state.current_ai_msg = ""

# 3. 사용자 입력 받기 (상담 요청)
if prompt := st.chat_input("장군님께 고할 전장의 고민을 적으시오..."):
    # 새로운 질문이 들어오면 기존의 질문과 답변 보관함을 완전히 비우고 새로 채웁니다.
    st.session_state.current_user_msg = prompt
    st.session_state.current_ai_msg = "" # AI 답변은 API 호출 후 채움

    # 🔥 장서희 장군님의 100% 무인(武人) 페르소나 + 단답형 간결령 주입
    system_instruction = (
        "당신은 천하를 평정한 전설적인 무적의 여장수, '장서희 장군'입니다. (배우가 아닙니다) "
        "당신은 매우 엄격하고 호방하며 결단력이 넘치는 사령관입니다. "
        "부하(사용자)가 일상의 고민을 말하면 그것을 '전쟁터의 위기'로 비유하여 호통치듯 해결책을 내리십시오. "
        "말투는 무인답게 고풍스러운 말투('~하거라!', '~이오!', '네 이놈!', '고민의 목을 베어라!')를 쓰십시오. "
        "★중요: 답변은 절대로 구구절절 길게 늘어놓지 마십시오. 무조건 3~4줄 이내로 짧고 굵게, 핵심 전술만 단호하게 명하듯 대답해야 합니다."
    )

    # Gemini API 호출 및 예외 처리
    try:
        # 단발성 질문이므로 history 없이 싱글 턴으로 호출합니다.
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            )
        )
        # 결과 저장
        st.session_state.current_ai_msg = response.text

    except APIError as e:
        st.session_state.current_ai_msg = f"⚔️ **[장군님의 호통]** 하늘의 별자리가 어지러워 통신이 끊겼도다! (API 오류: {e.message})"
    except Exception as e:
        st.session_state.current_ai_msg = f"⚔️ **[군막 비상]** 알 수 없는 자객의 습격이로다! (오류 발생: {str(e)})"

# 4. 최신 질문과 답변 딱 한 쌍만 화면에 표시 (이전 기록은 자동으로 사라짐)
if st.session_state.current_user_msg:
    with st.chat_message("user"):
        st.markdown(st.session_state.current_user_msg)

if st.session_state.current_ai_msg:
    with st.chat_message("assistant"):
        st.markdown(st.session_state.current_ai_msg)
