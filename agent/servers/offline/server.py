from typing import List, Dict, Annotated, Literal
from pydantic import Field, BaseModel
import os
import sys
import json
from functools import wraps

# This file is a subprocess launched by the MCP client as a script, so sys.path contains
# only its own directory; adding the repository root lets the tools reuse the root's
# llm_config.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if _REPO_ROOT not in sys.path:
    sys.path.append(_REPO_ROOT)

from mcp.server.fastmcp import FastMCP
from tools import compare_products_info
from tools import get_discount_info
from tools import get_fault_code_info
from tools import get_gift_info
from tools import get_image_info
from tools import get_installation_service_info
from tools import get_logistics_info
from tools import get_product_info
from tools import get_repair_info
from tools import manage_ecard
from tools import manage_exchange
from tools import manage_invoice
from tools import manage_order
from tools import manage_return
from tools import manage_urgent
from tools import register_cashback_by_review
from tools import schedule_service
from tools import transfer_to_specialist
from tools import set_up_logger
from tools import get_user_orders_info
from tools import get_auxiliary_materials_info
from tools import get_user_info

mcp = FastMCP("service")
data = None
logger = None
cache_dir = None


def log_mcp_tool(func):
    """Decorator: uniformly log the call arguments and return value of an MCP tool to
    the logger."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        global logger
        # Resolve positional arguments into parameter name -> value
        arg_names = func.__code__.co_varnames[: func.__code__.co_argcount]
        arg_dict = dict(zip(arg_names, args))
        arg_dict.update(kwargs)
        # Drop unnecessary fields such as the global data
        arg_dict.pop("data", None)
        try:
            args_repr = json.dumps(arg_dict, ensure_ascii=False)
        except Exception:
            args_repr = str(arg_dict)
        try:
            result = func(*args, **kwargs)
            if logger is not None:
                logger.info(
                    "[MCP Tool] %s args=%s result=%s",
                    func.__name__,
                    args_repr,
                    str(result),
                )
            return result
        except Exception:
            if logger is not None:
                logger.exception(
                    "[MCP Tool] %s error, args=%s",
                    func.__name__,
                    args_repr,
                )
            raise

    return wrapper


@mcp.tool()
@log_mcp_tool
def get_user_info_tool(
    user_id: Annotated[
        str,
        Field(..., description='user_id')
    ]
) -> str:
    """
    Used to fetch the default user information. Call this tool when the saved user
    information of a user needs to be looked up.
    """
    global data
    data, result = get_user_info(data = data, user_id = user_id)
    set_data(data)
    return result
    

@mcp.tool()
@log_mcp_tool
def get_user_orders_info_tool(
    platform: Annotated[
        str,
        Field(..., description='E-commerce platform')
    ],
    shop_id: Annotated[
        str,
        Field(..., description='shop_id')
    ],
    user_id: Annotated[
        str,
        Field(..., description='user_id')
    ]
) -> str:
    """
    Used to fetch all order IDs of a user from the user ID.
    """
    global data
    data, result = get_user_orders_info(data = data, platform = platform, shop_id = shop_id, user_id = user_id)
    set_data(data)
    return result

@mcp.tool()
@log_mcp_tool
def get_logistics_info_tool(
    platform: Annotated[
        str,
        Field(..., description='E-commerce platform')
    ],
    shop_id: Annotated[
        str,
        Field(..., description='shop_id')
    ],
    order_id: Annotated[
        str,
        Field(..., description='order_id')
    ],
    user_id: Annotated[
        str,
        Field(..., description='user_id')
    ]
) -> str:
    """
    Used to fetch logistics policy information.
    This tool may be called when the user asks about logistics-related questions.
    """
    global data
    data, result = get_logistics_info(data = data, platform = platform, shop_id = shop_id, order_id = order_id, user_id = user_id)
    set_data(data)
    return result


@mcp.tool()
@log_mcp_tool
def get_discount_info_tool(
    platform: Annotated[
        str,
        Field(..., description='E-commerce platform')
    ],
    shop_id: Annotated[
        str,
        Field(..., description='shop_id')
    ]
) -> str:
    """
    Used to fetch discount information.
    This tool may be called when the user asks about discount policies.
    """
    global data
    data, result = get_discount_info(data = data, platform = platform, shop_id = shop_id)
    set_data(data)
    return result



@mcp.tool()
@log_mcp_tool
def get_image_info_tool(
    summarized_query: Annotated[
        str,
        Field(..., description="Summarize the customer's requirement for the image based on the context (used for the task prompt)")
    ], 
    needed_query: Annotated[
        str,
        Field(..., description='Summarize the information you want to extract from the image')
    ],
    history_messages: Annotated[
        str,
        Field(..., description='Conversation context; must include the full image link.')
    ]
) -> str:
    """
    Image recognition tool: call it only in the following cases:
    1. the current or a historical message contains an image link (e.g. one with an
       extension such as `gif|png|jpg|jpeg|webp|svg|psd|bmp|tif|tiff|heic`); the call
       must include the complete image link
    2. you need to obtain information about the image content from the image in order to
       solve the problem
    """
    global data
    data, result = get_image_info(data, summarized_query, needed_query, history_messages)
    set_data(data)
    return result

@mcp.tool()
@log_mcp_tool
def get_repair_info_tool(
    platform: Annotated[
        str,
        Field(..., description='E-commerce platform')
    ],
    shop_id: Annotated[
        str,
        Field(..., description='shop_id')
    ],
    product_id: Annotated[
        str,
        Field(..., description='product_id')
    ]
) -> str:
    """
    Used to fetch repair service information. Call this tool when the user asks about
    repair services.
    """
    global data
    data, result = get_repair_info(data = data, platform = platform, shop_id = shop_id, product_id = product_id)
    set_data(data)
    return result

@mcp.tool()
@log_mcp_tool
def manage_return_tool(
    platform: Annotated[
        str,
        Field(..., description='E-commerce platform')
    ],
    shop_id: Annotated[
        str,
        Field(..., description='shop_id')
    ],
    order_id: Annotated[
        str,
        Field(..., description='order_id')
    ],
    user_id: Annotated[
        str,
        Field(..., description='user_id')
    ],
) -> str:
    """
    Used for handling return service information. Call this tool when the user needs to
    apply for a return.
    """
    global data
    data, result = manage_return(data = data, platform = platform, shop_id = shop_id, order_id = order_id, user_id = user_id)
    set_data(data)
    return result

@mcp.tool()
@log_mcp_tool
def manage_exchange_tool(
    platform: Annotated[
        str,
        Field(..., description='E-commerce platform')
    ],
    shop_id: Annotated[
        str,
        Field(..., description='shop_id')
    ],
    order_id: Annotated[
        str,
        Field(..., description='order_id')
    ],
    user_id: Annotated[
        str,
        Field(..., description='user_id')
    ],
    original_product_id: Annotated[
        str,
        Field(..., description='Original product ID')
    ],
    action: Annotated[
        Literal['query', 'exchange'],
        Field(..., description="Operation type: 'query' queries exchange information, 'exchange' processes an exchange request")
    ],
    exchange_product_id: Annotated[
        str,
        Field(None, description="Exchange product ID, required only when action is 'exchange'")
    ] = None
) -> str:
    """
    Used for handling exchange services. Call this tool when the user needs to submit an
    exchange request.
    """
    global data
    data, result = manage_exchange(data = data, platform = platform, shop_id = shop_id, order_id = order_id, user_id = user_id, original_product_id = original_product_id, exchange_product_id = exchange_product_id, action = action)
    set_data(data)
    return result

@mcp.tool()
def manage_urgent_tool(
    platform: Annotated[
        str,
        Field(..., description='E-commerce platform')
    ],
    shop_id: Annotated[
        str,
        Field(..., description='shop_id')
    ],
    order_id: Annotated[
        str,
        Field(..., description='order_id')
    ],
    user_id: Annotated[
        str,
        Field(..., description='user_id')
    ]
) -> bool:
    """
    Tool for handling expedited shipping/transport services. Call this tool when the user
    needs expedited shipping or transport.
    """
    global data
    data, result = manage_urgent(data = data, platform = platform, shop_id = shop_id, order_id = order_id, user_id = user_id)
    set_data(data)
    return result

@mcp.tool()
@log_mcp_tool
def get_auxiliary_materials_info_tool(
    platform: Annotated[
        str,
        Field(..., description='E-commerce platform')
    ],
    shop_id: Annotated[
        str,
        Field(..., description='shop_id')
    ],
    product_id: Annotated[
        str,
        Field(..., description='product_id')
    ]
) -> str:
    """
    Used to fetch a product's auxiliary-materials information. Call this tool when the
    user asks about a product's auxiliary materials.
    """
    global data
    data, result = get_auxiliary_materials_info(data = data, platform = platform, shop_id = shop_id, product_id = product_id)
    set_data(data)
    return result

@mcp.tool()
@log_mcp_tool
def get_gift_info_tool(
    platform: Annotated[
        str,
        Field(..., description='E-commerce platform')
    ],
    shop_id: Annotated[
        str,
        Field(..., description='shop_id')
    ],
    product_id: Annotated[
        str,
        Field(..., description='product_id')
    ]
) -> str:
    """
    Used to fetch gift information. Call this tool when the user asks about gifts.
    """
    global data
    data, result = get_gift_info(data= data, platform = platform, shop_id = shop_id, product_id = product_id)
    set_data(data)
    return result

@mcp.tool()
@log_mcp_tool
def manage_ecard_tool(
    platform: Annotated[
        str,
        Field(..., description='E-commerce platform')
    ],
    user_id: Annotated[
        str,
        Field(..., description='user_id')
    ],
    action: Annotated[
        Literal['Information inquiry', 'use_balance', 'Balance inquiry', 'refund'],
        Field(..., description='Operation type. Available values: information inquiry (query JD E-Card related information), balance use, balance inquiry, refund')
    ],
    shop_id: Annotated[
        str,
        Field(None, description='Shop ID (required only when action is balance use)')
    ] = None,
    product_id: Annotated[
        str,
        Field(None, description='Product ID (required only when action is balance use)')
    ] = None,
    quantity: Annotated[
        int,
        Field(None, description='Product purchase quantity (required only when action is balance use)')
    ] = None,
    amount: Annotated[
        float,
        Field(0, description='Refund amount (required only when action is refund)')
    ] = None
) -> str:
    """
    Used to manage JD E-card information (service query, use, balance query, refund).
    Call this tool when the user raises questions about the JD E-card.
    """
    global data
    data, result = manage_ecard(data = data, platform = platform, user_id = user_id, action = action, product_id = product_id, quantity = quantity, shop_id = shop_id, amount = amount)
    set_data(data)
    return result

@mcp.tool()
@log_mcp_tool
def get_installation_service_info_tool(
    platform: Annotated[
        str,
        Field(..., description='E-commerce platform')
    ],
    shop_id: Annotated[
        str,
        Field(..., description='shop_id')
    ],
    product_id: Annotated[
        str,
        Field(..., description='product_id')
    ]
) -> str:
    """
    Used to fetch a product's installation service information or issues. Call this tool
    when the user asks about installation services or the installation process.
    """
    global data
    data, result = get_installation_service_info(data = data, platform = platform, shop_id = shop_id, product_id = product_id)
    set_data(data)
    return result

@mcp.tool()
@log_mcp_tool
def get_product_info_tool(
    platform: Annotated[
        str,
        Field(..., description='E-commerce platform')
    ],
    shop_id: Annotated[
        str,
        Field(..., description='shop_id')
    ],
    product_id: Annotated[
        str,
        Field(..., description='product_id')
    ]
) -> str:
    """
    Used to fetch product details. Call this tool when the user asks about product
    information.
    """
    global data
    data, result = get_product_info(data = data, platform = platform, shop_id = shop_id, product_id = product_id)
    set_data(data)
    return result

class ProductInfo(BaseModel):
    product_id: Annotated[
        str,
        Field(..., description='product_id')
    ]
    quantity: Annotated[
        int,
        Field(..., description='Product quantity')
    ]
    

@mcp.tool()
@log_mcp_tool
def manage_order_tool(
    platform: Annotated[
        str,
        Field(..., description='E-commerce platform')
    ],
    shop_id: Annotated[
        str,
        Field(..., description='shop_id')
    ],
    user_id: Annotated[
        str,
        Field(..., description='user_id')
    ],
    action: Annotated[
        Literal['query', 'cancel', 'modify', 'add'],
        Field(..., description='Operation type. Available values: query, cancel, modify (address/phone number), add (place order)')
    ],
    payment: Annotated[
        Literal['bank_card', 'jd_ecard', 'wechat', 'alipay'],
        Field('alipay', description='Payment method (required only when action is add)')
    ] = None,
    order_id: Annotated[
        str,
        Field(None, description='Order ID (required only when action is query, cancel or modify)')
    ] = None,
    address: Annotated[
        str,
        Field(None, description='New delivery address (optional; only when action is modify)')
    ] = None,
    phone_number: Annotated[
        str,
        Field(None, description='New phone number (optional; only when action is modify)')
    ] = None,
    product_info_list: Annotated[
        List[ProductInfo],
        Field(None, description='Product information (required only when action is add)')
    ] = None
) -> str:
    """
    Used to manage order information, including querying an order, cancelling an order
    (requires confirming with the user again), modifying an order (address, phone
    number) and placing an order.
    The order information includes the items the user purchased, the shipping address and
    other specific details.
    """
    global data
    data, result = manage_order(data = data, platform = platform, order_id = order_id, shop_id = shop_id, user_id = user_id, action = action, address = address, phone_number = phone_number, product_info_list = product_info_list, payment = payment)
    set_data(data)
    return result

@mcp.tool()
@log_mcp_tool
def schedule_service_tool(
    platform: Annotated[
        str,
        Field(..., description='E-commerce platform')
    ],
    shop_id: Annotated[
        str,
        Field(..., description='shop_id')
    ],
    order_id: Annotated[
        str,
        Field(..., description='order_id')
    ],
    user_id: Annotated[
        str,
        Field(..., description='user_id')
    ],
    user_name: Annotated[
        str,
        Field(..., description='user_name')
    ],
    phone_number: Annotated[
        str,
        Field(..., description='User phone number')
    ],
    service_type: Annotated[
        Literal['Repair', 'Check', 'installation'],
        Field(..., description='The service type the user needs')
    ],
    service_time: Annotated[
        Literal['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        Field(..., description='The time when the user booked the service')
    ],
) -> str:
    """
    Used when the user wants to book a repair, an on-site inspection or an installation
    service.
    """
    global data
    data, result = schedule_service(data = data, platform = platform, shop_id = shop_id, order_id = order_id, user_id = user_id, user_name = user_name, phone_number = phone_number, service_type = service_type, service_time = service_time)
    set_data(data)
    return result

# @mcp.tool()
# def get_products_recommendation_tool(
#     platform: Annotated[
#         str,
#         Field(..., description="e-commerce platform")
#     ],
#     shop_id: Annotated[
#         str,
#         Field(..., description="shop ID")
#     ],
#     properties: Annotated[
#         dict,
#         Field(..., description="product attribute information")
#     ]
# ) -> str:
#     """
#     Used to fetch product recommendation information. Call this tool when the user asks
#     for product recommendations.
#     """
#     data, result = get_products_recommendation(data = data, platform = platform, shop_id = shop_id, properties = properties)
#     set_data(data)
#     return result

