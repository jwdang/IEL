from utils import Task, Action, Search, Validation, ProductInfo

platform = "jd"
shop_id = "xcat_shop_001"

ALL_TASKS = [
    Task(
        annotator="plus_000",
        user_id="cnjd_cloth_001",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nRational-comparison consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Steady mood; focused on completeness of information.</emotion>\n<meticulousness>Very high; will verify specifications and after-sales boundaries.</meticulousness>\n<patience>Medium-to-high; willing to confirm step by step.</patience>\n<trust>Medium; accepts suggestions but requires them to be grounded.</trust>\n<awareness_of_rights>Medium; prefers to confirm before deciding.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Asks about the differences first, then whether they fit their own needs.</questioning_style>\n<speaking_style>Clear and well-organized; tends toward rational expression.</speaking_style>\n<communication_pace>Advances step by step and does not skip steps.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first compare the differences between products 100910000001 and 100910000002 in terms of applicable scenarios, specifications and after-sales boundaries.\n<\\intent_1>\n<intent_2>\nThen explain the return and exchange rules for this category of products; I will make the decision first and do not need any action taken for now.\n<\\intent_2>\n',
        metadata=Validation(
            outputs=[],
            actions=[
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['100910000001', '100910000002']}),
            ],
        ),
    ),
    Task(
        annotator="plus_001",
        user_id="cnjd_cloth_002",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst help me check the current status of order 31002000002.\n<\\intent_1>\n<intent_2>\nThen look at the logistics milestones and the estimated delivery of order 31002000003; I just want to understand the situation first and will not take any action.\n<\\intent_2>\n<intent_3>\nIf there is a risk of delay, please alert me.\n<\\intent_3>\n',
        metadata=Validation(
            outputs=[],
            actions=[
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_002', 'order_id': '31002000002', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_002', 'order_id': '31002000003'}),
            ],
        ),
    ),
    Task(
        annotator="plus_002",
        user_id="cnjd_cloth_003",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nRational-comparison consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Steady mood; focused on completeness of information.</emotion>\n<meticulousness>Very high; will verify specifications and after-sales boundaries.</meticulousness>\n<patience>Medium-to-high; willing to confirm step by step.</patience>\n<trust>Medium; accepts suggestions but requires them to be grounded.</trust>\n<awareness_of_rights>Medium; prefers to confirm before deciding.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Asks about the differences first, then whether they fit their own needs.</questioning_style>\n<speaking_style>Clear and well-organized; tends toward rational expression.</speaking_style>\n<communication_pace>Advances step by step and does not skip steps.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare products 100910000005 and 100910000006.\n<\\intent_1>\n<intent_2>\nThen check the currently available discounts and free-gift information; for now do not perform any ordering or after-sales action.\n<\\intent_2>\n',
        metadata=Validation(
            outputs=[],
            actions=[
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['100910000005', '100910000006']}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '100910000005'}),
            ],
        ),
    ),
    Task(
        annotator="plus_003",
        user_id="cnjd_cloth_004",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nRational-comparison consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Steady mood; focused on completeness of information.</emotion>\n<meticulousness>Very high; will verify specifications and after-sales boundaries.</meticulousness>\n<patience>Medium-to-high; willing to confirm step by step.</patience>\n<trust>Medium; accepts suggestions but requires them to be grounded.</trust>\n<awareness_of_rights>Medium; prefers to confirm before deciding.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Asks about the differences first, then whether they fit their own needs.</questioning_style>\n<speaking_style>Clear and well-organized; tends toward rational expression.</speaking_style>\n<communication_pace>Advances step by step and does not skip steps.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first compare the differences between products 100910000007 and 100910000008 in terms of applicable scenarios, specifications and after-sales boundaries.\n<\\intent_1>\n<intent_2>\nThen explain the return and exchange rules for this category of products; I will make the decision first and do not need any action taken for now.\n<\\intent_2>\n',
        metadata=Validation(
            outputs=[],
            actions=[
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['100910000007', '100910000008']}),
            ],
        ),
    ),
    Task(
        annotator="plus_004",
        user_id="cnjd_cloth_005",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst help me check the current status of order 31005000002.\n<\\intent_1>\n<intent_2>\nThen look at the logistics milestones and the estimated delivery of order 31005000003; I just want to understand the situation first and will not take any action.\n<\\intent_2>\n<intent_3>\nIf there is a risk of delay, please alert me.\n<\\intent_3>\n',
        metadata=Validation(
            outputs=[],
            actions=[
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_005', 'order_id': '31005000002', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_005', 'order_id': '31005000003'}),
            ],
        ),
    ),
    Task(
        annotator="plus_005",
        user_id="cnjd_cloth_006",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nRational-comparison consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Steady mood; focused on completeness of information.</emotion>\n<meticulousness>Very high; will verify specifications and after-sales boundaries.</meticulousness>\n<patience>Medium-to-high; willing to confirm step by step.</patience>\n<trust>Medium; accepts suggestions but requires them to be grounded.</trust>\n<awareness_of_rights>Medium; prefers to confirm before deciding.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Asks about the differences first, then whether they fit their own needs.</questioning_style>\n<speaking_style>Clear and well-organized; tends toward rational expression.</speaking_style>\n<communication_pace>Advances step by step and does not skip steps.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare products 100910000011 and 100910000012.\n<\\intent_1>\n<intent_2>\nThen check the currently available discounts and free-gift information; for now do not perform any ordering or after-sales action.\n<\\intent_2>\n',
        metadata=Validation(
            outputs=[],
            actions=[
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['100910000011', '100910000012']}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '100910000011'}),
            ],
        ),
    ),
    Task(
        annotator="plus_006",
        user_id="cnjd_cloth_003",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first check the current status of order 31003000001.\n<\\intent_1>\n<intent_2>\nThen look at the logistics progress and the estimated delivery of order 31003000001.\n<\\intent_2>\n<intent_3>\nAlso tell me whether there are any discounts available at the moment.\n<\\intent_3>\n<intent_4>\nIf the conditions are met, please directly expedite order 31003000001 for me.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_003', 'order_id': '31003000001'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_003', 'order_id': '31003000001', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_003', 'order_id': '31003000001'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
            ],
        ),
    ),
    Task(
        annotator="plus_007",
        user_id="cnjd_cloth_001",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first confirm whether order 31001000001 is still in a cancellable state.\n<\\intent_1>\n<intent_2>\nThen check whether the coupon can still be used after cancellation.\n<\\intent_2>\n<intent_3>\nIf it can still be cancelled, please directly cancel order 31001000001 for me.\n<\\intent_3>\n<intent_4>\nGive me a receipt after the cancellation is complete.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_order", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_001', 'order_id': '31001000001', 'action': 'cancel'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_001', 'order_id': '31001000001', 'action': 'query'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
            ],
        ),
    ),
    Task(
        annotator="plus_008",
        user_id="cnjd_cloth_005",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nDocumentation-and-compliance-oriented consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Steady mood, but demands high accuracy of fields.</emotion>\n<meticulousness>Very high; will check the invoice title and phone number item by item.</meticulousness>\n<patience>Medium-to-high; can cooperate with verification.</patience>\n<trust>Medium; accepts the process but requires it to be traceable.</trust>\n<awareness_of_rights>Medium-to-high; values leaving a paper trail.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the order and identity information first, then asks for the invoice.</questioning_style>\n<speaking_style>Leans toward formal written expression, field-oriented.</speaking_style>\n<communication_pace>Confirms item by item, does not skip fields.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first check the status of order 31005000003 and confirm that an invoice can be issued.\n<\\intent_1>\n<intent_2>\nI will not repeat my name and phone number; please verify them from the system first.\n<\\intent_2>\n<intent_3>\nAfter verification, please issue a personal invoice directly.\n<\\intent_3>\n<intent_4>\nAnd return the invoice title and contact phone number.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_invoice", arguments={'title': 'Apparel User 5', 'order_id': '31005000003', 'phone_number': '13900010005', 'invoice_type': 'personal_invoice'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_005', 'order_id': '31005000003', 'action': 'query'}),
                Search(name="get_user_info_tool", arguments={'user_id': 'cnjd_cloth_005'}),
            ],
        ),
    ),
    Task(
        annotator="plus_009",
        user_id="cnjd_cloth_006",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst check the current status and the return eligibility of order 31006000001.\n<\\intent_1>\n<intent_2>\nThen confirm the return process and the time required.\n<\\intent_2>\n<intent_3>\nI have confirmed I want to return it; please directly initiate the return of order 31006000001 for me.\n<\\intent_3>\n<intent_4>\nAnd explain whether refunding to the E-card is supported.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_return", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_006', 'order_id': '31006000001'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_006', 'order_id': '31006000001', 'action': 'query'}),
                Search(name="manage_return_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_006', 'order_id': '31006000001', 'action': 'query'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_cloth_006', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
    Task(
        annotator="plus_010",
        user_id="cnjd_cloth_007",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst check the product details of order 31007000003.\n<\\intent_1>\n<intent_2>\nI plan to exchange 100910000001 for 100910000002; first confirm the stock and the exchange rules.\n<\\intent_2>\n<intent_3>\nThen explain the expected turnaround time for the exchange.\n<\\intent_3>\n<intent_4>\nI confirm the exchange; please directly submit the exchange for order 31007000003.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_exchange", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_007', 'order_id': '31007000003', 'original_product_id': '100910000001', 'exchange_product_id': '100910000002', 'action': 'exchange'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_007', 'order_id': '31007000003', 'action': 'query'}),
                Search(name="get_product_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '100910000002'}),
                Search(name="manage_exchange_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_007', 'order_id': '31007000003', 'original_product_id': '100910000001', 'action': 'query'}),
            ],
        ),
    ),
    Task(
        annotator="plus_011",
        user_id="cnjd_cloth_008",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nDocumentation-and-compliance-oriented consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Steady mood, but demands high accuracy of fields.</emotion>\n<meticulousness>Very high; will check the invoice title and phone number item by item.</meticulousness>\n<patience>Medium-to-high; can cooperate with verification.</patience>\n<trust>Medium; accepts the process but requires it to be traceable.</trust>\n<awareness_of_rights>Medium-to-high; values leaving a paper trail.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the order and identity information first, then asks for the invoice.</questioning_style>\n<speaking_style>Leans toward formal written expression, field-oriented.</speaking_style>\n<communication_pace>Confirms item by item, does not skip fields.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst check my E-card balance.\n<\\intent_1>\n<intent_2>\nThen verify the amount and status of order 31008000003.\n<\\intent_2>\n<intent_3>\nIf the balance can cover it, please complete the payment directly with the E-card balance.\n<\\intent_3>\n<intent_4>\nAnd tell me how the balance changes after payment.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_ecard", arguments={'platform': 'jd', 'user_id': 'cnjd_cloth_008', 'action': 'use_balance', 'shop_id': 'xcat_shop_001', 'product_id': '100910000005', 'quantity': 1}),
            ],
            searches=[
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_cloth_008', 'action': 'Balance inquiry'}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_008', 'order_id': '31008000003', 'action': 'query'}),
                Search(name="get_user_info_tool", arguments={'user_id': 'cnjd_cloth_008'}),
            ],
        ),
    ),
    Task(
        annotator="plus_012",
        user_id="cnjd_cloth_009",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst check the status and the logistics track of order 31009000002.\n<\\intent_1>\n<intent_2>\nThen explain why the current problem is hard for an ordinary customer service agent to close the loop on.\n<\\intent_2>\n<intent_3>\nI need the issue escalated and the record kept.\n<\\intent_3>\n<intent_4>\nPlease directly transfer me to a specialist for follow-up.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_009'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_009', 'order_id': '31009000002', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_009', 'order_id': '31009000002'}),
            ],
        ),
    ),
    Task(
        annotator="plus_013",
        user_id="cnjd_cloth_010",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first check the current status of order 31010000001.\n<\\intent_1>\n<intent_2>\nThen look at the logistics progress and the estimated delivery of order 31010000001.\n<\\intent_2>\n<intent_3>\nAlso tell me whether there are any discounts available at the moment.\n<\\intent_3>\n<intent_4>\nIf the conditions are met, please directly expedite order 31010000001 for me.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_010', 'order_id': '31010000001'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_010', 'order_id': '31010000001', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_010', 'order_id': '31010000001'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
            ],
        ),
    ),
    Task(
        annotator="plus_014",
        user_id="cnjd_cloth_001",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first confirm whether order 31001000001 is still in a cancellable state.\n<\\intent_1>\n<intent_2>\nThen check whether the coupon can still be used after cancellation.\n<\\intent_2>\n<intent_3>\nIf it can still be cancelled, please directly cancel order 31001000001 for me.\n<\\intent_3>\n<intent_4>\nGive me a receipt after the cancellation is complete.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_order", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_001', 'order_id': '31001000001', 'action': 'cancel'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_001', 'order_id': '31001000001', 'action': 'query'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
            ],
        ),
    ),
    Task(
        annotator="plus_015",
        user_id="cnjd_cloth_002",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nDocumentation-and-compliance-oriented consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Steady mood, but demands high accuracy of fields.</emotion>\n<meticulousness>Very high; will check the invoice title and phone number item by item.</meticulousness>\n<patience>Medium-to-high; can cooperate with verification.</patience>\n<trust>Medium; accepts the process but requires it to be traceable.</trust>\n<awareness_of_rights>Medium-to-high; values leaving a paper trail.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the order and identity information first, then asks for the invoice.</questioning_style>\n<speaking_style>Leans toward formal written expression, field-oriented.</speaking_style>\n<communication_pace>Confirms item by item, does not skip fields.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first check the status of order 31002000001 and confirm that an invoice can be issued.\n<\\intent_1>\n<intent_2>\nI will not repeat my name and phone number; please verify them from the system first.\n<\\intent_2>\n<intent_3>\nAfter verification, please issue a corporate invoice directly.\n<\\intent_3>\n<intent_4>\nAnd return the invoice title and contact phone number.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_invoice", arguments={'title': 'Xingchuan Apparel Trading Co., Ltd.', 'order_id': '31002000001', 'phone_number': '13900010002', 'invoice_type': 'corporate_invoice'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_002', 'order_id': '31002000001', 'action': 'query'}),
                Search(name="get_user_info_tool", arguments={'user_id': 'cnjd_cloth_002'}),
            ],
        ),
    ),
    Task(
        annotator="plus_016",
        user_id="cnjd_cloth_003",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst check the current status and the return eligibility of order 31003000002.\n<\\intent_1>\n<intent_2>\nThen confirm the return process and the time required.\n<\\intent_2>\n<intent_3>\nI have confirmed I want to return it; please directly initiate the return of order 31003000002 for me.\n<\\intent_3>\n<intent_4>\nAnd explain whether refunding to the E-card is supported.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_return", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_003', 'order_id': '31003000002'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_003', 'order_id': '31003000002', 'action': 'query'}),
                Search(name="manage_return_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_003', 'order_id': '31003000002', 'action': 'query'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_cloth_003', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
    Task(
        annotator="plus_017",
        user_id="cnjd_cloth_004",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst check the product details of order 31004000003.\n<\\intent_1>\n<intent_2>\nI plan to exchange 100910000008 for 100910000007; first confirm the stock and the exchange rules.\n<\\intent_2>\n<intent_3>\nThen explain the expected turnaround time for the exchange.\n<\\intent_3>\n<intent_4>\nI confirm the exchange; please directly submit the exchange for order 31004000003.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_exchange", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_004', 'order_id': '31004000003', 'original_product_id': '100910000008', 'exchange_product_id': '100910000007', 'action': 'exchange'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_004', 'order_id': '31004000003', 'action': 'query'}),
                Search(name="get_product_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '100910000007'}),
                Search(name="manage_exchange_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_004', 'order_id': '31004000003', 'original_product_id': '100910000008', 'action': 'query'}),
            ],
        ),
    ),
    Task(
        annotator="plus_018",
        user_id="cnjd_cloth_005",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nDocumentation-and-compliance-oriented consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Steady mood, but demands high accuracy of fields.</emotion>\n<meticulousness>Very high; will check the invoice title and phone number item by item.</meticulousness>\n<patience>Medium-to-high; can cooperate with verification.</patience>\n<trust>Medium; accepts the process but requires it to be traceable.</trust>\n<awareness_of_rights>Medium-to-high; values leaving a paper trail.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the order and identity information first, then asks for the invoice.</questioning_style>\n<speaking_style>Leans toward formal written expression, field-oriented.</speaking_style>\n<communication_pace>Confirms item by item, does not skip fields.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst check my E-card balance.\n<\\intent_1>\n<intent_2>\nThen verify the amount and status of order 31005000001.\n<\\intent_2>\n<intent_3>\nIf the balance can cover it, please complete the payment directly with the E-card balance.\n<\\intent_3>\n<intent_4>\nAnd tell me how the balance changes after payment.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_ecard", arguments={'platform': 'jd', 'user_id': 'cnjd_cloth_005', 'action': 'use_balance', 'shop_id': 'xcat_shop_001', 'product_id': '100910000001', 'quantity': 1}),
            ],
            searches=[
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_cloth_005', 'action': 'Balance inquiry'}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_005', 'order_id': '31005000001', 'action': 'query'}),
                Search(name="get_user_info_tool", arguments={'user_id': 'cnjd_cloth_005'}),
            ],
        ),
    ),
    Task(
        annotator="plus_019",
        user_id="cnjd_cloth_006",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst check the status and the logistics track of order 31006000001.\n<\\intent_1>\n<intent_2>\nThen explain why the current problem is hard for an ordinary customer service agent to close the loop on.\n<\\intent_2>\n<intent_3>\nI need the issue escalated and the record kept.\n<\\intent_3>\n<intent_4>\nPlease directly transfer me to a specialist for follow-up.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_006'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_006', 'order_id': '31006000001', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_006', 'order_id': '31006000001'}),
            ],
        ),
    ),
    Task(
        annotator="plus_020",
        user_id="cnjd_cloth_007",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first check the current status of order 31007000003.\n<\\intent_1>\n<intent_2>\nThen look at the logistics progress and the estimated delivery of order 31007000003.\n<\\intent_2>\n<intent_3>\nAlso tell me whether there are any discounts available at the moment.\n<\\intent_3>\n<intent_4>\nIf the conditions are met, please directly expedite order 31007000003 for me.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_007', 'order_id': '31007000003'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_007', 'order_id': '31007000003', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_007', 'order_id': '31007000003'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
            ],
        ),
    ),
    Task(
        annotator="plus_021",
        user_id="cnjd_cloth_008",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nDocumentation-and-compliance-oriented consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Steady mood, but demands high accuracy of fields.</emotion>\n<meticulousness>Very high; will check the invoice title and phone number item by item.</meticulousness>\n<patience>Medium-to-high; can cooperate with verification.</patience>\n<trust>Medium; accepts the process but requires it to be traceable.</trust>\n<awareness_of_rights>Medium-to-high; values leaving a paper trail.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the order and identity information first, then asks for the invoice.</questioning_style>\n<speaking_style>Leans toward formal written expression, field-oriented.</speaking_style>\n<communication_pace>Confirms item by item, does not skip fields.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first check the status of order 31008000001 and confirm that an invoice can be issued.\n<\\intent_1>\n<intent_2>\nI will not repeat my name and phone number; please verify them from the system first.\n<\\intent_2>\n<intent_3>\nAfter verification, please issue a corporate invoice directly.\n<\\intent_3>\n<intent_4>\nAnd return the invoice title and contact phone number.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_invoice", arguments={'title': 'Xingchuan Apparel Trading Co., Ltd.', 'order_id': '31008000001', 'phone_number': '13900010008', 'invoice_type': 'corporate_invoice'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_008', 'order_id': '31008000001', 'action': 'query'}),
                Search(name="get_user_info_tool", arguments={'user_id': 'cnjd_cloth_008'}),
            ],
        ),
    ),
    Task(
        annotator="plus_022",
        user_id="cnjd_cloth_005",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare the impact of the core differences between products 100910000009 and 100910000010.\n<\\intent_1>\n<intent_2>\nThen check the status and logistics of order 31005000003.\n<\\intent_2>\n<intent_3>\nAdd the current discount and free-gift information, and explain whether they can be stacked.\n<\\intent_3>\n<intent_4>\nThen verify the E-card balance and the applicable rules.\n<\\intent_4>\n<intent_5>\nPlease directly expedite order 31005000002 for me.\n<\\intent_5>\n<intent_6>\nAnd directly issue a personal invoice for order 31005000002 based on the system information.\n<\\intent_6>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_005'}),
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_005', 'order_id': '31005000002'}),
                Action(name="manage_invoice", arguments={'title': 'Apparel User 5', 'order_id': '31005000002', 'phone_number': '13900010005', 'invoice_type': 'personal_invoice'}),
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['100910000009', '100910000010']}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_005', 'order_id': '31005000003', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_005', 'order_id': '31005000003'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '100910000009'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_cloth_005', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
    Task(
        annotator="plus_023",
        user_id="cnjd_cloth_006",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare the impact of the core differences between products 100910000011 and 100910000012.\n<\\intent_1>\n<intent_2>\nThen check the status and logistics of order 31006000001.\n<\\intent_2>\n<intent_3>\nAdd the current discount and free-gift information, and explain whether they can be stacked.\n<\\intent_3>\n<intent_4>\nThen verify the E-card balance and the applicable rules.\n<\\intent_4>\n<intent_5>\nPlease directly expedite order 31006000003 for me.\n<\\intent_5>\n<intent_6>\nAnd directly initiate a return for order 31006000001.\n<\\intent_6>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_006'}),
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_006', 'order_id': '31006000003'}),
                Action(name="manage_return", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_006', 'order_id': '31006000001'}),
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['100910000011', '100910000012']}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_006', 'order_id': '31006000001', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_006', 'order_id': '31006000001'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '100910000011'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_cloth_006', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
    Task(
        annotator="plus_024",
        user_id="cnjd_cloth_007",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare the impact of the core differences between products 100910000013 and 100910000014.\n<\\intent_1>\n<intent_2>\nThen check the status and logistics of order 31007000002.\n<\\intent_2>\n<intent_3>\nAdd the current discount and free-gift information, and explain whether they can be stacked.\n<\\intent_3>\n<intent_4>\nThen verify the E-card balance and the applicable rules.\n<\\intent_4>\n<intent_5>\nPlease directly expedite order 31007000001 for me.\n<\\intent_5>\n<intent_6>\nAnd directly exchange 100910000001 in order 31007000003 for 100910000002.\n<\\intent_6>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_007'}),
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_007', 'order_id': '31007000001'}),
                Action(name="manage_exchange", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_007', 'order_id': '31007000003', 'original_product_id': '100910000001', 'exchange_product_id': '100910000002', 'action': 'exchange'}),
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['100910000013', '100910000014']}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_007', 'order_id': '31007000002', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_007', 'order_id': '31007000002'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '100910000013'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_cloth_007', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
    Task(
        annotator="plus_025",
        user_id="cnjd_cloth_008",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare the impact of the core differences between products 100910000015 and 100910000016.\n<\\intent_1>\n<intent_2>\nThen check the status and logistics of order 31008000003.\n<\\intent_2>\n<intent_3>\nAdd the current discount and free-gift information, and explain whether they can be stacked.\n<\\intent_3>\n<intent_4>\nThen verify the E-card balance and the applicable rules.\n<\\intent_4>\n<intent_5>\nPlease directly expedite order 31008000003 for me.\n<\\intent_5>\n<intent_6>\nAnd directly transfer the anomaly to a specialist for handling.\n<\\intent_6>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_008', 'order_id': '31008000003'}),
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_008'}),
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['100910000015', '100910000016']}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_008', 'order_id': '31008000003', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_008', 'order_id': '31008000003'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '100910000015'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_cloth_008', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
    Task(
        annotator="plus_026",
        user_id="cnjd_cloth_009",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare the impact of the core differences between products 100910000017 and 100910000018.\n<\\intent_1>\n<intent_2>\nThen check the status and logistics of order 31009000001.\n<\\intent_2>\n<intent_3>\nAdd the current discount and free-gift information, and explain whether they can be stacked.\n<\\intent_3>\n<intent_4>\nThen verify the E-card balance and the applicable rules.\n<\\intent_4>\n<intent_5>\nPlease directly expedite order 31009000003 for me.\n<\\intent_5>\n<intent_6>\nAnd directly issue a personal invoice for order 31009000003 based on the system information.\n<\\intent_6>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_009'}),
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_009', 'order_id': '31009000003'}),
                Action(name="manage_invoice", arguments={'title': 'Apparel User 9', 'order_id': '31009000003', 'phone_number': '13900010009', 'invoice_type': 'personal_invoice'}),
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['100910000017', '100910000018']}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_009', 'order_id': '31009000001', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_009', 'order_id': '31009000001'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '100910000017'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_cloth_009', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
    Task(
        annotator="plus_027",
        user_id="cnjd_cloth_010",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare the impact of the core differences between products 100910000001 and 100910000002.\n<\\intent_1>\n<intent_2>\nThen check the status and logistics of order 31010000001.\n<\\intent_2>\n<intent_3>\nAdd the current discount and free-gift information, and explain whether they can be stacked.\n<\\intent_3>\n<intent_4>\nThen verify the E-card balance and the applicable rules.\n<\\intent_4>\n<intent_5>\nPlease directly expedite order 31010000001 for me.\n<\\intent_5>\n<intent_6>\nAnd directly initiate a return for order 31010000002.\n<\\intent_6>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_010'}),
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_010', 'order_id': '31010000001'}),
                Action(name="manage_return", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_010', 'order_id': '31010000002'}),
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['100910000001', '100910000002']}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_010', 'order_id': '31010000001', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_010', 'order_id': '31010000001'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '100910000001'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_cloth_010', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
    Task(
        annotator="plus_028",
        user_id="cnjd_cloth_001",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare the impact of the core differences between products 100910000003 and 100910000004.\n<\\intent_1>\n<intent_2>\nThen check the status and logistics of order 31001000003.\n<\\intent_2>\n<intent_3>\nAdd the current discount and free-gift information, and explain whether they can be stacked.\n<\\intent_3>\n<intent_4>\nThen verify the E-card balance and the applicable rules.\n<\\intent_4>\n<intent_5>\nPlease directly expedite order 31001000002 for me.\n<\\intent_5>\n<intent_6>\nAnd directly exchange 100910000004 in order 31001000001 for 100910000003.\n<\\intent_6>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_001'}),
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_001', 'order_id': '31001000002'}),
                Action(name="manage_exchange", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_001', 'order_id': '31001000001', 'original_product_id': '100910000004', 'exchange_product_id': '100910000003', 'action': 'exchange'}),
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['100910000003', '100910000004']}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_001', 'order_id': '31001000003', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_001', 'order_id': '31001000003'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '100910000003'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_cloth_001', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
    Task(
        annotator="plus_029",
        user_id="cnjd_cloth_002",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare the impact of the core differences between products 100910000005 and 100910000006.\n<\\intent_1>\n<intent_2>\nThen check the status and logistics of order 31002000001.\n<\\intent_2>\n<intent_3>\nAdd the current discount and free-gift information, and explain whether they can be stacked.\n<\\intent_3>\n<intent_4>\nThen verify the E-card balance and the applicable rules.\n<\\intent_4>\n<intent_5>\nPlease directly expedite order 31002000001 for me.\n<\\intent_5>\n<intent_6>\nAnd directly transfer the anomaly to a specialist for handling.\n<\\intent_6>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_002', 'order_id': '31002000001'}),
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_002'}),
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['100910000005', '100910000006']}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_002', 'order_id': '31002000001', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_cloth_002', 'order_id': '31002000001'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '100910000005'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_cloth_002', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
    Task(
        annotator="plus_030",
        user_id="cnjd_food_001",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nRational-comparison consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Steady mood; focused on completeness of information.</emotion>\n<meticulousness>Very high; will verify specifications and after-sales boundaries.</meticulousness>\n<patience>Medium-to-high; willing to confirm step by step.</patience>\n<trust>Medium; accepts suggestions but requires them to be grounded.</trust>\n<awareness_of_rights>Medium; prefers to confirm before deciding.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Asks about the differences first, then whether they fit their own needs.</questioning_style>\n<speaking_style>Clear and well-organized; tends toward rational expression.</speaking_style>\n<communication_pace>Advances step by step and does not skip steps.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first compare the differences between products 200910000015 and 200910000016 in terms of applicable scenarios, specifications and after-sales boundaries.\n<\\intent_1>\n<intent_2>\nThen explain the return and exchange rules for this category of products; I will make the decision first and do not need any action taken for now.\n<\\intent_2>\n',
        metadata=Validation(
            outputs=[],
            actions=[
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['200910000015', '200910000016']}),
            ],
        ),
    ),
    Task(
        annotator="plus_031",
        user_id="cnjd_food_002",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst help me check the current status of order 32012000002.\n<\\intent_1>\n<intent_2>\nThen look at the logistics milestones and the estimated delivery of order 32012000001; I just want to understand the situation first and will not take any action.\n<\\intent_2>\n<intent_3>\nIf there is a risk of delay, please alert me.\n<\\intent_3>\n',
        metadata=Validation(
            outputs=[],
            actions=[
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_002', 'order_id': '32012000002', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_002', 'order_id': '32012000001'}),
            ],
        ),
    ),
    Task(
        annotator="plus_032",
        user_id="cnjd_food_003",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nRational-comparison consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Steady mood; focused on completeness of information.</emotion>\n<meticulousness>Very high; will verify specifications and after-sales boundaries.</meticulousness>\n<patience>Medium-to-high; willing to confirm step by step.</patience>\n<trust>Medium; accepts suggestions but requires them to be grounded.</trust>\n<awareness_of_rights>Medium; prefers to confirm before deciding.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Asks about the differences first, then whether they fit their own needs.</questioning_style>\n<speaking_style>Clear and well-organized; tends toward rational expression.</speaking_style>\n<communication_pace>Advances step by step and does not skip steps.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare products 200910000002 and 200910000003.\n<\\intent_1>\n<intent_2>\nThen check the currently available discounts and free-gift information; for now do not perform any ordering or after-sales action.\n<\\intent_2>\n',
        metadata=Validation(
            outputs=[],
            actions=[
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['200910000002', '200910000003']}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '200910000002'}),
            ],
        ),
    ),
    Task(
        annotator="plus_033",
        user_id="cnjd_food_004",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nRational-comparison consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Steady mood; focused on completeness of information.</emotion>\n<meticulousness>Very high; will verify specifications and after-sales boundaries.</meticulousness>\n<patience>Medium-to-high; willing to confirm step by step.</patience>\n<trust>Medium; accepts suggestions but requires them to be grounded.</trust>\n<awareness_of_rights>Medium; prefers to confirm before deciding.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Asks about the differences first, then whether they fit their own needs.</questioning_style>\n<speaking_style>Clear and well-organized; tends toward rational expression.</speaking_style>\n<communication_pace>Advances step by step and does not skip steps.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first compare the differences between products 200910000004 and 200910000017 in terms of applicable scenarios, specifications and after-sales boundaries.\n<\\intent_1>\n<intent_2>\nThen explain the return and exchange rules for this category of products; I will make the decision first and do not need any action taken for now.\n<\\intent_2>\n',
        metadata=Validation(
            outputs=[],
            actions=[
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['200910000004', '200910000017']}),
            ],
        ),
    ),
    Task(
        annotator="plus_034",
        user_id="cnjd_food_005",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst help me check the current status of order 32015000002.\n<\\intent_1>\n<intent_2>\nThen look at the logistics milestones and the estimated delivery of order 32015000003; I just want to understand the situation first and will not take any action.\n<\\intent_2>\n<intent_3>\nIf there is a risk of delay, please alert me.\n<\\intent_3>\n',
        metadata=Validation(
            outputs=[],
            actions=[
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_005', 'order_id': '32015000002', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_005', 'order_id': '32015000003'}),
            ],
        ),
    ),
    Task(
        annotator="plus_035",
        user_id="cnjd_food_006",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nRational-comparison consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Steady mood; focused on completeness of information.</emotion>\n<meticulousness>Very high; will verify specifications and after-sales boundaries.</meticulousness>\n<patience>Medium-to-high; willing to confirm step by step.</patience>\n<trust>Medium; accepts suggestions but requires them to be grounded.</trust>\n<awareness_of_rights>Medium; prefers to confirm before deciding.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Asks about the differences first, then whether they fit their own needs.</questioning_style>\n<speaking_style>Clear and well-organized; tends toward rational expression.</speaking_style>\n<communication_pace>Advances step by step and does not skip steps.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare products 200910000009 and 200910000010.\n<\\intent_1>\n<intent_2>\nThen check the currently available discounts and free-gift information; for now do not perform any ordering or after-sales action.\n<\\intent_2>\n',
        metadata=Validation(
            outputs=[],
            actions=[
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['200910000009', '200910000010']}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '200910000009'}),
            ],
        ),
    ),
    Task(
        annotator="plus_036",
        user_id="cnjd_food_003",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first check the current status of order 32013000001.\n<\\intent_1>\n<intent_2>\nThen look at the logistics progress and the estimated delivery of order 32013000001.\n<\\intent_2>\n<intent_3>\nAlso tell me whether there are any discounts available at the moment.\n<\\intent_3>\n<intent_4>\nIf the conditions are met, please directly expedite order 32013000001 for me.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_003', 'order_id': '32013000001'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_003', 'order_id': '32013000001', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_003', 'order_id': '32013000001'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
            ],
        ),
    ),
    Task(
        annotator="plus_037",
        user_id="cnjd_food_004",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first confirm whether order 32014000003 is still in a cancellable state.\n<\\intent_1>\n<intent_2>\nThen check whether the coupon can still be used after cancellation.\n<\\intent_2>\n<intent_3>\nIf it can still be cancelled, please directly cancel order 32014000003 for me.\n<\\intent_3>\n<intent_4>\nGive me a receipt after the cancellation is complete.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_order", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_004', 'order_id': '32014000003', 'action': 'cancel'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_004', 'order_id': '32014000003', 'action': 'query'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
            ],
        ),
    ),
    Task(
        annotator="plus_038",
        user_id="cnjd_food_005",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nDocumentation-and-compliance-oriented consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Steady mood, but demands high accuracy of fields.</emotion>\n<meticulousness>Very high; will check the invoice title and phone number item by item.</meticulousness>\n<patience>Medium-to-high; can cooperate with verification.</patience>\n<trust>Medium; accepts the process but requires it to be traceable.</trust>\n<awareness_of_rights>Medium-to-high; values leaving a paper trail.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the order and identity information first, then asks for the invoice.</questioning_style>\n<speaking_style>Leans toward formal written expression, field-oriented.</speaking_style>\n<communication_pace>Confirms item by item, does not skip fields.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first check the status of order 32015000003 and confirm that an invoice can be issued.\n<\\intent_1>\n<intent_2>\nI will not repeat my name and phone number; please verify them from the system first.\n<\\intent_2>\n<intent_3>\nAfter verification, please issue a personal invoice directly.\n<\\intent_3>\n<intent_4>\nAnd return the invoice title and contact phone number.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_invoice", arguments={'title': 'Food User 5', 'order_id': '32015000003', 'phone_number': '13800020005', 'invoice_type': 'personal_invoice'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_005', 'order_id': '32015000003', 'action': 'query'}),
                Search(name="get_user_info_tool", arguments={'user_id': 'cnjd_food_005'}),
            ],
        ),
    ),
    Task(
        annotator="plus_039",
        user_id="cnjd_food_006",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst check the current status and the return eligibility of order 32016000003.\n<\\intent_1>\n<intent_2>\nThen confirm the return process and the time required.\n<\\intent_2>\n<intent_3>\nI have confirmed I want to return it; please directly initiate the return of order 32016000003 for me.\n<\\intent_3>\n<intent_4>\nAnd explain whether refunding to the E-card is supported.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_return", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_006', 'order_id': '32016000003'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_006', 'order_id': '32016000003', 'action': 'query'}),
                Search(name="manage_return_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_006', 'order_id': '32016000003', 'action': 'query'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_food_006', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
    Task(
        annotator="plus_040",
        user_id="cnjd_food_007",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst check the product details of order 32017000001.\n<\\intent_1>\n<intent_2>\nI plan to exchange 200910000006 for 200910000003; first confirm the stock and the exchange rules.\n<\\intent_2>\n<intent_3>\nThen explain the expected turnaround time for the exchange.\n<\\intent_3>\n<intent_4>\nI confirm the exchange; please directly submit the exchange for order 32017000001.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_exchange", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_007', 'order_id': '32017000001', 'original_product_id': '200910000006', 'exchange_product_id': '200910000003', 'action': 'exchange'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_007', 'order_id': '32017000001', 'action': 'query'}),
                Search(name="get_product_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '200910000003'}),
                Search(name="manage_exchange_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_007', 'order_id': '32017000001', 'original_product_id': '200910000006', 'action': 'query'}),
            ],
        ),
    ),
    Task(
        annotator="plus_041",
        user_id="cnjd_food_008",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nDocumentation-and-compliance-oriented consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Steady mood, but demands high accuracy of fields.</emotion>\n<meticulousness>Very high; will check the invoice title and phone number item by item.</meticulousness>\n<patience>Medium-to-high; can cooperate with verification.</patience>\n<trust>Medium; accepts the process but requires it to be traceable.</trust>\n<awareness_of_rights>Medium-to-high; values leaving a paper trail.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the order and identity information first, then asks for the invoice.</questioning_style>\n<speaking_style>Leans toward formal written expression, field-oriented.</speaking_style>\n<communication_pace>Confirms item by item, does not skip fields.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst check my E-card balance.\n<\\intent_1>\n<intent_2>\nThen verify the amount and status of order 32018000003.\n<\\intent_2>\n<intent_3>\nIf the balance can cover it, please complete the payment directly with the E-card balance.\n<\\intent_3>\n<intent_4>\nAnd tell me how the balance changes after payment.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_ecard", arguments={'platform': 'jd', 'user_id': 'cnjd_food_008', 'action': 'use_balance', 'shop_id': 'xcat_shop_001', 'product_id': '200910000004', 'quantity': 1}),
            ],
            searches=[
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_food_008', 'action': 'Balance inquiry'}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_008', 'order_id': '32018000003', 'action': 'query'}),
                Search(name="get_user_info_tool", arguments={'user_id': 'cnjd_food_008'}),
            ],
        ),
    ),
    Task(
        annotator="plus_042",
        user_id="cnjd_food_009",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst check the status and the logistics track of order 32019000002.\n<\\intent_1>\n<intent_2>\nThen explain why the current problem is hard for an ordinary customer service agent to close the loop on.\n<\\intent_2>\n<intent_3>\nI need the issue escalated and the record kept.\n<\\intent_3>\n<intent_4>\nPlease directly transfer me to a specialist for follow-up.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_009'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_009', 'order_id': '32019000002', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_009', 'order_id': '32019000002'}),
            ],
        ),
    ),
    Task(
        annotator="plus_043",
        user_id="cnjd_food_010",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first check the current status of order 32020000003.\n<\\intent_1>\n<intent_2>\nThen look at the logistics progress and the estimated delivery of order 32020000003.\n<\\intent_2>\n<intent_3>\nAlso tell me whether there are any discounts available at the moment.\n<\\intent_3>\n<intent_4>\nIf the conditions are met, please directly expedite order 32020000003 for me.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_010', 'order_id': '32020000003'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_010', 'order_id': '32020000003', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_010', 'order_id': '32020000003'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
            ],
        ),
    ),
    Task(
        annotator="plus_044",
        user_id="cnjd_food_001",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first confirm whether order 32011000003 is still in a cancellable state.\n<\\intent_1>\n<intent_2>\nThen check whether the coupon can still be used after cancellation.\n<\\intent_2>\n<intent_3>\nIf it can still be cancelled, please directly cancel order 32011000003 for me.\n<\\intent_3>\n<intent_4>\nGive me a receipt after the cancellation is complete.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_order", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_001', 'order_id': '32011000003', 'action': 'cancel'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_001', 'order_id': '32011000003', 'action': 'query'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
            ],
        ),
    ),
    Task(
        annotator="plus_045",
        user_id="cnjd_food_002",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nDocumentation-and-compliance-oriented consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Steady mood, but demands high accuracy of fields.</emotion>\n<meticulousness>Very high; will check the invoice title and phone number item by item.</meticulousness>\n<patience>Medium-to-high; can cooperate with verification.</patience>\n<trust>Medium; accepts the process but requires it to be traceable.</trust>\n<awareness_of_rights>Medium-to-high; values leaving a paper trail.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the order and identity information first, then asks for the invoice.</questioning_style>\n<speaking_style>Leans toward formal written expression, field-oriented.</speaking_style>\n<communication_pace>Confirms item by item, does not skip fields.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first check the status of order 32012000002 and confirm that an invoice can be issued.\n<\\intent_1>\n<intent_2>\nI will not repeat my name and phone number; please verify them from the system first.\n<\\intent_2>\n<intent_3>\nAfter verification, please issue a corporate invoice directly.\n<\\intent_3>\n<intent_4>\nAnd return the invoice title and contact phone number.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_invoice", arguments={'title': 'Zehe Food Supply Chain Co., Ltd.', 'order_id': '32012000002', 'phone_number': '13800020002', 'invoice_type': 'corporate_invoice'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_002', 'order_id': '32012000002', 'action': 'query'}),
                Search(name="get_user_info_tool", arguments={'user_id': 'cnjd_food_002'}),
            ],
        ),
    ),
    Task(
        annotator="plus_046",
        user_id="cnjd_food_003",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst check the current status and the return eligibility of order 32013000001.\n<\\intent_1>\n<intent_2>\nThen confirm the return process and the time required.\n<\\intent_2>\n<intent_3>\nI have confirmed I want to return it; please directly initiate the return of order 32013000001 for me.\n<\\intent_3>\n<intent_4>\nAnd explain whether refunding to the E-card is supported.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_return", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_003', 'order_id': '32013000001'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_003', 'order_id': '32013000001', 'action': 'query'}),
                Search(name="manage_return_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_003', 'order_id': '32013000001', 'action': 'query'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_food_003', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
    Task(
        annotator="plus_047",
        user_id="cnjd_food_004",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst check the product details of order 32014000003.\n<\\intent_1>\n<intent_2>\nI plan to exchange 200910000008 for 200910000018; first confirm the stock and the exchange rules.\n<\\intent_2>\n<intent_3>\nThen explain the expected turnaround time for the exchange.\n<\\intent_3>\n<intent_4>\nI confirm the exchange; please directly submit the exchange for order 32014000003.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_exchange", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_004', 'order_id': '32014000003', 'original_product_id': '200910000008', 'exchange_product_id': '200910000018', 'action': 'exchange'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_004', 'order_id': '32014000003', 'action': 'query'}),
                Search(name="get_product_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '200910000018'}),
                Search(name="manage_exchange_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_004', 'order_id': '32014000003', 'original_product_id': '200910000008', 'action': 'query'}),
            ],
        ),
    ),
    Task(
        annotator="plus_048",
        user_id="cnjd_food_005",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nDocumentation-and-compliance-oriented consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Steady mood, but demands high accuracy of fields.</emotion>\n<meticulousness>Very high; will check the invoice title and phone number item by item.</meticulousness>\n<patience>Medium-to-high; can cooperate with verification.</patience>\n<trust>Medium; accepts the process but requires it to be traceable.</trust>\n<awareness_of_rights>Medium-to-high; values leaving a paper trail.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the order and identity information first, then asks for the invoice.</questioning_style>\n<speaking_style>Leans toward formal written expression, field-oriented.</speaking_style>\n<communication_pace>Confirms item by item, does not skip fields.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst check my E-card balance.\n<\\intent_1>\n<intent_2>\nThen verify the amount and status of order 32015000001.\n<\\intent_2>\n<intent_3>\nIf the balance can cover it, please complete the payment directly with the E-card balance.\n<\\intent_3>\n<intent_4>\nAnd tell me how the balance changes after payment.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_ecard", arguments={'platform': 'jd', 'user_id': 'cnjd_food_005', 'action': 'use_balance', 'shop_id': 'xcat_shop_001', 'product_id': '200910000002', 'quantity': 1}),
            ],
            searches=[
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_food_005', 'action': 'Balance inquiry'}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_005', 'order_id': '32015000001', 'action': 'query'}),
                Search(name="get_user_info_tool", arguments={'user_id': 'cnjd_food_005'}),
            ],
        ),
    ),
    Task(
        annotator="plus_049",
        user_id="cnjd_food_006",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst check the status and the logistics track of order 32016000003.\n<\\intent_1>\n<intent_2>\nThen explain why the current problem is hard for an ordinary customer service agent to close the loop on.\n<\\intent_2>\n<intent_3>\nI need the issue escalated and the record kept.\n<\\intent_3>\n<intent_4>\nPlease directly transfer me to a specialist for follow-up.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_006'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_006', 'order_id': '32016000003', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_006', 'order_id': '32016000003'}),
            ],
        ),
    ),
    Task(
        annotator="plus_050",
        user_id="cnjd_food_007",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first check the current status of order 32017000003.\n<\\intent_1>\n<intent_2>\nThen look at the logistics progress and the estimated delivery of order 32017000003.\n<\\intent_2>\n<intent_3>\nAlso tell me whether there are any discounts available at the moment.\n<\\intent_3>\n<intent_4>\nIf the conditions are met, please directly expedite order 32017000003 for me.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_007', 'order_id': '32017000003'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_007', 'order_id': '32017000003', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_007', 'order_id': '32017000003'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
            ],
        ),
    ),
    Task(
        annotator="plus_051",
        user_id="cnjd_food_008",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nDocumentation-and-compliance-oriented consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Steady mood, but demands high accuracy of fields.</emotion>\n<meticulousness>Very high; will check the invoice title and phone number item by item.</meticulousness>\n<patience>Medium-to-high; can cooperate with verification.</patience>\n<trust>Medium; accepts the process but requires it to be traceable.</trust>\n<awareness_of_rights>Medium-to-high; values leaving a paper trail.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the order and identity information first, then asks for the invoice.</questioning_style>\n<speaking_style>Leans toward formal written expression, field-oriented.</speaking_style>\n<communication_pace>Confirms item by item, does not skip fields.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nPlease first check the status of order 32018000003 and confirm that an invoice can be issued.\n<\\intent_1>\n<intent_2>\nI will not repeat my name and phone number; please verify them from the system first.\n<\\intent_2>\n<intent_3>\nAfter verification, please issue a corporate invoice directly.\n<\\intent_3>\n<intent_4>\nAnd return the invoice title and contact phone number.\n<\\intent_4>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_invoice", arguments={'title': 'Zehe Food Supply Chain Co., Ltd.', 'order_id': '32018000003', 'phone_number': '13800020008', 'invoice_type': 'corporate_invoice'}),
            ],
            searches=[
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_008', 'order_id': '32018000003', 'action': 'query'}),
                Search(name="get_user_info_tool", arguments={'user_id': 'cnjd_food_008'}),
            ],
        ),
    ),
    Task(
        annotator="plus_052",
        user_id="cnjd_food_005",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare the impact of the core differences between products 200910000012 and 200910000013.\n<\\intent_1>\n<intent_2>\nThen check the status and logistics of order 32015000003.\n<\\intent_2>\n<intent_3>\nAdd the current discount and free-gift information, and explain whether they can be stacked.\n<\\intent_3>\n<intent_4>\nThen verify the E-card balance and the applicable rules.\n<\\intent_4>\n<intent_5>\nPlease directly expedite order 32015000002 for me.\n<\\intent_5>\n<intent_6>\nAnd directly issue a personal invoice for order 32015000002 based on the system information.\n<\\intent_6>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_005'}),
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_005', 'order_id': '32015000002'}),
                Action(name="manage_invoice", arguments={'title': 'Food User 5', 'order_id': '32015000002', 'phone_number': '13800020005', 'invoice_type': 'personal_invoice'}),
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['200910000012', '200910000013']}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_005', 'order_id': '32015000003', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_005', 'order_id': '32015000003'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '200910000012'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_food_005', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
    Task(
        annotator="plus_053",
        user_id="cnjd_food_006",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare the impact of the core differences between products 200910000007 and 200910000008.\n<\\intent_1>\n<intent_2>\nThen check the status and logistics of order 32016000001.\n<\\intent_2>\n<intent_3>\nAdd the current discount and free-gift information, and explain whether they can be stacked.\n<\\intent_3>\n<intent_4>\nThen verify the E-card balance and the applicable rules.\n<\\intent_4>\n<intent_5>\nPlease directly expedite order 32016000001 for me.\n<\\intent_5>\n<intent_6>\nAnd directly initiate a return for order 32016000003.\n<\\intent_6>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_006'}),
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_006', 'order_id': '32016000001'}),
                Action(name="manage_return", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_006', 'order_id': '32016000003'}),
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['200910000007', '200910000008']}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_006', 'order_id': '32016000001', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_006', 'order_id': '32016000001'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '200910000007'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_food_006', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
    Task(
        annotator="plus_054",
        user_id="cnjd_food_007",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare the impact of the core differences between products 200910000015 and 200910000016.\n<\\intent_1>\n<intent_2>\nThen check the status and logistics of order 32017000002.\n<\\intent_2>\n<intent_3>\nAdd the current discount and free-gift information, and explain whether they can be stacked.\n<\\intent_3>\n<intent_4>\nThen verify the E-card balance and the applicable rules.\n<\\intent_4>\n<intent_5>\nPlease directly expedite order 32017000001 for me.\n<\\intent_5>\n<intent_6>\nAnd directly exchange 200910000006 in order 32017000001 for 200910000016.\n<\\intent_6>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_007'}),
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_007', 'order_id': '32017000001'}),
                Action(name="manage_exchange", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_007', 'order_id': '32017000001', 'original_product_id': '200910000006', 'exchange_product_id': '200910000016', 'action': 'exchange'}),
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['200910000015', '200910000016']}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_007', 'order_id': '32017000002', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_007', 'order_id': '32017000002'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '200910000015'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_food_007', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
    Task(
        annotator="plus_055",
        user_id="cnjd_food_009",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare the impact of the core differences between products 200910000011 and 200910000018.\n<\\intent_1>\n<intent_2>\nThen check the status and logistics of order 32019000003.\n<\\intent_2>\n<intent_3>\nAdd the current discount and free-gift information, and explain whether they can be stacked.\n<\\intent_3>\n<intent_4>\nThen verify the E-card balance and the applicable rules.\n<\\intent_4>\n<intent_5>\nPlease directly expedite order 32019000002 for me.\n<\\intent_5>\n<intent_6>\nAnd directly transfer the anomaly to a specialist for handling.\n<\\intent_6>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_009', 'order_id': '32019000002'}),
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_009'}),
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['200910000011', '200910000018']}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_009', 'order_id': '32019000003', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_009', 'order_id': '32019000003'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '200910000011'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_food_009', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
    Task(
        annotator="plus_056",
        user_id="cnjd_food_010",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare the impact of the core differences between products 200910000002 and 200910000003.\n<\\intent_1>\n<intent_2>\nThen check the status and logistics of order 32020000003.\n<\\intent_2>\n<intent_3>\nAdd the current discount and free-gift information, and explain whether they can be stacked.\n<\\intent_3>\n<intent_4>\nThen verify the E-card balance and the applicable rules.\n<\\intent_4>\n<intent_5>\nPlease directly expedite order 32020000003 for me.\n<\\intent_5>\n<intent_6>\nAnd directly issue a personal invoice for order 32020000001 based on the system information.\n<\\intent_6>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_010'}),
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_010', 'order_id': '32020000003'}),
                Action(name="manage_invoice", arguments={'title': 'Food User 10', 'order_id': '32020000001', 'phone_number': '13800020010', 'invoice_type': 'personal_invoice'}),
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['200910000002', '200910000003']}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_010', 'order_id': '32020000003', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_010', 'order_id': '32020000003'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '200910000002'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_food_010', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
    Task(
        annotator="plus_057",
        user_id="cnjd_food_001",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare the impact of the core differences between products 200910000004 and 200910000017.\n<\\intent_1>\n<intent_2>\nThen check the status and logistics of order 32011000002.\n<\\intent_2>\n<intent_3>\nAdd the current discount and free-gift information, and explain whether they can be stacked.\n<\\intent_3>\n<intent_4>\nThen verify the E-card balance and the applicable rules.\n<\\intent_4>\n<intent_5>\nPlease directly expedite order 32011000001 for me.\n<\\intent_5>\n<intent_6>\nAnd directly initiate a return for order 32011000001.\n<\\intent_6>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_001'}),
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_001', 'order_id': '32011000001'}),
                Action(name="manage_return", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_001', 'order_id': '32011000001'}),
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['200910000004', '200910000017']}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_001', 'order_id': '32011000002', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_001', 'order_id': '32011000002'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '200910000004'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_food_001', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
    Task(
        annotator="plus_058",
        user_id="cnjd_food_003",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nTime-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Under obvious time pressure; tone is on the urgent side.</emotion>\n<meticulousness>Medium-to-high; will repeatedly confirm milestone times.</meticulousness>\n<patience>Medium; willing to cooperate but does not want to wait long.</patience>\n<trust>Medium-to-low; needs clear commitments.</trust>\n<awareness_of_rights>Medium; mainly focused on the outcome of execution.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Checks progress first, then demands immediate action.</questioning_style>\n<speaking_style>Expresses things directly; focuses on asking when it will be done.</speaking_style>\n<communication_pace>Continuously presses on the key milestones.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare the impact of the core differences between products 200910000001 and 200910000014.\n<\\intent_1>\n<intent_2>\nThen check the status and logistics of order 32013000003.\n<\\intent_2>\n<intent_3>\nAdd the current discount and free-gift information, and explain whether they can be stacked.\n<\\intent_3>\n<intent_4>\nThen verify the E-card balance and the applicable rules.\n<\\intent_4>\n<intent_5>\nPlease directly expedite order 32013000002 for me.\n<\\intent_5>\n<intent_6>\nAnd directly exchange 200910000018 in order 32013000001 for 200910000014.\n<\\intent_6>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_003'}),
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_003', 'order_id': '32013000002'}),
                Action(name="manage_exchange", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_003', 'order_id': '32013000001', 'original_product_id': '200910000018', 'exchange_product_id': '200910000014', 'action': 'exchange'}),
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['200910000001', '200910000014']}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_003', 'order_id': '32013000003', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_003', 'order_id': '32013000003'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '200910000001'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_food_003', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
    Task(
        annotator="plus_059",
        user_id="cnjd_food_004",
        shop_id=shop_id,
        platform=platform,
        instruction='\n\n### This is your profile:\n<consumer_type>\nAfter-sales-rights-protection consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Sensitive to anomalies, firm in attitude.</emotion>\n<meticulousness>High; focuses on the boundary of responsibility and the chain of evidence.</meticulousness>\n<patience>Medium; wants everything explained clearly in one go.</patience>\n<trust>On the low side; worries about being fobbed off.</trust>\n<awareness_of_rights>High; emphasizes handling things according to the rules.</awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Verifies the facts first, then raises clear demands for action.</questioning_style>\n<speaking_style>Direct wording; emphasizes platform rules.</speaking_style>\n<communication_pace>Advances in three steps: problem—evidence—demand.</communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nFirst compare the impact of the core differences between products 200910000009 and 200910000010.\n<\\intent_1>\n<intent_2>\nThen check the status and logistics of order 32014000001.\n<\\intent_2>\n<intent_3>\nAdd the current discount and free-gift information, and explain whether they can be stacked.\n<\\intent_3>\n<intent_4>\nThen verify the E-card balance and the applicable rules.\n<\\intent_4>\n<intent_5>\nPlease directly expedite order 32014000003 for me.\n<\\intent_5>\n<intent_6>\nAnd directly transfer the anomaly to a specialist for handling.\n<\\intent_6>\n',
        metadata=Validation(
            outputs=[],
            actions=[
                Action(name="manage_urgent", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_004', 'order_id': '32014000003'}),
                Action(name="transfer_to_specialist", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_004'}),
            ],
            searches=[
                Search(name="compare_products_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_ids': ['200910000009', '200910000010']}),
                Search(name="manage_order_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_004', 'order_id': '32014000001', 'action': 'query'}),
                Search(name="get_logistics_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'user_id': 'cnjd_food_004', 'order_id': '32014000001'}),
                Search(name="get_discount_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001'}),
                Search(name="get_gift_info_tool", arguments={'platform': 'jd', 'shop_id': 'xcat_shop_001', 'product_id': '200910000009'}),
                Search(name="manage_ecard_tool", arguments={'platform': 'jd', 'user_id': 'cnjd_food_004', 'action': 'Balance inquiry'}),
            ],
        ),
    ),
]
