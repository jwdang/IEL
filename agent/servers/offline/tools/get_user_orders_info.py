from .utils import get_order
import json

def get_user_orders_info(data, platform, shop_id, user_id):
    orders = data.get("orders", {})
    order = orders.get(platform, {}).get(shop_id, {}).get(user_id, {})
    if not order:
        return data, f"Not found: orders for user {user_id}"
    result = {
        'order_id': list(order.keys())
    }
    return data, json.dumps(result, ensure_ascii=False)
