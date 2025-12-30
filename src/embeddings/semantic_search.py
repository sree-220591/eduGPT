import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_PATH = "data/processed/eduCPT_chunks.json"


def semantic_search(query, top_k=3):
    with open(DATA_PATH) as f:
        chunks = json.load(f)

    corpus = [c["question"] + " " + c["answer"] for c in chunks]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus)
    query_vec = vectorizer.transform([query])

    similarities = cosine_similarity(query_vec, tfidf_matrix)[0]
    top_indices = similarities.argsort()[-top_k:][::-1]

    return [chunks[i] for i in top_indices]

