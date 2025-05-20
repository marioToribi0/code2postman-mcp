# Code2Postman MCP

**Code2Postman MCP** - A Model Context Protocol (MCP) server implementation that automatically converts code directories into Postman collections.

## Overview

Code2Postman MCP is an open-source tool that leverages the Model Context Protocol to help developers quickly generate Postman collections from their codebase. This tool analyzes your code files, identifies API endpoints, and creates structured Postman collections that you can use for testing, documentation, and sharing.

## Features

* **Code Analysis**: Automatically scan your codebase to identify API endpoints and their parameters
* **Collection Generation**: Create complete Postman collections with proper structure
* **Folder Organization**: Organize endpoints logically in folders based on code structure
* **Variables Support**: Add and manage collection variables for greater flexibility
* **Authentication Configuration**: Set up authentication methods automatically based on code patterns
* **Event Scripts**: Generate pre-request and test scripts when applicable

## Supported Tools

* `create_postman_collection` - Create a new Postman collection
* `add_postman_collection_item` - Add a request item to a collection
* `read_postman_collection` - Read an existing Postman collection
* `add_postman_collection_info` - Add metadata to a collection
* `add_postman_collection_event` - Add pre-request or test scripts
* `add_postman_collection_variable` - Add variables to a collection
* `add_postman_collection_auth` - Configure authentication for a collection
* `add_postman_collection_protocol_behavior` - Configure protocol behaviors
* `delete_postman_collection_item` - Remove items from a collection
* `update_postman_collection_variable` - Update existing variables
* `add_postman_collection_folder` - Create folders for organizing requests
* `add_item_to_folder` - Add items to specific folders
* `get_tree_directory_from_path` - Get a file tree structure from a directory
* `read_file` - Read the contents of a specific file

## Installation

```bash
pip install code2postman-mcp
```

## Usage with Claude Desktop

1. Add Code2Postman MCP to your `claude_desktop_config.json` file:

```json
"code2postman-mcp": {
    "command": "uvx",
    "args": ["code2postman-mcp"]
}
```

2. Launch Claude Desktop and start using the MCP tools to analyze your code and generate Postman collections.

## Command Line Usage

You can also use Code2Postman MCP directly from the command line:

```bash
uvx code2postman-mcp
```

## Examples

### Creating a Postman Collection from Source Code

1. First, analyze your codebase to identify API endpoints.
2. Create a new Postman collection.
3. Add identified endpoints as items to the collection.
4. Configure authentication if needed.
5. Add collection variables for flexibility.
6. Export the collection as a JSON file that can be imported into Postman.

### Adding to an Existing Collection

You can also extend existing Postman collections by:

1. Reading an existing collection.
2. Adding new items or folders.
3. Updating variables or authentication methods.
4. Saving the updated collection.

## Development

To contribute to Code2Postman MCP:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/code2postman-mcp.git
   ```

2. Install development dependencies:
   ```bash
   cd code2postman-mcp
   uv pip install -e .
   ```

3. Run tests:
   ```bash
   uv run pytest tests/
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
