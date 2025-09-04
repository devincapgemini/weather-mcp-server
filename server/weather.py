

from typing import Any
from mcp.server.fastmcp import FastMCP
import httpx


# Initialize the MCP server

mcp = FastMCP("weather")

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "mcp-weather/1.0"


async def make_news_request(url: str) -> dict[str, Any] | None:

    headers ={
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return None
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

def format_alert(feature:dict)->str:
    """Format a weather alert as a string"""
    event = feature.get("properties", {}).get("event", "")
    severity = feature.get("properties", {}).get("severity", "")
    headline = feature.get("properties", {}).get("headline", "")
    description = feature.get("properties", {}).get("description", "")
    instruction = feature.get("properties", {}).get("instruction", "")

    return f"""
    Event: {event}
    Severity: {severity}
    Headline: {headline}
    Description: {description}
    Instruction: {instruction}      
    """

            

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_news_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.resource("echo://{message}")
def get_config(message:str)->str:

    # return "App Configuration here"
    return f"Resource Echo : {message}"
    
    


