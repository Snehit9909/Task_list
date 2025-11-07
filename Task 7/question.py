import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.llms.fake import FakeListLLM


def load_documents(file_path: str):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()

    splitter = CharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = splitter.split_documents(documents)

    print(f"Loaded {len(chunks)} text chunks from {file_path}")
    return chunks


def build_vectorstore(docs, index_path="faiss_index"):
    embeddings = FakeEmbeddings(size=128)
    store = FAISS.from_documents(docs, embeddings)
    store.save_local(index_path)
    print(f"Knowledge base saved to: {index_path}")


def query_knowledge_base(query, index_path="faiss_index"):
    embeddings = FakeEmbeddings(size=128)
    store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

    docs = store.similarity_search(query, k=3)
    context = " ".join(" ".join([d.page_content for d in docs]).split())

    prompt = f"""
    Use the context below to answer the question.
    <context>{context}</context>
    Question: {query}
    """

    llm = FakeListLLM(responses=[f"Mock Answer: {context[:300]}..."])
    result = llm.generate([{"role": "user", "content": prompt}])
    return result.generations[0][0].text


if __name__ == "__main__":
    print("Loading up of chunks to Knowledge Base")
    docs = load_documents("Networking.txt")
    docs=load_documents("OS.txt")
    build_vectorstore(docs)

    print("\n You have a question? Ask here")
    user_q = input("Question: ").strip()
    if user_q:
        answer = query_knowledge_base(user_q)
        print("\nAnswer:", answer)
    else:
        print("No question provided.")
