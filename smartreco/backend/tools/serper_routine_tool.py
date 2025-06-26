import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_API_URL = "https://google.serper.dev/search"

def serper_routine_search(user_profile: dict) -> list:
    """
    Use Serper to fetch a typical skincare routine for the user profile.
    Returns a list of routine steps (e.g., ['cleanser', 'serum', ...]).
    """
    skin_type = user_profile.get("skin_type", "")
    query = f"skincare routine for {skin_type} skin"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    data = {"q": query}
    try:
        resp = requests.post(SERPER_API_URL, headers=headers, json=data, timeout=10)
        resp.raise_for_status()
        results = resp.json()
        # Try to extract routine steps from snippets
        for item in results.get("organic", []):
            snippet = item.get("snippet", "").lower()
            # Look for common routine steps in the snippet
            steps = []
            for step in ["cleanser", "face wash", "serum", "moisturizer", "moisturiser", "sunscreen", "spf", "toner", "exfoliator", "eye cream"]:
                if step in snippet and step not in steps:
                    steps.append(step)
            if len(steps) >= 2:
                # Return unique steps in order found
                return steps
    except Exception as e:
        print("[SERPER ERROR]", e)
    # Fallback to a default routine
    return ["cleanser", "serum", "moisturizer", "sunscreen"] 