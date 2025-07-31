# generate_faiss.py

import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Paths
DATA_DIR = "data"
VECTORSTORE_PATH = "vectorstore/db_faiss"

# Embedding Model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def generate_faiss_vectorstore():
    print("📂 Loading PDFs from:", DATA_DIR)
    loader = DirectoryLoader(DATA_DIR, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    print(f"🧩 Splitting {len(documents)} documents...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_documents(documents)

    print("📦 Generating FAISS vectorstore...")
    vectorstore = FAISS.from_documents(docs, embedding_model)

    print("💾 Saving vectorstore to:", VECTORSTORE_PATH)
    vectorstore.save_local(VECTORSTORE_PATH)
    print("✅ FAISS vectorstore saved successfully.")

if __name__ == "__main__":
    generate_faiss_vectorstore()
