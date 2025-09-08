


import os

try:
	from server.weather import mcp
	# Base ASGI app from FastMCP
	base_app = mcp.app

	# Wrap with a lightweight ASGI router to serve /healthz
	async def app(scope, receive, send):
		if scope.get("type") == "http" and scope.get("path") == "/healthz":
			headers = [(b"content-type", b"application/json"), (b"cache-control", b"no-store")]
			await send({"type": "http.response.start", "status": 200, "headers": headers})
			await send({"type": "http.response.body", "body": b'{"status":"ok"}'})
			return
		# Delegate to the MCP app for all other routes
		await base_app(scope, receive, send)
except Exception as e:
	import sys
	print(f"Startup error: {e}", file=sys.stderr)
	# Fallback app that always returns 500
	async def app(scope, receive, send):
		headers = [(b"content-type", b"application/json")]
		await send({"type": "http.response.start", "status": 500, "headers": headers})
		await send({"type": "http.response.body", "body": b'{"error":"startup failure"}'})

