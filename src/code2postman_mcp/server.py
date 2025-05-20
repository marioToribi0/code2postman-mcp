from mcp.server.fastmcp import FastMCP
import code2postman_mcp.tools.handle_postman as handle_postman
import code2postman_mcp.tools.handle_files as handle_files
from loguru import logger
import sys

# Configure loguru logger
logger.remove()
logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
logger.add("logs/code2postman.log", rotation="10 MB", format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}")

mcp = FastMCP("code2postman-mcp")

def register_tools():
    """Register all the tools that will be used in the MCP"""
    
    logger.info("Registering Postman Collection tools")
    ## Postman Collection
    mcp.tool()(handle_postman.create_postman_collection)
    mcp.tool()(handle_postman.add_postman_collection_item)
    mcp.tool()(handle_postman.read_postman_collection)
    mcp.tool()(handle_postman.add_postman_collection_info)
    mcp.tool()(handle_postman.add_postman_collection_event)
    mcp.tool()(handle_postman.add_postman_collection_variable)
    mcp.tool()(handle_postman.add_postman_collection_auth)
    mcp.tool()(handle_postman.add_postman_collection_protocol_behavior)
    mcp.tool()(handle_postman.delete_postman_collection_item)
    mcp.tool()(handle_postman.update_postman_collection_variable)
    mcp.tool()(handle_postman.add_postman_collection_folder)
    mcp.tool()(handle_postman.add_item_to_folder)
    
    logger.info("Registering File handling tools")
    ## Files
    mcp.tool()(handle_files.get_tree_directory_from_path)
    mcp.tool()(handle_files.read_file)
    
    logger.success("All tools registered successfully")

def main():
    """Run the MCP server"""
    logger.info("Starting MCP server")
    register_tools()
    logger.info("Running server with stdio transport")
    mcp.run(transport="stdio")
    return mcp

if __name__ == "__main__":
    logger.info("Initializing Code2Postman MCP application")
    main()