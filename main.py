


from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
import httpx

app = FastAPI()

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-mcp-server/1.0"

class WeatherRequest(BaseModel):
	states: List[str]  # List of US state codes, e.g. ["CA", "NY"]

def format_alert(feature: dict) -> str:
	event = feature.get("properties", {}).get("event", "")
	severity = feature.get("properties", {}).get("severity", "")
	headline = feature.get("properties", {}).get("headline", "")
	description = feature.get("properties", {}).get("description", "")
	instruction = feature.get("properties", {}).get("instruction", "")
	return f"Event: {event}\nSeverity: {severity}\nHeadline: {headline}\nDescription: {description}\nInstruction: {instruction}"

@app.get("/healthz")
async def healthz():
	return {"status": "ok"}

@app.post("/weather")
async def get_weather(req: WeatherRequest):
	results = {}
	headers = {
		"User-Agent": USER_AGENT,
		"Accept": "application/geo+json",
	}
	async with httpx.AsyncClient() as client:
		for state in req.states:
			url = f"{NWS_API_BASE}/alerts/active/area/{state}"
			try:
				resp = await client.get(url, headers=headers)
				if resp.status_code == 200:
					data = resp.json()
					if not data.get("features"):
						results[state] = "No active alerts for this state."
					else:
						alerts = [format_alert(f) for f in data["features"]]
						results[state] = alerts
				else:
					results[state] = f"API error ({resp.status_code})"
			except Exception as e:
				results[state] = f"Error: {e}"
	return results

