from langchain.agents import initialize_agent, Tool
from langchain.prompts import PromptTemplate
from llm.groq_wrapper import GroqLLM
from tools.serper_routine_tool import serper_routine_search
from tools.filter_tool import filter_products
from typing import List, Dict

CATEGORY_MAP = {
    "cleanser": ["cleanser", "face wash", "facewash"],
    "serum": ["serum"],
    "moisturizer": ["moisturizer", "moisturiser"],
    "sunscreen": ["sunscreen", "sun screen", "spf"]
}

# Tool: Search for routine steps using Serper
serper_tool = Tool(
    name="SerperRoutineSearch",
    func=lambda user_profile: serper_routine_search(user_profile),
    description="Search the web for typical skincare routine steps for a user profile."
)

# Tool: Filter products by category
filter_tool = Tool(
    name="FilterByCategory",
    func=lambda products_and_category: [p for p in products_and_category[0] if products_and_category[1].lower() in p.get("category", "").lower()],
    description="Filter a list of products by category. Input is a tuple: (products, category)."
)

# Tool: Explain choice using LLM
llm = GroqLLM()
def explain_choice(args):
    product, step, user_profile = args
    prompt = (
        f"User profile: {user_profile}\n"
        f"Step: {step}\n"
        f"Product: {product['product_name']} by {product['brand']}\n"
        f"Product details: {product}\n"
        f"Explain why this is a good {step.lower()} for the user."
    )
    return llm(prompt)

explain_tool = Tool(
    name="ExplainChoice",
    func=explain_choice,
    description="Explain why a product is a good choice for a step and user profile. Input is a tuple: (product, step, user_profile)."
)

def run_true_langchain_routine_agent(user_profile: dict, best_product: Dict, filtered_products: List[Dict]):
    """
    True LangChain agent: receives tools and a prompt, and builds a skincare routine for the given product.
    """
    tools = [serper_tool, filter_tool, explain_tool]
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True,
        handle_parsing_errors=True,
    )
    prompt = (
        "You are an expert skincare routine builder. "
        "You must use ONLY the provided tools to answer. "
        "Always follow this format exactly:\n"
        "Thought: <your reasoning>\n"
        "Action: <tool name>\n"
        "Action Input: <input to the tool>\n"
        "Observation: <result of the tool>\n"
        "Repeat Thought/Action/Action Input/Observation as needed.\n"
        "When you are done, output:\n"
        "Final Answer: <your final answer>\n"
        f"Suggest a skincare routine for this product: {best_product}. Use only the provided tools."
    )
    result = agent.run(prompt)
    return result

def build_skincare_routine(user_profile: dict, products: List[Dict]) -> List[Dict]:
    """
    Build a skincare routine using only the given products and user profile.
    For each step, pick the best product (by rating) and explain the choice.
    """
    steps = [
        ("Cleanser", "cleanser"),
        ("Serum", "serum"),
        ("Moisturizer", "moisturizer"),
        ("Sunscreen", "sunscreen"),
    ]
    routine = []
    for step_name, category in steps:
        valid_categories = CATEGORY_MAP.get(category, [category])
        # Filter products by category (flexible mapping)
        candidates = filter_products(products, skin_type=user_profile.get("skin_type"))
        candidates = [
            p for p in candidates
            if p.get("category", "").lower().strip() in valid_categories
        ]
        if not candidates:
            continue
        # Pick the best product by rating
        best = max(candidates, key=lambda p: float(p.get("rating", 0)))
        # Use LLM to explain the choice
        prompt = (
            f"User profile: {user_profile}\n"
            f"Step: {step_name}\n"
            f"Product: {best['product_name']} by {best['brand']}\n"
            f"Product details: {best}\n"
            f"Explain why this is a good {step_name.lower()} for the user."
        )
        explanation = llm(prompt)
        routine.append({
            "step": step_name,
            "product": best,
            "explanation": explanation
        })
    return routine

def run_routine_react_agent(user_profile: dict, best_product: Dict, filtered_products: List[Dict]):
    """
    React-style agent: builds a skincare routine anchored on the best product, using serper for steps and thinking out loud.
    Returns (routine, thoughts)
    """
    routine_steps = serper_routine_search(user_profile)
    thoughts = []
    routine = []
    used_ids = set()
    for step in routine_steps:
        canonical = None
        for k, v in CATEGORY_MAP.items():
            if step in v:
                canonical = k
                break
        if not canonical:
            canonical = step
        if best_product.get("category", "").lower().strip() in CATEGORY_MAP.get(canonical, [canonical]) and best_product.get("product_name") not in used_ids:
            product = best_product
            used_ids.add(product.get("product_name"))
            reasoning = f"For step '{step}', using the anchor product: {product['product_name']} by {product['brand']} (category: {product['category']})."
        else:
            candidates = filter_products(filtered_products, skin_type=user_profile.get("skin_type"))
            candidates = [p for p in candidates if p.get("category", "").lower().strip() in CATEGORY_MAP.get(canonical, [canonical]) and p.get("product_name") not in used_ids]
            if not candidates:
                reasoning = f"No suitable product found for step '{step}'. Skipping."
                thoughts.append(reasoning)
                continue
            product = max(candidates, key=lambda p: float(p.get("rating", 0)))
            used_ids.add(product.get("product_name"))
            reasoning = f"For step '{step}', selected {product['product_name']} by {product['brand']} (category: {product['category']}) as the best available product."
        thoughts.append(reasoning)
        routine.append({
            "step": step,
            "product": product,
            "explanation": reasoning,
            "reasoning": reasoning
        })
    return routine, thoughts 