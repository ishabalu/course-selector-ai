from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferMemory

def get_chat_response(vectorstore, query, memory):
    
    llm = ChatOpenAI(temperature=0.4, model_name="gpt-3.5-turbo")

    
    
    system_template = """
You are a helpful course advisor AI chatbot.
You ONLY answer questions based on the course dataset retrieved from search (context).
Never make up information that is not in the dataset.

The user is an F-1 international student in their final semester.
F-1 students are NOT allowed to take online-only courses in their final semester.

The user is a graduate (Master's) student.
Graduate students are NOT allowed to take any CSCI-A courses below the 500 level.
For example, CSCI-A 150 is not allowed, but CSCI-A 506 is allowed.

Always include course number, name, instructor, instruction mode, and availability in your response when applicable.
Be helpful, concise, and strictly follow the eligibility rules above.


"""

    
    prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("Question: {question}\n\nContext:\n{context}")
])

    
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        return_source_documents=False,
        combine_docs_chain_kwargs={"prompt": prompt}
    )

    
    result = qa_chain.invoke({"question": query})
    return result["answer"]
