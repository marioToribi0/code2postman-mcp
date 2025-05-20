import os
import json
import pytest
from unittest.mock import patch, mock_open, MagicMock
import tempfile

from code2postman_mcp.tools.handle_postman import (
    validate_string,
    validate_dict,
    create_postman_collection,
    add_postman_collection_item,
    read_postman_collection,
    add_postman_collection_info,
    add_postman_collection_event,
    add_postman_collection_variable,
    add_postman_collection_auth,
    add_postman_collection_protocol_behavior,
    delete_postman_collection_item,
    update_postman_collection_variable,
    add_postman_collection_folder,
    add_item_to_folder
)


class TestValidationFunctions:
    def test_validate_string_valid(self):
        """Test validate_string with a valid string"""
        result = validate_string("test", "param_name")
        assert result == "test"

    def test_validate_string_invalid(self):
        """Test validate_string with invalid types raises TypeError"""
        invalid_values = [123, {"key": "value"}, [1, 2, 3], None]
        for value in invalid_values:
            with pytest.raises(TypeError):
                validate_string(value, "param_name")

    def test_validate_dict_valid(self):
        """Test validate_dict with a valid dictionary"""
        test_dict = {"key": "value"}
        result = validate_dict(test_dict, "param_name")
        assert result == test_dict

    def test_validate_dict_invalid(self):
        """Test validate_dict with invalid types raises TypeError"""
        invalid_values = ["string", 123, [1, 2, 3], None]
        for value in invalid_values:
            with pytest.raises(TypeError):
                validate_dict(value, "param_name")


class TestCreatePostmanCollection:
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    async def test_create_postman_collection_success(self, mock_file):
        """Test successful creation of a Postman collection"""
        file_path = "test_collection.json"
        name = "Test API"
        description = "Test API Description"
        
        result = await create_postman_collection(file_path, name, description)
        
        # Check file was created with correct data
        mock_file.assert_called_once_with(file_path, "w")
        
        # Verify template was formatted correctly
        assert name in result
        assert description in result
        assert "schema" in result
        
    @pytest.mark.asyncio
    async def test_create_postman_collection_invalid_extension(self):
        """Test creating a collection with invalid file extension"""
        file_path = "test_collection.txt"
        name = "Test API"
        description = "Test API Description"
        
        with pytest.raises(ValueError):
            await create_postman_collection(file_path, name, description)
    
    @pytest.mark.asyncio
    async def test_create_postman_collection_invalid_params(self):
        """Test creating a collection with invalid parameters"""
        # Test invalid file_path
        with pytest.raises(TypeError):
            await create_postman_collection(123, "Test API", "Description")
        
        # Test invalid name
        with pytest.raises(TypeError):
            await create_postman_collection("test.json", 123, "Description")
        
        # Test invalid description
        with pytest.raises(TypeError):
            await create_postman_collection("test.json", "Test API", 123)


class TestAddPostmanCollectionItem:
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    @patch("code2postman_mcp.utils.files.is_a_valid_item", return_value=True)
    async def test_add_item_success(self, mock_valid_item, mock_json_dump, mock_json_load, mock_file):
        """Test adding an item to a collection successfully"""
        file_path = "test_collection.json"
        item = {
            "name": "Get User",
            "request": {
                "method": "GET",
                "url": "https://api.example.com/users/1"
            }
        }
        
        # Mock the collection data with existing items
        mock_json_load.return_value = {
            "item": []
        }
        
        result = await add_postman_collection_item(file_path, item)
        
        # Check that json.load was called
        mock_json_load.assert_called_once()
        
        # Check that item was added to the collection
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        assert "item" in args[0]
        assert item in args[0]["item"]
        
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    @patch("code2postman_mcp.utils.files.is_a_valid_item", return_value=True)
    async def test_add_item_no_items_array(self, mock_valid_item, mock_json_dump, mock_json_load, mock_file):
        """Test adding an item to a collection with no items array"""
        file_path = "test_collection.json"
        item = {
            "name": "Get User",
            "request": {
                "method": "GET",
                "url": "https://api.example.com/users/1"
            }
        }
        
        # Mock the collection data without items array
        mock_json_load.return_value = {}
        
        result = await add_postman_collection_item(file_path, item)
        
        # Check that item array was created and item was added
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        assert "item" in args[0]
        assert item in args[0]["item"]
    
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("code2postman_mcp.utils.files.is_a_valid_item", return_value=False)
    async def test_add_invalid_item(self, mock_valid_item, mock_json_load, mock_file):
        """Test adding an invalid item to a collection"""
        file_path = "test_collection.json"
        item = {
            "invalid_key": "value"
        }
        
        # Mock the collection data
        mock_json_load.return_value = {
            "item": []
        }
        
        with pytest.raises(ValueError):
            await add_postman_collection_item(file_path, item)


