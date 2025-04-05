import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
client = OpenAI()

def get_chat_response(query, df):
    system_prompt = ("""
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
""")

    # Build dynamic context from sample data
    sample_courses = df.sample(min(10, len(df)))

    context_rows = []
    for _, row in sample_courses.iterrows():
        context_rows.append(
            f"Course: {row['course_name']} ({row['course_number']})\n"
            f"Instructor: {row['instructor']}\n"
            f"Instruction Mode: {row['instruction mode']}\n"
            f"Class Time: {row['class time']}\n"
            f"Seats Available: {row['availability']}\n"
            f"Term: {row['term']}\n"
            f"Credits: {row['credits']}\n"
            f"Description: {row['description']}\n"
            f"Prerequisites: {row['prerequisites']}\n"
            f"Career Tags: {row['career tags']}"
        )

    context = "\n\n---\n\n".join(context_rows)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"The following are sample course listings:\n{context}\n\nUser: {query}"},
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5
    )

    return response.choices[0].message.content
