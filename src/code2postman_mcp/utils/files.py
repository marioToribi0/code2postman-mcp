def count_lines(file_path: str) -> int:
    """
    Count the number of lines in a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Number of lines in the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return 0

def is_a_valid_item(item: dict) -> bool:
    """
    Check if the item is a valid Postman collection item
    """
    return "name" in item and "request" in item
