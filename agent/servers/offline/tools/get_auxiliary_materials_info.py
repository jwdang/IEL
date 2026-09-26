from .utils import get_product_detail, get_product_base
import json

def get_auxiliary_materials_info(data, platform, shop_id, product_id):
    if not product_id.isdigit():
        return data, f"Product ID {product_id} has an invalid format; must be a number"
    product = get_product_detail(data, platform, shop_id, product_id)
    if not product:
        return data, f"Not found: product {product_id} in shop {shop_id} on {platform}"
    auxiliary_materials = product.get('accessory_material', [])
    if not auxiliary_materials:
        return data, f"Product {product_id}: no accessory materials found"
    product_base = get_product_base(data, platform, shop_id, product_id)
    result = {
        **product_base,
        'accessory_material': auxiliary_materials
    }
    return data, json.dumps(result, ensure_ascii=False)
