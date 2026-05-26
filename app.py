import streamlit as st
from datetime import date

# 1. 앱 제목과 귀여운 헤더
st.title("💖 우리들의 비밀 연애 다이어리")
st.subheader("서로의 마음을 확인하고 기념일을 계산해보세요!")

# 2. 사이드바 - 우리 정보 입력
st.sidebar.header("💌 프로필 설정")
my_name = st.sidebar.text_input("내 이름", "너구리")
your_name = st.sidebar.text_input("상대방 이름", "고양이")
start_date = st.sidebar.date_input("처음 만난 날", date(2025, 1, 1))

# 3. 메인 화면 - 디데이 계산기
st.markdown("---")
st.header("🗓️ 우리가 사랑한 지 얼마나 됐을까?")

today = date.today()
days_passed = (today - start_date).days

if days_passed >= 0:
    st.info(f"✨ **{my_name}** ❤️ **{your_name}** 우리 오늘 {days_passed + 1}일째 연애 중!")
else:
    st.warning("미래의 날짜를 선택하셨어요! 설레는 만남을 기다리고 계시군요?")

# 4. 메인 화면 - 상시 플러팅 버튼
st.markdown("---")
st.header("💘 마음 전하기 토글")

# 버튼을 누르면 숨겨진 메시지가 나옵니다.
if st.button(f"{your_name}에게 비밀 메시지 보내기"):
    st.balloons()  # 화면에 풍선이 날아다니는 효과!
    st.success(f"💌 {my_name}(이)가 전하는 말: \"오늘도 많이 고맙고 사랑해!\"")
