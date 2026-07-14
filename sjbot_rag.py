# ==============================================================
# SJBot — RAG institucional
# Indexa el corpus institucional (admisión, matrícula, servicios, etc.)
# con embeddings locales (gratis, sin API) y FAISS.
# ==============================================================
import streamlit as st

from corpus_institucional import DOCUMENTOS_INSTITUCIONALES


@st.cache_resource(show_spinner="Cargando base de conocimiento institucional…")
def construir_retriever():
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_core.documents import Document
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    docs = []
    for d in DOCUMENTOS_INSTITUCIONALES:
        for chunk in splitter.split_text(d["texto"]):
            docs.append(Document(page_content=chunk, metadata={"titulo": d["titulo"]}))

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 3})
