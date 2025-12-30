PROBABILITY_KEYWORDS = [
    "probability", "event", "sample space", "random",
    "chance", "outcome", "experiment"
]

def is_in_scope(query):
    query = query.lower()
    return any(word in query for word in PROBABILITY_KEYWORDS)
