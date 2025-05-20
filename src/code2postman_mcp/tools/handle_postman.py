import os
import json
from typing import List, Any
from code2postman_mcp.consts.postman_template import POSTMAN_TEMPLATE
from code2postman_mcp.utils.files import is_a_valid_item
from loguru import logger

def validate_string(value: Any, param_name: str) -> str:
    """Validate that a value is a string"""
    if not isinstance(value, str):
        raise TypeError(f"{param_name} must be a string, got {type(value).__name__}")
    return value

def validate_dict(value: Any, param_name: str) -> dict:
    """Validate that a value is a dictionary"""
    if not isinstance(value, dict):
        raise TypeError(f"{param_name} must be a dictionary, got {type(value).__name__}")
    return value

async def create_postman_collection(file_path: str, name: str, description: str) -> str:
    """
    Create a Postman collection from a directory structure. Extension of the file must be .json

    Args:
        file_path: The path to the file to create the Postman collection from (string)
        name: The name of the project (string)
        description: The description of the project (string)
    Returns:
        The initial Postman collection in JSON format (string)
    """
    logger.info(f"Creating Postman collection: {name} at {file_path}")
    
    # Validate input types
    file_path = validate_string(file_path, "file_path")
    name = validate_string(name, "name")
    description = validate_string(description, "description")
    
    if not file_path.endswith(".json"):
        logger.error(f"Invalid file extension for {file_path}, must be .json")
        raise ValueError(f"{file_path} is not a JSON file")
    
    template = POSTMAN_TEMPLATE.format(project_name=name, project_description=description)
    logger.debug(f"Generated template for collection: {name}")
    with open(file_path, "w") as file:
        file.write(template)
    
    logger.success(f"Created Postman collection at {file_path}")
    return template

async def add_postman_collection_item(file_path: str, item: dict) -> dict:
    """
    Add an item to the Postman collection
    
    Args:
        file_path: The path to the Postman collection file (string)
        item: The item dictionary to add (dict containing at least 'name' and 'request' keys)
              Example: {
                  "name": "Get User",
                  "request": {
                      "method": "GET",
                      "url": "https://api.example.com/users/1"
                  }
              }
    Returns:
        The updated Postman collection data (dict)
    """
    logger.info(f"Adding item to Postman collection: {file_path}")
    
    # Validate input types
    file_path = validate_string(file_path, "file_path")
    item = validate_dict(item, "item")
    
    logger.debug(f"Item details: {item.get('name', 'unnamed')}")
    
    with open(file_path, "r") as file:
        data = json.load(file)
    
    if not is_a_valid_item(item):
        logger.error(f"Invalid item structure: {item}")
        raise ValueError("Invalid item")
    
    if "item" not in data:
        logger.warning(f"Collection has no 'item' array, creating one")
        data["item"] = []
    
    data["item"].append(item)
    logger.debug(f"Added item: {item.get('name', 'unnamed')} to collection")

    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
    
    logger.success(f"Updated collection with new item: {item.get('name', 'unnamed')}")
    return data

async def read_postman_collection(file_path: str) -> dict:
    """
    Read the Postman collection
    
    Args:
        file_path: The path to the Postman collection file (string)
    Returns:
        The Postman collection data (dict)
    """
    logger.info(f"Reading Postman collection: {file_path}")
    
    # Validate input types
    file_path = validate_string(file_path, "file_path")
    
    if not file_path.endswith(".json"):
        logger.error(f"Invalid file extension for {file_path}, must be .json")
        raise ValueError(f"{file_path} is not a JSON file")
    
    if not os.path.isfile(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"{file_path} does not exist")
    
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            logger.debug(f"Successfully read collection with {len(data.get('item', []))} items")
            return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {file_path}: {str(e)}")
        raise

