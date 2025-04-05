import streamlit as st
from chat_engine import get_chat_response
from data_handler import load_data, create_vectorstore
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
load_dotenv()



st.set_page_config(page_title="IU Course Chat Assistant", layout="wide")
st.title("🎓 IU Course Chat Assistant")


@st.cache_resource(show_spinner=False)
def load_courses_and_vectorstore():
    df = load_data("data/courses.csv")
    vectorstore = create_vectorstore(df)
    return df, vectorstore



df, vectorstore = load_courses_and_vectorstore()


if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


user_input = st.chat_input("Ask me about courses, prerequisites, eligibility rules, etc...")


if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        try:
            response = get_chat_response(
                vectorstore=vectorstore,
                query=user_input,
                memory=st.session_state.memory
            )
        except Exception as e:
            response = f"⚠️ Something went wrong: `{str(e)}`"

    st.session_state.chat_history.append({"role": "assistant", "content": response})


for chat in st.session_state.chat_history:
    with st.chat_message("user" if chat["role"] == "user" else "assistant"):
        st.markdown(chat["content"])