class TestReadPostmanCollection:
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("os.path.isfile", return_value=True)
    @patch("os.path.exists", return_value=True)
    async def test_read_collection_success(self, mock_exists, mock_isfile, mock_json_load, mock_file):
        """Test reading a Postman collection successfully"""
        file_path = "test_collection.json"
        test_data = {
            "info": {"name": "Test Collection"},
            "item": [{"name": "Item 1"}, {"name": "Item 2"}]
        }
        mock_json_load.return_value = test_data
        
        result = await read_postman_collection(file_path)
        
        # Check that json.load was called
        mock_json_load.assert_called_once()
        
        # Check that the correct data was returned
        assert result == test_data
    
    @pytest.mark.asyncio
    async def test_read_collection_invalid_extension(self):
        """Test reading a collection with invalid file extension"""
        file_path = "test_collection.txt"
        
        with pytest.raises(ValueError):
            await read_postman_collection(file_path)
    
    @pytest.mark.asyncio
    @patch("os.path.exists", return_value=False)
    async def test_read_collection_file_not_found(self, mock_exists):
        """Test reading a non-existent collection file"""
        file_path = "non_existent.json"
        
        with pytest.raises(FileNotFoundError):
            await read_postman_collection(file_path)
    
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("os.path.isfile", return_value=True)
    @patch("os.path.exists", return_value=True)
    async def test_read_collection_json_error(self, mock_exists, mock_isfile, mock_json_load, mock_file):
        """Test reading a collection with invalid JSON"""
        file_path = "test_collection.json"
        mock_json_load.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        
        with pytest.raises(json.JSONDecodeError):
            await read_postman_collection(file_path)


class TestAddPostmanCollectionInfo:
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    async def test_add_info_success(self, mock_json_dump, mock_json_load, mock_file):
        """Test adding info to a collection successfully"""
        file_path = "test_collection.json"
        info = {
            "name": "Updated Collection",
            "description": "Updated description"
        }
        
        # Mock the collection data
        mock_json_load.return_value = {
            "info": {"name": "Original Collection"}
        }
        
        result = await add_postman_collection_info(file_path, info)
        
        # Check that info was updated
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        assert args[0]["info"]["name"] == "Updated Collection"
        assert args[0]["info"]["description"] == "Updated description"
    
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    async def test_add_info_no_info_object(self, mock_json_dump, mock_json_load, mock_file):
        """Test adding info to a collection without an info object"""
        file_path = "test_collection.json"
        info = {
            "name": "New Collection",
            "description": "New description"
        }
        
        # Mock the collection data without info object
        mock_json_load.return_value = {}
        
        result = await add_postman_collection_info(file_path, info)
        
        # Check that info object was created
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        assert "info" in args[0]
        assert args[0]["info"]["name"] == "New Collection"
        assert args[0]["info"]["description"] == "New description"


