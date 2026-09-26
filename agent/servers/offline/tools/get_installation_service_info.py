from .utils import get_product_detail, get_product_base
import json

def get_installation_service_info(data, platform, shop_id, product_id):
    if not product_id.isdigit():
        return data, f"Product ID {product_id} has an invalid format; must be a number"
    product = get_product_detail(data, platform, shop_id, product_id)
    if not product:
        return data, f"Not found: product {product_id} in shop {shop_id} on {platform}"
    product_base = get_product_base(data, platform, shop_id, product_id)
    result = {
        **product_base,
        'installation_notes': product['installation_notes']
    }
    return data, json.dumps(result, ensure_ascii=False)