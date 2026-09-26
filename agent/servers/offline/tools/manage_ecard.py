from .utils import get_user, get_product_detail

ecard_service = f"""
The JD E-Card is an electronic prepaid card issued by JD Mall. It can be used to purchase JD self-operated products, covering many categories such as digital appliances, clothing and beauty, and home and daily necessities.
The card comes in two forms, electronic and physical, supports flexible denomination options, and can be bound to a JD account for convenient and quick use.
The JD E-Card is valid for 36 months from the date of activation, and any unused balance can be kept until the end of the validity period. It is suitable for personal spending or as a gift.
Note that the card can only be used for JD self-operated products; it does not support third-party seller products, virtual top-ups or certain special categories. When a refund is made, the amount is returned to the original card and cannot be withdrawn in cash, ensuring the safety of the funds.
Thanks to its convenience, security and wide applicability, the JD E-Card has become one of the payment methods favored by JD users.
"""

def manage_ecard(data, platform: str, user_id: str, action: str, product_id: str = None, quantity: int = None, shop_id: str = None, amount:float = 0):
    user_info = get_user(data, user_id)
    if not user_info:
        return data, f"Not found: user {user_id}"
    if action == 'Information inquiry':
        return data, ecard_service
    elif action == 'Balance inquiry':
        return data, f"User {user_id}'s e-card balance is {user_info['ecard_balance']} CNY"
    elif action == 'use_balance':
        if not product_id or not quantity or not shop_id:
            return data, f"Please provide the product ID, purchase quantity and shop ID"
        product = get_product_detail(data, platform, shop_id, product_id)
        if not product:
            return data, f"Not found: product {product_id}"
        product_price = product.get('product_price', 0)
        data['users_info'][user_id]['ecard_balance'] -= product_price * quantity
        return data, f"Purchased {quantity} units of product {product_id}, user {user_id}'s e-card balance is {data['users_info'][user_id]['ecard_balance']} CNY"
    elif action == 'refund':
        data['users_info'][user_id]['ecard_balance'] += float(amount)
        return data, f"'refunded'{amount} CNY, user {user_id}'s e-card balance is {data['users_info'][user_id]['ecard_balance']} CNY"