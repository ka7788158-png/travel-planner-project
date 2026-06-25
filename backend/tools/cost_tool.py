from langchain.tools import tool 

@tool
def calculate_trip_cost(
    flights_cost: float,
    hotel_per_night: float,
    number_of_nights: int,
    food_per_day: float, 
    number_of_days: int,
    activities_cost: float,
    local_transport_cost: float,
    currency: str = "INR"
) -> str:
    """
    Calculates the ttal estimated trip cost and provides a detailed mathematical breakdown.
    Use this tool AFTER gathering hotel prices, flight estimates, and daily food costs.
    Pass the numerical estimates to this tool to get a formatted cost breakdown.
    """

    # Calculate the totals
    hotel_total = hotel_per_night * number_of_nights
    food_total = food_per_day * number_of_days
    total_cost = flights_cost + hotel_total + food_total + activities_cost + local_transport_cost

    # format the transparent breakdown 
    breakdown = f"""### 💰 Estimated Cost Breakdown ({currency})
- **Flights:** {flights_cost}
- **Hotels:** {hotel_per_night} x {number_of_nights} nights = {hotel_total}
- **Food:** {food_per_day} x {number_of_days} days = {food_total}
- **Activities & Entry Fees:** {activities_cost}
- **Local Transport:** {local_transport_cost}
---
**Total Estimated Cost:** {total_cost} {currency}
*(Note: These are estimated figures based on current search trends and may vary.)*
"""
    return breakdown