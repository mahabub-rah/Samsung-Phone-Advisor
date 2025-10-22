from fastapi import FastAPI
from rag import rag_search
app = FastAPI()


@app.get("/{q}")
def ask(q: str):
    ques = q.lower()
    is_comparison = "compare" in ques or "vs" in ques or "compared" in ques

    if is_comparison:
        return {
            "question" : ques,
            "answer" : "implementation the agent running......."
        }
    else:
        return rag_search(ques)
    