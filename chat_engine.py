import re
import os
from openai import OpenAI
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
import streamlit as st

api_key = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=api_key)


def extract_registration_time(text):
    # Look for a time pattern like 12:15PM or 2:30PM
    match = re.search(r"\b(1[0-2]|0?[1-9]):[0-5][0-9]\s*(AM|PM)\b", text, re.IGNORECASE)
    return match.group(0) if match else None


def get_chat_response(query, vectorstore, course_df, history_df):
    # Step 1: Semantic Retrieval
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    relevant_docs = retriever.get_relevant_documents(query)

    # Step 2: Build Context
    context = "\n\n".join(doc.page_content for doc in relevant_docs)

    # Step 3: Extract registration time (optional)
    reg_time = extract_registration_time(query)
    time_remark = ""
    if reg_time:
        time_remark = f"The student’s registration time is {reg_time}. Use this to determine if they'll likely get the course."

    matched_courses = []

    for course_number in course_df["course_number"].unique():
        if course_number in query:
            matched_courses.append(course_number)

    if matched_courses:
        for course_code in matched_courses:
            extra_row = course_df[course_df["course_number"] == course_code]
            if not extra_row.empty:
                course_context = "\n".join(
                    f"{col}: {extra_row.iloc[0][col]}" for col in extra_row.columns
                )
                context += f"\n\n[EXACT MATCH: {course_code}]\n{course_context}"

    # Step 4: Prompt with all rules
    system_prompt = f"""
You are a course advisor AI. Follow these rules strictly:

RULES:
- F-1 international students in their **final semester** CANNOT take fully online courses.
- Graduate students CANNOT take CSCI-A courses below 500-level.
- If a course is extremely popular and the student registers late (e.g., 2:30PM), they are unlikely to get it.
- If the registration time is close to 12:15PM, chances are better.
- Courses with high dropout rates or low waitlists are more likely to be available.

TASKS:
- Recommend 2–3 courses based on interests.
- If probability to get a course is low (due to popularity or dropouts), suggest alternatives.
- Always include:
  - Course Number
  - Course Name
  - Instructor
  - Instruction Mode
  - Class Time
  - Total Slots
  - Popularity, Dropout Rate, Waitlist Trend (if known)

{time_remark}

DATA CONTEXT:
{context}
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5
    )

    return response.choices[0].message.content
