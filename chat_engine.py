# ✅ chat_engine.py (vector search enabled + OpenAI API + smart rules)

import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_community.vectorstores import FAISS

# Load API key from .env
load_dotenv()
client = OpenAI()
api_key = os.getenv("OPENAI_API_KEY")

def get_chat_response(query, vectorstore: FAISS, df=None):
    import re

    # 1. Try course code detection
    course_code_match = re.search(r"[A-Z]{2,}-[A-Z]?\s?\d{3}", query.upper())
    context = ""
    rule_override = ""

    if course_code_match and df is not None:
        course_code = course_code_match.group(0).replace(" ", "")
        matched_row = df[df["course_number"].str.upper().str.replace(" ", "") == course_code]

        if not matched_row.empty:
            course_info = matched_row.iloc[0]
            context = course_info.to_string()

            # Check rule manually
            if "CSCI-A" in course_code and int(course_code[-3:]) < 500:
                rule_override = (
                    f"\n\n⚠️ RULE TRIGGERED: {course_code} is below 500-level and belongs to CSCI-A. "
                    "Graduate students are NOT allowed to take this course."
                )
        else:
            # fallback to vector
            retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
            relevant_docs = retriever.get_relevant_documents(query)
            context = "\n\n".join(doc.page_content for doc in relevant_docs)
    else:
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        relevant_docs = retriever.get_relevant_documents(query)
        context = "\n\n".join(doc.page_content for doc in relevant_docs)

    # 2. Final system prompt
    system_prompt = f"""
You are a helpful university course advisor.

Only answer based on CONTEXT below.
NEVER make up information or suggest courses not shown in the context.

Check for student type and rules:
1. F-1 international students in their final semester CANNOT take online-only courses.
2. Graduate students CANNOT take CSCI-A courses below 500-level.

If a course violates a rule, clearly explain why the student CANNOT take it.

CONTEXT:
{context}
{rule_override}
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.4
    )

    return response.choices[0].message.content

