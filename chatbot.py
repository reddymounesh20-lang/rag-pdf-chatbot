import streamlit as st
import tempfile


from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings


st.title("📄 RAG PDF Chatbot")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    st.success("PDF uploaded successfully!")

    loader = PyPDFLoader(temp_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = splitter.split_documents(documents)

    st.write("Total Chunks:", len(docs))

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    db = FAISS.from_documents(docs, embeddings)

    retriever = db.as_retriever(search_kwargs={"k": 3})

    llm = Ollama(model="mistral")

    question = st.text_input("Ask a question about the PDF")

    if question:

        with st.spinner("Generating answer..."):

            retrieved_docs = retriever.invoke(question)

            context = "\n\n".join([doc.page_content for doc in retrieved_docs])

            prompt = f"""
You are an AI assistant.

Answer the question ONLY from the context below.

Context:
{context}

Question:
{question}

Answer:
"""

            answer = llm.invoke(prompt)

        st.subheader("Answer")
        st.write(answer)