async def add_postman_collection_info(file_path: str, info: dict) -> dict:
    """
    Update or add the info section of a Postman collection
    
    Args:
        file_path: The path to the Postman collection file (string)
        info: The info dictionary to update/add (dict)
              Example: {
                  "name": "Updated Collection",
                  "description": "Updated description",
                  "version": "1.0.0",
                  "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
              }
    Returns:
        The updated Postman collection data (dict)
    """
    logger.info(f"Updating info section in collection: {file_path}")
    
    # Validate input types
    file_path = validate_string(file_path, "file_path")
    info = validate_dict(info, "info")
    
    logger.debug(f"Info details: {info}")
    
    with open(file_path, "r") as file:
        data = json.load(file)
    
    if "info" not in data:
        logger.warning("Collection has no 'info' object, creating one")
        data["info"] = {}
    
    data["info"].update(info)
    logger.debug(f"Updated info section with: {info}")
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
    
    logger.success(f"Successfully updated collection info")
    return data

async def add_postman_collection_event(file_path: str, event: dict) -> dict:
    """
    Add an event to the Postman collection
    
    Args:
        file_path: The path to the Postman collection file (string)
        event: The event dictionary with keys like listen, script, etc. (dict)
              Example: {
                  "listen": "prerequest",
                  "script": {
                      "type": "text/javascript",
                      "exec": ["console.log('This runs before each request');"]
                  }
              }
    Returns:
        The updated Postman collection data (dict)
    """
    logger.info(f"Adding event to collection: {file_path}")
    
    # Validate input types
    file_path = validate_string(file_path, "file_path")
    event = validate_dict(event, "event")
    
    logger.debug(f"Event details: {event}")
    
    with open(file_path, "r") as file:
        data = json.load(file)
    
    if "event" not in data:
        logger.warning("Collection has no 'event' array, creating one")
        data["event"] = []
    
    data["event"].append(event)
    logger.debug(f"Added event with listen type: {event.get('listen', 'unknown')}")
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
    
    logger.success(f"Successfully added event to collection")
    return data

async def add_postman_collection_variable(file_path: str, variable: dict) -> dict:
    """
    Add a variable to the Postman collection
    
    Args:
        file_path: The path to the Postman collection file (string)
        variable: The variable dictionary with keys like key, value, type, etc. (dict)
                Example: {
                    "key": "base_url",
                    "value": "https://api.example.com",
                    "type": "string"
                }
    Returns:
        The updated Postman collection data (dict)
    """
    logger.info(f"Adding variable to collection: {file_path}")
    
    # Validate input types
    file_path = validate_string(file_path, "file_path")
    variable = validate_dict(variable, "variable")
    
    logger.debug(f"Variable details: {variable}")
    
    with open(file_path, "r") as file:
        data = json.load(file)
    
    if "variable" not in data:
        logger.warning("Collection has no 'variable' array, creating one")
        data["variable"] = []
    
    data["variable"].append(variable)
    logger.debug(f"Added variable: {variable.get('key', 'unnamed')}")
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
    
    logger.success(f"Successfully added variable: {variable.get('key', 'unnamed')} to collection")
    return data

async def add_postman_collection_auth(file_path: str, auth: dict) -> dict:
    """
    Add or update authentication information for the Postman collection
    
    Args:
        file_path: The path to the Postman collection file (string)
        auth: The auth dictionary with type and necessary auth parameters (dict)
              Example: {
                  "type": "bearer",
                  "bearer": [
                      {
                          "key": "token",
                          "value": "{{token_variable}}",
                          "type": "string"
                      }
                  ]
              }
    Returns:
        The updated Postman collection data (dict)
    """
    logger.info(f"Adding/updating auth in collection: {file_path}")
    
    # Validate input types
    file_path = validate_string(file_path, "file_path")
    auth = validate_dict(auth, "auth")
    
    logger.debug(f"Auth details: {auth}")
    
    with open(file_path, "r") as file:
        data = json.load(file)
    
    data["auth"] = auth
    logger.debug(f"Set auth type: {auth.get('type', 'unknown')}")
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
    
    logger.success(f"Successfully updated auth in collection")
    return data

