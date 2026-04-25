Required Libraries:\
__fastapi__ - A modern, fast (high-performance) web framework for 
            building APIs with Python 3.6+ based on standard Python type hints.\
*uvicorn - A lightning-fast ASGI server implementation, using uvloop and httptools.\
*langchain-core - A core library for building language model applications.\
*langchain-ollama - A library for integrating Ollama with LangChain,
        allowing you to use Ollama as a language model in your applications.\
*mcp - A library to create/ use the MCP servers.


Install the dependencies using pip:
 - pip install -r requirements.txt

Command to run the server:
 - uvicorn main:app --host 127.0.0.1 --port 9123 --reload