from collections import defaultdict

def register_cashback_by_review(data, platform, shop_id, user_id, order_id, action):
    if not data.get("register_cashback", None):
        data["register_cashback"] = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(bool))))
    if action == 'query':
        record = data.get("register_cashback", {}).get(platform, {}).get(shop_id, {}).get(user_id, {}).get(order_id, {})
        if not record:
            return data, f"Not found: review cashback record for order {order_id} of user {user_id} in shop {shop_id} on {platform} (review not submitted)'"
        return data, f"Confirmed: review cashback record for order {order_id} of user {user_id} in shop {shop_id} on {platform} (review submitted)'"
    elif action == 'cashback':
        try:
            data["register_cashback"][platform][shop_id][user_id][order_id] = True
            return data, f"Review cashback for order {order_id} of user {user_id} in shop {shop_id} on {platform} has entered the cashback process (cashback issued)'"
        except:
            data["register_cashback"] = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(bool))))
            data["register_cashback"][platform][shop_id][user_id][order_id] = True
            return data, f"Review cashback for order {order_id} of user {user_id} in shop {shop_id} on {platform} has entered the cashback process (cashback issued)'"
        