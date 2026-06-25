import os
from langchain.tools import tool
from tavily import TavilyClient

@tool
def get_hotel_recommendations(destination : str)-> str:
    """
    Searches the web for hotel recommendations at the destination.
    Returns categorized options for budget, mid-range, and luxury stays.
    Use this tool whenever the user need accomodation suggestions.
    """

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Error : Tavily API key is missing."
    
    try:
        client = TavilyClient(api_key=api_key)

        query = f"Best hotels to stay in {destination} categorized by budget, mid-range, and luxury with estimated price per night."
        response = client.search(query = query, search_depth ="advanced", max_results= 3)

        results_text = f"### Accomodations in {destination}:\n"
        for result in response.get("results", []):
            results_text += f"- {result['content']}\n"

        return results_text
    
    except Exception as e:
        return f"Error fetching Hotel data: {str(e)}"
    
    