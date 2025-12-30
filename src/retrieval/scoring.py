def score_chunk(query,chunk):
    score = 0
    query = query.lower()

    if query in chunk["topic"].lower():
        score += 3
    if query in chunk["question"].lower():
        score += 2
    if any(word in chunk["answer"].lower() for word in query.split()):
        score += 1

    return score