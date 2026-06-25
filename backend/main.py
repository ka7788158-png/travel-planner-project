from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Import our agents
from agents.trip_planner_agent import run_trip_planner
from agents.chat_agent import run_chat_agent

# Load environment variables
load_dotenv(dotenv_path="../.env")

# Initialize FastAPI app
app = FastAPI(title="Travel Planner AI API")

# Enable CORS for the pure HTML/JS frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models for Input Validation ---

class PlanRequest(BaseModel):
    destination: str
    from_date: str
    to_date: str

class ChatRequest(BaseModel):
    message: str
    trip_context: dict 

# --- REST API Endpoints ---

@app.post("/generate-plan")
async def generate_plan(request: PlanRequest):
    """
    Takes destination and dates, triggers the trip_planner_agent, 
    and returns the complete JSON travel plan.
    """
    try:
        # Execute our v1 create_agent pipeline
        final_plan = run_trip_planner(request.destination, request.from_date, request.to_date)
        
        # If the agent returned our fallback error dictionary, raise an HTTP 500
        if "error" in final_plan:
            raise HTTPException(status_code=500, detail=final_plan["error"])
            
        return final_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cost-breakdown")
async def cost_breakdown(request: PlanRequest):
    """
    Fallback endpoint. In our architecture, the comprehensive cost breakdown 
    is already fully generated and returned inside the /generate-plan JSON payload.
    """
    return {"status": "success", "message": "Cost breakdown is integrated directly into the main plan output."}

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Handles persistent chatbot Q&A, keeping the current trip plan in context.
    """
    try:
        # Pass both the user's message and the injected JSON trip context
        reply = run_chat_agent(request.message, request.trip_context)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))