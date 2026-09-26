from .utils import get_order, get_product_detail
import json

# Products that may be modified for exchange: 1. the product status is "listed" 2. the
# product ID is in the exchangeable-product list 3. by default only attributes such as
# colour may change for an exchange -- price and quantity may not, i.e. it must be a
# like-for-like substitute
# Exchangeable status enum: pending payment, paid, processing
def manage_exchange(data, platform, shop_id, order_id, user_id, original_product_id, exchange_product_id, action):
    order = get_order(data, platform, shop_id, user_id, order_id)
    original_product = get_product_detail(data, platform, shop_id, original_product_id)
    if not original_product:
        return data, f"Not found: product {original_product_id}"
    if not order:
        return data, f"Not found: order {order_id} of user {user_id} in shop {shop_id} on {platform}"
    if action == 'query':
        message = {
            'order_status': '',
            'exchangeable_products': []
        }
        if order.get('order_status', '') not in ['Pending payment', 'paid', 'processing']:
            message['order_status'] = f"Order {order_id}: exchange is unavailable (order status: {order.get('order_status', '')})"
        else:
            message['order_status'] = f"Order {order_id}: exchange is available (order status: {order.get('order_status', '')})"
        message['exchangeable_products'] = original_product.get('exchangeable_products', [])
        return data, json.dumps(message, ensure_ascii=False)
    
    elif action == 'exchange':
        order_products = order.get('order_items', [])
        original_product_index = next((index for index, product in enumerate(order_products) 
                            if product.get('product_id', "") == original_product_id), None)
        if original_product_index is None:
            return data, f"Order {order_id}: no product found among the purchased products ({original_product_id})"
        data['orders'][platform][shop_id][user_id][order_id]['order_items'][original_product_index]['product_id'] = exchange_product_id
        return data, f"Order {order_id}: product {original_product_id} exchange successful. The product ID after the exchange is {exchange_product_id}."
            