@mcp.tool()
@log_mcp_tool
def get_fault_code_info_tool(
    platform: Annotated[
        str,
        Field(..., description='E-commerce platform')
    ],
    shop_id: Annotated[
        str,
        Field(..., description='shop_id')
    ],
    product_id: Annotated[
        str,
        Field(..., description='product_id')
    ],
    fault_code: Annotated[
        str,
        Field(..., description='Product fault code')
    ]
) -> str:
    """
    Used to fetch the fault information corresponding to a product fault code. Call this
    tool when the user reports a product fault code.
    """
    global data
    data, result = get_fault_code_info(data = data, platform = platform, shop_id = shop_id, product_id = product_id, fault_code = fault_code)
    set_data(data)
    return result

@mcp.tool()
@log_mcp_tool
def register_cashback_by_review_tool(
    platform: Annotated[
        str,
        Field(..., description='E-commerce platform')
    ],
    shop_id: Annotated[
        str,
        Field(..., description='shop_id')
    ],
    user_id: Annotated[
        str,
        Field(..., description='user_id')
    ],
    order_id: Annotated[
        str,
        Field(..., description='order_id')
    ],
    action: Annotated[
        Literal['query', 'cashback'],
        Field(..., description="Operation type: 'query' - check the review status; 'cashback' - issue the cashback after confirming that a review has been posted")
    ]
) -> str:
    """
    Handles the query and cashback flow of review-based cashback on the e-commerce
    platform.
    """
    global data
    data, result = register_cashback_by_review(data = data, platform = platform, shop_id = shop_id, user_id = user_id, order_id = order_id, action = action)
    set_data(data)
    return result

