


from server.weather import mcp
import os

# The FastMCP instance has a .app attribute which is the ASGI application
app = mcp.app

# The uvicorn server will be started from the Dockerfile's CMD instruction.
# This allows Google Cloud Run to control the port.

