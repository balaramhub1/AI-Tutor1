from fastapi import FastAPI, HTTPException, Form
from llm_ollama import call_ollama

app = FastAPI()

@app.post("/chat/")
async def chat(query: str = Form(...)):
    # Here you would typically process the message and generate a response
    # For demonstration purposes, we'll just echo the message back
    #response = f"You said: {query}"
    return {"answer": call_ollama(query)}
