import requests 
from langchain.tools import tool

@tool
def get_user_location() -> str:
    """
    Detects the current location (city, region, country) of the user automatically.
    Use this tool when you need to know where the user is traveling FROM to estimate
    flights costs, travel times, or origin-based logistics.
    """

    try:
        # We use ip-api.com which is free and doesn't require an API key
        response = requests.get("http://ip-api.com/json/")

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                city = data.get("city")
                region = data.get("regionName")
                country = data.get("country")

                return f"The user is currently located in {city}, {region}, {country}."
            else:
                return "Could not determine the exact location."
            
        else:
            return "Failed to reach the geolocation service."
        
    except Exception as e:
        return f"Error fetching location: {str(e)}"
    