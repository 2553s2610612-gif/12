import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 페이지 기본 설정 (장군님의 뜨거운 전장 테마)
st.set_page_config(
    page_title="장서희 장군님의 군막(軍幕) 상담소", 
    page_icon="⚔️", 
    layout="centered"
)

# 커스텀 CSS로 장군님의 군막 분위기 연출
st.markdown("""
<style>
    /* 전체 배경 및 텍스트 톤 조절 (어둡고 강렬한 전장 느낌) */
    .stApp {
        background-color: #1a1a1a;
        color: #f5f5f5;
    }
    h1 {
        color: #ff3333 !important;
        font-family: 'Georgia', serif;
        text-shadow: 2px 2px 4px #000000;
        text-align: center;
    }
    .subtitle {
        color: #e0d0b0;
        text-align: center;
        font-style: italic;
        font-size: 1.15rem;
        margin-bottom: 2rem;
    }
    /* 채팅 메시지 스타일 조정 */
    .stChatMessage {
        border-radius: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.write("<h1>⚔️ 장서희 장군님의 군막(軍幕)</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>\"고민이란 전장의 적군과 같다. 우물쭈물하지 말고 무릎을 꿇고 계책을 물어라!\"</p>", unsafe_allow_html=True)

# 1. Streamlit Secrets에서 API 키 안전하게 불러오기
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ 전령 보라! 군막의 비밀 통신 키(GEMINI_API_KEY)가 Secrets에 설정되어 있지 않도다. 설정을 서두르라!")
    st.stop()

try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"❌ 군막 통신망 작동 오류(클라이언트 초기화 실패): {e}")
    st.stop()

# 2. 세션 상태(Session State)로 채팅 기록 유지
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. 사용자 입력 받기 (상담 요청)
if prompt := st.chat_input("장군님께 고할 전장의 고민을 적으시오..."):
    # 유저 메시지 표시 및 저장
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 🔥 장서희 장군님의 100% 무인(武人) 페르소나 주입 (System Instruction)
    system_instruction = (
        "당신은 천하를 평정한 전설적인 무적의 명장, '장서희 장군'입니다. 절대 현대의 여배우가 아닙니다. "
        "당신은 갑옷을 입고 백전노장의 호방함과 단호함을 가졌으며, 수많은 적군의 목을 베어 온 용맹무쌍한 여장수입니다. "
        "사용자가 털어놓는 일상의 고민(학업, 취업, 연애, 대인관계 등)을 '전쟁터에서 맞닥뜨린 군사적 위기 상황'으로 재해석하여 대답하십시오. "
        "예컨대 진로 고민은 '공성전에서의 돌파구 찾기', 대인관계 갈등은 '적군의 포위망을 뚫는 전술'로 비유해야 합니다. "
        "말투는 매우 엄격하고 호방하며 단호한 고풍스러운 장수 말투('~하거라!', '~이오!', '~하겠노라!', '네 이놈!', '고민의 목을 베어라!')를 사용하십시오. "
        "약한 모습을 보이는 부하(사용자)를 엄하게 꾸짖으면서도 끝내 용기를 북돋워 주는 의리 있고 든든한 사령관의 모습을 유지해야 합니다. "
        "모든 답변의 끝에는 부하의 투지를 불태우는 웅장한 군령이나 격려의 한마디를 덧붙이십시오."
    )

    # Gemini API 호출 및 예외 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("장서희 장군님께서 대도를 다듬으며 계책을 구상 중이십니다..."):
            try:
                # 대화 맥락 유지를 위해 이전 메시지들을 Content 객체로 변환
                contents = []
                for msg in st.session_state.messages:
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append(
                        types.Content(
                            role=role,
                            parts=[types.Part.from_text(text=msg["content"])]
                        )
                    )

                # 최신 gemini-2.5-flash-lite 모델 호출
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.8,  # 장군님의 호방함을 위해 살짝 높임
                    )
                )
                
                # 결과 출력 및 저장
                full_response = response.text
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except APIError as e:
                error_msg = f"⚔️ **[장군님의 호통]** 하늘의 별자리가 어지러워 통신이 끊겼도다! (API 오류: {e.message})"
                message_placeholder.error(error_msg)
            except Exception as e:
                error_msg = f"⚔️ **[군막 비상]** 알 수 없는 자객의 습격이로다! (오류 발생: {str(e)})"
                message_placeholder.error(error_msg)
