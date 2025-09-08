


from server.weather import mcp
import os

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

# The uvicorn server will be started from the Dockerfile's CMD instruction.
# This allows Google Cloud Run to control the port.

