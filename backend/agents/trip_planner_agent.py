import os
import json
from langchain_mistralai.chat_models import ChatMistralAI
from langchain.agents import create_agent

# Import the raw string prompt
from prompts.system_prompts import TRIP_PLANNER_PROMPT


# Import ALL our custom tools

from tools.weather_tool import get_weather
from tools.places_tool import get_places_to_visit
from tools.community_insights_tool import get_community_insights
from tools.hotels_tool import get_hotel_recommendations
from tools.food_tool import get_food_recommendations
from tools.currency_tool import get_currency_and_travel_tips
from tools.cost_tool import calculate_trip_cost
from tools.packing_tool import generate_packing_checklist
from tools.location_tool import get_user_location
from tools.transit_comparison_tool import compare_transit_options

# Compile them into a list for the agent
tools = [
    get_user_location, compare_transit_options, get_weather, 
    get_places_to_visit, get_community_insights, get_hotel_recommendations,
    get_food_recommendations, get_currency_and_travel_tips, 
    calculate_trip_cost, generate_packing_checklist
]

def run_trip_planner(destination: str, from_date: str, to_date: str) -> dict:
    """
    Initializes the agent, feeds it the user's request, and parses the final JSON output.
    """
    
    llm = ChatMistralAI(
        model="mistral-small-latest",
        api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.2,
        timeout=120,         # Tell Python to wait up to 2 minutes for Mistral's brain
        max_retries=3        # If it fails, silently retry up to 3 times
    )

    # 1. create_agent natively builds the execution graph, replacing AgentExecutor
    agent = create_agent(
        model=llm, 
        tools=tools,
        system_prompt=TRIP_PLANNER_PROMPT
    )

    # 2. Construct the user's input
    user_input = f"Plan a comprehensive trip to {destination}. Travel dates: {from_date} to {to_date}."
    
    try:
        # 3. Execute the agent using the standard LangGraph messages schema
        response = agent.invoke({"messages": [("user", user_input)]})
        
        # 4. The final response is the text inside the last message in the graph state
        output_string = response["messages"][-1].content
        
        # Strip out any potential markdown formatting around the JSON
        if output_string.startswith("```json"):
            output_string = output_string.replace("```json", "", 1).replace("```", "")
            
        final_plan_dict = json.loads(output_string.strip())
        return final_plan_dict
        
    except Exception as e:
        print(f"Error during agent execution: {str(e)}")
        # Fallback response so the frontend doesn't crash
        return {"error": f"Failed to generate plan. Details: {str(e)}"}