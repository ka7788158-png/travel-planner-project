import os
from tavily import TavilyClient
from langchain.tools import tool

@tool
def compare_transit_options(origin: str, destination: str) -> str:
    """
    Compares available transport modes (Flights, trains, Buses) from the user's origin city
    to the destination. Returns estimated prices, travel durations, and recommendations 
    on the best way to travel.
    Use this tool to provide transit options to the user.
    """

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Error: Tavily API key is missing."
    
    try:
        client = TavilyClient(api_key = api_key)

        # Query to discover transport options and rough costs
        query = f"How to travel from {origin} to {destination} by flight, train or bus. Cost estimation and duration comparison."
        response = client.search(query=query, search_depth="advanced", max_results= 2)

        # Clean up the origin/destination for building quick deep-links
        clean_origin = origin.split(",")[0].strip().replace(" ", "+")
        clean_dest = destination.split(",")[0].strip().replace(" ", "+")

        # Generate handy search deep-links for the user 
        google_flights_link = f"https://www.google.com/travel/flights?q=Flights+from+{clean_origin}+to+{clean_dest}"
        makemytrip_link = "https://www.makemytrip.com/"

        comparison_text = f"### Bus, Train, & Flight Options from {origin} to {destination}: \n\n"

        for result in response.get("results", []):
            comparison_text += f"- {result['content']}\n"

        comparison_text += f"""
---
### 🔗 Quick Booking Search Links:
- 🛫 [Search Live Prices on Google Flights]({google_flights_link})
- 🚆 [Check Live Trains/Buses on MakeMyTrip]({makemytrip_link})

*Note: AI cannot book tickets directly due to dynamic pricing and security authentication. Please use the verified links above to check live schedules and lock in your seats!*
"""
        return comparison_text
        
    except Exception as e:
        return f"Error comparing transit options: {str(e)}"