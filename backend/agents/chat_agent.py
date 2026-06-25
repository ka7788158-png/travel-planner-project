import os
import json
from langchain_mistralai.chat_models import ChatMistralAI
from langchain.agents import create_agent

# Import the new prompt
from prompts.system_prompts import CHAT_AGENT_PROMPT

def run_chat_agent(message: str, trip_context: dict) -> str:
    """
    Initializes a conversational agent that uses the generated trip plan as context
    to answer the user's travel questions.
    """

    # we set the temperature a bit higher (0.5) so that bot sounds more natural and conversational 
    llm = ChatMistralAI(
        model="mistral-small-latest",
        api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.5,
        timeout=120,         # Tell Python to wait up to 2 minutes for Mistral's brain
        max_retries=3        # If it fails, silently retry up to 3 times
    )

    # We use create_agent but with an empty tools list
    agent = create_agent(
        model = llm, 
        tools = [],
        system_prompt= CHAT_AGENT_PROMPT
    )

    # Convert the Python dictionary plan back into a readable string format for the AI
    context_string = json.dumps(trip_context, indent=2)

    try:
        # We pass the trip context as a background system message, followed by the user's actual question
        response = agent.invoke({
            "messages": [
                ("system", f"CURRENT TRIP PLAN CONTEXT:\n{context_string}"),
                ("user", message)
            ]
        })
        
        # Extract the final reply from the AI
        return response["messages"][-1].content
        
    except Exception as e:
        print(f"Error during chat agent execution: {str(e)}")
        return "Sorry, I am having trouble accessing your trip details right now. Please try asking again."