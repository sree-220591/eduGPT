def build_response(chunks, mode="teach"):
    if mode == "teach":
        return teach(chunks)
    if mode == "simplify":
        return simplify_chunks(chunks)
    return combine_chunks(chunks)

def teach(chunks):
    intro = "Let's understand this step by step.\n\n"
    body = ""

    for i, c in enumerate(chunks[:2], 1):
        body += f"{i}. {c['answer']}\n"

    return intro + body

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