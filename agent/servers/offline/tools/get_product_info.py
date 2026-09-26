from .utils import get_product_detail, format_product
import json


def get_product_info(data, platform, shop_id, product_id):
    if not product_id.isdigit():
        return data, f"Product ID {product_id} has an invalid format; must be a number"
    product = get_product_detail(data, platform, shop_id, product_id)
    if not product:
        return data, f"Not found: product {product_id} in shop {shop_id} on {platform}"
    product = format_product(product)
    return data, json.dumps(product, ensure_ascii=False)