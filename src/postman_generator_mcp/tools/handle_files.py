import os
import re
from src.postman_generator_mcp.consts.excluded_files import EXCLUDED_ITEMS, Language
from src.postman_generator_mcp.utils.files import count_lines

async def get_tree_directory_from_path(path: str, language: str) -> str:
    """
    Generate a tree directory structure as a string, excluding files and directories
    based on the specified programming language using regex patterns.
    
    Args:
        path: The root path to start generating the tree from
        language: The programming language to filter files. Possible values: ["python", "javascript", "java", "go", "ruby", "rust", "csharp", "generic"]
        
    Returns:
        A formatted string representing the directory tree with line counts for each file
    """
    # Normalize language and default to generic if not in allowed languages
    language = language.lower()
    if language not in [lang.value for lang in Language]:
        raise ValueError(f"Invalid language: {language}. Possible values: {Language.values()}")
    language = Language(language)
    
    # Get exclusion lists based on the language
    exclusions = EXCLUDED_ITEMS.get(language, EXCLUDED_ITEMS[Language.GENERIC])
    excluded_dirs_patterns = exclusions.get("directories", [])
    excluded_files_patterns = exclusions.get("files", [])   
    
    # Compile regex patterns for better performance
    dir_patterns = [re.compile(pattern) for pattern in excluded_dirs_patterns]
    file_patterns = [re.compile(pattern) for pattern in excluded_files_patterns]
    
    # Create tree structure
    tree_lines = []
    base_name = os.path.basename(path)
    tree_lines.append(f"{base_name}/")
    
    # Walk the directory tree and filter as needed
    for root, dirs, files in os.walk(path):
        # Skip processing if root is the same as path
        if root == path:
            # Filter directories for top level
            dirs[:] = [d for d in dirs if not any(pattern.search(d) for pattern in dir_patterns)]
            
            # Filter and add files at root level
            for file in sorted(files):
                if not any(pattern.search(file) for pattern in file_patterns):
                    file_path = os.path.join(root, file)
                    line_count = count_lines(file_path)
                    tree_lines.append(f"    {file} ({line_count} lines)")
            continue
        
        # Get the relative path from the root
        rel_path = os.path.relpath(root, path)
        
        # Skip excluded directories
        path_parts = rel_path.split(os.sep)
        if any(any(pattern.search(part) for pattern in dir_patterns) for part in path_parts):
            # This directory or any parent is excluded, so skip it
            continue
            
        # Filter out directories that should be excluded
        dirs[:] = [d for d in dirs if not any(pattern.search(d) for pattern in dir_patterns)]
        
        # Calculate the indentation level
        level = rel_path.count(os.sep)
        indent = ' ' * 4 * (level + 1)
        
        # Add the directory to the tree
        tree_lines.append(f"{indent}{os.path.basename(root)}/")
        
        # Add files
        for file in sorted(files):
            if not any(pattern.search(file) for pattern in file_patterns):
                file_path = os.path.join(root, file)
                line_count = count_lines(file_path)
                tree_lines.append(f"{' ' * 4 * (level + 2)}{file} ({line_count} lines)")
    
    return "\n".join(tree_lines)

async def read_file(file_path: str, start_line: int = 0, end_line: int = None) -> str:
    """
    Read content from a file with line numbers, validating the file path first.
    
    Args:
        file_path: Path to the file to read
        start_line: Line number to start reading from (0-indexed, default: 0)
        end_line: Line number to end reading at (0-indexed, inclusive, default: None for all lines)
        
    Returns:
        A string with numbered lines from the file
        
    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the line parameters are invalid
    """
    # Validate file path
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist")
    
    if not os.path.isfile(file_path):
        raise ValueError(f"{file_path} is not a file")
    
    # Validate line parameters
    if start_line < 0:
        raise ValueError("start_line must be non-negative")
    
    # Read the file and add line numbers
    result = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
        # Adjust end_line if it's None or exceeds the file length
        if end_line is None or end_line >= len(lines):
            end_line = len(lines) - 1
        
        if end_line < start_line:
            raise ValueError("end_line must be greater than or equal to start_line")
        
        result = ["Total lines: " + str(len(lines)) + "\n"]
        
        # Add line numbers and extract the requested lines
        for i in range(start_line, end_line + 1):
            result.append(f"{i+1:4d} | {lines[i]}")
    
    return "".join(result)
    