async def add_postman_collection_protocol_behavior(file_path: str, behavior: dict) -> dict:
    """
    Add or update protocol profile behavior settings for the Postman collection
    
    Args:
        file_path: The path to the Postman collection file (string)
        behavior: The protocolProfileBehavior dictionary (dict)
                 Example: {
                     "disableBodyPruning": true,
                     "followRedirects": false
                 }
    Returns:
        The updated Postman collection data (dict)
    """
    logger.info(f"Adding protocol behavior to collection: {file_path}")
    
    # Validate input types
    file_path = validate_string(file_path, "file_path")
    behavior = validate_dict(behavior, "behavior")
    
    logger.debug(f"Behavior details: {behavior}")
    
    with open(file_path, "r") as file:
        data = json.load(file)
    
    data["protocolProfileBehavior"] = behavior
    logger.debug(f"Set protocol behavior with {len(behavior)} settings")
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
    
    logger.success(f"Successfully updated protocol behavior in collection")
    return data

async def delete_postman_collection_item(file_path: str, item_name: str) -> dict:
    """
    Delete an item from the Postman collection by name
    
    Args:
        file_path: The path to the Postman collection file (string)
        item_name: The name of the item to delete (string)
    Returns:
        The updated Postman collection data (dict)
    """
    logger.info(f"Deleting item '{item_name}' from collection: {file_path}")
    
    # Validate input types
    file_path = validate_string(file_path, "file_path")
    item_name = validate_string(item_name, "item_name")
    
    with open(file_path, "r") as file:
        data = json.load(file)
    
    if "item" not in data:
        logger.warning(f"Collection has no items to delete")
        return data
    
    original_count = len(data["item"])
    data["item"] = [item for item in data["item"] if item.get("name") != item_name]
    deleted_count = original_count - len(data["item"])
    
    if deleted_count > 0:
        logger.debug(f"Removed {deleted_count} item(s) with name: {item_name}")
    else:
        logger.warning(f"No items found with name: {item_name}")
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
    
    logger.success(f"Successfully updated collection after deletion")
    return data

async def update_postman_collection_variable(file_path: str, key: str, new_value: str) -> dict:
    """
    Update a specific variable in the Postman collection by key
    
    Args:
        file_path: The path to the Postman collection file (string)
        key: The key of the variable to update (string)
        new_value: The new value for the variable (string)
    Returns:
        The updated Postman collection data (dict)
    """
    logger.info(f"Updating variable '{key}' in collection: {file_path}")
    
    # Validate input types
    file_path = validate_string(file_path, "file_path")
    key = validate_string(key, "key")
    new_value = validate_string(new_value, "new_value")
    
    logger.debug(f"New value: {new_value}")
    
    with open(file_path, "r") as file:
        data = json.load(file)
    
    if "variable" not in data or not isinstance(data["variable"], list):
        logger.warning(f"Collection has no variables to update")
        return data
    
    variable_found = False
    for var in data["variable"]:
        if var.get("key") == key:
            var["value"] = new_value
            variable_found = True
            logger.debug(f"Updated variable: {key}")
            break
    
    if not variable_found:
        logger.warning(f"Variable not found: {key}")
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
    
    logger.success(f"Successfully saved collection after updating variable")
    return data

async def add_postman_collection_folder(file_path: str, folder_name: str, items: List[dict] = None) -> dict:
    """
    Add a folder to the Postman collection
    
    Args:
        file_path: The path to the Postman collection file (string)
        folder_name: The name of the folder (string)
        items: Optional list of item dictionaries to add to the folder (list of dicts)
    Returns:
        The updated Postman collection data (dict)
    """
    logger.info(f"Adding folder '{folder_name}' to collection: {file_path}")
    
    # Validate input types
    file_path = validate_string(file_path, "file_path")
    folder_name = validate_string(folder_name, "folder_name")
    
    if items is not None and not isinstance(items, list):
        logger.error(f"Items must be a list, got {type(items).__name__}")
        raise TypeError(f"items must be a list, got {type(items).__name__}")
    
    folder = {
        "name": folder_name,
        "item": items or []
    }
    
    logger.debug(f"Created folder '{folder_name}' with {len(folder['item'])} items")
    
    # Use existing function to add the folder as an item
    result = await add_postman_collection_item(file_path, folder)
    logger.success(f"Successfully added folder '{folder_name}' to collection")
    
    return result

