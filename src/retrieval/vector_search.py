import json
from src.utils.topic_aliases import TOPIC_ALIASES
from src.generation.response_builder import build_response
from src.retrieval.scoring import score_chunk
from src.embeddings.semantic_search import semantic_search

DATA_PATH = "/home/user/eduGPT/data/processed/eduGPT_chunks.json"

def load_chunks():
    with open(DATA_PATH,"r") as f:
        return json.load(f)
    
def expand_query(query):
    expanded = [query]
    for key,values in TOPIC_ALIASES.items():
        if key in query:
            expanded.extend(values)
    return expanded

def search_chunks(query,chunks):
    query = query.lower()
    expanded_queries = expand_query(query)

    matched_chunks = []

    for chunk in chunks:
        text = (
            chunk["topic"].lower() + " " +
            chunk["question"].lower()
        )

        for q in expanded_queries:
            if q in text:
                matched_chunks.append(chunk)
                break
        # if (
        #     query in chunk["topic"].lower()
        #     or query in chunk["question"].lower()
        #     or chunk["topic"].lower() in query
        # ):
        #     results.append(chunk)
    scored_chunks = []
    for chunk in matched_chunks:
        score = score_chunk(query,chunk)
        scored_chunks.append((score,chunk))

    scored_chunks.sort(reverse=True, key=lambda x: x[0])
    
    return [chunk for score, chunk in scored_chunks]

if __name__ == "__main__":
    chunks = load_chunks()
    last_chunks = []

    while True:
        user_query = input("\nAsk eduGPT a question (or type 'exit'): ")
        if user_query.lower() == 'exit':
            break
        
        if "simplify" in user_query.lower() and last_chunks:
            answer = build_response(last_chunks, mode="simplify")
            print(f"eduGPT: {answer}")
            continue 

        matches = search_chunks(user_query, chunks)

        if not matches:
            matches = semantic_search(user_query)

        else:
            last_chunks = matches
            answer = build_response(matches)
            print(f"\neduGPT: {answer}")


            