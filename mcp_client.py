"""
MCP Client Module

This module provides client functionality for interacting with a Model Context Protocol (MCP)
server via Server-Sent Events (SSE). It enables the AI Tutor to discover and execute tools
available on the MCP server.

The MCP (Model Context Protocol) allows language models to access external tools and resources
through a standardized interface.
"""

from mcp import ClientSession
from mcp.client.sse import sse_client

# URL endpoint of the MCP server using Server-Sent Events transport
MCP_URL = "http://127.0.0.1:8000/sse"

"""
    Retrieve the list of available tools from the MCP server.

    This function establishes a connection to the MCP server via SSE, initializes
    a client session, and requests the catalog of tools that can be invoked.

    Returns:
        list: A list of tool definitions available on the MCP server. Each tool
            definition typically includes the tool's name, description, and parameter schema.

    Raises:
        Exception: If the connection to the MCP server fails or if the server
            returns an error during tool listing.

    Notes:
        - Uses SSE (Server-Sent Events) for real-time communication
        - Automatically manages connection lifecycle with context managers
        - Debug output is printed to console for monitoring
    """
async def list_mcp_tools():
    # Establish SSE connection to the MCP server
    async with sse_client(url=MCP_URL) as streams:
        # Create a client session using the established streams
        async with ClientSession(*streams) as session:
            # Initialize the session handshake with the server
            await session.initialize()

            # Request the list of available tools from the MCP server
            tools = await session.list_tools()
            print("MCP-Client : Available tools - ", tools)
            return tools

"""
    Execute a specific tool on the MCP server with provided arguments.

    This function connects to the MCP server, invokes the named tool with the given
    arguments, and returns the result. Each invocation creates a fresh connection
    to ensure clean state.

    Args:
        tool_name (str): The name of the tool to execute. This must match one of
            the tools available from list_mcp_tools().
        arguments (dict): A dictionary of arguments to pass to the tool. The expected
            keys and value types depend on the specific tool's schema.

    Returns:
        The result returned by the tool execution. The structure and type depend
        on the specific tool being called.

    Raises:
        Exception: If the tool name is invalid, arguments don't match the tool's
            schema, or if any connection/execution error occurs.

    Notes:
        - Each call establishes a new connection to the MCP server
        - Tool execution results are logged to console for debugging
        - Arguments must conform to the tool's expected schema
    """
async def call_mcp_tool(tool_name: str, arguments: dict):
    # Establish SSE connection to the MCP server
    async with sse_client(url=MCP_URL) as streams:
        # Create a client session using the established streams
        async with ClientSession(*streams) as session:
            # Initialize the session handshake with the server
            await session.initialize()
            # Call the specified tool with the provided arguments
            result = await session.call_tool(tool_name, arguments)
            print(f"MCP-Client : Result from tool '{tool_name}' - ", result)
            return result