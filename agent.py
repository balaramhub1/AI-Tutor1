from mcp_client import list_mcp_tools, call_mcp_tool
from llm_ollama import call_ollama
from prompt import get_prompt
from langchain_core.messages import AIMessage

class ChatAgent:

    def needs_tool_execution(self, llm_response: AIMessage) -> bool:
        return bool(llm_response.tool_calls)

    async def run(self, query: str, pdf_path: str) -> str:
        tools_response = await list_mcp_tools()

        tools = [
            {
                "type": "function",
                "function": {
                    #"name": tool["name"],
                    "name": tool.name,
                    #"description": tool["description"],
                    "description": tool.description,
                    #"parameters": tool["inputSchema"],
                    "parameters": tool.inputSchema,
                },
            }
            for tool in tools_response.tools
        ]

        print("agent.py -> Available tools for LLM: ", tools)

        custom_prompt = get_prompt(query, pdf_path)

        print("agent.py -> Custom prompt for LLM: ", custom_prompt)

        llm_response = call_ollama(custom_prompt, tools)

        print("agent.py -> LLM response: ", llm_response)

        if self.needs_tool_execution(llm_response):
            tool_call = llm_response.tool_calls[0]
            #tool_name = tool_call["name"]
            #tool_args = tool_call["arguments"]
            #arguments = tool_call["arguments"]

            tool_result = await call_mcp_tool(
                tool_name = tool_call["name"],
                arguments = tool_call["args"]
            )

            print("agent.py -> Tool execution result: ", tool_result)

            final_prompt = get_prompt(query, pdf_path, tool_result)

            print("agent.py -> Final prompt for LLM after tool execution: ", final_prompt)

            final_response = call_ollama(final_prompt, tools)

            print("agent.py -> Final LLM response after tool execution: ", final_response)

            final_answer = final_response.content
        else:
            final_answer = llm_response.content

        return final_answer


"""
    def __init__(self):
        self.tools = None

    async def initialize(self):
        self.tools = await list_mcp_tools()

    async def respond(self, query: str) -> str:
        tool_result = None
        if self.tools:
            tool_result = await call_mcp_tool(self.tools[0], {"coin": "bitcoin", "currency": "usd"})

        prompt = get_prompt(query, tool_result)
        response = call_ollama(prompt, tools=self.tools)
        return response.content if isinstance(response, AIMessage) else response
"""


