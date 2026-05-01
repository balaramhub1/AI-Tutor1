"""
AI Tutor FastAPI Application

This module defines the main FastAPI application for the AI Tutor service.
It provides a REST API endpoint for handling chat queries and generating responses.
"""
import os
from fastapi import FastAPI, HTTPException, Form
from agent import ChatAgent
from llm_ollama import call_ollama

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "..", "uploaded_pdfs")

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize the FastAPI application instance
app = FastAPI()

chat_agent = ChatAgent()


@app.post("/chat")
async def chat(query: str = Form(...),
               file: UploadFile | None = File(None)
               ):
    """
    Handle chat queries and return AI-generated responses.

    This endpoint accepts a user query via form data and processes it to generate
    an appropriate response. Currently returns an echo response for demonstration,
    but is designed to be extended with actual AI processing logic.

    Args:
        query (str): The user's question or message, submitted as form data.
            This parameter is required (indicated by Form(...)).

    Returns:
        dict: A JSON response containing the answer with the following structure:
            {
                "answer": str  # The generated response to the user's query
            }

    Raises:
        HTTPException: 400 status code if the query is empty or invalid.

    Example:
        POST /chat
        Form Data: query="What is machine learning?"
        Response: {"answer": "What is machine learning?"}

    Notes:
        - This is a placeholder implementation that echoes the query back
        - In production, this should integrate with the LLM and agent logic
        - The endpoint expects application/x-www-form-urlencoded content type
    """
    # Validate that the query is not empty
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    pdf_path = None

    if file:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        pdf_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(pdf_path, "wb") as f:
            f.write(await file.read())

    result = await chat_agent.run(query, pdf_path)


    # Invoke the Ollama LLM with the user's query and return the response
    # The call_ollama function handles the communication with the local Ollama server
    # and returns the model's generated answer, which is then wrapped in a JSON response
    # return {"answer": call_ollama(query)}
    result = await chat_agent.run(query)
    return {"answer": result}