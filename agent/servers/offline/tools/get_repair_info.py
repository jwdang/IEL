from .utils import get_product_detail, get_product_base
import json
def get_repair_info(data, platform, shop_id, product_id):
    product = get_product_detail(data=data, platform=platform, shop_id=shop_id, product_id=product_id)
    if not product:
        return data, f"Not found: repair information for product {product_id}"
    product_base = get_product_base(data=data, platform=platform, shop_id=shop_id, product_id=product_id)
    result = {
        **product_base,
        'repair_notes': product.get('repair_notes', "")
    }
    
    return data, json.dumps(result, ensure_ascii=False)