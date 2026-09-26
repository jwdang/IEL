from .utils import get_product_detail, get_product_base
import json

def get_fault_code_info(data, platform, shop_id, product_id, fault_code):
    if not product_id.isdigit():
        return data, f"Product ID {product_id} has an invalid format; must be a number"
    product = get_product_detail(data, platform, shop_id, product_id)
    if not product:
        return data, f"Not found: product {product_id} in shop {shop_id} on {platform}"
    fault_code_infos = product.get('common_faults', [])
    fault_code_info = next((x for x in fault_code_infos if x['fault_code'] == fault_code), None)
    if not fault_code_info:
        return data, f"Not found: fault code {fault_code} for product {product_id} in shop {shop_id} on {platform}"
    product_base = get_product_base(data, platform, shop_id, product_id)
    result = {
        **product_base,
        'Fault information': fault_code_info
    }
    return data, json.dumps(result, ensure_ascii=False)