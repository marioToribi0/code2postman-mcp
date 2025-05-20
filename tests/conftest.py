import os
import sys
import pytest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure pytest markers
def pytest_configure(config):
    config.addinivalue_line("markers", "asyncio: mark test as an asyncio coroutine") 