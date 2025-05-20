#!/bin/bash

# Run pytest with coverage and asyncio support
uv run pytest --cov=src --cov-report=term-missing tests/ 