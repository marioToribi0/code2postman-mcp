from mcp.server.fastmcp import FastMCP
import code2postman_mcp.tools.handle_postman as handle_postman
import code2postman_mcp.tools.handle_files as handle_files

mcp = FastMCP()

def register_tools():
    """Register all the tools that will be used in the MCP"""
    
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
    
    ## Files
    mcp.tool()(handle_files.get_tree_directory_from_path)
    mcp.tool()(handle_files.read_file)

def run_server():
    """Run the MCP server"""
    register_tools()
    mcp.run(transport="stdio")
    return mcp

if __name__ == "__main__":
    run_server()