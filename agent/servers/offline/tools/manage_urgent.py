from .utils import get_order

def manage_urgent(data, platform, shop_id, order_id, user_id):
    order = get_order(data, platform, shop_id, user_id, order_id)
    if not order:
        return data, f"Not found: order {order_id} of user {user_id} in shop {shop_id} on {platform}"
    data["orders"][platform][shop_id][user_id][order_id]['is_urgent'] = True
    return data, f"Order {order_id} of user {user_id} in shop {shop_id} on {platform} has been set to expedited"
        