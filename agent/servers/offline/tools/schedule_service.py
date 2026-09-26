from .utils import get_order

def schedule_service(data, platform, shop_id, order_id, user_id, user_name, phone_number, service_type, service_time):
    order = get_order(data, platform, shop_id, user_id, order_id)
    if not order:
        return data, f"Not found: order {order_id} of user {user_id} in shop {shop_id} on {platform}"
    if 'service' not in data:
        data['service'] = {}
    
    if platform not in data['service']:
        data['service'][platform] = {}
    if shop_id not in data['service'][platform]:
        data['service'][platform][shop_id] = {}
    if user_id not in data['service'][platform][shop_id]:
        data['service'][platform][shop_id][user_id] = {}
    
    record = {
        'service_type': service_type,
        'shop_id': shop_id,
        'user_id': user_id,
        'order_id': order_id,
        'platform': platform,
        'phone_number': phone_number,
        'user_name': user_name,
        'appointment_date': service_time,
    }
    data['service'][platform][shop_id][user_id][order_id] = record
    return data, f"Appointment for {service_type} service successful"