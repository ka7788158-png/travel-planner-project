import os
from langchain.tools import tool
from tavily import TavilyClient

@tool
def get_community_insights(destination: str) -> str:
    """
    Fetches real human perspectives, hidden gems, tourist traps to avoid, 
    local tips, hotel warnings, and restaurant recommendations for a destination 
    from forums like Reddit and Quora.
    Use this tool to add authentic, non-commercial advice regarding places, food, and stays.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Error: Tavily API key is missing."

    try:
        client = TavilyClient(api_key=api_key)
        
        # Supercharged query targeting hidden gems, hotel red flags, and raw restaurant advice on Reddit/Quora
        query = (
            f"{destination} travel advice hidden gems tourist traps "
            f"hotel recommendations restaurant reviews site:reddit.com OR site:quora.com"
        )
        
        response = client.search(query=query, search_depth="advanced", max_results=4)
        
        results_text = f"### 👥 Community Perspectives & Real Human Advice for {destination}:\n"
        for result in response.get("results", []):
            results_text += f"- **From Forums:** {result['content']}\n"
            
        return results_text
        
    except Exception as e:
        return f"Error fetching comprehensive community insights: {str(e)}"