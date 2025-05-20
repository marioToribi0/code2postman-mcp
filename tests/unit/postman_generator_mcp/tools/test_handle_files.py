import os
import pytest
import tempfile
import re
from unittest.mock import patch, mock_open, MagicMock

from code2postman_mcp.consts.excluded_files import Language
from code2postman_mcp.tools.handle_files import get_tree_directory_from_path, read_file


class TestGetTreeDirectoryFromPath:
    @pytest.fixture
    def mock_directory_structure(self):
        """Create a mock directory structure for testing"""
        return {
            "root": {
                "dirs": ["dir1", "node_modules", "__pycache__"],
                "files": ["file1.py", "file2.py", "__init__.py"]
            },
            "root/dir1": {
                "dirs": ["subdir1"],
                "files": ["file3.py", "file4.py"]
            },
            "root/dir1/subdir1": {
                "dirs": [],
                "files": ["file5.py"]
            },
            "root/node_modules": {
                "dirs": [],
                "files": ["package.json"]
            },
            "root/__pycache__": {
                "dirs": [],
                "files": ["file1.pyc"]
            }
        }

    @pytest.mark.asyncio
    @patch("code2postman_mcp.tools.handle_files.Language")
    async def test_get_tree_directory_invalid_language(self, mock_language):
        """Test if the function raises ValueError for invalid language"""
        # Set up the mock to correctly handle the comparison and enum value listing
        mock_language.__iter__.return_value = [Language.PYTHON, Language.JAVASCRIPT]
        mock_language.side_effect = lambda x: x
        mock_language.PYTHON = Language.PYTHON
        mock_language.JAVASCRIPT = Language.JAVASCRIPT
        
        # Set up mock to raise ValueError with custom message
        valid_langs = [lang.value for lang in Language]
        error_msg = f"Invalid language: invalid_language. Possible values: {valid_langs}"
        mock_language.return_value.side_effect = ValueError(error_msg)
        
        with pytest.raises(ValueError):
            await get_tree_directory_from_path("/path/to/dir", "invalid_language")

    @pytest.mark.asyncio
    @patch("os.walk")
    @patch("code2postman_mcp.utils.files.count_lines")
    @patch("os.path.basename", return_value="root")
    async def test_get_tree_directory_python(self, mock_basename, mock_count_lines, mock_walk, mock_directory_structure):
        """Test tree directory generation for Python language"""
        # Configure count_lines to return 10 for all files
        mock_count_lines.return_value = 10
        
        # Configure os.walk to return our mock directory structure
        mock_walk.return_value = [
            ("root", ["dir1"], ["file1.py", "file2.py"]),
            ("root/dir1", [], ["file3.py"])
        ]
        
        # Call the function
        result = await get_tree_directory_from_path("root", "python")
        
        # Verify the structure of the result based on the actual output format
        expected_patterns = [
            r"root/",
            r"\s+file1\.py \(\d+ lines\)",
            r"\s+file2\.py \(\d+ lines\)",
            r"\s+root/",
            r"\s+file3\.py \(\d+ lines\)"
        ]
        for pattern in expected_patterns:
            assert re.search(pattern, result), f"Pattern '{pattern}' not found in result"
        
        # Python-specific exclusions should be applied
        assert "__pycache__" not in result
        assert "__init__.py" not in result
        assert "node_modules" not in result
        
    @pytest.mark.asyncio
    @patch("os.walk")
    @patch("code2postman_mcp.utils.files.count_lines")
    @patch("os.path.relpath")
    @patch("os.path.basename")
    async def test_get_tree_directory_with_different_languages(self, mock_basename, mock_relpath, 
                                                               mock_count_lines, mock_walk):
        """Test tree directory generation with different language filters"""
        mock_count_lines.return_value = 10
        mock_basename.side_effect = lambda x: x.split("/")[-1]
        mock_relpath.side_effect = lambda x, y: x.replace(y + "/", "")
        
        # Basic directory structure for testing
        mock_walk.return_value = [
            ("root", ["dir1", "node_modules", ".git"], ["file1.js", "package-lock.json"]),
            ("root/dir1", ["subdir1"], ["file2.py", "file3.js"]),
            ("root/node_modules", [], ["package.json"]),
            ("root/.git", [], ["config"])
        ]
        
        # Test with JavaScript
        js_result = await get_tree_directory_from_path("root", "javascript")
        
        # JavaScript should exclude node_modules and package-lock.json
        assert "node_modules" not in js_result
        assert "package-lock.json" not in js_result
        assert "file1.js" in js_result
        
        # Test with generic
        generic_result = await get_tree_directory_from_path("root", "generic")
        
        # Generic should exclude .git, node_modules
        assert ".git" not in generic_result
        assert "node_modules" not in generic_result


