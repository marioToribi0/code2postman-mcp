server:
	uv run src/code2postman_mcp/server.py

install:
	uv pip install -e .

build:
	uv pip install build
	uv run python -m build

test:
	uv run pytest tests/

upload:
	uv run twine upload dist/*

.PHONY: server test upload install build



