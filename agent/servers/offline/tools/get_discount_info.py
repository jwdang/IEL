from .utils import get_discount
import json 
def get_discount_info(data, platform:str, shop_id:str) -> str:
    """
    Used to fetch discount information.
    This function may be called when the user asks about discount policies.
    Args:
        platform: e-commerce platform information
        shop_id: shop ID
        order_id: order ID
    Returns:
        A formatted string with the discount information
    """
    discount_info = get_discount(data = data, platform = platform, shop_id = shop_id)
    if discount_info is None:
        return data, f"Not found: discount information for shop {shop_id} on {platform}"
    return data, json.dumps(discount_info, ensure_ascii=False)