server:
	uv run src/code2postman_mcp/server.py

test:
	uv run pytest tests/

upload:
	uv run twine upload dist/*

.PHONY: server test upload



