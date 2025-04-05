import pandas as pd
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

load_dotenv()


def load_data(course_path, history_path):
    course_df = pd.read_csv(course_path)
    history_df = pd.read_csv(history_path)

    course_df.fillna("", inplace=True)
    history_df.fillna("", inplace=True)

    return course_df, history_df


def create_vectorstore(course_df):
    # Combine important course details into a searchable text field
    course_df["text"] = course_df.apply(lambda row: f"""
Course Number: {row['course_number']}
Course Name: {row['course_name']}
Instructor: {row['instructor']}
Class Time: {row['class time']}
Instruction Mode: {row['instruction mode']}
Total Slots: {row['total_slots']}
Term: {row['term']}
Credits: {row['credits']}
Course Type: {row['course_type']}
Difficulty: {row['difficulty']}
Popularity: {row['popularity']}
Description: {row['description']}
Keywords: {row['keywords']}
Prerequisites: {row['prerequisites']}
""", axis=1)

    # Load documents from the DataFrame
    loader = DataFrameLoader(course_df, page_content_column="text")
    documents = loader.load()

    # Optional: chunk the documents (useful for large rows)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(documents)

    # Generate vector embeddings
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    return vectorstore
