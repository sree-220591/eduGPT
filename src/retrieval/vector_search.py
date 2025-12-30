import json
from src.utils.topic_aliases import TOPIC_ALIASES
from src.generation.response_builder import build_response
from src.retrieval.scoring import score_chunk
from src.embeddings.semantic_search import semantic_search
from src.reasoning.probability_rules import RULES
from src.reasoning.stepwise import STEPWISE_RULES


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
        print(f"[DEBUG] User query received: {user_query}")
        if user_query.lower() == 'exit':
            break

        if "step by step" in user_query.lower() or "steps" in user_query.lower():
            for key, func in STEPWISE_RULES.items():
                if key in user_query.lower():
                    print("\neduGPT:", func())
                    continue


        normalized_query = user_query.lower()

        for rule_key, rule_func in RULES.items():
            if rule_key in normalized_query:
                print("\neduGPT:", rule_func())
                continue

        else:
            matches = search_chunks(user_query, chunks)


            if not matches:
                print("[DEBUG] No keyword matches found")

                semantic_matches = semantic_search(user_query)

                if semantic_matches:
                    print("[DEBUG] Semantic matches found")
                    matches = semantic_matches
                else:
                    print("[DEBUG] No semantic matches found")

                    from src.utils.scope_guard import is_in_scope

                    if is_in_scope(user_query):
                        print("\neduGPT: I know this is about probability, but I haven't learned this concept yet.")
                    else:
                        print("\neduGPT: This is outside my current scope (probability).")

                    continue


            else:
                last_chunks = matches
                answer = build_response(matches)
                print(f"\neduGPT: {answer}")


            