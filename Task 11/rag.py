from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate

loaders = [
    TextLoader("text1.txt"),
    TextLoader("text2.txt"),
    TextLoader("text3.txt")
]

documents = []
for l in loaders:
    documents.extend(l.load())

text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = FAISS.from_documents(docs, embedding_model)
vectorstore.save_local("faiss_index")

def rag_query(query, k=3):
    vs = FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)
    
    results = vs.similarity_search(query, k=3)
    context = "\n\n".join([r.page_content for r in results])
    
    template = PromptTemplate(
        input_variables=["query", "context"],
        template="Question: {query}\n\nRelevant Information:\n{context}\n\nAnswer (summary from context):"
    )
    return template.format(query=query, context=context)

if __name__ == "__main__":
    user_query = input("Ask your question: ")
    answer = rag_query(user_query, k=3)
    print("\n Answer to the query:\n")
    print(answer)
