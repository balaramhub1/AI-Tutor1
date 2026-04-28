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

# **Request via POST MAN:**
http://127.0.0.1:9123/chat (POST)
Request Body: key = query, value = "What is the price of bitcoin?"

## **AI Tutor Application - Complete Workflow Summary**

### **Architecture Overview**
This is an AI-powered tutoring system built with FastAPI that integrates a local Ollama LLM with the Model Context Protocol (MCP) to provide tool-augmented AI responses. 
The system follows an agent-based architecture where the AI can dynamically discover and use external tools to answer user queries.

---

### **Component Breakdown**

#### **1. Entry Point: `main.py` (FastAPI Application)**
- **Purpose**: HTTP server that exposes the chat API endpoint
- **Framework**: FastAPI with form-based input
- **Endpoint**: `POST /chat`
  - Accepts user queries via form data
  - Validates input (non-empty)
  - Delegates to `ChatAgent` for processing
  - Returns JSON response with the answer

#### **2. Core Logic: `agent.py` (ChatAgent Class)**
- **Purpose**: Orchestrates the entire AI workflow with tool calling capability
- **Key Method**: `async run(query: str) -> str`

**Workflow Steps:**
1. **Tool Discovery**: Fetches available tools from MCP server via `list_mcp_tools()`
2. **Tool Formatting**: Converts MCP tool schemas into LangChain-compatible format
3. **Initial LLM Call**: Sends query with tool definitions to Ollama
4. **Decision Point**: Checks if LLM wants to use tools via `needs_tool_execution()`
5. **Tool Execution Path** (if tools needed):
   - Extracts tool name and arguments from LLM response
   - Calls the tool via `call_mcp_tool()`
   - Creates enhanced prompt with tool results
   - Makes second LLM call with context
6. **Direct Response Path** (if no tools needed):
   - Returns LLM's direct answer
7. **Returns**: Final answer string

#### **3. LLM Interface: `llm_ollama.py`**
- **Purpose**: Abstracts Ollama LLM communication
- **Configuration**:
  - Model: `qwen3:8b`
  - Temperature: `0` (deterministic)
  - Server: `http://localhost:11434`
- **Function**: `call_ollama(input, tools=None)`
  - Without tools: Direct text generation
  - With tools: Binds tools and enables function calling

#### **4. MCP Client: `mcp_client.py`**
- **Purpose**: Interfaces with external MCP server for tool access
- **Protocol**: Server-Sent Events (SSE)
- **Server URL**: `http://127.0.0.1:8000/sse`

**Functions:**
- `list_mcp_tools()`: Discovers available tools on MCP server
- `call_mcp_tool(tool_name, arguments)`: Executes specific tool with parameters

#### **5. Prompt Engineering: `prompt.py`**
- **Purpose**: Generates structured prompts for the LLM
- **Function**: `get_prompt(query, tool_result=None)`
- **Logic**:
  - **With tool result**: Instructs LLM to base answer on tool output
  - **Without tool result**: Answer from general knowledge
  - Ensures LLM prioritizes tool data when available

---

### **Complete Request Flow**

```
User Query
    ↓
[1] POST /chat endpoint (main.py)
    ↓
[2] ChatAgent.run() (agent.py)
    ↓
[3] list_mcp_tools() → MCP Server
    ↓
[4] Format tools for LangChain
    ↓
[5] get_prompt(query) → Create initial prompt
    ↓
[6] call_ollama(prompt, tools) → Ollama LLM
    ↓
[7] Check if LLM wants to use tools
    ↓
    ├─ YES: Tool Required
    │   ↓
    │   [8] Extract tool_call (name + args)
    │   ↓
    │   [9] call_mcp_tool() → MCP Server executes tool
    │   ↓
    │   [10] get_prompt(query, tool_result) → Enhanced prompt
    │   ↓
    │   [11] call_ollama(enhanced_prompt, tools) → Second LLM call
    │   ↓
    │   [12] Extract final answer
    │
    └─ NO: Direct Answer
        ↓
        [8] Extract content from LLM response
    ↓
[13] Return {"answer": final_answer}
    ↓
User receives response
```

---

### **Key Design Patterns**

1. **Agent Pattern**: `ChatAgent` acts as an autonomous agent that decides when to use tools
2. **Tool Augmentation**: LLM can request external tool execution to enhance responses
3. **ReAct Pattern**: Reasoning (LLM) → Acting (tool call) → Reasoning (final answer)
4. **Separation of Concerns**: Each module has a single responsibility
5. **Async/Await**: Properly handles asynchronous MCP communication

---

### **Technology Stack**

- **Web Framework**: FastAPI
- **LLM**: Ollama (qwen3:8b model)
- **LLM Framework**: LangChain
- **Tool Protocol**: MCP (Model Context Protocol)
- **Transport**: SSE (Server-Sent Events)
- **Language**: Python 3.12+

---

### **Dependencies & Setup**

**Requirements:**
- `fastapi` - Web API framework
- `uvicorn` - ASGI server
- `langchain-core` - LLM framework core
- `langchain-ollama` - Ollama integration
- `mcp` - Model Context Protocol client

