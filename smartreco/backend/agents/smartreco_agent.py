from tools.semantic_search import semantic_search
from tools.filter_tool import filter_products
from tools.scrape_tool import get_real_time_price
from tools.compare_tool import select_best_product
from llm.groq_wrapper import GroqLLM
from agents.routine_agent import run_true_langchain_routine_agent

# You may need to adjust imports if running as a module

def recommend_product(query: str, user_profile: dict) -> dict:
    """
    Full SmartReco agent pipeline.
    Args:
        query: User's product query (e.g., 'suggest a moisturizer')
        user_profile: Dict with user preferences (skin_type, age, ethnicity, budget, preferred brands)
    Returns:
        Dict with best product, explanation, and skincare routine (from true agent).
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
    # 6. Build skincare routine using true LangChain agent
    best_category = best.get('category', '').lower()
    routine = run_true_langchain_routine_agent(user_profile, best, filtered, routine_type=best_category)

    # 7. Expand and format the routine using LLM
    expand_prompt = (
        f"User profile: {user_profile}\n"
        f"Recommended product: {best['product_name']} by {best['brand']} (Price: {best.get('real_time_price', best.get('price'))})\n"
        f"Here is a skincare routine (in raw steps):\n{routine}\n"
        "Please expand on this routine, making it concise, actionable, and tailored to the user's profile. "
        "Format it under the heading '## Skincare Routine', and ensure each step is clearly explained. "
        f"Highlight where the recommended product '{best['product_name']}' is used in the routine. "
        "Do not repeat the product justification, only focus on the routine. "
        "Output the routine as a clear, short, step-by-step list."
    )
    expanded_routine = llm(expand_prompt)

    return {"product": best, "explanation": explanation, "routine": routine, "expanded_routine": expanded_routine} 