class TestAddPostmanCollectionEvent:
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    async def test_add_event_success(self, mock_json_dump, mock_json_load, mock_file):
        """Test adding an event to a collection successfully"""
        file_path = "test_collection.json"
        event = {
            "listen": "prerequest",
            "script": {
                "type": "text/javascript",
                "exec": ["console.log('This runs before each request');"]
            }
        }
        
        # Mock the collection data
        mock_json_load.return_value = {
            "event": []
        }
        
        result = await add_postman_collection_event(file_path, event)
        
        # Check that event was added
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        assert event in args[0]["event"]
    
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    async def test_add_event_no_events_array(self, mock_json_dump, mock_json_load, mock_file):
        """Test adding an event to a collection without an events array"""
        file_path = "test_collection.json"
        event = {
            "listen": "prerequest",
            "script": {
                "type": "text/javascript",
                "exec": ["console.log('This runs before each request');"]
            }
        }
        
        # Mock the collection data without events array
        mock_json_load.return_value = {}
        
        result = await add_postman_collection_event(file_path, event)
        
        # Check that events array was created
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        assert "event" in args[0]
        assert event in args[0]["event"]


class TestAddPostmanCollectionVariable:
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    async def test_add_variable_success(self, mock_json_dump, mock_json_load, mock_file):
        """Test adding a variable to a collection successfully"""
        file_path = "test_collection.json"
        variable = {
            "key": "base_url",
            "value": "https://api.example.com",
            "type": "string"
        }
        
        # Mock the collection data
        mock_json_load.return_value = {
            "variable": []
        }
        
        result = await add_postman_collection_variable(file_path, variable)
        
        # Check that variable was added
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        assert variable in args[0]["variable"]
    
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    async def test_add_variable_no_variables_array(self, mock_json_dump, mock_json_load, mock_file):
        """Test adding a variable to a collection without a variables array"""
        file_path = "test_collection.json"
        variable = {
            "key": "base_url",
            "value": "https://api.example.com",
            "type": "string"
        }
        
        # Mock the collection data without variables array
        mock_json_load.return_value = {}
        
        result = await add_postman_collection_variable(file_path, variable)
        
        # Check that variables array was created
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        assert "variable" in args[0]
        assert variable in args[0]["variable"]


class TestAddPostmanCollectionAuth:
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    async def test_add_auth_success(self, mock_json_dump, mock_json_load, mock_file):
        """Test adding auth to a collection successfully"""
        file_path = "test_collection.json"
        auth = {
            "type": "bearer",
            "bearer": [
                {
                    "key": "token",
                    "value": "{{token_variable}}",
                    "type": "string"
                }
            ]
        }
        
        # Mock the collection data
        mock_json_load.return_value = {}
        
        result = await add_postman_collection_auth(file_path, auth)
        
        # Check that auth was added
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        assert args[0]["auth"] == auth


class TestAddPostmanCollectionProtocolBehavior:
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    async def test_add_protocol_behavior_success(self, mock_json_dump, mock_json_load, mock_file):
        """Test adding protocol behavior to a collection successfully"""
        file_path = "test_collection.json"
        behavior = {
            "disableBodyPruning": True,
            "followRedirects": False
        }
        
        # Mock the collection data
        mock_json_load.return_value = {}
        
        result = await add_postman_collection_protocol_behavior(file_path, behavior)
        
        # Check that protocol behavior was added
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        assert args[0]["protocolProfileBehavior"] == behavior


class TestDeletePostmanCollectionItem:
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    async def test_delete_item_success(self, mock_json_dump, mock_json_load, mock_file):
        """Test deleting an item from a collection successfully"""
        file_path = "test_collection.json"
        item_name = "Item to Delete"
        
        # Mock the collection data with the item to delete
        mock_json_load.return_value = {
            "item": [
                {"name": "Item 1"},
                {"name": item_name},
                {"name": "Item 3"}
            ]
        }
        
        result = await delete_postman_collection_item(file_path, item_name)
        
        # Check that item was deleted
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        assert len(args[0]["item"]) == 2
        assert all(item["name"] != item_name for item in args[0]["item"])
    
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    async def test_delete_item_not_found(self, mock_json_dump, mock_json_load, mock_file):
        """Test deleting a non-existent item from a collection"""
        file_path = "test_collection.json"
        item_name = "Non-existent Item"
        
        # Mock the collection data without the item to delete
        mock_json_load.return_value = {
            "item": [
                {"name": "Item 1"},
                {"name": "Item 2"},
                {"name": "Item 3"}
            ]
        }
        
        result = await delete_postman_collection_item(file_path, item_name)
        
        # Check that collection was unchanged
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        assert len(args[0]["item"]) == 3


