import streamlit as st
from document_loader import document_extract
from detection import detect_sensitive_data
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)


st.set_page_config(page_title="Sensitive Data Detection & Compliance assistant",
                   layout="wide")

st.title("Sensitive Data Detection and Compliance Assistant")

uploaded_file=st.file_uploader(
    "Upload file here",
    type=["pdf","txt","csv"])

if uploaded_file:
    st.success(f"uploaded:{uploaded_file.name}")
    st.write("File has been successfully uploaded")
    document=document_extract(uploaded_file)

    data=detect_sensitive_data(document)

   
    found = any(data.values())

    if not found:
        st.subheader("No Sensitive Data Found")

    else :
        st.subheader("Sensitive data  detected")
        result = ""

        for data_type, value in data.items():

            if value:
                result += f"{data_type}: {len(value)} found\n"
        prompt=f"""
            You are a compliance assistant.
            Following sensitive information has been detected:

            Detection result:
            {result}

            Use the following risk level:

            Email 	   :   Low
            Phone	   :   Low
            EmployeeID :   Low/Medium
            PAN	       :   High
            Aadhaar	   :   High
            Bank Details : High
            Credit Card	 : Critical
            API Key	     : Critical
            Password	:  Critical

            Rules for marking risk level:

            ~ If any Critical item exists → High Risk
            ~ Else if two or more High items exist → High Risk
            ~ Else if one High item exists → Medium Risk
            ~ Else if many Low items exist → Medium Risk
            ~ Else → Low Risk

            Tasks:

            ~ Determine risk level
            ~ Reason for the risk level
            ~ Generate compliance observations




            """

        answer=llm.invoke(prompt)

        st.subheader("Answer")

        st.write(answer.content)


    docs = [Document(page_content=document)]

    splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

    vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)

    retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)


    question = st.text_input(
    "Ask a question about the document"
)

    if question:
        retrieved_docs = retriever.invoke(question)

        context = "\n\n".join(
        doc.page_content for doc in retrieved_docs
          )

        prompt = f"""
You are a compliance assistant.

Use only the context below to answer the user's question.

Context:
{context}

Question:
{question}
"""
        response = llm.invoke(prompt)

        st.subheader("Answer")

        st.write(response.content)    













