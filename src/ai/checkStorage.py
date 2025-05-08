import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

load_dotenv()
caminho_faiss = os.getenv("FAISS_PATH")

embeddings = OpenAIEmbeddings()
faiss = FAISS.load_local(caminho_faiss, embeddings, allow_dangerous_deserialization=True)

# Recupera todos os documentos armazenados
docs = faiss.similarity_search(" ", k=1000)

for i, doc in enumerate(docs):
    print(f"\nDocumento {i+1}")
    print(f"ID: {doc.metadata["id"]}")
    print(f"Conteúdo: {doc.page_content}")
    print(f"Metadados: {doc.metadata}")