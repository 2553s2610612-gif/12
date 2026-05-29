import streamlit as st
from g4f.client import Client
import time

# 1. 페이지 설정
st.set_page_config(
    page_title="장서희 장군의 AI 고민 해결소",
    page_icon="⚔️",
    layout="centered"
)

# 2. AI 클라이언트 초기화 (무료 GPT-4/GPT-3.5 구동용)
client = Client()

# 장서희 장군 콘셉트를 주입하기 위한 시스템 프롬프트 (AI의 인격 설정)
SYSTEM_PROMPT = """
너는 지금부터 배우 장서희 님의 카리스마 있고 당찬 '장군' 캐릭터다. 
드라마 '아내의 유혹' 등에서 보여준 독하고, 당당하며, 불의를 참지 못하고, 한편으로는 속이 뻥 뚫리는 사이다 위로를 건네는 인물이다.

사용자가 고민을 말하면 다음 원칙을 반드시 지켜서 답해라:
1. 말투는 당당하고 기백 넘치는 장군의 어조(~해라, ~다, 정신 차려라! 등)를 사용한다.
2. 절대 뻔하고 착하기만 한 위로는 하지 마라. 가끔은 정신이 번쩍 들게 호통을 치고 독해지라고 주문해라.
3. 하지만 마지막에는 반드시 사용자의 편이 되어주며 "내가 네 뒤에 있으니 당당하게 맞서라"라는 식의 든든한 위로를 건네라.
4. 너무 길게 말하지 말고 3~4문장 내외로 강렬하고 굵직하게 답해라.
"""

# 3. 앱 타이틀
st.title("⚔️ 장서희 장군의 AI 고민 해결소")
st.caption("“정해진 답은 없다! AI 장서희 장군이 당신의 고민을 실시간으로 베어드립니다.”")
st.markdown("---")

# 4. 세션 상태 유지 (새로고침 시 답변 날아감 방지)
if "ai_answer" not in st.session_state:
    st.session_state.ai_answer = None
if "last_question" not in st.session_state:
    st.session_state.last_question = ""

# 5. 사용자 고민 입력
question = st.text_input(
    "장군에게 털어놓을 고민을 입력하세요:", 
    placeholder="예시: 상사가 자꾸 제 공을 가로채는데 화가 나요."
)

# 6. 고민 해결 버튼 클릭 시 AI 호출
if st.button("장군에게 답을 구하다"):
    if not question.strip():
        st.warning("⚠️ 고민 내용을 입력하셔야 장군께서 호통을 치십니다!")
    else:
        with st.spinner("장서희 장군이 당신의 고민을 듣고 분노하는 중입니다..."):
            try:
                # 무료 AI API 호출 (gpt-3.5-turbo 모델 기준)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"내 고민은 이거야: {question}"}
                    ]
                )
                
                # 결과 저장
                st.session_state.ai_answer = response.choices[0].message.content
                st.session_state.last_question = question
                
            except Exception as e:
                st.error("⚠️ AI 장군과의 연결이 잠시 원활하지 않습니다. 다시 한번 버튼을 눌러주십시오!")
                # 개발자 확인용 에러 로그 (앱 화면에는 아주 작게 표시)
                st.caption(f"에러 상세: {str(e)}")

# 7. AI 답변 출력
if st.session_state.ai_answer and question == st.session_state.last_question:
    st.markdown("---")
    st.subheader("🗣️ 장서희 장군의 AI 진단")
    
    # 카리스마 있는 스타일의 안내 상자
    st.info(f"{st.session_state.ai_answer}")
    
    st.success("💪 장군의 독한 기운을 받았으니, 이제 당당하게 행동하십시오!")
