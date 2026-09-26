from .utils import get_logistics
import json

def get_logistics_info(data, platform: str, shop_id: str, order_id: str, user_id: str) -> str:
    """
    Used to fetch logistics policy information.
    This function may be called when the user asks about logistics policies.
    Args:
        platform: e-commerce platform information
        shop_id: shop ID
        order_id: order ID
        user_id: user ID
    Returns:
        A formatted string with the logistics information
    """
    logistics_info = get_logistics(data = data, platform = platform, shop_id = shop_id, order_id = order_id, user_id = user_id)
    if logistics_info is None:
        return data, f"Not found: shipping information for order {order_id} of user {user_id} in shop {shop_id} on {platform}"
    return data, json.dumps(logistics_info, ensure_ascii=False)
    