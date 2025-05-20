from loguru import logger

def count_lines(file_path: str) -> int:
    """
    Count the number of lines in a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Number of lines in the file
    """
    logger.debug(f"Counting lines in file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            line_count = sum(1 for _ in f)
            logger.debug(f"Counted {line_count} lines in {file_path}")
            return line_count
    except Exception as e:
        logger.error(f"Error counting lines in {file_path}: {str(e)}")
        return 0

def is_a_valid_item(item: dict) -> bool:
    """
    Check if the item is a valid Postman collection item
    """
    logger.debug(f"Validating Postman item: {item.get('name')}")
    is_valid = "name" in item
    if not is_valid:
        logger.warning(f"Invalid Postman item: missing required fields 'name'")
    return is_valid
