"""
LLM Ollama Configuration Module

This module configures and initializes a ChatOllama client for interacting with
a locally-hosted Ollama language model server. It provides a ready-to-use LLM
instance and a convenience function for making calls to the model with optional
tool binding support.
"""

from typing import Any, Dict, List, Optional
from langchain_ollama import ChatOllama

# The model identifier for the Ollama model to use
# This corresponds to a model that should be available in your local Ollama installation
MODEL_NAME = "qwen3:8b"

# Initialize the ChatOllama client with the following configuration:
# - model: The Ollama model to use (qwen3:8b in this case)
# - temperature: Set to 0 for deterministic, reproducible outputs (no randomness)
# - base_url: The HTTP endpoint where the local Ollama server is running
#   (default Ollama port is 11434)
llm = ChatOllama(model=MODEL_NAME, temperature=0, base_url="http://localhost:11434")


def call_ollama(input: str,
                tools: Optional[List[Dict[str, Any]]] = None):
    """
    Invoke the Ollama language model with an input string and optional tools.

    This function provides a convenient interface for calling the LLM with or without
    tool binding. When tools are provided, the model can use them to perform actions
    or retrieve information beyond its base capabilities.

    Args:
        input (str): The input prompt or message to send to the language model.
        tools (Optional[List[Dict[str, Any]]]): An optional list of tool definitions
            that the model can use during execution. Each tool should be a dictionary
            containing the tool's specification. Defaults to None.

    Returns:
        The model's response. The exact return type depends on whether tools are bound:
        - With tools: Returns a response that may include tool calls
        - Without tools: Returns a standard chat completion response

    Examples:
        # Simple text generation
        response = call_ollama("What is the capital of France?")

        # With tools enabled
        tools = [{"type": "function", "function": {...}}]
        response = call_ollama("Search for recent news", tools=tools)
    """
    if tools:
        # Bind the provided tools to the LLM and invoke with the input
        return llm.bind_tools(tools).invoke(input)

    # Invoke the LLM directly without any tool binding
    return llm.invoke(input)