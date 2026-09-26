from .utils import get_order
import json
# Status enum for return/refund: received (delivered)
def manage_return(data, platform: str, shop_id: str, order_id: str, user_id: str) -> str:
    """
    Process a return request
    """
    order = get_order(data, platform, shop_id, user_id, order_id)
    if not order:
        return data, f"Not found: order {order_id}"
    data["orders"][platform][shop_id][user_id][order_id]['order_status'] = 'returned'
    return data, f"The return request has been processed. The order being returned is {json.dumps(order, ensure_ascii=False)}"