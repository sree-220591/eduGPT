from src.utils.examples import EXAMPLES

def add_example(answer_text):
    for key, example in EXAMPLES.items():
        if key in answer_text.lower():
            return answer_text + "\n\n" + example
    return answer_text

def build_response(chunks, mode="teach"):
    if mode == "teach":
        answer = teach(chunks)
    elif mode == "simplify":
        answer = simplify_chunks(chunks)
    else:
        answer = combine_chunks(chunks)

    final_answer = add_example(answer)
    return final_answer


def teach(chunks):
    intro = "Based on what I have learned so far,let's understand this step by step.\n\n"
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