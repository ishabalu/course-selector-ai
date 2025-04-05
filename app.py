import streamlit as st
from streamlit_chat import message
from chat_engine import get_chat_response
from data_handler import load_data, create_vectorstore

st.set_page_config(page_title="🎓 Course Chat Assistant", layout="wide")
st.title("🎓 Course Chat Assistant")

@st.cache_resource(show_spinner=False)
def load_resources():
    course_df, history_df = load_data("data/courses.csv", "data/CourseHistory.csv")
    vectorstore = create_vectorstore(course_df)
    return (course_df, history_df), vectorstore

(course_df, history_df), vectorstore = load_resources()

# Set up session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_input = st.chat_input("Ask me about courses, prerequisites, eligibility rules, etc...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        response = get_chat_response(user_input, vectorstore, course_df=course_df, history_df=history_df)

    st.session_state.chat_history.append({"role": "assistant", "content": response})

# Display messages
for chat in st.session_state.chat_history:
    message(chat["content"], is_user=(chat["role"] == "user"))