class TestReadFile:
    @pytest.fixture
    def sample_file_content(self):
        return "Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n"

    @pytest.mark.asyncio
    async def test_read_file_not_found(self):
        """Test if the function raises FileNotFoundError for non-existent file"""
        with pytest.raises(FileNotFoundError):
            await read_file("non_existent_file.py")

    @pytest.mark.asyncio
    @patch("os.path.exists")
    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    async def test_read_file_is_not_a_file(self, mock_file, mock_isfile, mock_exists):
        """Test if the function raises ValueError when path is not a file"""
        mock_exists.return_value = True
        mock_isfile.return_value = False
        
        with pytest.raises(ValueError):
            await read_file("directory/")

    @pytest.mark.asyncio
    @patch("os.path.exists")
    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    async def test_read_file_invalid_line_params(self, mock_file, mock_isfile, mock_exists):
        """Test if the function raises ValueError for invalid line parameters"""
        mock_exists.return_value = True
        mock_isfile.return_value = True
        
        # Test negative start_line
        with pytest.raises(ValueError):
            await read_file("file.py", start_line=-1)
        
        # Test end_line less than start_line
        mock_file.return_value.readlines.return_value = ["Line 1", "Line 2", "Line 3"]
        with pytest.raises(ValueError):
            await read_file("file.py", start_line=5, end_line=3)

    @pytest.mark.asyncio
    @patch("os.path.exists")
    @patch("os.path.isfile")
    @patch("builtins.open")
    async def test_read_file_full_content(self, mock_file, mock_isfile, mock_exists, sample_file_content):
        """Test reading the entire file"""
        mock_exists.return_value = True
        mock_isfile.return_value = True
        
        # Setup mock file
        mock_file_instance = MagicMock()
        mock_file_instance.__enter__.return_value.readlines.return_value = sample_file_content.split("\n")
        mock_file.return_value = mock_file_instance
        
        result = await read_file("file.py")
        
        # Check that the file was opened correctly
        mock_file.assert_called_once_with("file.py", "r", encoding="utf-8")
        
        # Check that the result contains line numbers and total lines
        assert "Total lines: " in result
        assert "1 | Line 1" in result
        
    @pytest.mark.asyncio
    @patch("os.path.exists")
    @patch("os.path.isfile")
    @patch("builtins.open")
    async def test_read_file_partial_content(self, mock_file, mock_isfile, mock_exists, sample_file_content):
        """Test reading a specific range of lines"""
        mock_exists.return_value = True
        mock_isfile.return_value = True
        
        # Setup mock file
        mock_file_instance = MagicMock()
        mock_file_instance.__enter__.return_value.readlines.return_value = sample_file_content.split("\n")
        mock_file.return_value = mock_file_instance
        
        result = await read_file("file.py", start_line=1, end_line=3)
        
        # Check that the file was opened correctly
        mock_file.assert_called_once_with("file.py", "r", encoding="utf-8")
        
        # Check that only the specified range was included
        assert "2 | Line 2" in result
        assert "3 | Line 3" in result
        assert "4 | Line 4" in result
        assert "1 | Line 1" not in result
        assert "5 | Line 5" not in result 