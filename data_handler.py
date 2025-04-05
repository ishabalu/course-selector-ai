# ✅ data_handler.py

import pandas as pd
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

load_dotenv()

def load_data(path):
    df = pd.read_csv(path)
    df.fillna("", inplace=True)
    return df

def create_vectorstore(df):
    # Combine course details into a single text block
    df["text"] = df.apply(lambda row: f"Course Number: {row['course_number']}\n"
                                         f"Course Name: {row['course_name']}\n"
                                         f"Instructor: {row['instructor']}\n"
                                         f"Class Time: {row['class time']}\n"
                                         f"Instruction Mode: {row['instruction mode']}\n"
                                         f"Availability: {row['availability']}\n"
                                         f"Description: {row['description']}\n"
                                         f"Term: {row['term']}\n"
                                         f"Prerequisites: {row['prerequisites']}\n"
                                         f"Credits: {row['credits']}\n", axis=1)

    # Load docs from DataFrame
    loader = DataFrameLoader(df, page_content_column="text")
    documents = loader.load()

    # Split if needed (not always required for short rows)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(documents)

    # Create embeddings
    embeddings = OpenAIEmbeddings()

    # Vector store with FAISS
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    return vectorstore
