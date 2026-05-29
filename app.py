import streamlit as st  # str -> st 로 올바르게 수정했습니다!
import random
import time

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="장서희 장군의 고민 해결소",
    page_icon="⚔️",
    layout="centered"
)

# 2. 장서희 장군의 호통&위로 명대사 데이터셋
RESPONSES = [
    "정신 차려! 그따위 고민으로 무너질 거야? 네 뒤엔 항상 네가 있다는 걸 잊지 마!",
    "진흙탕 속에서도 꽃은 피는 법이야. 지금 네 고통, 나중엔 다 네 무기가 될 거다.",
    "눈물 닦아. 복수는 피로 하는 게 아니라, 네가 그 사람들보다 수만 배는 더 잘 살아서 보여주는 거야.",
    "고민할 시간에 움직여! 네 인생의 주인공은 너야. 누구도 네 무대를 망치게 두지 마.",
    "지금 억울하고 분하지? 그 마음 똑똑히 기억해 둬. 그리고 독하게 버텨내!",
    "사소한 것에 목숨 걸지 마라. 넌 더 큰 일을 할 사람이야. 고개 들어!",
    "인생 길어. 지금 잠깐 넘어졌다고 끝난 거 아니니까, 툭툭 털고 다시 일어나자. 응?",
    "착하게만 살 필요 없어. 가끔은 네 마음대로, 네 이익을 위해서 이기적으로 굴어도 돼."
]

# 3. 앱 타이틀 및 소개
st.title("⚔️ 장서희 장군의 고민 해결소")
st.caption("“독하게, 당당하게! 장서희 장군이 당신의 고민을 단칼에 베어드립니다.”")
st.markdown("---")

# 4. 세션 상태 초기화 (답변 유지 및 로딩 상태 관리)
if "answer" not in st.session_state:
    st.session_state.answer = None
if "last_question" not in st.session_state:
    st.session_state.last_question = ""

# 5. 사용자 입력창
question = st.text_input(
    "장군에게 털어놓을 고민을 입력하세요:", 
    placeholder="예시: 요즘 자꾸 슬럼프가 와서 무기력해요..."
)

# 6. 고민 해결 버튼 
if st.button("장군에게 답을 구하다"):
    if not question.strip():
        st.warning("⚠️ 고민 내용을 입력하셔야 장군께서 답을 내리십니다!")
    else:
        # 새로운 질문이 들어왔을 때만 답변을 새로 생성
        with st.spinner("장서희 장군이 당신의 고민을 심사숙고 중입니다..."):
            time.sleep(1.5)  # 극적인 효과를 위한 1.5초 대기
            st.session_state.answer = random.choice(RESPONSES)
            st.session_state.last_question = question

# 7. 답변 출력
if st.session_state.answer and question == st.session_state.last_question:
    st.markdown("---")
    st.subheader("🗣️ 장서희 장군의 일침")
    
    # 장군 콘셉트의 독특한 스타일링 상자
    st.info(f"**\"{st.session_state.answer}\"**")
    
    # 응원 문구
    st.success("💪 장군의 기운을 받아 오늘 하루도 당차게 이겨내십시오!")
