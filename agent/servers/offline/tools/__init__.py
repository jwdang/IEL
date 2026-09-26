from .compare_products_info import compare_products_info
from .get_discount_info import get_discount_info
from .get_fault_code_info import get_fault_code_info
from .get_gift_info import get_gift_info
# from .get_image_info import get_image_info
from .get_image_info_mock import get_image_info
from .get_installation_service_info import get_installation_service_info
from .get_logistics_info import get_logistics_info
from .get_product_info import get_product_info
from .get_repair_info import get_repair_info
from .manage_ecard import manage_ecard
from .manage_exchange import manage_exchange
from .manage_invoice import manage_invoice
from .manage_order import manage_order
from .manage_return import manage_return
from .manage_urgent import manage_urgent
from .register_cashback_by_review import register_cashback_by_review
from .schedule_service import schedule_service
from .transfer_to_specialist import transfer_to_specialist
from .get_user_orders_info import get_user_orders_info
from .get_auxiliary_materials_info import get_auxiliary_materials_info
from .get_user_info import get_user_info


import logging
import os
def set_up_logger(force=True):    
    # file_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # log_dir = os.path.join(file_dir, 'logs')
    # os.makedirs(log_dir, exist_ok=True)
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filemode='w',  # start writing the log from scratch each time
        force=force  # force reconfiguration of logging
    )

    # Disable buffering
    logger = logging.getLogger()
    for handler in logger.handlers:
        if hasattr(handler, 'setLevel'):
            handler.setLevel(logging.INFO)
        if hasattr(handler, 'flush'):
            handler.flush()
    return logger

class ActionTools:
    def __init__(self):
        # Initialize the dictionary of available tool functions
        self.tools_dict = {
            "compare_products_info": compare_products_info,
            "get_discount_info": get_discount_info,
            "get_fault_code_info": get_fault_code_info,
            "get_gift_info": get_gift_info,
            "get_image_info": get_image_info,
            "get_installation_service_info": get_installation_service_info,
            "get_logistics_info": get_logistics_info,
            "get_product_info": get_product_info,
            "get_repair_info": get_repair_info,
            "manage_ecard": manage_ecard,
            "manage_exchange": manage_exchange,
            "manage_invoice": manage_invoice,
            "manage_order": manage_order,
            "manage_return": manage_return,
            "manage_urgent": manage_urgent,
            "register_cashback_by_review": register_cashback_by_review,
            "schedule_service": schedule_service,
            "transfer_to_specialist": transfer_to_specialist,
            "get_user_orders_info": get_user_orders_info,
            "get_auxiliary_materials_info": get_auxiliary_materials_info,
            "get_user_info": get_user_info
        }
        # Keep a list of tool function names for easy lookup
        self.tools_names = list(self.tools_dict.keys())
        
    def call_function(self, function_name, **kwargs):
        """
        Dynamically call the corresponding function by its name

        Args:
            function_name (str): name of the function to call
            **kwargs: arguments passed to the function

        Returns:
            The return value of the function call

        Raises:
            ValueError: if the function name does not exist
        """
        if function_name not in self.tools_dict:
            raise ValueError(f"Function '{function_name}' does not exist")
            
        # Fetch the corresponding function and call it with the kwargs
        func = self.tools_dict[function_name]
        return func(**kwargs)
    
    def get_available_functions(self):
        """
        Get the list of all available function names

        Returns:
            list: list of function names
        """
        return self.tools_names