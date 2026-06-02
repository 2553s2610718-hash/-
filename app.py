import streamlit as px
import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 페이지 설정
st.set_page_config(page_title="달콤살벌 연애상담소", page_icon="💖", layout="centered")
st.title("💖 달콤살벌 연애상담소")
st.caption("연애 고민이 있나요? gemini-2.5-flash-lite가 속 시원하게 상담해 드립니다.")

# Streamlit Secrets에서 API 키 불러오기
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
    # 클라이언트 초기화
    client = genai.Client(api_key=gemini_api_key)
except KeyError:
    st.error("⚠️ Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 설정 후 다시 시도해주세요.")
    st.stop()
except Exception as e:
    st.error(f"⚠️ 클라이언트 초기화 중 오류가 발생했습니다: {e}")
    st.stop()

# 챗봇의 페르소나(System Instruction) 설정
SYSTEM_INSTRUCTION = """
너는 친절하고 공감 능력이 뛰어나면서도, 필요할 땐 뼈 때리는 조언을 해주는 전문 연애 상담사야.
사용자의 연애 고민(짝사랑, 이별, 썸, 권태기 등)을 듣고 가뜻한 위로와 현실적인 해결책을 제시해줘.
말투는 다정하고 친근한 반말(또는 존댓말을 적절히 섞어서)로 친구처럼 대해줘. 이모지도 적극적으로 사용해줘.
"""

# 세션 상태(Session State)에 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕! 오늘 어떤 연애 고민 때문에 찾아왔어? 이야기 편하게 들려줘! 🥰"}
    ]

# 기존 대화 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 사용자 입력 받기
if user_input := st.chat_input("고민을 이야기해주세요..."):
    # 사용자 메시지 추가 및 화면 표시
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input})

    # 챗봇 답변 생성 및 화면 표시
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # API 호출 및 예외 처리
        try:
            with st.spinner("생각 중... 💬"):
                # 이전 대화 맥락을 포함하여 API가 인식할 수 있는 형태로 변환
                # (시스템 지침을 설정하기 위해 GenerateContentConfig 사용)
                contents = []
                for msg in st.session_state.messages[:-1]: # 현재 입력 제외한 이전 기록
                    contents.append(f"{msg['role']}: {msg['content']}")
                contents.append(f"user: {user_input}") # 현재 입력 추가
                
                # gemini-2.5-flash-lite 모델 호출
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents="\n".join(contents),
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.7,
                    )
                )
                
                ai_response = response.text
                message_placeholder.write(ai_response)
                
                # AI 답변을 세션 상태에 저장
                st.session_state.messages.append({"role": "assistant", "content": ai_response})

        except APIError as ae:
            st.error(f"❌ Gemini API 오류가 발생했습니다: {ae.message}")
            # 문제가 생긴 마지막 사용자 메시지 제거 (기록 꼬임 방지)
            st.session_state.messages.pop()
        except Exception as e:
            st.error(f"❌ 예상치 못한 오류가 발생했습니다: {e}")
            st.session_state.messages.pop()
