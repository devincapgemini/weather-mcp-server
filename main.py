


from server.weather import mcp
import uvicorn
import os

def main():
    """Starts the MCP server using uvicorn."""
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(mcp.app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()

