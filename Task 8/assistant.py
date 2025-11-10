import os
import re
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


def load_documents(folder_path):
    docs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt") or filename.endswith(".md"):
            path = os.path.join(folder_path, filename)
            loader = TextLoader(path)
            docs.extend(loader.load())
    return docs


def split_documents(documents, chunk_size=300, chunk_overlap=0):
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)


def store_chunks(chunks, persist_dir="chroma_store"):
    return Chroma.from_documents(documents=chunks, embedding=None, persist_directory=persist_dir)


def keyword_retrieve(query, chunks, top_k=3):
    scored = []
    for chunk in chunks:
        text = chunk.page_content
        score = len(re.findall(query.lower(), text.lower()))
        if score > 0:
            scored.append((score, text))
    scored.sort(reverse=True)
    return [text for _, text in scored[:top_k]]


if __name__ == "__main__":
    print(" Loading and preparing documents...")
    raw_docs = load_documents("data")
    chunks = split_documents(raw_docs)
    store = store_chunks(chunks)

    print(" Assistant is ready! Ask me anything about your files.\n")

    while True:
        query = input(" You: ")
        if query.lower() in ["exit", "quit"]:
            print(" Goodbye!")
            break

        results = keyword_retrieve(query, chunks)
        if results:
            print("\n Top relevant chunks:\n")
            for i, chunk in enumerate(results, 1):
                print(f"{i}. {chunk}\n")
        else:
            print(" No relevant content found.\n")
