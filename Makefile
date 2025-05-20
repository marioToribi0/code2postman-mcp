server:
	uv run src/code2postman_mcp/server.py

test:
	uv run pytest tests/

.PHONY: server test



