import os
from langchain.tools import tool
from tavily import TavilyClient

@tool 
def get_places_to_visit(destination:str) ->str:
    """
    Searches the web for top tourist spots, attractions, and places to visit at a given destination.
    Use this tool to build the itinerary and recommend activities.
    """
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return "Error: Tavily API key is missing."
    
    try:
        # Initiaze the Tavily Client 
        client = TavilyClient(api_key = api_key)
        
        # Execute the search query
        query = f"Top tourist spots, attractions, and things to do in {destination}. Best time to visit each."
        response = client.search(query=query, search_depth="advanced", max_results=3)
        
        # Format the results into a single string for the AI agent
        results_text = f"Places to visit in {destination}:\n"
        for result in response.get("results", []):
            results_text += f"- {result['title']}: {result['content']}\n"
            
        return results_text
    
    except Exception as e:
        return f"Error fetching places to visit: {str(e)}"