class TestUpdatePostmanCollectionVariable:
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    async def test_update_variable_success(self, mock_json_dump, mock_json_load, mock_file):
        """Test updating a variable in a collection successfully"""
        file_path = "test_collection.json"
        variable_key = "base_url"
        new_value = "https://new-api.example.com"
        
        # Mock the collection data with the variable to update
        mock_json_load.return_value = {
            "variable": [
                {"key": "token", "value": "abc123"},
                {"key": variable_key, "value": "https://api.example.com"}
            ]
        }
        
        result = await update_postman_collection_variable(file_path, variable_key, new_value)
        
        # Check that variable was updated
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        updated_variable = next((v for v in args[0]["variable"] if v["key"] == variable_key), None)
        assert updated_variable is not None
        assert updated_variable["value"] == new_value
    
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    async def test_update_variable_not_found(self, mock_json_dump, mock_json_load, mock_file):
        """Test updating a non-existent variable in a collection"""
        file_path = "test_collection.json"
        variable_key = "non_existent"
        new_value = "some_value"
        
        # Mock the collection data without the variable to update
        mock_json_load.return_value = {
            "variable": [
                {"key": "token", "value": "abc123"},
                {"key": "base_url", "value": "https://api.example.com"}
            ]
        }
        
        result = await update_postman_collection_variable(file_path, variable_key, new_value)
        
        # Check that collection was unchanged
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        assert len(args[0]["variable"]) == 2
        assert all(v["key"] != variable_key for v in args[0]["variable"])


class TestAddPostmanCollectionFolder:
    @pytest.mark.asyncio
    @patch("code2postman_mcp.tools.handle_postman.add_postman_collection_item")
    async def test_add_folder_success(self, mock_add_item):
        """Test adding a folder to a collection successfully"""
        file_path = "test_collection.json"
        folder_name = "Test Folder"
        items = [{"name": "Item 1"}, {"name": "Item 2"}]
        
        # Mock the result of add_postman_collection_item
        mock_add_item.return_value = {"item": [{"name": folder_name, "item": items}]}
        
        result = await add_postman_collection_folder(file_path, folder_name, items)
        
        # Check that add_postman_collection_item was called with correct params
        mock_add_item.assert_called_once()
        args, _ = mock_add_item.call_args
        assert args[0] == file_path
        assert args[1]["name"] == folder_name
        assert args[1]["item"] == items
    
    @pytest.mark.asyncio
    @patch("code2postman_mcp.tools.handle_postman.add_postman_collection_item")
    async def test_add_folder_no_items(self, mock_add_item):
        """Test adding a folder without items to a collection"""
        file_path = "test_collection.json"
        folder_name = "Empty Folder"
        
        # Mock the result of add_postman_collection_item
        mock_add_item.return_value = {"item": [{"name": folder_name, "item": []}]}
        
        result = await add_postman_collection_folder(file_path, folder_name)
        
        # Check that add_postman_collection_item was called with correct params
        mock_add_item.assert_called_once()
        args, _ = mock_add_item.call_args
        assert args[0] == file_path
        assert args[1]["name"] == folder_name
        assert args[1]["item"] == []


