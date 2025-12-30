import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_PATH = "data/processed/eduGPT_chunks.json"
SIMILARITY_THRESHOLD = 0.2

def semantic_search(query, top_k=3):
    with open(DATA_PATH, "r") as f:
        chunks = json.load(f)

    # Combine all educational text
    corpus = [
        f"{c['topic']} {c['question']} {c['answer']}"
        for c in chunks
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(corpus)
    query_vec = vectorizer.transform([query])

    similarities = cosine_similarity(query_vec, tfidf_matrix)[0]
    
    scored = list(enumerate(similarities))
    scored.sort(key=lambda x: x[1],reverse=True)

    filtered = [
        chunks[i] for i, score in scored[:top_k]
        if score >= SIMILARITY_THRESHOLD
    ]

    return filtered


