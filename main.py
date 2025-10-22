from fastapi import FastAPI
from rag import rag_search
from agent_2 import review_generator



app = FastAPI()


@app.get("/{q}")
def ask(q: str):
    ques = q.lower()
    is_comparison = "compare" in ques or "vs" in ques or "compared" in ques

    if is_comparison:
        return review_generator(ques)
    else:
        return rag_search(ques)
    