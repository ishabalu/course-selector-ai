# ✅ app.py (Updated and working with vector search)
import streamlit as st
from streamlit_chat import message
from chat_engine import get_chat_response
from data_handler import load_data, create_vectorstore

st.set_page_config(page_title="AI Course Chat", layout="wide")
st.title("🎓 Course Chat Assistant")

# Load data and vectorstore once
@st.cache_resource(show_spinner=False)
def load_resources():
    df = load_data("data/courses.csv")
    vectorstore = create_vectorstore(df)
    return df, vectorstore

df, vectorstore = load_resources()

# Set up session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_input = st.chat_input("Ask me about courses, prerequisites, eligibility rules, etc...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        response = get_chat_response(user_input, vectorstore, df=df)

    st.session_state.chat_history.append({"role": "assistant", "content": response})

# Display messages
for chat in st.session_state.chat_history:
    message(chat["content"], is_user=(chat["role"] == "user"))