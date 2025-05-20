import os
import pytest
from unittest.mock import patch, mock_open, MagicMock

from src.code2postman_mcp.utils.files import count_lines


class TestCountLines:
    def test_count_lines_success(self):
        """Test counting lines of a file successfully"""
        mock_content = "Line 1\nLine 2\nLine 3\n"
        
        with patch("builtins.open", mock_open(read_data=mock_content)) as mock_file:
            result = count_lines("test_file.txt")
            
            # Check file was opened correctly
            mock_file.assert_called_once_with("test_file.txt", 'r', encoding='utf-8', errors='ignore')
            
            # Check the correct line count is returned
            assert result == 3
    
    def test_count_lines_exception(self):
        """Test count_lines handles exceptions properly"""
        with patch("builtins.open", side_effect=Exception("File error")) as mock_file:
            result = count_lines("non_existent_file.txt")
            
            # Check function returns 0 on exception
            assert result == 0 