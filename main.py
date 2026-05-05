"""
AI Tutor FastAPI Application

This module defines the main FastAPI application for the AI Tutor service.
It provides a REST API endpoint for handling chat queries and generating responses.
"""
import os
from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from agent import ChatAgent
from llm_ollama import call_ollama

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#BASE_DIR = os.path.dirname(os.getcwd())
UPLOAD_DIR = os.path.join(BASE_DIR,"..", "uploaded_pdfs")

print("AI Tutor - Upload directory path: ", UPLOAD_DIR)
print("Base directory path: ", BASE_DIR)

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
        :param query:
        :param file:
    """
    # Validate that the query is not empty
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    pdf_path = None

    if file:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        pdf_path = os.path.join(UPLOAD_DIR, file.filename)
        print("Received file upload path : ", pdf_path)
        print("Received file upload: ", file.filename)

        with open(pdf_path, "wb") as f:
            f.write(await file.read())

    result = await chat_agent.run(query, pdf_path)

    return {"answer": result}