import json

DATA_PATH = "/home/user/eduGPT/data/processed/eduGPT_chunks.json"

def load_chunks():
    with open(DATA_PATH,"r") as f:
        return json.load(f)
    
def search_chunks(query,chunks):
    query = query.lower()
    results = []

    for chunk in chunks:
        if (
            query in chunk["topic"].lower()
            or query in chunk["question"].lower()
            or chunk["topic"].lower() in query
        ):
            results.append(chunk)
    
    return results

if __name__ == "__main__":
    chunks = load_chunks()

    while True:
        user_query = input("\nAsk eduGPT a question (or type 'exit'): ")
        if user_query.lower() == 'exit':
            break

        matches = search_chunks(user_query, chunks)

        if not matches:
            print("\neduGPT: I don't have enough information on that yet.")

        else:
            print("\neduGPT found this:\n")
            for m in matches:
                print(f"- {m['answer']}")


            