**Running the Application:**
```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --host 127.0.0.1 --port 9123 --reload
```

**Prerequisites:**
1. Ollama server running on `localhost:11434` with `qwen3:8b` model
2. MCP server running on `localhost:8000/sse` with available tools

---

### **Example Use Case**

**Scenario**: User asks "What's the price of Bitcoin?"

1. User sends POST request to `/chat`
2. Agent fetches available tools (e.g., `get_crypto_price`)
3. LLM receives query + tool definitions
4. LLM decides to use `get_crypto_price` tool
5. Agent calls MCP server to execute tool
6. Tool returns: `{"bitcoin": "$45,000"}`
7. Agent creates new prompt with tool result
8. LLM generates natural language answer: "The current price of Bitcoin is $45,000"
9. User receives formatted response

---

### **Strengths**

✅ Modular, maintainable architecture  
✅ Tool-augmented AI for dynamic capabilities  
✅ Deterministic LLM output (temperature=0)  
✅ Proper async handling for I/O operations  
✅ Clear separation between routing, logic, and integrations  

### **Potential Improvements**

⚠️ Error handling could be more robust  
⚠️ No caching mechanism for tool lists  
⚠️ Limited logging/observability  
⚠️ No retry logic for external service calls  
⚠️ Hardcoded URLs and configuration  

This system effectively demonstrates a production-grade AI agent architecture with external tool integration capabilities!

===================================================================================================

## Complete Workflow (Runtime)

1. A client sends `POST /chat` with form field `query` to `main.py`.
2. `chat()` in `main.py` validates the query (`query.strip()` must not be empty).
3. If valid, it calls `await chat_agent.run(query)` on a `ChatAgent` instance from `agent.py`.
4. In `ChatAgent.run()`:
   - It calls `await list_mcp_tools()` from `mcp_client.py`.
   - `list_mcp_tools()` opens an SSE connection to `MCP_URL` (`http://127.0.0.1:8000/sse`), initializes an MCP `ClientSession`, and fetches available tools.
5. `ChatAgent` converts MCP tool objects (`tool.name`, `tool.description`, `tool.inputSchema`) into LangChain/OpenAI-style tool definitions.
6. It builds an initial prompt via `get_prompt(query)` from `prompt.py` (no tool result yet).
7. It calls `call_ollama(custom_prompt, tools)` from `llm_ollama.py`.
   - This uses `ChatOllama` configured with model `qwen3:8b`, temperature `0`, base URL `http://localhost:11434`.
8. Agent checks `llm_response.tool_calls` via `needs_tool_execution()`:
   - **If tool call exists**:
     - Takes first tool call (`llm_response.tool_calls[0]`)
     - Executes it through `await call_mcp_tool(tool_name=..., arguments=...)`
     - Builds final prompt with `get_prompt(query, tool_result)`
     - Calls LLM again with tools: `call_ollama(final_prompt, tools)`
     - Returns `final_response.content`
   - **If no tool call**:
     - Returns `llm_response.content`
9. `main.py` wraps the final text into JSON: `{"answer": result}`.

---

## File-by-File Role Summary

- `main.py`
  - FastAPI app and `/chat` endpoint.
  - Input validation + orchestration entrypoint.
  - Uses `ChatAgent` as main processing path.

- `agent.py`
  - Central orchestrator.
  - Discovers tools dynamically from MCP.
  - Performs 1-pass or 2-pass LLM flow depending on whether tools are requested.

- `mcp_client.py`
  - MCP integration layer over SSE transport.
  - `list_mcp_tools()` for discovery.
  - `call_mcp_tool()` for execution.

- `llm_ollama.py`
  - LLM client configuration and invocation abstraction.
  - Supports both plain prompts and tool-bound prompts.

- `prompt.py`
  - Prompt template builder.
  - Explicitly instructs the model to prioritize tool results when present.

- `readme.md`
  - Dependency and run instructions.
  - Also contains a long architecture summary (which mostly matches current logic).

---

## Key Behavior Notes

- Tool use is **model-driven**: the LLM decides whether to call a tool.
- Tool execution is currently limited to the **first** tool call only (`tool_calls[0]`).
- The pipeline is effectively a **ReAct-style two-step** when tool usage occurs:
  - LLM decides action -> tool runs -> LLM synthesizes final answer.
- External dependencies required at runtime:
  - Ollama server with `qwen3:8b` available at `localhost:11434`
  - MCP server at `127.0.0.1:8000/sse`

---

## Current Gaps / Risks to Be Aware Of

- `mcp_client.py` has standalone triple-quoted strings placed before functions (not function docstrings); harmless but not ideal.
- `main.py` still has some outdated comments saying “placeholder/echo”, while it now calls the full agent flow.
- Minimal error handling around:
  - MCP connectivity failures
  - Invalid tool-call payloads from model
  - Ollama invocation failures
- No retries/timeouts/circuit-breaker behavior yet.

If you want, I can next give you a compact “sequence diagram style” version and a prioritized hardening checklist (error handling, retries, and observability) tailored to this exact code.
