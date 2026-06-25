import streamlit as st
import requests
from datetime import date, timedelta

# FastAPI Backend URL
API_BASE_URL = "http://127.0.0.1:8000"

# --- Page Configuration ---
st.set_page_config(page_title="AI Travel Planner", page_icon="🌍", layout="wide")

# --- Session State Initialization ---
# We use session_state to remember the plan and chat history across reruns
if "trip_context" not in st.session_state:
    st.session_state.trip_context = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Header ---
st.title("🌍 AI-Powered Travel Planner")
st.markdown("Enter your destination and dates to generate a complete, data-driven itinerary.")

# --- Input Section ---
with st.form("travel_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        destination = st.text_input("Destination (e.g., Tokyo, Japan)", placeholder="City, Country")
    with col2:
        from_date = st.date_input("From Date", min_value=date.today())
    with col3:
        to_date = st.date_input("To Date", min_value=from_date + timedelta(days=1))
        
    submit_button = st.form_submit_button("Generate Trip Plan 🚀", type="primary")

# --- Logic: Generate Plan ---
if submit_button:
    if not destination:
        st.warning("Please enter a destination first!")
    else:
        # Clear previous plan/chat when generating a new one
        st.session_state.trip_context = None
        st.session_state.chat_history = []
        
        with st.spinner("🤖 AI is researching your trip... This usually takes 30-60 seconds..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/generate-plan",
                    json={
                        "destination": destination,
                        "from_date": str(from_date),
                        "to_date": str(to_date)
                    },
                    timeout=150 # Make sure Streamlit waits long enough for the AI
                )
                
                if response.status_code == 200:
                    st.session_state.trip_context = response.json()
                    st.success("Trip plan generated successfully!")
                    # Add initial greeting to chat
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": f"Hello! I generated your plan for {destination}. What would you like to know about it?"
                    })
                else:
                    # This will actually show us WHAT broke in the backend!
                    st.error(f"Backend Error [{response.status_code}]: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")

# --- UI: Display the Plan ---
if st.session_state.trip_context:
    st.divider()
    st.header(f"📋 Your Itinerary for {st.session_state.trip_context.get('destination', 'your trip')}")
    
    plan = st.session_state.trip_context
    
    # We use Streamlit Tabs to make the massive amount of data look clean
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "💰 Costs", "✈️ Transit", "🏨 Hotels", "🍽️ Food", 
        "🏛️ Places", "🌤️ Weather", "🎒 Packing", "💡 Tips"
    ])
    
    with tab1: st.markdown(plan.get("cost_breakdown", "No cost data available."))
    with tab2: st.markdown(plan.get("transit_options", "No transit data available."))
    with tab3: st.markdown(plan.get("hotels", "No hotel data available."))
    with tab4: st.markdown(plan.get("food", "No food data available."))
    with tab5: st.markdown(plan.get("places_to_visit", "No places data available."))
    with tab6: st.markdown(plan.get("weather_info", "No weather data available."))
    with tab7: st.markdown(plan.get("packing_list", "No packing data available."))
    with tab8: st.markdown(plan.get("currency_and_tips", "No tips available."))

    st.divider()
    
    # --- UI: Persistent Chatbot ---
    st.header("💬 Travel Assistant")
    
    # Display previous chat messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Chat Input
    if user_message := st.chat_input("Ask a question about your trip..."):
        # Display user message instantly
        with st.chat_message("user"):
            st.markdown(user_message)
        st.session_state.chat_history.append({"role": "user", "content": user_message})
        
        # Hit the backend chat endpoint
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    chat_res = requests.post(
                        f"{API_BASE_URL}/chat",
                        json={
                            "message": user_message,
                            "trip_context": st.session_state.trip_context
                        }
                    )
                    if chat_res.status_code == 200:
                        reply = chat_res.json().get("reply", "No reply received.")
                        st.markdown(reply)
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    else:
                        st.error(f"Chat Error: {chat_res.text}")
                except Exception as e:
                    st.error(f"Chat Connection Error: {e}")