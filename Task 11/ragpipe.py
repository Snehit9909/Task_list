import time
import argparse
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi


loaders = [TextLoader("t1.txt"), TextLoader("t2.txt"), TextLoader("t3.txt")]
documents = []
for l in loaders:
    documents.extend(l.load())

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=200)
docs = text_splitter.split_documents(documents)
corpus = [doc.page_content for doc in docs]

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
faiss_store = FAISS.from_documents(docs, embedding_model)
faiss_retriever = faiss_store.as_retriever(search_kwargs={"k": 3})

tfidf_vectorizer = TfidfVectorizer().fit(corpus)
tfidf_matrix = tfidf_vectorizer.transform(corpus)

tokenized_corpus = [doc.split() for doc in corpus]
bm25 = BM25Okapi(tokenized_corpus)

dataset = [
    {"question": "What is machine learning?", "answer": "machine learning is a field of artificial intelligence"},
    {"question": "Who developed Python?", "answer": "python was created by guido van rossum"},
    {"question": "What is FAISS used for?", "answer": "faiss is a library developed by facebook ai research for efficient similarity search"}
]

def evaluate_retriever(dataset, retriever_name, retriever_func, k=3):
    results = []
    for item in dataset:
        q = item["question"]
        ground_truth = item["answer"].lower()
        
        start = time.time()
        retrieved_texts = retriever_func(q, k)
        latency = time.time() - start
        
        relevant_hits = sum([1 for text in retrieved_texts if ground_truth in text.lower()])
        recall = 1.0 if relevant_hits > 0 else 0.0
        precision = relevant_hits / k if k > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
        
        results.append({
            "Retriever": retriever_name,
            "Question": q,
            "Recall@k": recall,
            "Precision@k": precision,
            "F1": f1,
            "Latency (s)": round(latency, 4)
        })
    return results

def faiss_func(query, k):
    docs = faiss_retriever.invoke(query)
    return [doc.page_content for doc in docs]

def tfidf_func(query, k):
    q_vec = tfidf_vectorizer.transform([query])
    scores = (tfidf_matrix * q_vec.T).toarray().ravel()
    top_idx = scores.argsort()[::-1][:k]
    return [corpus[i] for i in top_idx]

def bm25_func(query, k):
    scores = bm25.get_scores(query.split())
    top_idx = scores.argsort()[::-1][:k]
    return [corpus[i] for i in top_idx]

def main(compare=False):
    retrievers = {
        "FAISS": faiss_func,
        "TF-IDF": tfidf_func,
        "BM25": bm25_func
    }
    
    all_results = []
    for name, func in retrievers.items():
        results = evaluate_retriever(dataset, name, func, k=3)
        all_results.extend(results)
    
    df = pd.DataFrame(all_results)
    print(tabulate(df, headers="keys", tablefmt="grid"))
    
    if compare:
        plt.figure(figsize=(8,6))
        for name in retrievers.keys():
            subset = df[df["Retriever"] == name]
            plt.plot(subset["Recall@k"], subset["Precision@k"], marker="o", label=name)
        
        plt.xlabel("Recall@k")
        plt.ylabel("Precision@k")
        plt.title("Precision–Recall Comparison")
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare", action="store_true", help="Compare multiple retrievers")
    args = parser.parse_args()
    main(compare=args.compare)