class TestAddItemToFolder:
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    @patch("code2postman_mcp.utils.files.is_a_valid_item", return_value=True)
    async def test_add_item_to_folder_success(self, mock_valid_item, mock_json_dump, mock_json_load, mock_file):
        """Test adding an item to a folder successfully"""
        file_path = "test_collection.json"
        folder_name = "Test Folder"
        item = {
            "name": "Test Item",
            "request": {
                "method": "GET",
                "url": "https://api.example.com/test"
            }
        }
        
        # Mock the collection data with the folder
        mock_json_load.return_value = {
            "item": [
                {
                    "name": folder_name,
                    "item": []
                }
            ]
        }
        
        result = await add_item_to_folder(file_path, folder_name, item)
        
        # Check that item was added to the folder
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        folder = next((f for f in args[0]["item"] if f["name"] == folder_name), None)
        assert folder is not None
        assert item in folder["item"]
    
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("code2postman_mcp.utils.files.is_a_valid_item", return_value=False)
    async def test_add_invalid_item_to_folder(self, mock_valid_item, mock_json_load, mock_file):
        """Test adding an invalid item to a folder"""
        file_path = "test_collection.json"
        folder_name = "Test Folder"
        item = {"invalid_key": "value"}
        
        # Mock the collection data with the folder
        mock_json_load.return_value = {
            "item": [
                {
                    "name": folder_name,
                    "item": []
                }
            ]
        }
        
        with pytest.raises(ValueError):
            await add_item_to_folder(file_path, folder_name, item)
    
    @pytest.mark.asyncio
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("code2postman_mcp.utils.files.is_a_valid_item", return_value=True)
    async def test_add_item_to_nonexistent_folder(self, mock_valid_item, mock_json_load, mock_file):
        """Test adding an item to a non-existent folder"""
        file_path = "test_collection.json"
        folder_name = "Non-existent Folder"
        item = {
            "name": "Test Item",
            "request": {
                "method": "GET",
                "url": "https://api.example.com/test"
            }
        }
        
        # Mock the collection data without the folder
        mock_json_load.return_value = {
            "item": [
                {
                    "name": "Other Folder",
                    "item": []
                }
            ]
        }
        
        with pytest.raises(ValueError):
            await add_item_to_folder(file_path, folder_name, item)


# Integration test with a temporary file
class TestIntegrationWithTempFile:
    @pytest.mark.asyncio
    @pytest.mark.skipif(os.name == 'nt', reason="Test is unstable on Windows due to file locking issues")
    async def test_full_collection_workflow(self):
        """Test a full workflow of creating and manipulating a collection"""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as temp_file:
            file_path = temp_file.name
            
        try:
            # Create the collection
            await create_postman_collection(file_path, "Test API", "Test API Collection")
            
            # Add a variable
            await add_postman_collection_variable(file_path, {
                "key": "base_url",
                "value": "https://api.example.com",
                "type": "string"
            })
            
            # Add authentication
            await add_postman_collection_auth(file_path, {
                "type": "bearer",
                "bearer": [
                    {
                        "key": "token",
                        "value": "{{token}}",
                        "type": "string"
                    }
                ]
            })
            
            # Add a folder
            await add_postman_collection_folder(file_path, "Users")
            
            # Add an item to the folder
            await add_item_to_folder(file_path, "Users", {
                "name": "Get User",
                "request": {
                    "method": "GET",
                    "url": "{{base_url}}/users/1"
                }
            })
            
            # Read and verify the collection
            collection = await read_postman_collection(file_path)
            
            # Verify the structure
            assert collection["info"]["name"] == "Test API"
            assert "variable" in collection
            assert collection["variable"][0]["key"] == "base_url"
            assert collection["auth"]["type"] == "bearer"
            
            # Find the Users folder
            users_folder = next((f for f in collection["item"] if f["name"] == "Users"), None)
            assert users_folder is not None
            assert len(users_folder["item"]) == 1
            assert users_folder["item"][0]["name"] == "Get User"
            
        finally:
            # Ensure all file handles are closed before attempting to delete
            import gc
            gc.collect()
            
            # Clean up - with error handling for Windows
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except PermissionError:
                # On Windows, just log this rather than failing the test
                print(f"Warning: Could not delete temporary file {file_path}") 