async def add_item_to_folder(file_path: str, folder_name: str, item: dict) -> dict:
    """
    Add an item to a specific folder in the Postman collection
    
    Args:
        file_path: The path to the Postman collection file (string)
        folder_name: The name of the folder to add the item to (string)
        item: The item dictionary to add (dict)
    Returns:
        The updated Postman collection data (dict)
    """
    logger.info(f"Adding item to folder '{folder_name}' in collection: {file_path}")
    
    # Validate input types
    file_path = validate_string(file_path, "file_path")
    folder_name = validate_string(folder_name, "folder_name")
    item = validate_dict(item, "item")
    
    if not is_a_valid_item(item):
        logger.error(f"Invalid item structure: {item}")
        raise ValueError("Invalid item")
    
    with open(file_path, "r") as file:
        data = json.load(file)
    
    if "item" not in data:
        logger.warning("Collection has no items, cannot find folder")
        raise ValueError(f"Collection has no items, cannot find folder '{folder_name}'")
    
    folder_found = False
    for collection_item in data["item"]:
        if collection_item.get("name") == folder_name and "item" in collection_item:
            collection_item["item"].append(item)
            folder_found = True
            logger.debug(f"Added item to folder '{folder_name}'")
            break
    
    if not folder_found:
        logger.warning(f"Folder '{folder_name}' not found in collection")
        raise ValueError(f"Folder '{folder_name}' not found in collection")
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
    
    logger.success(f"Successfully added item to folder '{folder_name}'")
    return data

if __name__ == "__main__":
    import asyncio
    
    async def test_postman_collection():
        # Create a basic collection
        collection_path = "test_collection.json"
        await create_postman_collection(collection_path, "Test API", "Test API Collection")
        
        # Add collection-level variables
        await add_postman_collection_variable(collection_path, {
            "key": "base_url",
            "value": "https://api.example.com",
            "type": "string"
        })
        
        await add_postman_collection_variable(collection_path, {
            "key": "token",
            "value": "",
            "type": "string"
        })
        
        # Add collection-level auth
        await add_postman_collection_auth(collection_path, {
            "type": "bearer",
            "bearer": [
                {
                    "key": "token",
                    "value": "{{token}}",
                    "type": "string"
                }
            ]
        })
        
        # Add a folder for authentication endpoints
        await add_postman_collection_folder(collection_path, "Authentication")
        
        # Add items to the Authentication folder
        await add_item_to_folder(collection_path, "Authentication", {
            "name": "Login",
            "request": {
                "method": "POST",
                "url": "{{base_url}}/auth/login",
                "body": {
                    "mode": "raw",
                    "raw": "{\n\t\"username\": \"user\",\n\t\"password\": \"pass\"\n}",
                    "options": {
                        "raw": {
                            "language": "json"
                        }
                    }
                }
            }
        })
        
        await add_item_to_folder(collection_path, "Authentication", {
            "name": "Refresh Token",
            "request": {
                "method": "POST",
                "url": "{{base_url}}/auth/refresh"
            }
        })
        
        # Add another folder for user endpoints
        await add_postman_collection_folder(collection_path, "Users")
        
        # Add items to the Users folder
        await add_item_to_folder(collection_path, "Users", {
            "name": "Get User Profile",
            "request": {
                "method": "GET",
                "url": "{{base_url}}/users/me"
            }
        })
        
        # Read and print the final collection
        final_collection = await read_postman_collection(collection_path)
        print(json.dumps(final_collection, indent=2))
        
        print("Test completed successfully!")
    
    asyncio.run(test_postman_collection())