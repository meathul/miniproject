# Placeholder for web scraping tool logic

import random
import os
import requests
import re
from typing import Dict
from dotenv import load_dotenv

load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_API_URL = "https://google.serper.dev/search"

def scrape_product_data(url):
    # Implement web scraping logic here
    pass

def extract_price(text: str):
    # Extracts the first price like $12.34 or ₹999 from text
    match = re.search(r"[\$₹€]\s?([0-9]+(?:\.[0-9]{1,2})?)", text)
    if match:
        return float(match.group(1))
    return None

def get_real_time_price(product: Dict) -> Dict:
    """
    Use Serper API to search for the product's real-time price using its name.
    Args:
        product: Product dict with a 'product_name' field.
    Returns:
        Product dict with an added 'real_time_price' field.
    """
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    query = product.get("product_name", "")
    data = {"q": query}
    price = None
    try:
        resp = requests.post(SERPER_API_URL, headers=headers, json=data, timeout=10)
        resp.raise_for_status()
        results = resp.json()
        # Search in organic results' titles and snippets
        for item in results.get("organic", []):
            for field in [item.get("title", ""), item.get("snippet", "")]:
                price = extract_price(field)
                if price:
                    break
            if price:
                break
    except Exception:
        price = None
    # Fallback to base price if not found
    if not price:
        price = float(product.get("price", 0))
    product_with_price = product.copy()
    product_with_price["real_time_price"] = price
    return product_with_price
