import streamlit as st
from streamlit_chat import message
from chat_engine import get_chat_response
from data_handler import load_data

st.set_page_config(page_title="AI Course Chat", layout="wide")
st.title("Course Chat Assistant")

# Load your data
df = load_data("data/courses.csv")

# Set up session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_input = st.chat_input("Ask me about courses, prerequisites, availability, etc...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        response = get_chat_response(user_input, df)
    st.session_state.chat_history.append({"role": "assistant", "content": response})

# Display messages
for chat in st.session_state.chat_history:
    message(chat["content"], is_user=(chat["role"] == "user"))