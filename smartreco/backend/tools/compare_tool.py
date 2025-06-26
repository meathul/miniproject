# Placeholder for compare tool logic

from typing import List, Dict

def compare_products(product_a, product_b):
    # Implement comparison logic here
    pass

def select_best_product(products: List[Dict]) -> Dict:
    """
    Select the product with the lowest real_time_price (or price if not available).
    Args:
        products: List of product dicts.
    Returns:
        The best product dict.
    """
    def get_price(prod):
        return float(prod.get("real_time_price", prod.get("price", float('inf'))))
    if not products:
        return None
    return min(products, key=get_price)
