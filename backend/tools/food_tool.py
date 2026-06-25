import os
from langchain.tools import tool
from tavily import TavilyClient

@tool
def get_food_recommendations(destination: str) -> str:
    """
    Searches the web for must-try local cuisine, traditional dishes, 
    and top-rated resturants or food spots at the destination. 
    Use this tool whenever food or dinning recommendations are needed.
    """

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Error: Tavily API key is missing."
    
    try:
        client = TavilyClient(api_key = api_key)

        # Gathering both traditional dishes and top food joints
        query = f"Must-try local dishes and top rated resturants to eat at in {destination}."
        response = client.serach(query = query, search_depth = "advanced", max_results =3)

        results_text = f"### Food & Dinning in {destination}: \n"
        for result in response.get("results", []):
            results_text += f"- {result['content']}\n"

        return results_text
    
    except Exception as e:
        return f"Error fetching food recommendations: {str(e)}"
    
