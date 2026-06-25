import os
from tavily import TavilyClient
from langchain.tools import tool
import requests

@tool
def get_currency_and_travel_tips(destination : str, currency_code: str) -> str:
    """
    Fetches the currency exchange rate from INR to the destination's currency code (e.g., USD, EUR, JPY, AED)
    along with essential visa information, local customs, and key travel tips for that country.
    Use this tool whenever you need currency exchange rates, visa guidance, or cultural tips.
    """

    exchangerate_key = os.getenv("EXCANGERATE_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")

    # --- Step 1: Fetch Live Exchange Rate
    rate_text = ""
    try:
        # we fetch the rates with INR  as the base currency
        url = f"https://v6.exchangerate-api.com/v6/{exchangerate_key}/latest/INR"
        response = requests.get(url)

        if response.status_code ==200:
            data = response.json()
            conversion_rates = data.get("conversion_rates", {})

            # Extract the conversion rate for the target currency code
            rate = conversion_rates.get(currency_code.upper())
            if rate:
                rate_text = f"💰 **Currency Exchange:** 1 INR = {rate} {currency_code.upper()}\n"
            else:
                rate_text = f"⚠️ Could not find conversion rate for currency code: {currency_code.upper()}\n"
        else:
            rate_text = "⚠️ Failed to reach the ExchangeRate API server.\n"
    except Exception as e:
        rate_text = f"⚠️ Error processing currency conversion: {str(e)}\n"

    # --- Step 2: Fetch Visa, Customs, and Local Tips via Tavily ---
    tips_text = f"### 🌍 Visa, Customs & Essential Tips for {destination}:\n"
    try:
        client = TavilyClient(api_key=tavily_key)
        query = f"Visa requirements for Indian citizens visiting {destination}, local customs, safety guidelines, and essential travel tips."
        search_response = client.search(query=query, search_depth="advanced", max_results=2)
        
        for result in search_response.get("results", []):
            tips_text += f"- {result['content']}\n"
            
    except Exception as e:
        tips_text += f"⚠️ Error fetching travel tips: {str(e)}\n"

    # Combine both datasets into one single output for the agent
    return f"{rate_text}\n{tips_text}"