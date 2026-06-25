import os
import requests
from langchain.tools import tool
from tavily import TavilyClient

@tool
def get_weather(destination: str, travel_dates: str) -> str:
    """
    Fetches the current live weather (via OpenWeatherMap) AND the expected typical climate 
    for the specific travel dates (via Tavily).
    Use this tool to determine what the weather WILL be like when the user actually travels.
    """
    openweather_key = os.getenv("OPENWEATHER_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    
    if not openweather_key or not tavily_key:
        return "Error: Missing API keys for weather or web search tools."

    # --- Step 1: Fetch Current Live Weather (OpenWeatherMap) ---
    current_weather_text = ""
    try:
        geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={destination}&limit=1&appid={openweather_key}"
        geo_response = requests.get(geocode_url).json()
        
        if geo_response:
            lat, lon = geo_response[0]["lat"], geo_response[0]["lon"]
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={openweather_key}&units=metric"
            weather_data = requests.get(weather_url).json()
            
            temp = weather_data["main"]["temp"]
            desc = weather_data["weather"][0]["description"]
            current_weather_text = f"**Current Live Weather:** {temp}°C, {desc}.\n"
    except Exception as e:
        current_weather_text = "Could not fetch live weather.\n"

    # --- Step 2: Fetch Expected Climate for Travel Dates (Tavily) ---
    climate_text = ""
    try:
        client = TavilyClient(api_key=tavily_key)
        query = f"Typical weather, average temperature, and climate in {destination} during {travel_dates}. Does it rain or snow?"
        search_response = client.search(query=query, search_depth="basic", max_results=2)
        
        climate_text = f"**Expected Climate for {travel_dates}:**\n"
        for result in search_response.get("results", []):
            climate_text += f"- {result['content']}\n"
    except Exception as e:
        climate_text = "Could not fetch climate data for those dates.\n"

    # Combine both so the agent has total context
    return f"{current_weather_text}\n{climate_text}"