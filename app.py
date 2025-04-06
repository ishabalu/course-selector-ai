import streamlit as st
from streamlit_chat import message
from chat_engine import get_chat_response
from data_handler import load_data, create_vectorstore

# Configure the page first, before any other Streamlit commands
st.set_page_config(
    page_title="IU Course Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': 'IU Course Selection Assistant'
    }
)

# Basic page styling
st.markdown("""
    <style>
        div.block-container {
            padding-top: 2rem;
        }
        div.stTitle {
            font-size: 2.5rem;
            font-weight: bold;
            color: #990000;
            text-align: center;
            margin-bottom: 2rem;
        }
        .stChatInputContainer textarea {
            font-weight: 600 !important;
        }
        .stChatInputContainer textarea::placeholder {
            font-weight: 600 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Main content
st.markdown("<h1 style='text-align: center; color: #990000; padding: 1rem; border-bottom: 3px solid #990000; margin-bottom: 2rem;'>🎓 IU Course Chat Assistant</h1>", unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def load_resources():
    course_df, history_df = load_data("data/courses.csv", "data/CourseHistory.csv")
    vectorstore = create_vectorstore(course_df)
    return (course_df, history_df), vectorstore

# Initialize resources
with st.spinner("Loading resources..."):
    (course_df, history_df), vectorstore = load_resources()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_input = st.chat_input("Type your question (e.g., 'Can I take CSCI-A 110 as a grad student?')")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        response = get_chat_response(user_input, vectorstore, course_df=course_df, history_df=history_df)
    st.session_state.chat_history.append({"role": "assistant", "content": response})

# Display chat messages
for chat in st.session_state.chat_history:
    message(chat["content"], is_user=(chat["role"] == "user"), key=str(id(chat)))
