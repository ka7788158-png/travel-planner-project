from langchain.tools import tool

@tool
def generate_packing_checklist(expected_climate: str, trip_duration_days: int) -> str:
    """
    Generates a structured packing checklist based on the EXPECTED climate for the travel dates 
    and the number of days.
    Use this tool AFTER fetching the weather/climate data to output the packing list.
    """
    climate = expected_climate.lower()
    
    # Smarter dynamic logic based on the expected climate
    if any(word in climate for word in ["rain", "shower", "storm", "monsoon", "wet"]):
        weather_gear = "- Umbrella / Sturdy Raincoat\n- Waterproof shoes or covers\n- Dry bags for electronics"
    elif any(word in climate for word in ["snow", "cold", "winter", "freezing", "ice"]):
        weather_gear = "- Thermal inner-wear\n- Heavy insulated winter jacket\n- Gloves, scarf, and beanie\n- Winter boots"
    elif any(word in climate for word in ["hot", "clear", "sun", "summer", "humid"]):
        weather_gear = "- Sunglasses & Sun hat\n- Sunscreen (SPF 50+)\n- Light breathable cotton/linen clothing\n- Swimwear (if applicable)"
    else:
        weather_gear = "- Light jacket or sweater\n- Comfortable layers (t-shirts and long sleeves)"

    checklist = f"""### 🎒 Smart Packing Checklist ({trip_duration_days} Days)

**🧥 Clothing (Adapted for Expected Climate)**
- {trip_duration_days + 2}x Undergarments & Socks
- {trip_duration_days}x Tops / Shirts
- Bottoms / Trousers (as needed)
{weather_gear}

**🪥 Essentials**
- Toothbrush & Toothpaste
- Deodorant & Toiletries
- Hand sanitizer & Wet wipes

**🛂 Documents**
- Passport & Visa / ID Card
- Travel Insurance Details
- Flight & Hotel booking printouts / offline digital copies

**🔌 Gadgets**
- Smartphone & Charger
- Universal Power Adapter
- Power Bank

**💊 Medicines**
- Personal prescriptions
- Pain relievers (e.g., Paracetamol)
- Motion sickness pills (if needed)
- Band-aids and basic first-aid
"""
    return checklist