from typing import List, Dict, Optional

def filter_products(
    products: List[Dict],
    price: Optional[float] = None,
    skin_type: Optional[str] = None,
    brands: Optional[List[str]] = None,
    budget: Optional[float] = None
) -> List[Dict]:
    """
    Filter products by price, skin type, and brand.
    Args:
        products: List of product dicts.
        price: (Optional) Exact price to match.
        skin_type: (Optional) Skin type to match.
        brands: (Optional) List of preferred brands.
        budget: (Optional) Max price allowed.
    Returns:
        Filtered list of products. If no products match all filters, returns all products (or all under budget) as fallback.
    """
    filtered = []
    for product in products:
        if price is not None and float(product.get("price", 0)) != price:
            continue
        if budget is not None and float(product.get("price", 0)) > budget:
            continue
        if skin_type and product.get("skin_type", "").lower() != skin_type.lower():
            continue
        if brands and product.get("brand", "").lower() not in [b.lower() for b in brands]:
            continue
        filtered.append(product)
    # Fallback: if nothing matched, return all products (or all under budget)
    if not filtered:
        if budget is not None:
            return [p for p in products if float(p.get("price", 0)) <= budget]
        return products
    return filtered