@mcp.tool()
@log_mcp_tool
def compare_products_info_tool(
    shop_id: Annotated[
        str,
        Field(..., description='shop_id')
    ],
    platform: Annotated[
        str,
        Field(..., description='E-commerce platform')
    ],
    product_ids: Annotated[
        List[str],
        Field(..., description='List of product IDs to compare')
    ]
) -> str:
    """
    Used to compare the information of several products under the same shop. Call this
    tool when the user needs to compare product parameters, configuration, price, etc.
    """
    global data
    data, result = compare_products_info(data = data, shop_id = shop_id, platform = platform, product_ids = product_ids)
    set_data(data)
    return result

@mcp.tool()
@log_mcp_tool
def manage_invoice_tool(
    title:Annotated[
        str,
        Field(..., description="Invoice title, such as a company name or an individual's name")
    ],
    order_id: Annotated[
        str,
        Field(..., description='order_id')
    ],
    phone_number: Annotated[
        str,
        Field(..., description='Contact phone')
    ],
    invoice_type: Annotated[
        Literal['personal_invoice', 'corporate_invoice', 'VAT special invoice'],
        Field(..., description='Invoice type. Available values: personal invoice, corporate invoice, VAT special invoice; must be provided by the user.')
    ]
    ) -> str:
    """
    Used to apply for an invoice. Call this tool when the user needs an invoice issued.
    """
    global data
    data, result = manage_invoice(data = data, title = title, order_id = order_id, phone_number = phone_number, invoice_type = invoice_type)
    set_data(data)
    return result


