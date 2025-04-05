# data_handler.py

import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
load_dotenv()


def load_data(path):
    df = pd.read_csv(path)
    df.fillna("", inplace=True)
    return df

def create_vectorstore(df):
    
    df["text"] = df.apply(lambda row: "\n".join(str(val) for val in row), axis=1)

    
    loader = DataFrameLoader(df, page_content_column="text")
    documents = loader.load()

    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.split_documents(documents)

    
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    return vectorstore
