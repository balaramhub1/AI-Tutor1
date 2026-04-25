from typing import List, Dict, Any, Optional
from langchain_ollama import ChatOllama

MODEL_NAME = "qwen3:8b"

# Create the Ollama LLM instance
llm = ChatOllama(
    model=MODEL_NAME,
    # base url of the Ollama server, default is "http://localhost:11434"
    # reference: https://docs.ollama.com/api/introduction
    base_url="http://localhost:11434",
    temperature=0,
)

# Method to call the Ollama LLM with a prompt
def call_ollama(input: str, tools: Optional[List[Dict[str, Any]]] = None):
    # Create the prompt for the LLM
    if tools:
        print("\n\nAvailable tools:\n")
        return llm.bind_tools(tools).invoke(input)

    return llm.invoke(input)