@mcp.tool()
@log_mcp_tool
def transfer_to_specialist_tool(
    platform: Annotated[
        str,
        Field(..., description='E-commerce platform')
    ],
    shop_id: Annotated[
        str,
        Field(..., description='shop_id')
    ],
    user_id: Annotated[
        str,
        Field(..., description='user_id')
    ]
) -> str:
    """
    Used to transfer to the corresponding dedicated-line agent. Call this tool when the
    agent needs to transfer the buyer to a dedicated-line agent.
    """
    global data
    data, result = transfer_to_specialist(data, platform, shop_id, user_id)
    set_data(data)
    return result




    
def set_data(data):
    for file_name, file_data in data.items():
        file_path = os.path.join(cache_dir, file_name + '.json')
        with open(file_path, 'w',encoding='utf-8') as f:
            json.dump(file_data, f, ensure_ascii=False, indent=2)
    

def get_data(cache_dir):
    # Read all json files from the given directory
    data = {}
    files = os.listdir(cache_dir)
    json_files = [f for f in files if f.endswith('.json')]
    if len(json_files) == 0:
        return {}
    else:
        # Read the json files
        for json_file in json_files:
            file_path = os.path.join(cache_dir, json_file)
            file_name = os.path.splitext(json_file)[0]
            with open(file_path, 'r',encoding='utf-8') as f:
                data[file_name] = json.load(f)
    return data

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="MultiServerMCPClient")
    parser.add_argument("--cache_dir", type=str, default="cache", help="Cache directory")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    cache_dir = args.cache_dir
    logger = set_up_logger()
    data = get_data(args.cache_dir)
    mcp.run(transport="stdio")
