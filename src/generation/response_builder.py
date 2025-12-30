def build_response(chunks, mode="normal"):
    if mode == "simplify":
        return simplify_chunks(chunks)
    return combine_chunks(chunks)

def combine_chunks(chunks):
    response = ""
    for c in chunks:
        response += c["answer"] + " "

    return response.strip()

def simplify_chunks(chunks):
    simplified = []

    for c in chunks:
        simplified.append(shorten(c["answer"]))

    return " ".join(simplified)

def shorten(text):
    sentences = text.split(".")
    return sentences[0] + "."