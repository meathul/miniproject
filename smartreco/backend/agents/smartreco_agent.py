from tools.semantic_search import semantic_search
from tools.filter_tool import filter_products
from tools.scrape_tool import get_real_time_price
from tools.compare_tool import select_best_product
from llm.groq_wrapper import GroqLLM

# You may need to adjust imports if running as a module

def recommend_product(query: str, user_profile: dict) -> dict:
    """
    Full SmartReco agent pipeline.
    Args:
        query: User's product query (e.g., 'suggest a moisturizer')
        user_profile: Dict with user preferences (skin_type, age, ethnicity, budget, preferred brands)
    Returns:
        Dict with best product and explanation.
    """
    # 1. Retrieve relevant products
    products = semantic_search(query)
    print("[DEBUG] Semantic search results:", products)
    # 2. Filter by user profile
    filtered = filter_products(
        products,
        skin_type=user_profile.get("skin_type"),
        brands=user_profile.get("preferred_brands"),
        budget=user_profile.get("budget")
    )
    print("[DEBUG] After filtering:", filtered)
    # 3. Get real-time prices
    with_prices = [get_real_time_price(p) for p in filtered]
    print("[DEBUG] After real-time pricing:", with_prices)
    # 4. Select best product
    best = select_best_product(with_prices)
    print("[DEBUG] Best product selected:", best)
    if not best:
        return {"error": "No suitable product found."}
    # 5. Generate explanation
    llm = GroqLLM()
    prompt = (
        f"User profile: {user_profile}\n"
        f"Query: {query}\n"
        f"Recommended product: {best['product_name']} by {best['brand']} (Price: {best.get('real_time_price', best.get('price'))})\n"
        f"Product details: {best.get('description', '')}\n"
        "Explain in detail why this product is the best match for the user, considering their profile and preferences."
    )
    explanation = llm(prompt)
    return {"product": best, "explanation": explanation} 