from typing import Any, Dict, List, Optional

def get_prompt(query: str, pdf_path: str = None, tool_result: Optional[Any] = None) -> str:

    prompt = f"""
    You are an AI assistant that helps users with their queries. Your task is answer the user's query using the information provided.
    
    ## User Query: {query}
    
    ## PDF Path: {pdf_path if pdf_path else "No PDF uploaded"}
    
    ## Tool Result: {tool_result if tool_result else "No tool result available"}
    
    ## Instructions:
    1. If tool result is available:
    - You MUST use the information from the tool result to answer the user's query.
    - Base your answer primarily on the tool result content.
    - Do NOT ignore the tool result or answer from general knowledge when tool result exists.
    
    2. If tool result is NOT available:
     - Answer based on your general knowledge and understanding of the user's query.
     - Be clear that you're answering without specific document context.
     
    """
    return prompt
