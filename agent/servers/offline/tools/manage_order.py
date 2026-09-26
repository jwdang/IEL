from .utils import get_order, get_user, get_product_detail
import json

# Cancellable status enum: pending payment, paid, processing
# Status enum for modifying address/phone: pending payment, paid, processing

def manage_order(data, platform: str, shop_id: str, user_id: str, action: str, order_id:str = None, address: str = None, phone_number: str = None, product_info_list = None, payment:str ='alipay'):
    if action == 'add':
        order_id = '1234567890'
        if not product_info_list:
            return data, f"The product list is empty, so the order cannot be placed"
        user_info = get_user(data, user_id)
        if not user_info:
            return data, f"Not found: user {user_id}"
        recipient = {
            'recipient_name': user_info['user_name'],
            'phone_number': user_info['phone_number'],
            'country': user_info['address_info']['country'],
            'province': user_info['address_info']['province'],
            'city': user_info['address_info']['city'],
            'district': user_info['address_info']['district'],
            'street_address': user_info['address_info']['street_address']
        }
        total_amount = 0
        order_product_list = []
        for product_info in product_info_list:
            product_id = product_info.product_id
            quantity = product_info.quantity
            product = get_product_detail(data, platform, shop_id, product_id)
            if not product:
                continue
            order_product_list.append({
                'product_id': product_id,
                'product_price': product['product_price'],
                'quantity': quantity,
            })
            total_amount += product['product_price'] * quantity
        order = {
            'user_id': user_id,
            'order_id': order_id,
            'order_status': 'paid',
            'order_total': total_amount,
            'is_urgent': False,
            'order_items': order_product_list,
            'shipping_address': recipient,
            'payment_method': payment,
        }
        if platform not in data["orders"]:
            data["orders"][platform] = {}
        if shop_id not in data["orders"][platform]:
            data["orders"][platform][shop_id] = {}
        if user_id not in data["orders"][platform][shop_id]:
            data["orders"][platform][shop_id][user_id] = {}
        data["orders"][platform][shop_id][user_id][order_id] = order
        return data, f"Order {order_id} has been added. Order details: {json.dumps(order, ensure_ascii=False)}"
    order = get_order(data, platform, shop_id, user_id, order_id)
    if not order:
        return data, f"Not found: order {order_id}"
    if action == 'query':
        return data, json.dumps(order, ensure_ascii=False)
    elif action == 'cancel':
        data["orders"][platform][shop_id][user_id][order_id]['order_status'] = 'cancelled'
        return data, f"Order {order_id} has been cancelled. The cancelled order is {json.dumps(order, ensure_ascii=False)}"
    elif action == 'modify':
        if not address and not phone_number:
            return data, f"Both the new address and the new phone number are empty, so the modification cannot be made"
        if address: # By default only the detailed address is modified
            data["orders"][platform][shop_id][user_id][order_id]['shipping_address']['street_address'] = address
        if phone_number:
            data["orders"][platform][shop_id][user_id][order_id]['shipping_address']['phone_number'] = phone_number
        return data, f"Order {order_id}'s address and phone number have been modified. The modified order is {json.dumps(order, ensure_ascii=False)}"
    else:
        return data, f"Unsupported operation: {action}"
            