import os
import json
from code2postman_mcp.consts.postman_template import POSTMAN_TEMPLATE
from code2postman_mcp.utils.files import is_a_valid_item

async def create_postman_collection(file_path: str, name: str, description: str) -> str:
    """
    Create a Postman collection from a directory structure. Extension of the file must be .json

    Args:
        file_path: The path to the file to create the Postman collection from
        name: The name of the project
        description: The description of the project
    Returns:
        The initial Postman collection in JSON format
    """
    if not file_path.endswith(".json"):
        raise ValueError(f"{file_path} is not a JSON file")
    
    template = POSTMAN_TEMPLATE.format(project_name=name, project_description=description)
    print(template)
    with open(file_path, "w") as file:
        file.write(template)
    
    return template

async def add_postman_collection_item(file_path: str, item: dict) -> str:
    """
    Add an item to the Postman collection
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    
    if not is_a_valid_item(item):
        raise ValueError("Invalid item")
    
    if "item" not in data:
        data["item"] = []
    
    data["item"].append(item)

    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
    
    return data

async def read_postman_collection(file_path: str) -> dict:
    """
    Read the Postman collection
    """
    if not file_path.endswith(".json"):
        raise ValueError(f"{file_path} is not a JSON file")
    
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"{file_path} does not exist")
    
    with open(file_path, "r") as file:
        return json.load(file)

async def add_postman_collection_info(file_path: str, info: dict) -> dict:
    """
    Update or add the info section of a Postman collection
    
    Args:
        file_path: The path to the Postman collection file
        info: The info dictionary to update/add with keys like name, description, schema, etc.
    Returns:
        The updated Postman collection data
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    
    if "info" not in data:
        data["info"] = {}
    
    data["info"].update(info)
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
    
    return data

async def add_postman_collection_event(file_path: str, event: dict) -> dict:
    """
    Add an event to the Postman collection
    
    Args:
        file_path: The path to the Postman collection file
        event: The event dictionary with keys like listen, script, etc.
    Returns:
        The updated Postman collection data
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    
    if "event" not in data:
        data["event"] = []
    
    data["event"].append(event)
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
    
    return data

async def add_postman_collection_variable(file_path: str, variable: dict) -> dict:
    """
    Add a variable to the Postman collection
    
    Args:
        file_path: The path to the Postman collection file
        variable: The variable dictionary with keys like key, value, type, etc.
    Returns:
        The updated Postman collection data
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    
    if "variable" not in data:
        data["variable"] = []
    
    data["variable"].append(variable)
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
    
    return data

async def add_postman_collection_auth(file_path: str, auth: dict) -> dict:
    """
    Add or update authentication information for the Postman collection
    
    Args:
        file_path: The path to the Postman collection file
        auth: The auth dictionary with type and necessary auth parameters
    Returns:
        The updated Postman collection data
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    
    data["auth"] = auth
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
    
    return data

async def add_postman_collection_protocol_behavior(file_path: str, behavior: dict) -> dict:
    """
    Add or update protocol profile behavior settings for the Postman collection
    
    Args:
        file_path: The path to the Postman collection file
        behavior: The protocolProfileBehavior dictionary
    Returns:
        The updated Postman collection data
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    
    data["protocolProfileBehavior"] = behavior
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
    
    return data

async def delete_postman_collection_item(file_path: str, item_name: str) -> dict:
    """
    Delete an item from the Postman collection by name
    
    Args:
        file_path: The path to the Postman collection file
        item_name: The name of the item to delete
    Returns:
        The updated Postman collection data
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    
    if "item" not in data:
        return data
    
    data["item"] = [item for item in data["item"] if item.get("name") != item_name]
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
    
    return data

async def update_postman_collection_variable(file_path: str, key: str, new_value: str) -> dict:
    """
    Update a specific variable in the Postman collection by key
    
    Args:
        file_path: The path to the Postman collection file
        key: The key of the variable to update
        new_value: The new value for the variable
    Returns:
        The updated Postman collection data
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    
    if "variable" not in data:
        return data
    
    for var in data["variable"]:
        if var.get("key") == key:
            var["value"] = new_value
            break
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
    
    return data