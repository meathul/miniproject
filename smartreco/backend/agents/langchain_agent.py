# Placeholder for SmartReco LangChain Agent logic

# Example:
# from langchain.agents import initialize_agent
# ...
import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

from llm.groq_wrapper import GroqLLM
from tools.semantic_search import search_products
from tools.scrape_tool import scrape_price
from tools.compare_tool import compare_products
from tools.filter_tool import filter_results
from database.mongo import save_product, get_user_profile

load_dotenv()

llm = GroqLLM(api_key=os.getenv("GROQ_API_KEY"))

search_tool = Tool(
    name="ProductSearch",
    func=lambda q: search_products(q, get_user_profile("athul_001")),
    description="Searches for skin care products based on user profile"
)

scrape_tool = Tool(
    name="ScrapePrices",
    func=lambda p: scrape_price(p["product_name"]),
    description="Gets current price and source of a product"
)

compare_tool = Tool(
    name="CompareProducts",
    func=compare_products,
    description="Compares multiple products and selects the best one"
)

filter_tool = Tool(
    name="FilterByPreferences",
    func=filter_results,
    description="Filters product list based on price, brand, or skin type preferences"
)

def build_agent():
    return initialize_agent(
        tools=[search_tool, scrape_tool, filter_tool, compare_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )