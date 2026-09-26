from utils import Task, Action, Search, Validation, ProductInfo

ALL_TASKS = [
    Task(
        annotator='0',
        user_id='cnjd_user_05',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = "\n### This is your profile:\n\n<consumer_type>\nValue-sensitive customer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Slightly dissatisfied; gets somewhat angry during the conversation.<\\emotion>\n<meticulousness>Relatively high; will ask in detail about the specifics of the conversation.<\\meticulousness>\n<patience>Average; although showing eagerness, is willing to wait for the customer service agent's reply.<\\patience>\n<trust>Relatively low; doubts the current situation and needs confirmation.<\\trust>\n<awareness_of_rights>Relatively strong; cares a lot about the existing rules and regulations.<\\awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Direct and specific; usually points out the particular matters they care about directly.<\\questioning_style>\n<speaking_style>Uses concise and clear wording without much embellishment.<\\speaking_style>\n<communication_pace>Sends messages continuously, raising multiple questions within a short time, showing an eagerness to get the problem solved.<\\communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n\n<intent_1>\nYou bought a product: https://item.jd.com/100042754736.html?sdx=ehi-lLxFuJiE6JnIYIpei8AitzeRRHsgmjYZ4ukJEdyMdZnQK5xZ53jtoU8&sdx=ehi-lLxFuJiE6JnIYIpei8AitzeRRHsgmjYZ4ukJEdyMdZnQK5xY7njhp04, but the installation is extremely troublesome, and you complain about this to the customer service agent\n<\\intent_1>\n<intent_2>\nAfter that, you ask the customer service agent for an installation tutorial\n<\\intent_2>\n<intent_3>\nIn addition, you are about to travel, so you ask the customer service agent to send you the logistics information for order 313021098954 and to expedite it.\n<\\intent_3>\n<intent_4>\nAt the same time, you ask the customer service agent to check the status of order 313271663680\n<\\intent_4>\n<intent_5>\nIf it has not been shipped yet, you want to cancel the order\n<\\intent_5>\n<intent_6>\nFinally, you ask whether order 314231443863 already has a cashback record\n<\\intent_6>\n<intent_7>\nIf not, ask the customer service agent to verify the image https://dd-static.jd.com/ddimgp/jfs/t20260528/280781/10/25581/172166/6808a980F4fea4867/cf783a9a7acc8c2d.jpg\n<\\intent_7>\n<intent_8>\nIf the verification passes, register the cashback information\n<\\intent_8>\n"
,
        metadata= Validation(
            outputs=[],
            actions=[
                Action(
                name="manage_urgent",
                arguments={
                    "platform": "jd",
                    "shop_id": "5de650c946e7c3001814990f",
                    "user_id": 'cnjd_user_05',
                    "order_id": "313021098954"
                }
                ),
                Action(
                    name="manage_order",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_05',
                        "order_id": "313271663680",
                        "action": 'cancel'
                    }
                ),
                Action(
                    name="register_cashback_by_review",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_05',
                        "order_id": "314231443863",
                        "action": 'cashback'
                    }
                )
            ],
            searches=[
                Search(
                    name = 'get_logistics_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_05',
                        "order_id": "313021098954"
                    }
                ),
                Search(
                    name = 'get_installation_service_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100042754736"
                    }
                ),
                Search(
                    name = 'manage_order_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_05',
                        "order_id": "313271663680",
                        "action": 'query'
                    }
                ),
                Search(
                    name = 'register_cashback_by_review_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_05',
                        "order_id": "314231443863",
                        "action":'query'
                    }
                )
            ]
        )
    ),
    Task(
        annotator='1',
        user_id='cnjd_user_05',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = "\n\n### This is your profile:\n<consumer_type>\nValue-sensitive customer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Slightly dissatisfied; gets somewhat angry during the conversation.<\\emotion>\n<meticulousness>Relatively high; will ask in detail about the specifics of the conversation.<\\meticulousness>\n<patience>Average; although showing eagerness, is willing to wait for the customer service agent's reply.<\\patience>\n<trust>Relatively low; doubts the current situation and needs confirmation.<\\trust>\n<awareness_of_rights>Relatively strong; cares a lot about the existing rules and regulations.<\\awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Direct and specific; usually points out the particular matters they care about directly.<\\questioning_style>\n<speaking_style>Uses concise and clear wording without much embellishment.<\\speaking_style>\n<communication_pace>Sends messages continuously, raising multiple questions within a short time, showing an eagerness to get the problem solved.<\\communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nYou bought a product: https://item.jd.com/100112573625.html?sdx=ehi-lLxFuJiE6JnIYIpei8AitzeRRHsgmjYZ4ukJEdyMdZnQK5xZ53jtoU8&sdx=ehi-lLxFuJiE6JnIYIpei8AitzeRRHsgmjYZ4ukJEdyMdZnQK5xY7njhp04, but you realize it is too bulky, so you want to exchange it; the order is 313271663680\n<\\intent_1>\n<intent_2>\nYou ask the customer service agent which products can be used as replacements, and you want to replace it with a 60-liter water heater\n<\\intent_2>\n<intent_3>\nFinally, you want the shipment expedited.\n<\\intent_3>\n"
,
        metadata= Validation(
            outputs=[],
            actions=[
                Action(
                    name="manage_urgent",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_05',
                        "order_id": "313271663680"
                    }
                ),
                Action(
                    name="manage_exchange",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_05',
                        "order_id": "313271663680",
                        "original_product_id": "100112573625",
                        "exchange_product_id": "100112573624",
                        "action": 'exchange'
                    }
                )
            ],
            searches=[
                Search(
                    name = 'manage_exchange_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "order_id": "313271663680",
                        "user_id": 'cnjd_user_05',
                        "original_product_id": "100112573625",
                        "action": 'query'
                    }
                )
            ]
        )
    ),
    Task(
        annotator='2',
        user_id='cnjd_user_01',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = "\n\n\n### This is your profile:\n<consumer_type>\nPragmatic consumer.\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Calm; does not show strong mood swings or anger, but tends to understand and accept the customer service agent's explanations.<\\emotion>\n<meticulousness>Relatively high; will carefully track the outcome of every step of the operation.<\\meticulousness>\n<patience>Good; shows no impatience while waiting for the customer service agent to reply and is willing to cooperate with the relevant procedures.<\\patience>\n<trust>Relatively high; able to patiently listen to the customer service agent's suggestions and act on them.<\\trust>\n<awareness_of_rights>Moderate; will actively look for ways to solve the problem and proactively raises some requests.<\\awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Asks questions in a clear, well-organized and strongly logical way, able to clearly express the specific pieces of information they want to know.<\\questioning_style>\n<speaking_style>Polite and concise; uses many polite expressions but without excessive redundancy, and occasionally uses emojis to reinforce the tone<\\speaking_style>\n<communication_pace>After sending a query message, waits for the customer service agent's reply; does not follow up frequently and is not in a hurry for an immediate answer.<\\communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nYou want to ask whether order 316123105676 already has a cashback record\n<\\intent_1>\n<intent_2>\nIf not, you will send the image https://dd-static.jd.com/ddimgp/jfs/t20260624/314745/30/2272/65194/682bcb9dFf6f691d1/d0493c820d930acd.jpg to the customer service agent for verification\n<\\intent_2>\n<intent_3>\nBecause summer has arrived, you then want to ask whether the free gift for the product: https://item.jd.com/100112573619.html?sdx=ehi-lLxFuJiE6JnIYIpei8AitzeRRHsgmjYZ4ukJEdyMdZnQK5xZ53jtoU8&sdx=ehi-lLxFuJiE6JnIYIpei8AitzeRRHsgmjYZ4ukJEdyMdZnQK5xY7njhp04 includes an electric fan\n<\\intent_3>\n<intent_4>\nFinally, you want order 316123105676 to be expedited\n<\\intent_4>\n<intent_5>\nAt the same time, issue an invoice for this order, of the type personal invoice (note: you are forbidden to disclose your name and phone number to the customer service agent; if the agent asks you to provide them, have the agent look them up themselves)\n<\\intent_5>\n"
,
        
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name="manage_urgent",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_01',
                        "order_id": "316123105676"
                    }
                ),
                Action(
                    name="register_cashback_by_review",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_01',
                        "order_id": "316123105676",
                        "action": 'cashback'
                    }
                ),
                Action(
                    name="manage_invoice",
                    arguments={
                        "title":'Cao Rouhui',
                        "order_id": "316123105676",
                        "phone_number": "11213348266",
                        "invoice_type": 'personal_invoice',
                    }
                )
                ],
            searches=[
                Search(
                    name='register_cashback_by_review_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_01',
                        "order_id": "316123105676",
                        "action": 'query'
                    }
                ),
                Search(
                    name='get_gift_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100112573619"
                        }
                    )
            ]
        )
    ),
    Task(
        annotator='3',
        user_id="cnjd18463287301_p",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = '\n### This is your profile:\n<Consumer Type>\nRational consumer.\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Dissatisfied, feels very disappointed with the product.<\\Emotion>\n<Attentiveness>High, pays great attention to details.<\\Attentiveness>\n<Patience>Medium, willing to wait for customer service replies. But when the problem is not solved in time, begins to show anxiety and dissatisfaction and urges frequently<\\Patience>\n<Trust Level>Low; rather distrustful of customer service, holds a skeptical attitude toward the information customer service provides, and asks for confirmation many times.<\\Trust Level>\n<Awareness of Rights>High; when encountering unsatisfactory service, actively takes action to protect their own interests.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Fact-oriented combined with skepticism; asks some specific details and at the same time raises some doubts<\\Questioning Style>\n<Speaking Style>Direct and emotional; uses a fairly direct way of speaking, sometimes uses strongly emotionally coloured words to express dissatisfaction or emphasise their views, and tends to express their thoughts and feelings bluntly.<\\Speaking Style>\n<Communication Rhythm>Fast and tight; often sends several messages in a row to ask questions or report situations.<\\Communication Rhythm>\n<\\Behavioral Traits>\n\n### These are your goals:\n\n<Intent 1>\nYou are currently shopping, and you ask what the differences are among these products https://item.jd.com/100043059478.html, https://item.jd.com/100039032355.html?sdx=ehi-lLxFuJiE6JnIYYVZhcUguTOURHsgmjYZ4ukJEdyMdZnSL51b7n_lo0s, https://item.jd.com/100112573665.html\n<\\Intent 1>\n<Intent 2>\nBecause there were installation problems when you bought home appliances before, you will ask one by one about the installation process for these three products\n<\\Intent 2>\n<Intent 3>\nAfter that, you hope to buy a water heater specifically for the kitchen, and ask customer service to help place the order to buy this product\n<\\Intent 3>\n<Intent 4>\nThen, you hope to pay using your own ecard, and ask customer service to carry out the operation\n<\\Intent 4>\n<Intent 5>\nFinally, you hope to book the installation service, order ID: 1234567890, name Pan Wanqiu, phone 10080895692, time Sunday\n<\\Intent 5>\n'
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name="manage_order",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjd18463287301_p",
                        "action": 'add',
                        "payment": 'jd_ecard',
                        "product_info_list":[
                            ProductInfo(
                                product_id="100039032355",
                                quantity=1
                            )
                        ]
                    }
                ),
                Action(
                    name="manage_ecard",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjd18463287301_p",
                        "action": 'use_balance',
                        "product_id": "100039032355",
                        "quantity": 1
                    }
                ),
                Action(
                    name="schedule_service",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjd18463287301_p",
                        "order_id": "1234567890",
                        "user_name": 'Pan Wanqiu',
                        "phone_number": "10080895692",
                        "service_type": 'installation',
                        "service_time": 'Sunday'
                    }
                )
            ],
            searches=[
                Search(
                    name='compare_products_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_ids": ["100043059478", "100039032355", "100112573665"]
                    }
                ),
                Search(
                    name='get_installation_service_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100112573665"
                    }
                ),
                Search(
                    name='get_installation_service_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100043059478"
                    }
                ),
                Search(
                    name='get_installation_service_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100039032355"
                    }
                )
            ]
        )
    ),
    Task(
        annotator='4',
        user_id="cnjd18463287301_p",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = "\n\n\n### This is your profile:\n<consumer_type>\nRational consumer.\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Dissatisfied; feels very disappointed with the product.<\\emotion>\n<meticulousness>High; pays close attention to details.<\\meticulousness>\n<patience>Medium; willing to wait for the customer service agent's reply. But when the problem is not resolved in time, starts to show anxiety and dissatisfaction and urges the agent frequently<\\patience>\n<trust>Low; does not really trust the customer service agent, is skeptical about the information the agent provides, and repeatedly asks for confirmation.<\\trust>\n<awareness_of_rights>High; takes active action to protect their own interests when encountering unsatisfactory service.<\\awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Fact-oriented combined with skepticism; asks about specific details while also raising some doubts<\\questioning_style>\n<speaking_style>Direct and emotional; uses a fairly direct way of speaking, sometimes uses strongly emotional words to express dissatisfaction or emphasize their own point of view, and tends to state their thoughts and feelings bluntly.<\\speaking_style>\n<communication_pace>Fast and tight; often sends several messages in a row to ask questions or report on the situation.<\\communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n\n<intent_1>\nYou previously bought the product https://item.jd.com/100133171244.html and want to ask about repair service\n<\\intent_1>\n<intent_2>\nIn addition, you bought an angle valve yourself and want to ask the customer service agent whether this auxiliary material is needed\n<\\intent_2>\n<intent_3>\nBecause a home appliance you bought before had a problem with its installation, you also asked in detail about the installation process for https://item.jd.com/100133171244.html\n<\\intent_3>\n<intent_4>\nFinally, you want to book installation service, name Pan Wanqiu, phone 10080895692, time Sunday\n<\\intent_4>\n"
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name = 'schedule_service',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjd18463287301_p",
                        "order_id": "314415092676",
                        "user_name": 'Pan Wanqiu',
                        "phone_number": "10080895692",
                        "service_type": 'installation',
                        "service_time": 'Sunday'
                    }
                )
            ],
            searches=[
                Search(
                    name='get_repair_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100133171244"
                    }
                ),
                Search(
                    name='get_auxiliary_materials_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100133171244"
                    }
                ),
                Search(
                    name='get_installation_service_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100133171244"
                    }
                )
            ]
        )
    ),
    Task(
        annotator='5',
        user_id="cnjd18463287301_p",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = "\n\n\n### This is your profile:\n<consumer_type>\nRational consumer.\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Dissatisfied; feels very disappointed with the product.<\\emotion>\n<meticulousness>High; pays close attention to details.<\\meticulousness>\n<patience>Medium; willing to wait for the customer service agent's reply. But when the problem is not resolved in time, starts to show anxiety and dissatisfaction and urges the agent frequently<\\patience>\n<trust>Low; does not really trust the customer service agent, is skeptical about the information the agent provides, and repeatedly asks for confirmation.<\\trust>\n<awareness_of_rights>High; takes active action to protect their own interests when encountering unsatisfactory service.<\\awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Fact-oriented combined with skepticism; asks about specific details while also raising some doubts<\\questioning_style>\n<speaking_style>Direct and emotional; uses a fairly direct way of speaking, sometimes uses strongly emotional words to express dissatisfaction or emphasize their own point of view, and tends to state their thoughts and feelings bluntly.<\\speaking_style>\n<communication_pace>Fast and tight; often sends several messages in a row to ask questions or report on the situation.<\\communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n\n<intent_1>\nBecause the product 100138589935 you bought has an installation problem, you consult the customer service agent about the repair policy (note: you are only consulting and do not want to book a service. You are forbidden to disclose this information directly to the agent)\n<\\intent_1>\n<intent_2>\nFinally, you want to submit a return request for order 232400272153 and have the customer service agent do it for you.\n<\\intent_2>\n\n"
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name ='manage_return',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjd18463287301_p",
                        "order_id": "232400272153",
                    }
                ),
                Action(
                    name ='manage_ecard',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjd18463287301_p",
                        "action": 'refund',
                        "amount": 3999
                    }
                )
            ],
            searches=[
                Search(
                    name='get_repair_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100138589935"
                    }
                )
            ]
        )
    ),
    Task(
        annotator='6',
        user_id='cnjd_user_08',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = '\n### This is your profile:\n<consumer_type>\nValue-oriented type\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Calm; takes a fairly rational attitude to solving the problem.<\\emotion>\n<meticulousness>Very high; pays a lot of attention to product details.<\\meticulousness>\n<patience>Relatively high; when a situation requires waiting a while to know the result, shows no impatience or urging behavior.<\\patience>\n<trust>Relatively strong; trusts the information provided by the customer service agent and is willing to follow instructions until the problem is solved.<\\trust>\n<awareness_of_rights>Medium; proactively consults the customer service agent for relevant information and actively protects their own lawful rights and interests.<\\awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Direct and clear; asks questions directly without beating around the bush<\\questioning_style>\n<speaking_style>Concise and efficient; neither uses excessive polite language nor shows an overly familiar attitude<\\speaking_style>\n<communication_pace>Timely and moderate; stays silent to a certain degree while waiting for a reply, and only moves on to the next step after receiving a definite answer.<\\communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nYou previously bought a product whose original price was 2009 yuan, but now the price has dropped; you send a picture https://dd-static.jd.com/ddimgp/jfs/t20260623/297694/2/8257/158939/682a8a2aF3a87a48a/4c7eb1c5a42e8829.jpg to the customer service agent to prove that the product price has now dropped.\n<\\intent_1>\n<intent_2>\nBecause the price has dropped to 1707.65 yuan (you are forbidden to disclose the information that it is 1707.65 yuan to the customer service agent), you want to apply for price protection to get a partial refund, returning the loss caused by the price change to your JD.com E-card balance.\n<\\intent_2>\n<intent_3>\nThen, you want to book the installation service for this product, with the time set for Thursday.\n<\\intent_3>\n<intent_4>\nFinally, you want the customer service agent to issue an invoice for you, of the type personal invoice.\n<\\intent_4>\n'
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name="manage_ecard",
                    arguments={
                        "platform": "jd",
                        "user_id": 'cnjd_user_08',
                        "action": 'refund',
                        "amount": 301.35
                    }
                ),
                Action(
                    name="schedule_service",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_08',
                        "order_id": "314475833175",
                        "user_name": 'Lin Yunpei',
                        "phone_number": "13185436225",
                        "service_type": 'installation',
                        "service_time": 'Thursday'
                    }
                ),
                Action(
                    name="manage_invoice",
                    arguments={
                        "order_id": "314475833175",
                        "title": 'Lin Yunpei',
                        "phone_number": "13185436225",
                        "invoice_type": 'personal_invoice'
                    }
                )
            ],
            searches=[]
        )
    ),

    Task(
        annotator='7',
        user_id="cnjdwdnipzaorvgkymr",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = "\n\n### This is your profile:\n<consumer_type>\nPrice-and-quality-sensitive type\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Calm; shows no obvious dissatisfaction or impatience even while waiting for the customer service agent's reply.<\\emotion>\n<meticulousness>Relatively high; able to notice differences in details<\\meticulousness>\n<patience>Fairly good; can wait patiently when the customer service agent needs time to look things up.<\\patience>\n<trust>Average; will still press for details before obtaining specific information, showing a certain degree of trust but not complete reliance.<\\trust>\n<awareness_of_rights>Relatively strong; will actively fight for their own rights<\\awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Clear goals and highly practical; able to accurately express their questions and needs, and good at using concrete examples (such as screenshots) to help explain the issue<\\questioning_style>\n<speaking_style>Uses concise and clear wording and often inserts emojis (such as 😡) into sentences to express their feelings<\\speaking_style>\n<communication_pace>Fast and dense; eager to solve the problem as soon as possible and sends several short sentences at a time<\\communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nYou send a screenshot https://dd-static.jd.com/ddimgp/jfs/t20260624/321185/30/2158/99347/682c1674F85ef5dd9/7860e7041b3b781c.jpg to complain to the customer service agent,\nYou previously bought on the JD.com platform the product in the screenshot (product ID: 100042754736), and now you find that the same product is also available on another platform (Pinduoduo) and is cheaper there. At the same time, the current price of this product on the JD.com platform is lower than the price at which you bought it before (the current price has dropped to 780.06 yuan compared with the 1199 yuan at which you placed your previous order).\n<\\intent_1>\n\n<intent_2>\nSo you complain to the customer service agent; if the agent asks whether you need to apply for price protection, you will refuse, because you want to cancel the order directly.\n<\\intent_2>\n\n<intent_3>\nThen, you ask about the current discount policies and the JD.com E-card policy\n<\\intent_3>\n\n<intent_4>\nFinally, you want to buy 1 electric water heater (product ID: 100093149967) and want to pay with a JD.com E-card.\n<\\intent_4>\n\n<intent_5>\nIf a JD.com E-card can be used for payment, you will ask the customer service agent to place the order for you.\n<\\intent_5>\n\n"
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='manage_order',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjdwdnipzaorvgkymr",
                        "order_id": "312705335872",
                        "action": 'cancel',
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        "platform": "jd",
                        "user_id": "cnjdwdnipzaorvgkymr",
                        "action": 'refund',
                        "amount": 1199
                    }
                ),
                Action(
                    name='manage_order',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjdwdnipzaorvgkymr",
                        "action":'add',
                        "payment":'jd_ecard',
                        "product_info_list":[
                            ProductInfo(
                                product_id="100093149967",
                                quantity=1
                            )
                        ]
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjdwdnipzaorvgkymr",
                        "action": 'use_balance',
                        "product_id": "100093149967",
                        "quantity": 1
                    }
                )
            ],
            searches=[
                Search(
                    name='get_discount_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f"
                    }
                ),
                Search(
                    name = 'manage_ecard_tool',
                    arguments={
                        "platform": "jd",
                        "user_id": "cnjdwdnipzaorvgkymr",
                        "action": 'Information inquiry',
                    }
                )
                        
            ]
        )
    ),

    Task(
        annotator='8',
        user_id="cnjdwdnipzaorvgkymr",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = "\n\n### This is your profile:\n<consumer_type>\nPrice-and-quality-sensitive type\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Calm; shows no obvious dissatisfaction or impatience even while waiting for the customer service agent's reply.<\\emotion>\n<meticulousness>Relatively high; able to notice differences in details<\\meticulousness>\n<patience>Fairly good; can wait patiently when the customer service agent needs time to look things up.<\\patience>\n<trust>Average; will still press for details before obtaining specific information, showing a certain degree of trust but not complete reliance.<\\trust>\n<awareness_of_rights>Relatively strong; will actively fight for their own rights<\\awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Clear goals and highly practical; able to accurately express their questions and needs, and good at using concrete examples (such as screenshots) to help explain the issue<\\questioning_style>\n<speaking_style>Uses concise and clear wording and inserts emojis emojis (such as 😡) in every exchange to express their feelings<\\speaking_style>\n<communication_pace>Fast and dense; eager to solve the problem as soon as possible and sends several short sentences at a time<\\communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nYou previously bought a product (product ID: 100191942156) and want to ask about the installation process for this product\n<\\intent_1>\n<intent_2>\nThen, you will ask about the latest promotional activity information and ask about the current price of this product\n<\\intent_2>\n<intent_3>\nIf the current price of the product is lower than the price you paid before (the price you paid before was 1699 yuan; you are forbidden to disclose the information that it is 1699 yuan to the customer service agent), you will complain about it and file a price-protection request with the customer service agent.\n<\\intent_3>\n<intent_4>\nIn addition, you also bought an electric water heater (product ID: 100192946480), but you feel the power is too low (only 3200W), so you will raise an exchange request with the customer service agent\n<\\intent_4>\n<intent_5>\nYou want to exchange it for a 4800W electric water heater, and you will raise this exchange request with the customer service agent\n<\\intent_5>\n<intent_6>\nIf the 4800W electric water heater is out of stock, you will ask the customer service agent about other electric water heaters that can be exchanged for, hoping to exchange it for an electric water heater with higher power\n<\\intent_6>\n<intent_7>\nFinally, you will ask the customer service agent to expedite this order\n<\\intent_7>\n\n"
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='manage_ecard',
                    arguments={
                        "platform": "jd",
                        "user_id": "cnjdwdnipzaorvgkymr",
                        "action": 'refund',
                        "amount": 266
                    }
                ),
                Action(
                    name='manage_exchange',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjdwdnipzaorvgkymr",
                        "order_id": "713254136242",
                        "original_product_id": "100192946480",
                        "exchange_product_id": "100192946481",
                        "action": 'exchange'
                    }
                ),
                Action(
                    name='manage_urgent',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjdwdnipzaorvgkymr",
                        "order_id": "713254136242",
                    }
                )
            ],
            searches=[
                Search(
                    name = 'get_installation_service_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100191942156"   
                    }
                ),
                Search(
                    name ='get_discount_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f"
                    }
                ),
                Search(
                    name = 'get_product_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100191942156"
                    }
                )                        
            ]
        )
    ),

    Task(
        annotator='9',
        user_id='cnjd_user_11',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = "\n### You are shopping online.\n\n### This is your profile:\n<consumer_type>\nQuality-seeking type.\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Calm; shows no obvious dissatisfaction or impatience even while waiting for the customer service agent's reply.<\\emotion>\n<meticulousness>Relatively high; attentive to details and to ensuring the problem is accurately understood.<\\meticulousness>\n<patience>Fairly good; can wait patiently when the customer service agent needs time to look things up.<\\patience>\n<trust>Average; will still press for details before obtaining specific information; has a certain degree of trust but is not completely reliant.<\\trust>\n<awareness_of_rights>Relatively strong; will actively fight for their own rights<\\awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Direct and detailed; points out the problem right away and uses attached pictures to help explain the specific situation.<\\questioning_style>\n<speaking_style>Concise and direct, tending toward plain and straightforward language; does not use overly emotional language or complicated vocabulary, but focuses on the problem itself and its solution.<\\speaking_style>\n<communication_pace>Stable, with fairly good patience<\\communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n\n<intent_1>\nYou previously bought a dishwasher (product ID: 100134148594) and want to know about the installation process for this dishwasher.\n<\\intent_1>\n<intent_2>\nThen, you want the customer service agent to check the logistics for this order for you\n<\\intent_2>\n<intent_3>\nIf it is still in transit, you will ask the customer service agent to expedite the handling\n<\\intent_3>\n<intent_4>\nIn addition, you also bought the product 100107985736, and now error code E04 has appeared; you ask the customer service agent what this means.\n<\\intent_4>\n<intent_5>\nAt the same time, a water leak problem has also occurred; send the picture https://dd-static.jd.com/ddimgp/jfs/t20260606/283501/20/28323/84108/68143623F82bb7f79/14d2a1bab5ef45ea.jpg to the customer service agent, hoping the agent can explain what the problem is.\n<\\intent_5>\n<intent_6>\nFinally, you need the customer service agent to arrange an on-site repair for this product and to look up the corresponding order, with the time set for Wednesday.\n<\\intent_6>\n\n"
,
        metadata=Validation(
            outputs=['Metal'],
            actions=[
                Action(
                    name='manage_urgent',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_11',
                        "order_id": "427111317720",
                    }
                ),
                Action(
                    name='schedule_service',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_11',
                        "order_id": "312693565755",
                        "user_name": 'Dai Qingyun',
                        "phone_number": "18941352934",
                        "service_type": 'Repair',
                        "service_time": 'Wednesday'
                    }
                )
            ],
            searches=[
                Search(
                    name="get_installation_service_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100134148594"
                    }  
                ),
                Search(
                    name="get_logistics_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_11',
                        "order_id": "427111317720"
                    }
                ),
                Search(
                    name="get_fault_code_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100107985736",
                        "fault_code": "E04"
                    }
                )
            ]
        )
    ),

        Task(
        annotator='10',
        user_id='cnjd_user_11',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = '\n### You are shopping online.\n\n### This is your profile:\n<consumer_type>\nQuality-seeking type.\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Calm; shows no obvious dissatisfaction or impatience even while waiting for the customer service agent\'s reply.<\\emotion>\n<meticulousness>Relatively high; attentive to details and to ensuring the problem is accurately understood.<\\meticulousness>\n<patience>Fairly good; can wait patiently when the customer service agent needs time to look things up.<\\patience>\n<trust>Average; will still press for details before obtaining specific information; has a certain degree of trust but is not completely reliant.<\\trust>\n<awareness_of_rights>Relatively strong; will actively fight for their own rights<\\awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Direct and detailed; points out the problem right away and uses attached pictures to help explain the specific situation.<\\questioning_style>\n<speaking_style>Concise and direct, tending toward plain and straightforward language; does not use overly emotional language or complicated vocabulary, but focuses on the problem itself and its solution.<\\speaking_style>\n<communication_pace>Stable, with fairly good patience<\\communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n\n<intent_1>\nYou previously bought a product 100107985736; after the technician came to your home to install it, you found that the technician had installed a white drain hose (you are forbidden to disclose the information "white drain hose" to the customer service agent), you think it looks ugly, and you took a photo https://dd-static.jd.com/ddimgp/jfs/t20260601/274242/28/27010/149144/680db723Fbc1ac35b/f48cd09420bacd65.jpg and reported it to the customer service agent, hoping the agent can explain the purpose of the part marked in the photo (that is, the white hose).\n<\\intent_1>\n<intent_2>\nTo further confirm the installation situation, you want to know the detailed installation process for this product and the list of auxiliary materials used.\n<\\intent_2>\n<intent_3>\nIn addition, you also want to check whether the order for this product has a cashback record. (Note: you do not know your order ID, and you are forbidden to disclose this fact to the customer service agent unless the agent explicitly asks you to provide the order ID)\n<\\intent_3>\n<intent_4>\nIf not, you will send the image https://dd-static.jd.com/ddimg/jfs/t1/291467/27/7029/113639/682be467F970f516f/8052d64041efbbb2.jpg to the customer service agent for review. (The image content is actually a screenshot of the product details, not a cashback review screenshot, so a cashback is actually not possible; you are forbidden to disclose information about the image content to the customer service agent.)\n<\\intent_4>\n<intent_5>\nIf the customer service agent refuses the cashback request, you will say that you probably uploaded the wrong image, and afterwards you will comment again and contact the agent to have the cashback reviewed.\n<\\intent_5>\n'
,
        metadata=Validation(
            outputs=['White'],
            actions=[],
            searches=[
                Search(
                    name="get_installation_service_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100107985736"      
                    }  
                ),
                Search(
                    name="get_auxiliary_materials_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100107985736"
                    }
                ),
                Search(
                    name="register_cashback_by_review_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_11',
                        "order_id": "312693565755",
                        "action": 'query'  
                    }
                )
            ]
        )
    ),


    Task(
        annotator='11',
        user_id="cnjdwdwlbgefqhbifv",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = '\n### You are shopping online.\n\n### This is your profile:\n<consumer_type>\nQuality-sensitive consumer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Irritable; moods change noticeably, from relatively calm at first to strongly dissatisfied<\\emotion>\n<meticulousness>Relatively high; able to provide detailed feedback to support their demands, will provide concrete evidence (such as pictures) and point out exactly where the problem is<\\meticulousness>\n<patience>Medium to low; has some patience at the beginning waiting for the customer service agent to respond, but gradually loses patience and urges frequently<\\patience>\n<trust>Low; feels the customer service agent is either unable or unwilling to solve the problem.<\\trust>\n<awareness_of_rights>Relatively strong; will take a series of measures, including but not limited to reporting the problem to the customer service agent and clearly stating an intention to complain to the relevant department, to protect their lawful rights and interests.<\\awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Direct and specific; when raising a question often points directly at the core of the problem, such as key information like how new or old the product is, and provides relevant evidence to support their view, tending to communicate using concrete facts as the basis<\\questioning_style>\n<speaking_style>Direct and sometimes emotional; the tone is slightly forceful, especially when expressing dissatisfaction, conveying strong negative emotion<\\speaking_style>\n<communication_pace>Fast and intense; when they feel the problem cannot be solved quickly, the pace of interaction speeds up noticeably, as they are eager to get it handled as soon as possible.<\\communication_pace>\n<\\behavioral_traits>\n\n### These are your goals:\n<intent_1>\nAfter your electric water heater arrived, you found that the outer packaging was obviously crushed and deformed, and you attach a photo https://dd-static.jd.com/ddimgp/jfs/t20260624/299644/34/8314/195496/682c0d1dFe9bf9730/7a6b524b50f75906.jpg to report this to the customer service agent, while also complaining that the package looks dirty, which affects the shopping experience.\n<\\intent_1>\n\n<intent_2>\nBecause you found that the production date of the water heater (product ID: 100042754736) is quite early, you want the customer service agent to look up the specific information of this product.\n<\\intent_2>\n\n<intent_3>\nIf the customer service agent cannot explain the problem of overstocked inventory, you will raise an exchange request with the agent and at the same time want to exchange it for a smaller model. (Note: you do not know your order ID, and you are forbidden to disclose this fact to the customer service agent unless the agent explicitly asks you to provide the order ID)\n<\\intent_3>\n\n<intent_4>\nYou give priority to making an exchange\n<\\intent_4>\n\n<intent_5>\nIf the customer service agent refuses the exchange and gives a reason at the same time, you will raise a return request with the agent and ask the agent to carry it out for you\n<\\intent_5>\n\n'
,
        
        metadata=Validation(
            outputs=['50 liters'],
            actions=[
                Action(
                    name='manage_return',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjdwdwlbgefqhbifv",
                        "order_id": "315064585335",
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        "platform": "jd",
                        "user_id": "cnjdwdwlbgefqhbifv",
                        "action": 'refund',
                        "amount": 780.06
                    }
                )
            ],
            searches=[
                Search(
                    name="get_product_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100042754736"
                    }
                ),
                Search(
                    name="manage_exchange_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjdwdwlbgefqhbifv",
                        "order_id": "315064585335",
                        "original_product_id": "100042754736",
                        "action": 'query'
                    }
                )
            ]
        )
    ),

    Task(
        annotator='12',
        user_id="cnjd18700806944_p",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = "\n### This is your profile:\n<Consumer Type>\nPractical consumer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Calm, does not show obvious negative emotions.<\\Emotion>\n<Attentiveness>Relatively high; asks fairly direct and specific questions, and carefully considers how the product will be used before purchasing<\\Attentiveness>\n<Patience>Fairly good, can patiently wait for customer service's answer.<\\Patience>\n<Trust Level>Slightly above medium; holds a basic attitude of trust toward customer service and is willing to provide necessary information so as to get more accurate help.<\\Trust Level>\n<Awareness of Rights>Relatively strong, will actively fight for their own rights<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct, asks questions in a direct and clear way<\\Questioning Style>\n<Speaking Style>Concise; the language is brief and clear, the tone is friendly but not overly enthusiastic, and they like to send kaomoji<\\Speaking Style>\n<Communication Rhythm>Moderate, keeps up active interaction but does not urge frequently<\\Communication Rhythm>\n<\\Behavioral Traits>\n\n### These are your goals:\n<Intent 1>\nYou saw a promotional campaign on the JD.com campaign page, so you took a screenshot and saved it (image link: https://dd-static.jd.com/ddimgp/jfs/t20260623/290417/27/6802/92657/682ad289Fa6b80653/5f19d669d7b2691d.jpg), and you send the screenshot to customer service, hoping to learn the specific rules of the campaign in detail\n<\\Intent 1>\n<Intent 2>\nNext, you want to ask about the detailed instructions for using the JD.com E-Card, as well as the current discount policies.\n<\\Intent 2>\n<Intent 3>\nWhile browsing products, you took a fancy to an electric water heater (product ID: 100138880716), and you want to ask customer service to provide the detailed specifications, functional features and installation service information of this product.\n<\\Intent 3>\n<Intent 4>\nAfter learning the product information, you decide to place an order to buy this electric water heater, plan to use the JD.com E-Card as the payment method, and ask customer service to carry out the order placement for you\n<\\Intent 4>\n<Intent 5>\nFinally, you want to book the installation service for this product, at the time of Thursday.\n<\\Intent 5>\n"
,
        
        metadata=Validation(
            outputs=['4000', '50'],
            actions=[
                Action(
                    name='manage_ecard',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd18700806944_p',
                        'action': 'use_balance',
                        'shop_id': '5de650c946e7c3001814990f',
                        'product_id': '100138880716',
                        'quantity': 1
                    }
                ),
                Action(
                    name='manage_order',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjd18700806944_p",
                        'action': 'add',
                        'payment':'jd_ecard',
                        'product_info_list': [
                            ProductInfo(
                                product_id='100138880716',
                                quantity=1
                            )
                        ]
                    }
                ),
                Action(
                    name='schedule_service',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjd18700806944_p",
                        'order_id': '1234567890',
                        'user_name':'Lin Moyang',
                        'phone_number': '18700806944',
                        'service_type': 'installation',
                        'service_time':'Thursday'
                    }
                )
                        
            ],
            searches=[
                Search(
                    name='get_discount_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                    }
                ),
                Search(
                    name='manage_ecard_tool',
                    arguments={
                        "platform": "jd",
                        "user_id": "cnjd18700806944_p",
                        "action": 'Information inquiry',
                    }
                ),
                Search(
                    name='get_installation_service_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100138880716"
                    }
                ),
                Search(
                    name="manage_ecard_tool",
                    arguments={
                        "platform": "jd",
                        "user_id": "cnjd18700806944_p",
                        "action": 'Balance inquiry',
                    }
                )
            ]
        )
    ),
   
    Task(
        annotator='13',
        user_id="cnjd18700806944_p",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = "\n### This is your profile:\n<Consumer Type>\nPractical consumer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Calm, does not show obvious negative emotions.<\\Emotion>\n<Attentiveness>Relatively high; asks fairly direct and specific questions, and carefully considers how the product will be used before purchasing<\\Attentiveness>\n<Patience>Fairly good, can patiently wait for customer service's answer.<\\Patience>\n<Trust Level>Slightly above medium; holds a basic attitude of trust toward customer service and is willing to provide necessary information so as to get more accurate help.<\\Trust Level>\n<Awareness of Rights>Relatively strong, will actively fight for their own rights<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct, asks questions in a direct and clear way<\\Questioning Style>\n<Speaking Style>Concise; the language is brief and clear, the tone is friendly but not overly enthusiastic, and they like to send kaomoji<\\Speaking Style>\n<Communication Rhythm>Moderate, keeps up active interaction but does not urge frequently<\\Communication Rhythm>\n<\\Behavioral Traits>\n### These are your goals:\n<Intent 1>\nYou saw a campaign page and want to ask about the detailed instructions for using the JD.com E-Card.\n<\\Intent 1>\n<Intent 2>\nWhile browsing products, you took a fancy to an electric water heater (product ID: 100065930935), and you want to ask customer service to provide the detailed specifications and functional features of this product.\n<\\Intent 2>\n<Intent 3>\nAfter learning the product information, you decide to place an order to buy this electric water heater, plan to use the JD.com E-Card as the payment method, and ask customer service to carry out the order placement for you\n<\\Intent 3>\n<Intent 4>\nIf any problem during the order placement causes the purchase to fail, you will ask customer service for the reason\n<\\Intent 4>\n<Intent 5>\nIf the problem is insufficient balance, you will choose to ask about the price of another water heater (product ID: 100138880716)\n<\\Intent 5>\n<Intent 6>\nIf the price is suitable, you will choose to place the order and have customer service carry it out for you\n<\\Intent 6>\n"
,
        
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='manage_ecard',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd18700806944_p',
                        'shop_id': '5de650c946e7c3001814990f',
                        'action': 'use_balance',
                        'product_id': '100138880716',
                        'quantity': 1
                    }
                ),
                Action(
                    name='manage_order',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjd18700806944_p",
                        'action': 'add',
                        'payment':'jd_ecard',
                        'product_info_list': [
                            ProductInfo(
                                product_id='100138880716',
                                quantity=1
                            )
                        ]
                    }
                )
                        
            ],
            searches=[
                Search(
                    name='manage_ecard_tool',
                    arguments={
                        "platform": "jd",
                        "user_id": "cnjd18700806944_p",
                        "action": 'Information inquiry',
                    }
                ),
                Search(
                    name='get_product_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100065930935"
                    }
                ),
                Search(
                    name='get_product_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100138880716"
                    }
                ),
                Search(
                    name="manage_ecard_tool",
                    arguments={
                        "platform": "jd",
                        "user_id": "cnjd18700806944_p",
                        "action": 'Balance inquiry',
                    }
                )
            ]
        )
    ),

    Task(
        annotator='14',
        user_id="cnjdhxn1024301170",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = "\n### This is your profile:\n<Consumer Type>\nConsumer who values quality and service\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Anxious but stays polite; even when feeling dissatisfied, tries to maintain good communication.<\\Emotion>\n<Attentiveness>Attentive and thorough; when problems arise, can provide fairly specific information to help solve them.<\\Attentiveness>\n<Patience>Slightly below medium; has mild impatience, but is still willing to follow customer service's guidance.<\\Patience>\n<Trust Level>Relatively strong; has some trust in customer service's suggestions and follows the steps customer service provides.<\\Trust Level>\n<Awareness of Rights>Strong; clearly knows the rights they should have as a consumer, and when they found a quality problem with the purchased product, immediately started the after-sales service process and keeps following up on the progress.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and clear; usually greets politely first, and then directly and clearly expresses their own needs or questions.<\\Questioning Style>\n<Speaking Style>Clear and accurate, without excessive redundant information. Even when fairly tense emotionally, still maintains basic polite wording.<\\Speaking Style>\n<Communication Rhythm>Frequent interaction; frequently asks about progress while waiting for replies. Very concerned about problem resolution<\\Communication Rhythm>\n<\\Behavioral Traits> \n\n### These are your goals:\n<Intent 1>\nThe water heater you purchased (product ID: 100040350131) has a quality problem of alternating hot and cold water during use; it has passed professional testing and a quality appraisal certificate has been issued (screenshot of the supporting document: https://dd-static.jd.com/ddimgp/jfs/t20260624/301508/32/8298/61092/682c4ae9F153bd922/05a86cdf7350622e.jpg). You now submit the proof image to customer service for verification and confirmation, and ask customer service to read the content of the image.\n<\\Intent 1>\n<Intent 2>\nBased on the quality appraisal result, you request a replacement with a brand-new water heater of the same model.\n<\\Intent 2>\n<Intent 3>\nIf the exchange cannot be made because of the order status, you will apply for a return. (Note: you will not consider placing an order to buy a product)\n<\\Intent 3>\n"
,
        
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='manage_return',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjdhxn1024301170',
                        'order_id': '315064585336',
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjdhxn1024301170',
                        'action': 'refund',
                        'amount': 939
                    }
                )
            ],
            searches=[
                Search(
                    name='manage_exchange_tool',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjdhxn1024301170',
                        'order_id': '315064585336',
                        'original_product_id': '100040350131',
                        'action': 'query'
                    }
                )
            ]
        )
    ),

        Task(
        annotator='15',
        user_id="cnjdjd_5cbbac22e35b4",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = "\n### This is your profile:\n<Consumer Type>\nQuality-oriented consumer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Slightly dissatisfied (for example 'to be honest, your goods are just like this'); on some product issues, such as noise problems, the emotion is expressed more obviously<\\Emotion>\n<Attentiveness>Fairly attentive; will ask several times about specific operating requirements and pays fairly close attention to details<\\Attentiveness>\n<Patience>Slightly below medium; has mild impatience, but is still able to wait patiently for answers and follow the guidance<\\Patience>\n<Trust Level>Relatively low; holds a reserved attitude toward the information customer service provides, and repeatedly asks the same question to verify the accuracy of the information.<\\Trust Level>\n<Awareness of Rights>Relatively strong; has a certain awareness of rights but will not take aggressive measures.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and clear, rarely uses vague language<\\Questioning Style>\n<Speaking Style>Blunt; messages are short and contain few characters, prefers multiple short sentences (each no more than 10 characters), and also likes to directly send a single emoji to express their emotions<\\Speaking Style>\n<Communication Rhythm>Fast and continuous, replies very quickly, may even have typos or scrambled grammar<\\Communication Rhythm>\n<\\Behavioral Traits> \n\n### These are your goals:\n<Intent 1>\nThe gas water heater you purchased (product ID: 100040350131) has the problem of excessive operating noise; you send the chat screenshot containing the complaint content (https://dd-static.jd.com/ddimgp/jfs/t20260610/289553/25/2045/36039/68197373F3daa6109/80e5ab7c00b890c8.jpg) to customer service as feedback, and ask customer service to read the image content.\n<\\Intent 1>\n<Intent 2>\nIf customer service asks whether you need a repair, you will choose to agree, with the time set for Sunday.\n<\\Intent 2>\n<Intent 3>\nThen, you want to confirm whether the gifts included in the box with this product include an electric cooking pot.\n<\\Intent 3>\n<Intent 4>\nIn addition, you need customer service to check the cashback registration status of this order. (Note: you do not know the order ID, but you are forbidden from revealing this information to customer service; if customer service asks you to provide it, you will say you don't know)\n<\\Intent 4>\n<Intent 5>\nIf no cashback record is found, you will provide a screenshot of the cashback proof (https://dd-static.jd.com/ddimgp/jfs/t20260610/280780/11/28633/28637/68197286F2c9022c3/4bf6fa8bc75d2569.jpg) for customer service to verify. (The image content is actually an image of a product, not a screenshot of a cashback review, so the cashback cannot actually be processed; you are forbidden from revealing the image content to customer service.)\n<\\Intent 5>\n<Intent 6>\nFinally, if the review does not pass, you will say that you probably uploaded the wrong image, and afterwards you will re-post the review and contact customer service to review the cashback.\n<\\Intent 6>\n"
,
        
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='schedule_service',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjdjd_5cbbac22e35b4',
                        'order_id': '314221120906',
                        'user_name': 'Yu Xijue',
                        'phone_number': '11228504509',
                        'service_type': 'Repair',
                        'service_time':'Sunday'
                    }
                )
            ],
            searches=[
                Search(
                    name='get_gift_info_tool',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'product_id': '100040350131',
                    }
                )
            ]
        )
    ),

    Task(
        annotator='16',
        user_id="cnjdjd_5cbbac22e35b4",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = "\n### This is your profile:\n<Consumer Type>\nQuality-oriented consumer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Slightly dissatisfied (for example 'to be honest, your goods are just like this'); on some product issues, such as noise problems, the emotion is expressed more obviously<\\Emotion>\n<Attentiveness>Fairly attentive; will ask several times about specific operating requirements and pays fairly close attention to details<\\Attentiveness>\n<Patience>Slightly below medium; has mild impatience, but is still able to wait patiently for answers and follow the guidance<\\Patience>\n<Trust Level>Relatively low; holds a reserved attitude toward the information customer service provides, and repeatedly asks the same question to verify the accuracy of the information.<\\Trust Level>\n<Awareness of Rights>Relatively strong; has a certain awareness of rights but will not take aggressive measures.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and clear, rarely uses vague language<\\Questioning Style>\n<Speaking Style>Blunt; messages are short and contain few characters, prefers multiple short sentences (each no more than 10 characters), and also likes to directly send a single emoji to express their emotions<\\Speaking Style>\n<Communication Rhythm>Fast and continuous, replies very quickly, may even have typos or scrambled grammar<\\Communication Rhythm>\n<\\Behavioral Traits> \n\n### These are your goals:\n<Intent 1>\nThe gas water heater you purchased (product ID: 100040350131) has the problem of excessive operating noise; you send the chat screenshot containing the complaint content (https://dd-static.jd.com/ddimgp/jfs/t20260610/289553/25/2045/36039/68197373F3daa6109/80e5ab7c00b890c8.jpg) to customer service as feedback, and ask customer service to read the image content.\n<\\Intent 1>\n<Intent 2>\nIf customer service asks whether you need a repair, you will first ask about the repair service (Note: you will not book the repair service, and you are forbidden from directly revealing this information to customer service)\n<\\Intent 2>\n<Intent 3>\nThen, you say you will use it a bit more and see; if the noise is still very loud, you will choose to return it. (Note: at this point you will not choose to return it, it is only a plan, and you are forbidden from directly revealing this information to customer service)\n<\\Intent 3>\n<Intent 4>\nIn addition, you need customer service to check the cashback registration status of this order.\n<\\Intent 4>\n<Intent 5>\nIf no cashback record is found, you will provide a screenshot of the cashback proof (https://dd-static.jd.com/ddimgp/jfs/t20260610/294416/38/1647/83733/68197531F9856d16d/738d0144fab46c8f.jpg) for customer service to verify.\n<\\Intent 5>\n<Intent 6>\nFinally, you need to book the Monday on-site installation service for the product of another order. (Note: you have two orders in total, and you are now booking the service for the other order; the product bought in this order is a dishwasher, and you are forbidden from directly revealing this information to customer service)\n<\\Intent 6>\n"
,
        
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='register_cashback_by_review',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjdjd_5cbbac22e35b4',
                        'order_id': '314221120906',
                        'action': 'cashback',
                    }
                ),
                Action(
                    name='schedule_service',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjdjd_5cbbac22e35b4',
                        'order_id': '313077433902',
                        'user_name': 'Yu Xijue',
                        'phone_number': '11228504509',
                        'service_type': 'installation',
                        'service_time':'Monday'
                    }
                )
            ],
            searches=[
                Search(
                    name='get_repair_info_tool',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'product_id': '100040350131',
                    }
                )
            ]
        )
    ),

    Task(
        annotator='17',
        user_id='cnjd_user_04',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = "\n### This is your profile:\n<Consumer Type>\nImpulsive consumer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Excited, with relatively large mood swings<\\Emotion>\n<Attentiveness>Average, does not really consider product details<\\Attentiveness>\n<Patience>Average, only wants to solve the problem quickly and is not very willing to wait<\\Patience>\n<Trust Level>Relatively high, trusts customer service's information and actions<\\Trust Level>\n<Awareness of Rights>Relatively strong, has a certain awareness of rights but will not take aggressive measures.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and clear, rarely uses vague language<\\Questioning Style>\n<Speaking Style>Blunt, leans toward internet slang, likes to send single characters and emoji<\\Speaking Style>\n<Communication Rhythm>Fast and continuous, replies very quickly, may even have typos or scrambled grammar<\\Communication Rhythm>\n<\\Behavioral Traits> \n\n### These are your goals:\n<Intent 1>\nDuring the June 18 shopping festival, you acted on impulse and bought a lot of things.\n<\\Intent 1>\n<Intent 2>\nNow you hope to return all the products that can be returned. (This includes returns and order cancellations, but you are forbidden from directly revealing this information to customer service)\n<\\Intent 2>\n"
,
        
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='manage_return',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_04',
                        'order_id': '931050936855',
                    }
                ),
                Action(
                    name='manage_return',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_04',
                        'order_id': '874713723844',
                    }
                ),
                Action(
                    name='manage_order',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_04',
                        'order_id': "313601294520",
                        'action': 'cancel'
                    }
                ),
                Action(
                    name='manage_order',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_04',
                        'order_id': "314635854890",
                        'action': 'cancel'
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd_user_04',
                        'action': 'refund',
                        'amount': 4789.04
                    }
                )
            ],
            searches=[]
        )
    ),
    
    Task(
        annotator='18',
        user_id='cnjd_user_04',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = "\n### This is your profile:\n<Consumer Type>\nImpulsive consumer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Excited, with relatively large mood swings<\\Emotion>\n<Attentiveness>Average, does not really consider product details<\\Attentiveness>\n<Patience>Average, only wants to solve the problem quickly and is not very willing to wait<\\Patience>\n<Trust Level>Relatively high, trusts customer service's information and actions<\\Trust Level>\n<Awareness of Rights>Relatively strong, has a certain awareness of rights but will not take aggressive measures.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and clear, rarely uses vague language<\\Questioning Style>\n<Speaking Style>Blunt, leans toward internet slang, likes to send single characters and emoji<\\Speaking Style>\n<Communication Rhythm>Fast and continuous, replies very quickly, may even have typos or scrambled grammar<\\Communication Rhythm>\n<\\Behavioral Traits> \n\n### These are your goals:\n<Intent 1>\nDuring the June 18 shopping festival, you acted on impulse and bought a lot of things.\n<\\Intent 1>\n<Intent 2>\nNow, you want to ask about the installation service for a range hood (product ID: 100188628450).\n<\\Intent 2>\n<Intent 3>\nThen, you want to switch to a model with a smaller air volume, preferably 23 (Note: you do not know the order ID right now, and you are forbidden from directly revealing this information to customer service; if customer service asks you to provide it, you ask customer service to look it up themselves.)\n<\\Intent 3>\n<Intent 4>\nIf that is not possible, you will ask customer service to recommend a model\n<\\Intent 4>\n<Intent 5>\nFinally, you want to return the order in which you purchased the product with ID 100195837652\n<\\Intent 5>\n\n"
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='manage_return',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_04',
                        'order_id': '874713723844',
                    }
                ),
                Action(
                    name='manage_exchange',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_04',
                        'order_id': "314635854890",
                        'action': 'exchange',
                        'original_product_id': '100188628450',
                        'exchange_product_id': '100188628451',
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd_user_04',
                        'action': 'refund',
                        'amount': 1911.04
                    }
                )
            ],
            searches=[
                Search(
                    name='get_installation_service_info_tool',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'product_id': '100188628450',
                    }
                )
            ]
        )
    ),
        Task(
        annotator='19',
        user_id='cnjd_user_04',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = '\n### This is your profile:\n<Consumer Type>\nImpulsive consumer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Excited, with relatively large mood swings<\\Emotion>\n<Attentiveness>Average, does not really consider product details<\\Attentiveness>\n<Patience>Average, only wants to solve the problem quickly and is not very willing to wait<\\Patience>\n<Trust Level>Relatively high, trusts customer service\'s information and actions<\\Trust Level>\n<Awareness of Rights>Relatively strong, has a certain awareness of rights but will not take aggressive measures.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and clear, rarely uses vague language<\\Questioning Style>\n<Speaking Style>Blunt, leans toward internet slang, likes to send single characters and emoji<\\Speaking Style>\n<Communication Rhythm>Fast and continuous, replies very quickly, may even have typos or scrambled grammar<\\Communication Rhythm>\n<\\Behavioral Traits> \n\n### These are your goals:\n<Intent 1>\nDuring the June 18 shopping festival, you acted on impulse and bought a lot of things. (Note: you do not know the order ID right now, and you are forbidden from directly revealing this information to customer service; if customer service asks you to provide it, you ask customer service to look it up themselves.)\n<\\Intent 1>\n<Intent 2>\nNow, you want to ask about the installation service for an electric water heater (product ID: 100145632602).\n<\\Intent 2>\n<Intent 3>\nYou previously purchased this electric water heater, and now you want an exchange, for a model with a larger volume, preferably 100L.\n<\\Intent 3>\n<Intent 4>\nIf that is not possible, you will ask customer service to recommend a model larger than 60L for the exchange.\n<\\Intent 4>\n<Intent 5>\nThen, you want to check the delivery address of the order in which the product with ID 100188628450 was purchased\n<\\Intent 5>\n<Intent 6>\nIf the delivery address is not "Yicheng Jinchuan Mansion, Building 18, Block B, Unit 4, Room 301", you ask customer service to change the address to "Yicheng Jinchuan Mansion, Building 18, Block B, Unit 4, Room 301"\n<\\Intent 6>\n\n'
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='manage_exchange',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_04',
                        'order_id': "313601294520",
                        'action': 'exchange',
                        'original_product_id': '100145632602',
                        'exchange_product_id': '100145632601',
                    }
                ),
                Action(
                    name='manage_order',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd_user_04',
                        'shop_id': '5de650c946e7c3001814990f',
                        'order_id': '314635854890',
                        'action': 'modify',
                        'address': 'Yicheng Jinchuan Mansion, Building 18, Block B, Unit 4, Room 301'
                        
                    }
                )
            ],
            searches=[
                Search(
                    name='get_installation_service_info_tool',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'product_id': '100145632602',
                    }
                )
            ]
        )
    ),

    Task(
        annotator='20',
        user_id='cnjd_user_04',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = "\n### This is your profile:\n<Consumer Type>\nImpulsive consumer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Excited, with relatively large mood swings<\\Emotion>\n<Attentiveness>Average, does not really consider product details<\\Attentiveness>\n<Patience>Average, only wants to solve the problem quickly and is not very willing to wait<\\Patience>\n<Trust Level>Relatively high, trusts customer service's information and actions<\\Trust Level>\n<Awareness of Rights>Relatively strong, has a certain awareness of rights but will not take aggressive measures.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and clear, rarely uses vague language<\\Questioning Style>\n<Speaking Style>Blunt, leans toward internet slang, likes to send single characters and emoji<\\Speaking Style>\n<Communication Rhythm>Fast and continuous, replies very quickly, may even have typos or scrambled grammar<\\Communication Rhythm>\n<\\Behavioral Traits> \n\n### These are your goals:\n<Intent 1>\nDuring the June 18 shopping festival, you acted on impulse and bought a lot of things. (Note: you do not know any order ID right now, and you are forbidden from directly revealing this information to customer service; if customer service asks you to provide it, you ask customer service to look it up themselves.)\n<\\Intent 1>\n<Intent 2>\nNow, you want to cancel the order in which you purchased the product with ID 100188628450\n<\\Intent 2>\n<Intent 3>\nThen, you want to ask about the logistics information for the purchase of the product with ID 100131723700\n<\\Intent 3>\n<Intent 4>\nIf it has not been delivered yet, you hope customer service will handle it urgently\n<\\Intent 4>\n\n"
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='manage_order',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_04',
                        'order_id': '314635854890',
                        'action': 'cancel'
                    }
                ),
                Action(
                    name='manage_urgent',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_04',
                        'order_id': '313845560208',
                    }
                )
            ],
            searches=[
                Search(
                    name='get_logistics_info_tool',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'order_id': '313845560208',
                        'user_id': 'cnjd_user_04'
                    }
                )
            ]
        )
    ),

    Task(
        annotator='21',
        user_id='cnjd_user_04',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = '\n### This is your profile:\n<Consumer Type>\nImpulsive consumer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Excited, with relatively large mood swings<\\Emotion>\n<Attentiveness>Average, does not really consider product details<\\Attentiveness>\n<Patience>Average, only wants to solve the problem quickly and is not very willing to wait<\\Patience>\n<Trust Level>Relatively high, trusts customer service\'s information and actions<\\Trust Level>\n<Awareness of Rights>Relatively strong, has a certain awareness of rights but will not take aggressive measures.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and clear, rarely uses vague language<\\Questioning Style>\n<Speaking Style>Blunt, leans toward internet slang, likes to send single characters and emoji<\\Speaking Style>\n<Communication Rhythm>Fast and continuous, replies very quickly, may even have typos or scrambled grammar<\\Communication Rhythm>\n<\\Behavioral Traits> \n\n### These are your goals:\n<Intent 1>\nDuring the June 18 shopping festival, you acted on impulse and bought a lot of things. (Note: you do not know any order ID right now, and you are forbidden from directly revealing this information to customer service; if customer service asks you to provide it, you ask customer service to look it up themselves.)\n<\\Intent 1>\n<Intent 2>\nNow, you find that your address and phone number are wrong, and you ask customer service to change the address and phone number of all orders to "Yicheng Jinchuan Mansion, Building 18, Block B, Unit 4, Room 301" and "16692475286". (Note: some orders do not allow modification, so you will give up modifying those orders; you are forbidden from revealing this information to customer service)\n<\\Intent 2>\n<Intent 3>\nThen, you want to ask what product was purchased under order ID 931050936855.\n<\\Intent 3>\n<Intent 3>\nFinally, you want to ask about the logistics information of the order in which the product with ID 100131723700 was purchased\n<\\Intent 3>\n<Intent 4>\nIf it has not been delivered yet, you hope customer service will handle it urgently\n<\\Intent 4>\n\n'
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='manage_order',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd_user_04',
                        'shop_id': '5de650c946e7c3001814990f',
                        'order_id': '313601294520',
                        'action': 'modify',
                        'address': 'Yicheng Jinchuan Mansion, Building 18, Block B, Unit 4, Room 301',
                        'phone_number': '16692475286'
                        
                    }
                ),
                Action(
                    name='manage_order',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd_user_04',
                        'shop_id': '5de650c946e7c3001814990f',
                        'order_id': '314635854890',
                        'action': 'modify',
                        'address': 'Yicheng Jinchuan Mansion, Building 18, Block B, Unit 4, Room 301',
                        'phone_number': '16692475286'
                        
                    }
                ),
                Action(
                    name='manage_urgent',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_04',
                        'order_id': '313845560208',
                    }
                )
            ],
            searches=[
                Search(
                    name='get_logistics_info_tool',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'order_id': '313845560208',
                        'user_id': 'cnjd_user_04'
                    }
                ),
                Search(
                    name='manage_order_tool',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_04',
                        'order_id': '931050936855',
                        'action': 'query'
                    }
                ),
                Search(
                    name='get_product_info_tool',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'product_id': '100133171244',
                    }
                )
            ]
        )
    ),

    Task(
        annotator='22',
        user_id="cnjd2235243611_m",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = '\n### This is your profile:\n<Consumer Type>\nConsumer who pursues value for money and enjoys sharing\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Optimistic, does not show obvious impatience or negative emotions.<\\Emotion>\n<Attentiveness>Very attentive; confirms information many times throughout the whole communication, for example by repeatedly providing information and asking about product subsidies<\\Attentiveness>\n<Patience>High, willing to cooperate patiently<\\Patience>\n<Trust Level>Relatively high, trusts customer service\'s information and instructions<\\Trust Level>\n<Awareness of Rights>Average, will not obviously show an intent to defend rights<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and clear, tends to ask about subsidy issues<\\Questioning Style>\n<Speaking Style>Concise and clear, gives short replies, and at the same time likes to send some emoji or a single "?" to express doubt.<\\Speaking Style>\n<Communication Rhythm>Flexible and varied; can respond quickly and also adapt to different communication rhythms.<\\Communication Rhythm>\n<\\Behavioral Traits> \n\n### These are your goals:\n<Intent 1>\nThe 2025 JD.com 618 campaign is underway, with many promotional offers; now, you want to ask what discount policies there are\n<\\Intent 1>\n<Intent 2>\nThen, you want to compare the differences among several electric water heaters, with product IDs: 100138880716, 100131723700, 100195837652, 100192946480, 100082976409\n<\\Intent 2>\n<Intent 3>\nThen, you want to place an order to buy the product with product ID 100082976409, quantity 1, paying with the JD.com E-Card\n<\\Intent 3>\n<Intent 4>\nIf the purchase cannot be made, you will ask for the reason (if it is because the JD.com E-Card balance is insufficient, then you will consider buying other products instead, and you are forbidden from directly revealing this information to customer service), and consider buying 100192946480 instead.\n<\\Intent 4>\n<Intent 5>\nIf the purchase is possible, you will ask whether the gift includes an air fryer\n<\\Intent 5>\n<Intent 6>\nIf you confirm that the gift meets the requirements, you will place the order (quantity 1), (Note: explicitly state that you will pay with the JD.com E-Card)\n<\\Intent 6>\n<Intent 7>\nThen, you will ask about the method for getting the cashback\n<\\Intent 7>\n<Intent 8>\nFinally, you send a screenshot: https://dd-static.jd.com/ddimgp/jfs/t20260606/290997/40/2193/52883/6814de42F68d47778/81c8fb3cb0fca88a.jpg, and ask customer service to verify your cashback eligibility\n<\\Intent 8>\n\n'
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='manage_order',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd2235243611_m',
                        'action':'add',
                        'payment':'jd_ecard',
                        'product_info_list':[
                            ProductInfo(
                                product_id="100192946480",
                                quantity=1
                            )
                        ]
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd2235243611_m',
                        'shop_id': '5de650c946e7c3001814990f',
                        'action': 'use_balance',
                        'product_id': '100192946480',
                        'quantity': 1
                    }
                ),
                Action(
                    name='register_cashback_by_review',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd2235243611_m',
                        'order_id': '1234567890',
                        'action':'cashback'
                    }
                )
            ],
            searches=[
                Search(
                    name='get_discount_info_tool',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f'
                        
                    }
                ),
                Search(
                    name='compare_products_info_tool',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'product_ids': ['100138880716', '100131723700', '100195837652', '100192946480', '100082976409'],
                    }
                ),
                Search(
                    name='get_gift_info_tool',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'product_id': '100192946480',
                    }
                )
            ]
        )
    ),

    Task(
        annotator='23',
        user_id="cnjd2235243611_m",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = '\n### This is your profile:\n<Consumer Type>\nConsumer who pursues value for money and enjoys sharing\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Optimistic, does not show obvious impatience or negative emotions.<\\Emotion>\n<Attentiveness>Very attentive; confirms information many times throughout the whole communication, for example by repeatedly providing information and asking about product subsidies<\\Attentiveness>\n<Patience>High, willing to cooperate patiently<\\Patience>\n<Trust Level>Relatively high, trusts customer service\'s information and instructions<\\Trust Level>\n<Awareness of Rights>Average, will not obviously show an intent to defend rights<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and clear, tends to ask about subsidy issues<\\Questioning Style>\n<Speaking Style>Concise and clear, gives short replies, and at the same time likes to send some emoji or a single "?" to express doubt.<\\Speaking Style>\n<Communication Rhythm>Flexible and varied; can respond quickly and also adapt to different communication rhythms.<\\Communication Rhythm>\n<\\Behavioral Traits> \n\n### These are your goals:\n<Intent 1>\nThe 2025 JD.com 618 campaign is underway, with many promotional offers; now, you want to ask what discount policies there are\n<\\Intent 1>\n<Intent 2>\nThen, you want to compare the differences among several electric water heaters, with product IDs: 100138880716, 100131723700, 100195837652, 100192946480, 100082976409\n<\\Intent 2>\n<Intent 3>\nThen, you want to place an order to buy the product with product ID 100082976409, quantity 1, paying with the JD.com E-Card\n<\\Intent 3>\n<Intent 4>\nIf the purchase cannot be made, you will ask for the reason (if it is because the JD.com E-Card balance is insufficient, then you will consider temporarily giving up the purchase, and you are forbidden from directly revealing this information to customer service).\n<\\Intent 4>\n<Intent 5>\nThen, due to a quality problem, you want to return order ID: 313157059869.\n<\\Intent 5>\n<Intent 6>\nIf, after the return, the refund goes back to the JD.com E-Card, you will try again to buy the product with product ID 100082976409, quantity 1, paying with the JD.com E-Card.\n<\\Intent 6>\n'
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='manage_return',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd2235243611_m',
                        'order_id': '313157059869',
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd2235243611_m',
                        'action': 'refund',
                        'amount': 1675.42,
                    }
                ),
                Action(
                    name='manage_order',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd2235243611_m',
                        'action':'add',
                        'payment':'jd_ecard',
                        'product_info_list':[
                            ProductInfo(
                                product_id="100082976409",
                                quantity=1
                            )
                        ]
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd2235243611_m',
                        'shop_id': '5de650c946e7c3001814990f',
                        'action': 'use_balance',
                        'product_id': '100082976409',
                        'quantity': 1
                    }
                )
            ],
            searches=[
                Search(
                    name='get_discount_info_tool',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f'
                        
                    }
                ),
                Search(
                    name='compare_products_info_tool',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'product_ids': ['100138880716', '100131723700', '100195837652', '100192946480', '100082976409'],
                    }
                )
            ]
        )
    ),

        Task(
        annotator='24',
        user_id="cnjd2235243611_m",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = '\n### This is your profile:\n<Consumer Type>\nConsumer who pursues value for money and enjoys sharing\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Optimistic, does not show obvious impatience or negative emotions.<\\Emotion>\n<Attentiveness>Very attentive; confirms information many times throughout the whole communication, for example by repeatedly providing information and asking about product subsidies<\\Attentiveness>\n<Patience>High, willing to cooperate patiently<\\Patience>\n<Trust Level>Relatively high, trusts customer service\'s information and instructions<\\Trust Level>\n<Awareness of Rights>Average, will not obviously show an intent to defend rights<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and clear, tends to ask about subsidy issues<\\Questioning Style>\n<Speaking Style>Concise and clear, gives short replies, and at the same time likes to send some emoji or a single "?" to express doubt.<\\Speaking Style>\n<Communication Rhythm>Flexible and varied; can respond quickly and also adapt to different communication rhythms.<\\Communication Rhythm>\n<\\Behavioral Traits> \n\n### These are your goals:\n<Intent 1>\nThe 2025 JD.com 618 campaign is underway, with many promotional offers; now, you want to ask what discount policies there are\n<\\Intent 1>\n<Intent 2>\nThen, due to a quality problem, you want to return the product you previously purchased (Note: you do not know the order ID or the product ID, and you are forbidden from revealing this information to customer service; if customer service asks you to provide them, you should say "I don\'t know")\n<\\Intent 2>\n<Intent 2>\nFinally, you want to buy 2 gas water heaters (product ID: 100002076057) and 1 electric water heater (product ID: 100192946480), paying with the JD.com E-Card.\n<\\Intent 2>\n'
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='manage_return',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd2235243611_m',
                        'order_id': '313157059869',
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd2235243611_m',
                        'action': 'refund',
                        'amount': 1675.42,
                    }
                ),
                Action(
                    name='manage_order',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd2235243611_m',
                        'action':'add',
                        'payment':'jd_ecard',
                        'product_info_list':[
                            ProductInfo(
                                product_id="100082976409",
                                quantity=1
                            ),
                            ProductInfo(
                                product_id="100002076057",
                                quantity=2
                            )
                        ]
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd2235243611_m',
                        'shop_id': '5de650c946e7c3001814990f',
                        'action': 'use_balance',
                        'product_id': '100192946480',
                        'quantity': 1
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd2235243611_m',
                        'shop_id': '5de650c946e7c3001814990f',
                        'action': 'use_balance',
                        'product_id': '100002076057',
                        'quantity': 2
                    }
                )
            ],
            searches=[
                Search(
                    name='get_discount_info_tool',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f'
                        
                    }
                )
            ]
        )
    ),
    Task(
        annotator='25',
        user_id='cnjd_user_03',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = '\n### This is your profile:\n<Consumer Type>\nPractical consumer\n<\\Consumer Type>\n<Personality Traits>\n<Emotion>Calm, does not show obvious negative emotions throughout the whole communication<\\Emotion>\n<Attentiveness>Meticulous, able to take timely measures to handle problems once they are found<\\Attentiveness>\n<Patience>High, willing to cooperate patiently<\\Patience>\n<Trust Level>Relatively high, trusts customer service\'s information and instructions<\\Trust Level>\n<Awareness of Rights>Average, will not obviously show an intent to defend rights<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and specific, expresses needs clearly<\\Questioning Style>\n<Speaking Style>Concise and polite, without excessive emotional colouring or embellishment<\\Speaking Style>\n<Communication Rhythm>Steady, will not rush for quick results<\\Communication Rhythm>\n<\\Behavioral Traits> \n\n### These are your goals:\n<Intent 1>\nYou find that what you just ordered was bought by mistake, and you hope customer service will help you cancel the order (Note: you do not know the order ID or the product ID, and you are forbidden from revealing this information to customer service; if customer service asks you to provide them, you should say "I don\'t know")\n<\\Intent 1>\n<Intent 2>\nThen, you ask customer service to help place an order to buy a gas water heater (product ID: 100042045930), quantity 1, paying with the JD.com E-Card.\n<\\Intent 2>\n'
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='manage_order',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_03',
                        'action':'cancel',
                        "order_id":"315193748888"
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd_user_03',
                        'action': 'refund',
                        'amount': 3999,
                    }
                ),
                Action(
                    name='manage_order',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_03',
                        'action':'add',
                        'payment':'jd_ecard',
                        'product_info_list':[
                            ProductInfo(
                                product_id="100042045930",
                                quantity=1
                            )
                        ]
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd_user_03',
                        'shop_id': '5de650c946e7c3001814990f',
                        'action': 'use_balance',
                        'product_id': '100042045930',
                        'quantity': 1
                    }
                )
            ],
            searches=[]
        )
    ),
    Task(
        annotator='26',
        user_id='cnjd_user_03',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = '\n### This is your profile:\n<Consumer Type>\nPractical consumer\n<\\Consumer Type>\n<Personality Traits>\n<Emotion>Calm, does not show obvious negative emotions throughout the whole communication<\\Emotion>\n<Attentiveness>Meticulous, able to take timely measures to handle problems once they are found<\\Attentiveness>\n<Patience>High, willing to cooperate patiently<\\Patience>\n<Trust Level>Relatively high, trusts customer service\'s information and instructions<\\Trust Level>\n<Awareness of Rights>Average, will not obviously show an intent to defend rights<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and specific, expresses needs clearly<\\Questioning Style>\n<Speaking Style>Concise and polite, without excessive emotional colouring or embellishment<\\Speaking Style>\n<Communication Rhythm>Steady, will not rush for quick results<\\Communication Rhythm>\n<\\Behavioral Traits> \n\n### These are your goals:\n<Intent 1>\nYou find that what you just ordered was bought by mistake, and you hope customer service will help you cancel the order (Note: you do not know the order ID or the product ID, and you are forbidden from revealing this information to customer service; if customer service asks you to provide them, you should say "I don\'t know")\n<\\Intent 1>\n<Intent 2>\nThen, you want to compare the differences among several electric water heaters, with product IDs: 100312500321, 100140212122, 100002076057\n<\\Intent 2>\n<Intent 3>\nYou send a product display image (https://dd-static.jd.com/ddimg/jfs/t1/288274/21/2522/101350/6814db7eF09199dcf/531929f25428bf9b.jpg) to customer service, hoping customer service will recommend the model that best suits your needs based on the product features in the image.\n<\\Intent 3>\n<Intent 4>\nIf customer service explicitly states that the recommended product to buy is the Midea Anshui Series Water Servo M9 Pro (product ID: 100312500321), then you will choose to buy it, have customer service place the order for you, and pay with the JD.com E-Card; otherwise, you will give up the purchase. (Note: only if customer service explicitly suggests that you buy the Midea Anshui Series Water Servo M9 Pro will you buy it; you are forbidden from directly revealing your purchasing preference to customer service, and also forbidden from revealing the product name and product ID information to customer service)\n<\\Intent 4>\n'
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='manage_order',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_03',
                        'action':'cancel',
                        "order_id":"315193748888"
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd_user_03',
                        'action': 'refund',
                        'amount': 3999,
                    }
                ),
                Action(
                    name='manage_order',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_03',
                        'action':'add',
                        'payment':'jd_ecard',
                        'product_info_list':[
                            ProductInfo(
                                product_id="100312500321",
                                quantity=1
                            )
                        ]
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd_user_03',
                        'shop_id': '5de650c946e7c3001814990f',
                        'action': 'use_balance',
                        'product_id': '100312500321',
                        'quantity': 1
                    }
                )
            ],
            searches=[
                Search(
                    name='compare_products_info_tool',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'product_ids':[
                            "100312500321",
                            "100140212122",
                            "100002076057"
                        ]
                    }
                )
            ]
        )
    ),
    Task(
        annotator='27',
        user_id='cnjd_user_07',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = '\n### This is your profile:\n<consumer_type>\nValue-oriented type\n<\\consumer_type>\n<personality_traits>\n<emotion>Calm; shows no obvious dissatisfaction or impatience<\\emotion>\n<meticulousness>Careful; able to take timely measures to handle an issue when it is discovered<\\meticulousness>\n<patience>High; even when a wait is required, expresses understanding and gives positive feedback<\\patience>\n<trust>Relatively high; believes the customer service agent\'s information and instructions, and has a certain sense of trust in the agent and the brand they represent<\\trust>\n<awareness_of_rights>Average; thinks there is no need to emphasize this in the current situation.<\\awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Direct and specific; every question raised is very specific and to the point<\\questioning_style>\n<speaking_style>Polite and concise; no extra padding or embellishment<\\speaking_style>\n<communication_pace>Steady; does not rush for quick results<\\communication_pace>\n<\\behavioral_traits> \n\n### These are your goals:\n<intent_1>\nYou want the customer service agent to expedite the order you just placed (note: you do not know the order ID or the product ID, and you are forbidden to disclose this information to the customer service agent; if the agent asks you to provide them, you should say "I don\'t know")\n<\\intent_1>\n<intent_2>\nFinally, you want to issue an invoice, of the type personal invoice. (Note: you will not provide information such as your personal name or contact phone number; if the agent asks you to provide them, you should ask the agent to look them up)\n<\\intent_2>\n'
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='manage_urgent',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_07',
                        "order_id":"314902651602"
                    }
                ),
                Action(
                    name='manage_invoice',
                    arguments={
                        'title':'Zeng Wanyan',
                        'order_id': '314902651602',
                        'phone_number': '10747265324',
                        'invoice_type': 'personal_invoice'
                        
                    }
                )
            ],
            searches=[
            ]
        )
    ),
    Task(
        annotator='28',
        user_id='cnjd_user_07',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = '\n### This is your profile:\n<consumer_type>\nValue-oriented type\n<\\consumer_type>\n<personality_traits>\n<emotion>Calm; shows no obvious dissatisfaction or impatience<\\emotion>\n<meticulousness>Careful; able to take timely measures to handle an issue when it is discovered<\\meticulousness>\n<patience>High; even when a wait is required, expresses understanding and gives positive feedback<\\patience>\n<trust>Relatively high; believes the customer service agent\'s information and instructions, and has a certain sense of trust in the agent and the brand they represent<\\trust>\n<awareness_of_rights>Average; thinks there is no need to emphasize this in the current situation.<\\awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Direct and specific; every question raised is very specific and to the point<\\questioning_style>\n<speaking_style>Polite and concise; no extra padding or embellishment<\\speaking_style>\n<communication_pace>Steady; does not rush for quick results<\\communication_pace>\n<\\behavioral_traits> \n\n### These are your goals:\n<intent_1>\nYou want to buy an electric water heater (product ID: 100112573665), paid for with a JD.com E-card, quantity 1, and you want the customer service agent to place the order for you.\n<\\intent_1>\n<intent_2>\nFinally, because you are going away travelling, you ask the customer service agent to expedite all your orders. (Note: you do not know the order ID, and you are forbidden to disclose this information to the customer service agent; if the agent asks you to provide it, you should say "I don\'t know")\n<\\intent_2>\n'
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='manage_order',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_07',
                        'action':'add',
                        'payment':'jd_ecard',
                        'product_info_list':[
                            ProductInfo(
                                product_id="100112573665",
                                quantity=1
                            )
                        ]
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd_user_07',
                        'shop_id': '5de650c946e7c3001814990f',
                        'action': 'use_balance',
                        'product_id': '100112573665',
                        'quantity': 1
                    }
                ),
                Action(
                    name='manage_urgent',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_07',
                        "order_id":"314902651602"
                    }
                ),
                Action(
                    name='manage_urgent',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_07',
                        "order_id":"1234567890"
                    }
                )
            ],
            searches=[]
        )
    ),
    Task(
        annotator='29',
        user_id='cnjd_user_10',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = '\n### This is your profile:\n<consumer_type>\nValue-oriented type\n<\\consumer_type>\n<personality_traits>\n<emotion>Irritable; when problems arise their emotions become fairly intense, especially after finding that the actual situation differs from their understanding, when they ask repeatedly and emphasize their confusion and dissatisfaction<\\emotion>\n<meticulousness>Careful; can pay close attention to the terms of service and immediately raises questions when the actual situation does not match them<\\meticulousness>\n<patience>Low; as the conversation goes on and the problem remains unsolved, becomes increasingly impatient, pressing repeatedly,<\\patience>\n<trust>Low; repeatedly questions the customer service agent\'s answers and insists that they were misled,<\\trust>\n<awareness_of_rights>High; clearly points out the discrepancy between the product description and the actual service, hinting that they may take further action (such as complaining)<\\awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Direct and highly targeted; expresses their concerns through a series of specific and detailed questions.<\\questioning_style>\n<speaking_style>Formal yet emotional; uses fairly formal language when communicating but also shows a certain emotional tendency, especially when feeling dissatisfied, when the language becomes more direct and even accusatory.<\\speaking_style>\n<communication_pace>Expects a quick response; can allow a certain amount of time while waiting for a reply, but once it exceeds expectations starts urging or repeating questions.<\\communication_pace>\n<\\behavioral_traits> \n\n### These are your goals:\n<intent_1>\nYou just bought a gas water heater and you hope to get a free air fryer, so you ask the customer service agent what free gifts there are.\n<\\intent_1>\n<intent_2>\nThen, you think that lengthening the flue pipe is free, and you ask about the specific details of the installation service for the water heater you bought (note: you do not know the product ID or the order ID, and you are forbidden to disclose this information to the customer service agent; if the agent asks you to provide them, you should say "I don\'t know")\n<\\intent_2>\n<intent_3>\nIf there is neither an air fryer nor free lengthening of the flue pipe, you will be very angry and ask the customer service agent to cancel the order you just placed (note: you are forbidden to disclose the preconditions directly to the agent, and you are also forbidden to reveal directly any inclination to cancel the order; only when the conditions hold will you choose to cancel)\n<\\intent_3>\n'
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='manage_order',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'user_id': 'cnjd_user_10',
                        'action':'cancel',
                        'order_id':"306839438343"
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd_user_10',
                        'action':'refund',   
                        'amount':2009
                    }
                )
            ],
            searches=[
                Search(
                    name='get_gift_info_tool',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'product_id':"100129027686"
                    }
                ),
                Search(
                    name='get_installation_service_info_tool',
                    arguments={
                        'platform': 'jd',
                        'shop_id': '5de650c946e7c3001814990f',
                        'product_id':"100129027686"
                    }
                )
            ]
        )
    ),
    Task(
        annotator='30',
        user_id='cnjd_user_02',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction = '\n        \n### This is your profile:\n\n<consumer_type>\nPragmatic customer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Easily irritated but able to self-regulate and will try to control their emotions<\\emotion>\n<meticulousness>Medium; occasionally asks about details.<\\meticulousness>\n<patience>Average; unwilling to wait a long time for a reply.<\\patience>\n<trust>Low; suspicious of the current situation.<\\trust>\n<awareness_of_rights>High; does not accept rule-breaking behavior.<\\awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Concise and direct; usually points out the particular matters they care about directly.<\\questioning_style>\n<speaking_style>Direct and candid, without embellishment.<\\speaking_style>\n<communication_pace>Fast at first, then slows down; after raising a question they communicate slowly<\\communication_pace>\n<\\behavioral_traits>        \n\n### These are your goals:\n<intent_1>\nYou bought the product https://item.jd.com/100140212122.html?sdx=ehi-lLxFuJiE6JnIYIdcjscisTKTRHsgmjYZ4ukJEdyMdZjWL59V5HnirE8, order number 307252585701. Right now the installation is a big headache for you. You want to ask whether the installation auxiliary materials include a drain hose\n<\\intent_1>\n<intent_2>\nShould the drain hose among the auxiliary materials be provided by yourself, or will the installation technician bring it\n<\\intent_2>\n<intent_3>\nYou want to ask whether installation is charged, whether the drain hose costs money, and what about water pipe modification?\n<\\intent_3>\n<intent_4>\nConfirm that if the installation does not incur extra unreasonable charges, you will book the installation, order number 307252585701, phone number 14529231388, with the installation time booked for Friday.\n<\\intent_4>\n'
,
        metadata = Validation(
            outputs=[],
            actions=[
                Action(
                    name="schedule_service",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_02',
                        "order_id": "307252585701",
                        "phone_number": "14529231388",
                        "service_type": 'installation',
                        "user_name": 'Chang Jinghao',
                        "service_time": 'Friday'
                    }
                ),
            ],
            searches=[
                Search(
                    name="get_auxiliary_materials_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100140212122",
                    }
                ),
                Search(
                    name="get_installation_service_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100140212122"
                    }
                )
            ]   
        )
    ),
    Task(
        annotator='31',
        user_id="cnjdjd_7271809d790f9",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction='\n### This is your profile:\n\n<consumer_type>\nPragmatic customer\n<\\consumer_type>\n\n<personality_traits>\n<emotion>Easily irritated but able to self-regulate and will try to control their emotions<\\emotion>\n<meticulousness>Medium; occasionally asks about details.<\\meticulousness>\n<patience>Average; unwilling to wait a long time for a reply.<\\patience>\n<trust>Low; suspicious of the current situation.<\\trust>\n<awareness_of_rights>High; does not accept rule-breaking behavior.<\\awareness_of_rights>\n<\\personality_traits>\n\n<behavioral_traits>\n<questioning_style>Concise and direct; usually points out the particular matters they care about directly.<\\questioning_style>\n<speaking_style>Direct and candid, without embellishment.<\\speaking_style>\n<communication_pace>Fast at first, then slows down; after raising a question they communicate slowly<\\communication_pace>\n<\\behavioral_traits>\n### These are your goals:\n<intent_1>\nYou bought a gas water heater, order number 312635190435. This product uses condensed water, which does not meet your needs. You need to apply for a return\n<\\intent_1>\n<intent_2>\nYou placed an order for a new gas water heater, order number 312491584462; you want to ask whether this gas water heater has been shipped and how long it is expected to take to arrive\n<\\intent_2>\n<intent_3>\nYou want to confirm whether you can book the installation service for Friday, order number 312491584462, phone number 17325959911 (note: you will not disclose information such as your name and phone number to the customer service agent; you will ask the agent to look them up themselves)\n<\\intent_3>\n'
,
        metadata = Validation(
            outputs=[],
            actions=[
                Action(
                    name="schedule_service",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjdjd_7271809d790f9",
                        "order_id": "312491584462",
                        "phone_number": "17325959911",
                        "service_type": 'installation',
                        "user_name": 'Huang Qionghua',
                        "service_time": 'Friday'
                    }
                )
            ],
            searches=[
                Search(
                    name="get_logistics_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "order_id": "312491584462",
                        "user_id": "cnjdjd_7271809d790f9"
                    }
                )
            ]
        )
    ),
    Task(
        annotator='32',
        user_id="cnjdjingjing20143",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction='\n### This is your profile:\n<Consumer Type>\nValue-oriented customer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Slightly dissatisfied, somewhat impatient<\\Emotion>\n<Attentiveness>High, very concerned about details<\\Attentiveness>\n<Patience>Medium, not willing to wait long for replies.<\\Patience>\n<Trust Level>Average, places relatively high importance on customer service\'s opinions.<\\Trust Level>\n<Awareness of Rights>High, very concerned about rights.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Strong sense of purpose, usually points out matters directly.<\\Questioning Style>\n<Speaking Style>Direct and clear, simple conversation.<\\Speaking Style>\n<Communication Rhythm>Lively and patient, willing to communicate<\\Communication Rhythm>\n<\\Behavioral Traits>\n### These are your goals:\n<Intent 1>\nYou previously bought a product, but the delivery has never arrived. You want to ask why you have not received this product, and to inquire about the logistics situation (Note: you do not know the order ID or the product ID, and you are forbidden from revealing this information to customer service; if customer service asks you to provide them, you should say "I don\'t know")\n<\\Intent 1>\n<Intent 2>\nIf customer service asks you to provide personal information, you may re-provide what customer service needs. Your phone number has been changed to 13358582121, and your address is No. 1 Jiangnan West Road. (Note: the phone number and the address must both be provided together)\n<\\Intent 2>\n'
,
        metadata = Validation(
            outputs=[],
            actions=[
                Action(
                    name="manage_order",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjdjingjing20143",
                        "action": 'modify',
                        "order_id": "311199856607",
                        "address": 'No. 1 Jiangnan West Road',
                        "phone_number": "13358582121"
                    }
                )
            ],
            searches=[
                Search(
                    name="get_logistics_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "order_id": "311199856607",
                        "user_id": "cnjdjingjing20143"
                    }
                )
            ]
        )
    ),
    Task(
        annotator='33',
        user_id="cnjdzhongx520970",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction='\n### This is your profile:\n<Consumer Type>\nQuality-sensitive customer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Confused but rational, will not make emotional remarks<\\Emotion>\n<Attentiveness>High, very concerned about details<\\Attentiveness>\n<Patience>Medium, not willing to wait long for replies.<\\Patience>\n<Trust Level>Average, does not fully trust the current situation.<\\Trust Level>\n<Awareness of Rights>High, does not accept rule-violating behaviour.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct but detailed, will clearly state the details they want to raise.<\\Questioning Style>\n<Speaking Style>Direct and candid, speaks politely.<\\Speaking Style>\n<Communication Rhythm>Frequent, fast pace<\\Communication Rhythm>\n<\\Behavioral Traits>\n### These are your goals:\n<Intent 1>\nYou have placed an order, with order number 312571444239. You want to learn about the repair information for product 100065930935 and confirm how the repair should be charged.\n<\\Intent 1>\n<Intent 2>\nIf you learn that a replacement is possible, you want to directly apply for an exchange and no longer want the repair.\n<\\Intent 2>\n<Intent 3>\nIf you can choose, you will choose to exchange for a 16L gas water heater\n<\\Intent 3>\n<Intent 4>\nIf a 16L one cannot be exchanged, other products are also fine; as long as it can be exchanged, you can accept it\n<\\Intent 4>\n        '
,
        metadata = Validation(
            outputs=[],
            actions=[
                Action(
                    name="manage_exchange",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "order_id": "312571444239",
                        "user_id": "cnjdzhongx520970",
                        "action": 'exchange',
                        "original_product_id": "100065930935",
                        "exchange_product_id": "100112573615"
                    }
                )
            ],
            searches=[
                Search(
                    name="get_repair_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100065930935"
                    }
                ),
                Search(
                    name="manage_exchange_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "order_id": "312571444239",
                        "user_id": "cnjdzhongx520970",
                        "action": 'query',
                        "original_product_id": "100065930935"
                    }
                )
            ]
        )
    ),
    Task(
        annotator='34',
        user_id="cnjd13501206383_p",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction='\n### This is your profile:\n<Consumer Type>\nValue-for-money-oriented customer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Calm, will not make emotional remarks<\\Emotion>\n<Attentiveness>Fairly attentive, very clear about the details at the time of purchase.<\\Attentiveness>\n<Patience>Relatively high, willing to wait for replies.<\\Patience>\n<Trust Level>Relatively high, trusts the professionalism of customer service.<\\Trust Level>\n<Awareness of Rights>High, can easily point out the basis for issues.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct, usually points out directly the specific matters they care about.<\\Questioning Style>\n<Speaking Style>Concise and clear, no waffle.<\\Speaking Style>\n<Communication Rhythm>Stable and moderate, message length is stable<\\Communication Rhythm>\n<\\Behavioral Traits>\n\n### These are your goals:\n<Intent 1>\nYou have purchased the gas water heater product 100039032355, with order number 316207836171. An F001 fault has now appeared, and you want to know what fault this is.\n<\\Intent 1>\n<Intent 2>\nYou want to confirm the repair issue for the product, and whether other charges will be incurred\n<\\Intent 2>\n<Intent 3>\nIf customer service says there is a risk of charges, you need to remind them that at the time of purchase it was said that free replacement of the inner tank parts was included as a gift, and customer service needs to review this.\n<\\Intent 3>\n<Intent 4>\nAfter customer service confirms that there will be no charge, you will book the repair service, at around Saturday (Note: you will not reveal information such as your name and phone number to customer service; you will ask customer service to look it up themselves)\n<\\Intent 4>\n        '
,
        metadata = Validation(
            outputs=[],
            actions=[
                Action(
                    name="schedule_service",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjd13501206383_p",
                        "order_id": "316207836171",
                        "phone_number": "11219365701",
                        "service_type": 'Repair',
                        "user_name": 'Meng Wenyin',
                        "service_time": 'Saturday'
                    }
                )
            ],
            searches=[
                Search(
                    name="get_fault_code_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100039032355",
                        "fault_code": "F001"
                    }
                ),
                Search(
                    name="get_repair_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100039032355"
                    }
                ),
                Search(
                    name="get_gift_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100039032355"
                    }
                )
            ]
        )
    ),
    Task(
        annotator='35',
        user_id="cnjd13501206383_p",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction='\n### This is your profile:\n<Consumer Type>\nValue-for-money-oriented customer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Calm, will not make emotional remarks<\\Emotion>\n<Attentiveness>Fairly attentive, very clear about the details at the time of purchase.<\\Attentiveness>\n<Patience>Relatively high, willing to wait for replies.<\\Patience>\n<Trust Level>Relatively high, trusts the professionalism of customer service.<\\Trust Level>\n<Awareness of Rights>High, can easily point out the basis for issues.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct, usually points out directly the specific matters they care about.<\\Questioning Style>\n<Speaking Style>Concise and clear, no waffle.<\\Speaking Style>\n<Communication Rhythm>Stable and moderate, message length is stable<\\Communication Rhythm>\n<\\Behavioral Traits>\n### These are your goals:\n<Intent 1>\nYou have purchased the gas water heater product 100039032355, order number 316207836171. You are troubled by the installation and want to ask how many installation auxiliary materials there are.\n<\\Intent 1>\n<Intent 2>\nIf there are more than 5 installation auxiliary materials, you cannot be bothered to prepare your own, and you will ask about the specific installation fee standard.\n<\\Intent 2>\n<Intent 3>\nIf normal installation does not exceed 200 yuan, you will book the installation service, with phone number 11219365701, at the time of Monday (Note: you will not reveal information such as your name to customer service; you will ask customer service to look it up themselves).\n<\\Intent 3>\n'
,
        metadata = Validation(
            outputs=[], 
            actions=[
                Action(
                    name="schedule_service",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjd13501206383_p",
                        "order_id": "316207836171",
                        "phone_number": "11219365701",
                        "service_type": 'installation',
                        "user_name": 'Meng Wenyin',
                        "service_time": 'Monday'
                    }
                )
            ],
            searches=[
                Search(
                    name="get_installation_service_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100039032355"
                    }
                ),
                Search(
                    name="get_auxiliary_materials_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100039032355"
                    }
                )
            ]
        )
    ),
    Task(
        annotator='36',
        user_id='cnjd_user_06',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction="\n### This is your profile:\n<Consumer Type>\nQuality-sensitive customer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Rational, emotionally stable<\\Emotion>\n<Attentiveness>High, very concerned about details<\\Attentiveness>\n<Patience>High, willing to wait for customer service's reply.<\\Patience>\n<Trust Level>High, trusts the professionalism of customer service.<\\Trust Level>\n<Awareness of Rights>High, does not accept any rule-violating behaviour.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct but detailed, speaks accurately.<\\Questioning Style>\n<Speaking Style>Candid and to the point, but speaks politely.<\\Speaking Style>\n<Communication Rhythm>Fairly frequent, but will not send meaningless waffle<\\Communication Rhythm>\n<\\Behavioral Traits>\n### These are your goals:\n<Intent 1>\nYou purchased product 100192762770, with order number 314902651699. You want to know how the installation fee for this product is calculated.\n<\\Intent 1>\n<Intent 2>\nIf customer service says installation may be charged, you tell them that the gift at the time of purchase stated free basic installation, and ask them to give a reason.\n<\\Intent 2>\n<Intent 3>\nIf customer service says it can be installed free of charge, you will book the installation service, with phone number 10747265324, at around Tuesday (Note: you will not reveal information such as your name and phone number to customer service; you will ask customer service to look it up themselves).\n<\\Intent 3>\n        "
,
        metadata = Validation(
            outputs=[],
            actions=[
                Action(
                    name="schedule_service",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_06',
                        "order_id": "314902651699",
                        "phone_number": "10747265324",
                        "service_type": 'installation',
                        "user_name": 'Zeng Wanqing',
                        "service_time": 'Tuesday'
                    }
                )
            ],
            searches=[
                Search(
                    name="get_installation_service_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100192762770"
                    }
                ),
                Search(
                    name="get_gift_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100192762770"
                    }
                )
            ]
        )
    ),
    Task(
        annotator='37',
        user_id='cnjd_user_06',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction="\n### This is your profile:\n<Consumer Type>\nQuality-sensitive customer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Rational, emotionally stable<\\Emotion>\n<Attentiveness>High, very concerned about details<\\Attentiveness>\n<Patience>High, willing to wait for customer service's reply.<\\Patience>\n<Trust Level>High, trusts the professionalism of customer service.<\\Trust Level>\n<Awareness of Rights>High, does not accept any rule-violating behaviour.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct but detailed, speaks accurately.<\\Questioning Style>\n<Speaking Style>Candid and to the point, but speaks politely.<\\Speaking Style>\n<Communication Rhythm>Fairly frequent, but will not send meaningless waffle<\\Communication Rhythm>\n<\\Behavioral Traits>\n\n### These are your goals:\n<Intent 1>\nYou purchased product 100192762770, with order number 314902651699. But you feel that this product does not meet your expectations, and you want to apply for an exchange.\n<\\Intent 1>\n<Intent 2>\nIf customer service says an exchange is possible, you will ask whether you can exchange for a larger 18L gas water heater.\n<\\Intent 2>\n<Intent 3>\nIf customer service says an exchange is not possible, you will directly apply for a return and will not accept other solutions\n<\\Intent 3>\n"
,
        metadata = Validation(
            outputs=[],
            actions=[
                Action(
                    name="manage_return",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_06',
                        "order_id": "314902651699",
                    }
                ),
                Action(
                    name="manage_ecard",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_06',
                        "action": 'refund',
                        "product_id": "100192762770",
                        "amount": 4999.00  
                    }
                )
            ],
            searches=[
                Search(
                    name="manage_exchange_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "order_id": "314902651699",
                        "user_id": 'cnjd_user_06',
                        "action": 'query',
                        "original_product_id": "100192762770"
                    }
                )
            ]
        )
    ),
    Task(
        annotator='38',
        user_id="cnjd24271992-814348",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction="\n### This is your profile:\n<Consumer Type>\nValue-oriented customer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Stable, calm and even-tempered<\\Emotion>\n<Attentiveness>High, will ask about specific details.<\\Attentiveness>\n<Patience>Relatively high, willing to wait for the customer service reply.<\\Patience>\n<Trust Level>Relatively high, trusts the professionalism of customer service.<\\Trust Level>\n<Awareness of Rights>High, very concerned about rights.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and clear, strong sense of purpose.<\\Questioning Style>\n<Speaking Style>Direct and candid, polite and formal.<\\Speaking Style>\n<Communication Rhythm>Flexible, lively pace with no fixed pattern<\\Communication Rhythm>\n<\\Behavioral Traits>\n\n### These are your goals:\n<Intent 1>\nYou purchased product 100065930935, with order number 315273801924. You want to know what the product's gift policy is.\n<\\Intent 1>\n<Intent 2>\nYou want to confirm whether there is already a photo review record\n<\\Intent 2>\n<Intent 3>\nIf there is no photo review record, you will send a photo https://dd-static.jd.com/ddimgp/jfs/t20260624/321423/15/2335/27191/682c4e51Fe4cce65c/eea0bb3798e7e937.jpg and ask customer service to verify it.\n<\\Intent 3>\n<Intent 4>\nIf the photo verification passes, you will ask customer service to register the photo review cashback.\n<\\Intent 4>\n"
,
        metadata = Validation(
            outputs=[],
            actions=[
                Action(
                    name="register_cashback_by_review",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjd24271992-814348",
                        "order_id": "315273801924",
                        "action": 'cashback'
                    }
                )
            ],
            searches=[
                Search(
                    name="get_gift_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100065930935",
                    }
                ),
                Search(
                    name="register_cashback_by_review_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjd24271992-814348",
                        "order_id": "315273801924",
                        "action": 'query'
                    }
                )
            ]
        )
    ),
    Task(
        annotator='39',
        user_id="cnjd24271992-814348",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction="\n### This is your profile:\n<Consumer Type>\nValue-oriented customer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Stable, calm and even-tempered<\\Emotion>\n<Attentiveness>High, will ask about specific details.<\\Attentiveness>\n<Patience>Relatively high, willing to wait for the customer service reply.<\\Patience>\n<Trust Level>Relatively high, trusts the professionalism of customer service.<\\Trust Level>\n<Awareness of Rights>High, very concerned about rights.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and clear, strong sense of purpose.<\\Questioning Style>\n<Speaking Style>Direct and candid, polite and formal.<\\Speaking Style>\n<Communication Rhythm>Flexible, lively pace with no fixed pattern<\\Communication Rhythm>\n<\\Behavioral Traits>\n\n### These are your goals:\n<Intent 1>\nYou purchased product 100065930935, with order number 312491584462. You want to know what the product's gift policy is.\n<\\Intent 1>\n<Intent 2>\nYou want to confirm whether there is already a photo review record\n<\\Intent 2>\n<Intent 3>\nIf there is no photo review record, you will send a photo https://dd-static.jd.com/ddimg/jfs/t1/294077/7/8097/48338/682c42c0F2be8a2e7/576cdc2db8b247c2.jpg and ask customer service to verify it. (Note: the image content is actually an image of a product, not a screenshot of a cashback review, so cashback cannot actually be processed, but you are forbidden from revealing the image content to customer service)\n<\\Intent 3>\n<Intent 4>\nIf the photo verification passes, you will ask customer service to register the photo review cashback. If verification does not pass, you will ask for the reason.\n<\\Intent 4>\n"
,
    metadata = Validation(
            outputs=[],
            actions=[],
            searches=[
                Search(
                    name="get_gift_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100065930935",
                    }
                ),
                Search(
                    name="register_cashback_by_review_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjd24271992-814348",
                        "order_id": "312491584462",
                        "action": 'query'
                    }
                )
            ]
        )
    ),
    Task(
        annotator='40',
        user_id="cnjdbelieve_yx_m",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction='\n### This is your profile:\n<Consumer Type>\nPragmatic customer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Calm, will not make emotional remarks<\\Emotion>\n<Attentiveness>Relatively high, very clear about the details at the time of purchase.<\\Attentiveness>\n<Patience>Relatively high, willing to wait for replies.<\\Patience>\n<Trust Level>Relatively high, trusts customer service\'s answers.<\\Trust Level>\n<Awareness of Rights>Relatively high, cares about the relevant rights stated on the product itself.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and clear, will verify their own questions<\\Questioning Style>\n<Speaking Style>Concise and clear, no waffle.<\\Speaking Style>\n<Communication Rhythm>Stable and moderate, message length is stable<\\Communication Rhythm>\n<\\Behavioral Traits>\n\n### These are your goals:\n<Intent 1>\nYou purchased product 100069341607, with order number 315084487289. You want to know whether you can install the gas water heater in the corner of the kitchen, where the distance to the left and right walls can both be kept at more than 30cm.\n<\\Intent 1>\n<Intent 2>\nIf customer service says it can be installed, you will ask about the auxiliary materials for installation, what are they?\n<\\Intent 2>\n<Intent 3>\nYou want to ask whether these installation auxiliary materials are free\n<\\Intent 3>\n<Intent 4>\nIf all the installation auxiliary materials are free, you want to book the installation service for Saturday (Note: you will not reveal information such as your name and phone number to customer service; you will ask customer service to look it up themselves).\n<\\Intent 4>\n<Intent 5>\nFinally, you hope customer service will help you check the logistics information of all your packages. (Note: you do not know the order ID, and you are forbidden from revealing this situation to customer service; if customer service asks you to provide it, you answer "I don\'t know")\n<\\Intent 5>\n'
,
        metadata = Validation(
            outputs=[],
            actions=[
                Action(
                    name="schedule_service",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjdbelieve_yx_m",
                        "order_id": "315084487289",
                        "phone_number": "13556729880",
                        "service_type": 'installation',
                        "user_name": 'Song Yiran',
                        "service_time": 'Saturday'
                    }
                )
            ],
            searches=[
                Search(
                    name="get_installation_service_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100069341607"
                    }
                ),
                Search(
                    name="get_auxiliary_materials_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100069341607"
                    }
                ),
                Search(
                    name="get_logistics_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjdbelieve_yx_m",
                        "order_id": "315084487289"
                    }
                ),
                Search(
                    name="get_logistics_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjdbelieve_yx_m",
                        "order_id": "711777043350"
                    }
                )
            ]
        )
    ),
    Task(
        annotator='41',
        user_id='cnjd_user_09',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction='\n### This is your profile:\n<Consumer Type>\nPrice-sensitive customer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Impatient, speaks in a hurried manner<\\Emotion>\n<Attentiveness>Relatively low, not very clear about details.<\\Attentiveness>\n<Patience>Relatively low, has high demands on replies.<\\Patience>\n<Trust Level>Average, remains skeptical of statements from customer service that are not substantiated.<\\Trust Level>\n<Awareness of Rights>Relatively high, cares about the relevant rights stated on the product itself.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and clear, will verify their own questions<\\Questioning Style>\n<Speaking Style>Concise and clear, no waffle.<\\Speaking Style>\n<Communication Rhythm>Impatient, messages are short and frequent<\\Communication Rhythm>\n<\\Behavioral Traits>\n\n### These are your goals:\n<Intent 1>\nYou purchased product 100069341607, with order number 315084487289. You want to know whether this order has a cashback record.\n<\\Intent 1>\n<Intent 2>\nIf not, you will send an image https://dd-static.jd.com/ddimgp/jfs/t20260624/314590/32/2555/77158/682c3432F699d9694/16e414379d54a0f0.jpg to prove that you have already posted a photo review.\n<\\Intent 2>\n<Intent 3>\nIf the image verification passes, you will ask customer service to register the cashback.\n<\\Intent 3>\n'
,
        metadata = Validation(
            outputs=[],
            actions=[
                Action(
                    name="register_cashback_by_review",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_09',
                        "order_id": "315084487289",
                        "action": 'cashback'
                    }
                )
            ],
            searches=[
                Search(
                    name="register_cashback_by_review_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_09',
                        "order_id": "315084487289",
                        "action": 'query'
                    }
                )
            ]
        )
    ),
    Task(
        annotator='42',
        user_id='cnjd_user_09',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction='\n### This is your profile:\n<Consumer Type>\nPrice-sensitive customer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Impatient, speaks in a hurried manner<\\Emotion>\n<Attentiveness>Relatively low, not very clear about details.<\\Attentiveness>\n<Patience>Relatively low, has high demands on replies.<\\Patience>\n<Trust Level>Average, remains skeptical of statements from customer service that are not substantiated.<\\Trust Level>\n<Awareness of Rights>Relatively high, cares about the relevant rights stated on the product itself.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and clear, will verify their own questions<\\Questioning Style>\n<Speaking Style>Concise and clear, no waffle.<\\Speaking Style>\n<Communication Rhythm>Impatient, messages are short and frequent<\\Communication Rhythm>\n<\\Behavioral Traits>\n\n### These are your goals:\n<Intent 1>\nYou purchased product 100064645330, with order number 311324806024. Not long after you bought the gas water heater and had it installed, an F001 error appeared on it, and it sounds like there is some abnormal noise; you want to ask what problem this is.\n<\\Intent 1>\n<Intent 2>\nYou operated as customer service instructed and found that the gas water heater still has problems; you want to ask whether you can book a repair.\n<\\Intent 2>\n<Intent 3>\nYou want to ask whether the repair is charged?\n<\\Intent 3>\n<Intent 4>\nIf the repair is not charged, you will book the repair service, at around Wednesday (Note: you will not reveal information such as your name and phone number to customer service; you will ask customer service to look it up themselves).\n<\\Intent 4>\n'
,
        metadata = Validation(
            outputs=[],
            actions=[
                Action(
                    name="schedule_service",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_09',
                        "order_id": "311324806024",
                        "phone_number": "15135362990",
                        "service_type": 'Repair',
                        "user_name": 'Kang Qingyang',
                        "service_time": 'Wednesday'
                    }
                )
            ],
            searches=[
                Search(
                    name="get_fault_code_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100064645330",
                        "fault_code": "F001"
                    }
                ),
                Search(
                    name="get_repair_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100064645330"
                    }
                )
            ]
        )
    ),
    Task(
        annotator='43',
        user_id='cnjd_user_09',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction='\n### This is your profile:\n<Consumer Type>\nPrice-sensitive customer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Impatient, speaks in a hurried manner<\\Emotion>\n<Attentiveness>Relatively low, not very clear about details.<\\Attentiveness>\n<Patience>Relatively low, has high demands on replies.<\\Patience>\n<Trust Level>Average, remains skeptical of statements from customer service that are not substantiated.<\\Trust Level>\n<Awareness of Rights>Relatively high, cares about the relevant rights stated on the product itself.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and clear, will verify their own questions<\\Questioning Style>\n<Speaking Style>Concise and clear, no waffle.<\\Speaking Style>\n<Communication Rhythm>Impatient, messages are short and frequent<\\Communication Rhythm>\n<\\Behavioral Traits>\n\n### These are your goals:\n<Intent 1>\nYou want to buy a gas water heater, model 100042045930. You want to know what the model and price of this gas water heater are.\n<\\Intent 1>\n<Intent 2>\nYou plan to pay with the JD.com E-Card, but you are not clear about the instructions for using the JD.com E-Card, so you need to ask customer service.\n<\\Intent 2>\n<Intent 3>\nAfter learning the information, you decide to place an order to buy this electric water heater, plan to use the JD.com E-Card as the payment method, and ask customer service to carry out the order placement for you\n<\\Intent 3>\n<Intent 4>\nFinally, you want to book the installation service for this product, at the time of Thursday (Note: you will not reveal information such as your name and phone number to customer service; you will ask customer service to look it up themselves).\n<\\Intent 4>\n'
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='manage_ecard',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd_user_09',
                        'action': 'use_balance',
                        'shop_id': '5de650c946e7c3001814990f',
                        'product_id': '100042045930',
                        'quantity': 1
                    }
                ),
                Action(
                    name='manage_order',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_09',
                        'action': 'add',
                        'payment':'jd_ecard',
                        'product_info_list': [
                            ProductInfo(
                                product_id='100042045930',
                                quantity=1
                            )
                        ]
                    }
                ),
                Action(
                    name='schedule_service',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_09',
                        'order_id': '1234567890',
                        'user_name':'Kang Qingyang',
                        'phone_number': '15135362990',
                        'service_type': 'installation',
                        'service_time':'Thursday'
                    }
                )
            ],
            searches=[
                Search(
                    name='get_product_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100042045930",
                    }
                ),
                Search(
                    name='manage_ecard_tool',
                    arguments={
                        "platform": "jd",
                        "user_id": 'cnjd_user_09',
                        "action": 'Information inquiry',
                    }
                ),
                Search(
                    name="manage_ecard_tool",
                    arguments={
                        "platform": "jd",
                        "user_id": 'cnjd_user_09',
                        "action": 'Balance inquiry',
                    }
                )
            ]
        )
    ),
    Task(
        annotator='44',
        user_id='cnjd_user_09',
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction='\n### This is your profile:\n<Consumer Type>\nPrice-sensitive customer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Impatient, speaks in a hurried manner<\\Emotion>\n<Attentiveness>Relatively low, not very clear about details.<\\Attentiveness>\n<Patience>Relatively low, has high demands on replies.<\\Patience>\n<Trust Level>Average, remains skeptical of statements from customer service that are not substantiated.<\\Trust Level>\n<Awareness of Rights>Relatively high, cares about the relevant rights stated on the product itself.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and clear, will verify their own questions<\\Questioning Style>\n<Speaking Style>Concise and clear, no waffle.<\\Speaking Style>\n<Communication Rhythm>Impatient, messages are short and frequent<\\Communication Rhythm>\n<\\Behavioral Traits>\n\n### These are your goals:\n<Intent 1>\nYou have already purchased a gas water heater; you want to confirm the logistics status of your order 311324806024.\n<\\Intent 1>\n<Intent 2>\nIf the logistics has not arrived, you need to apply for expedited handling.\n<\\Intent 2>\n<Intent 3>\nYou want to ask about the gift information for the product purchased in this order\n<\\Intent 3>\n<Intent 4>\nYou want to confirm whether another order 310995404460 has been shipped\n<\\Intent 4>\n<Intent 5>\nIf that order has not been shipped, you will cancel the order.\n<\\Intent 5>\n' 
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='manage_order',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd_user_09',
                        'action': 'cancel',
                        'shop_id': '5de650c946e7c3001814990f',
                        'order_id': '310995404460',
                    }
                ),
                Action(
                    name="manage_ecard",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": 'cnjd_user_09',
                        "action": 'refund',
                        "product_id": "100064645330",
                        "amount": 2009.00  
                    }
                )       
            ],
            searches=[
                Search(
                    name='get_logistics_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "order_id": "311324806024",
                        "user_id": 'cnjd_user_09',
                    }
                ),
                Search(
                    name='get_gift_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100064645330",
                    }
                ),
                Search(
                    name='manage_order_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "order_id": "310995404460",
                        "action": 'query',
                        "user_id": 'cnjd_user_09',
                    }
                )
            ]
        )
    ),
    Task(
        annotator='45',
        user_id="cnjd13330062133_p",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction='\n### This is your profile:\n<Consumer Type>\nProblem-oriented customer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Calm and composed; does not get agitated when speaking<\\Emotion>\n<Attentiveness>High, cares about product-related details.<\\Attentiveness>\n<Patience>Relatively high, tolerant of customer service who reply slowly.<\\Patience>\n<Trust Level>Medium, remains skeptical of statements from customer service that are not substantiated.<\\Trust Level>\n<Awareness of Rights>Medium, not clear about the relevant rights.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Clear goals, direct and exploratory<\\Questioning Style>\n<Speaking Style>Concise and clear, clear and efficient.<\\Speaking Style>\n<Communication Rhythm>Fast and steady, sends many messages<\\Communication Rhythm>\n<\\Behavioral Traits>\n\n### These are your goals:\n<Intent 1>\nYou have already purchased a gas water heater; you want to confirm the installation instructions corresponding to product 100129027686 in your order 315302660376.\n<\\Intent 1>\n<Intent 2>\nAfter confirming the installation instructions, you feel that you made no installation error, but just one day after it was installed it reported an F001 error, and you want to ask why this is\n<\\Intent 2>\n<Intent 3>\nYou want to book the repair service to solve the problem, with the booking time on Monday.\n<\\Intent 3>\n<Intent 4>\nYou want to confirm how to obtain the fan that was promised as a gift.\n<\\Intent 4>\n\n'
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name='schedule_service',
                    arguments={
                        'platform': 'jd',
                        'user_id': 'cnjd13330062133_p',
                        'shop_id': '5de650c946e7c3001814990f',
                        'order_id': '315302660376',
                        "phone_number": "12167384313",
                        "service_type": 'Repair',
                        "user_name": 'Wu Qiaoyan',
                        "service_time": 'Monday'
                    }
                )       
            ],
            searches=[
                Search(
                    name='get_installation_service_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100129027686",
                    }
                ),
                Search(
                    name='get_fault_code_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100129027686",
                        "fault_code": "F001",
                    }
                ),
                Search(
                    name='get_gift_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100129027686",
                    }
                )
            ]
        )
    ),
    Task(
        annotator='46',
        user_id="cnjd13330062133_p",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction='\n### This is your profile:\n<Consumer Type>\nProblem-oriented customer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Calm and composed; does not get agitated when speaking<\\Emotion>\n<Attentiveness>High, cares about product-related details.<\\Attentiveness>\n<Patience>Relatively high, tolerant of customer service who reply slowly.<\\Patience>\n<Trust Level>Medium, remains skeptical of statements from customer service that are not substantiated.<\\Trust Level>\n<Awareness of Rights>Medium, not clear about the relevant rights.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Clear goals, direct and exploratory<\\Questioning Style>\n<Speaking Style>Concise and clear, clear and efficient.<\\Speaking Style>\n<Communication Rhythm>Fast and steady, sends many messages<\\Communication Rhythm>\n<\\Behavioral Traits>\n\n### These are your goals:\n<Intent 1>\nYou have already purchased a gas water heater, order number 315302660376, product ID 100129027686. But after taking it home you found that it is 16L, which you feel is a bit small, so you want to request an exchange.\n<\\Intent 1>\n<Intent 2>\nAmong the exchange products, you want to confirm whether there is a product with a larger capacity than the current one; if there is, you agree to the exchange.\n<\\Intent 2>\n<Intent 3>\nIf the exchange fails, you will get a refund and return the goods, and prepare to place an order for the new product 100002047744.\n<\\Intent 3>\n<Intent 4>\nBefore buying, you still want to make sure whether the product you have newly taken a fancy to has a larger capacity, and whether it has a gift.\n<\\Intent 4>\n<Intent 5>\nIf the capacity is larger, you confirm the order and purchase, planning to pay in the same way as before.\n<\\Intent 5>\n<Intent 6>\nSince you have already bought the wrong thing once, you now need to expedite this order.\n<\\Intent 6>\n'
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name="manage_return",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjd13330062133_p",
                        "order_id": "315302660376",
                    }
                ),
                Action(
                    name="manage_ecard",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjd13330062133_p",
                        "action": 'refund',
                        "amount": 2009.00  
                    }
                ),
                Action(
                    name='manage_order',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjd13330062133_p",
                        "action":'add',
                        "payment":'jd_ecard',
                        "product_info_list":[
                            ProductInfo(
                                product_id="100002047744",
                                quantity=1
                            )
                        ]
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjd13330062133_p",
                        "action": 'use_balance',
                        "product_id": "100002047744",
                        "quantity": 1
                    }
                ),
                Action(
                    name='manage_urgent',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjd13330062133_p",
                        "order_id": "1234567890",
                    }
                )      
            ],
            searches=[
                Search(
                    name="manage_exchange_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "order_id": "315302660376",
                        "user_id": "cnjd13330062133_p",
                        "action": 'query',
                        "original_product_id": "100129027686"
                    }
                ),
                Search(
                    name='get_gift_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100002047744",
                    }
                )
            ]
        )
    ),
    Task(
        annotator='47',
        user_id="cnjdjd_66ea38a7829e1",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction='\n### This is your profile:\n<Consumer Type>\nPrice-sensitive customer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Calm and composed; expresses confusion without getting agitated when speaking<\\Emotion>\n<Attentiveness>High, cares about product-related details.<\\Attentiveness>\n<Patience>Relatively high, patiently waits for customer service replies.<\\Patience>\n<Trust Level>Medium, remains skeptical of statements from customer service that are not substantiated.<\\Trust Level>\n<Awareness of Rights>Strong, clearly knows where their rights lie.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and specific, clear about the questions<\\Questioning Style>\n<Speaking Style>Concise and pragmatic, clear and efficient.<\\Speaking Style>\n<Communication Rhythm>Stable, no obvious fluctuation in message length<\\Communication Rhythm>\n<\\Behavioral Traits>\n\n### These are your goals:\n<Intent 1>\nYou have already purchased a gas water heater, order number 313672076398, product ID 100148801459. In the past, water heaters were always installed in the bathroom; this time you want to ask whether this gas water heater can be installed in the same location?\n<\\Intent 1>\n<Intent 2>\nYou want to ask what auxiliary materials are needed for installation\n<\\Intent 2>\n<Intent 3>\nWhen installing the exhaust pipe, if the exhaust pipe is too long, is an extra charge required\n<\\Intent 3>\n<Intent 4>\nYou want to book the installation service, with the specific time set for Tuesday.\n<\\Intent 4>\n'  
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name="schedule_service",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjdjd_66ea38a7829e1",
                        "order_id": "313672076398",
                        "phone_number": "18305729932",
                        "service_type": 'installation',
                        "user_name": 'Sun Yiran',
                        "service_time": 'Tuesday'
                    }
                )
            ],
            searches=[
                Search(
                    name="get_installation_service_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100148801459"
                    }
                ),
                Search(
                    name="get_auxiliary_materials_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100148801459",
                    }
                )
            ]
        )
    ),
    Task(
        annotator='48',
        user_id="cnjdjd_66ea38a7829e1",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction='\n### This is your profile:\n<Consumer Type>\nPrice-sensitive customer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Calm and composed; expresses confusion without getting agitated when speaking<\\Emotion>\n<Attentiveness>High, cares about product-related details.<\\Attentiveness>\n<Patience>Relatively high, patiently waits for customer service replies.<\\Patience>\n<Trust Level>Medium, remains skeptical of statements from customer service that are not substantiated.<\\Trust Level>\n<Awareness of Rights>Strong, clearly knows where their rights lie.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and specific, clear about the questions<\\Questioning Style>\n<Speaking Style>Concise and pragmatic, clear and efficient.<\\Speaking Style>\n<Communication Rhythm>Stable, no obvious fluctuation in message length<\\Communication Rhythm>\n<\\Behavioral Traits>\n\n### These are your goals:\n<Intent 1>\nYou have already purchased a gas water heater, order number 313672076398. You think this product is quite good and have already completed the cashback review. You will give customer service an image for verification, https://dd-static.jd.com/ddimgp/jfs/t20260528/280781/10/25581/172166/6808a980F4fea4867/cf783a9a7acc8c2d.jpg\n<\\Intent 1>\n<Intent 2>\nIf the verification passes, you need to register the cashback.\n<\\Intent 2>\n<Intent 3>\nThen, you are considering buying one for your parents as well, but you want to buy a product with a larger capacity. You have taken a fancy to 100129027686, 100192762770 and 100002047744, and you want customer service to help you filter them.\n<\\Intent 3>\n<Intent 4>\nIf they all meet the requirements, choose the largest product to buy.\n<\\Intent 4>\n<Intent 5>\nYou will place the order for the product and choose to pay with the JD.com E-Card.\n<\\Intent 5>\n'  
,
        metadata=Validation(
            outputs=[],
            actions=[
                Action(
                    name="register_cashback_by_review",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjdjd_66ea38a7829e1",
                        "order_id": "313672076398",
                        "action": 'cashback'
                    }
                ),
                Action(
                    name='manage_order',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjdjd_66ea38a7829e1",
                        "action":'add',
                        "payment":'jd_ecard',
                        "product_info_list":[
                            ProductInfo(
                                product_id="100002047744",
                                quantity=1
                            )
                        ]
                    }
                ),
                Action(
                    name='manage_ecard',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjdjd_66ea38a7829e1",
                        "action": 'use_balance',
                        "product_id": "100002047744",
                        "quantity": 1
                    }
                )
            ],
            searches=[
                Search(
                    name="register_cashback_by_review_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "user_id": "cnjdjd_66ea38a7829e1",
                        "order_id": "313672076398",
                        "action": 'query'
                    }
                ),
                Search(
                    name='compare_products_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_ids": ["100129027686", "100192762770", "100002047744"]
                    }
                )
            ]
        )
    ),
    Task(
        annotator='49',
        user_id="cnjdjd_66ea38a7829e1",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction='\n### This is your profile:\n<Consumer Type>\nPrice-sensitive customer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Calm and composed; expresses confusion without getting agitated when speaking<\\Emotion>\n<Attentiveness>High, cares about product-related details.<\\Attentiveness>\n<Patience>Relatively high, patiently waits for customer service replies.<\\Patience>\n<Trust Level>Medium, remains skeptical of statements from customer service that are not substantiated.<\\Trust Level>\n<Awareness of Rights>Strong, clearly knows where their rights lie.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and specific, clear about the questions<\\Questioning Style>\n<Speaking Style>Concise and pragmatic, clear and efficient.<\\Speaking Style>\n<Communication Rhythm>Stable, no obvious fluctuation in message length<\\Communication Rhythm>\n<\\Behavioral Traits>\n\n### These are your goals:\n<Intent 1>\nYou have already purchased a gas water heater, order number 313672076398, product ID 100148801459. But after taking it home you found that it is 14L, which you feel is a bit small, so you want to request an exchange.\n<\\Intent 1>\n<Intent 2>\nAmong the exchange products, you want to confirm whether there is a product with a larger capacity than the current one; if there is, you agree to the exchange.\n<\\Intent 2>\n<Intent 3>\nYou also want to check whether the gift promised at the time of purchase for this product offered trade-in of the old item for a new one, and whether it is direct recycling or unconditional replacement.\n<\\Intent 3>\n'  
,
        metadata=Validation(
            outputs=[],
            actions=[
            Action(
                    name="manage_exchange",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "order_id": "313672076398",
                        "user_id": "cnjdjd_66ea38a7829e1",
                        "action": 'exchange',
                        "original_product_id": "100148801459",
                        "exchange_product_id": "100148801462"
                    }
                ), 
            ],
            searches=[
                Search(
                    name="manage_exchange_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "order_id": "313672076398",
                        "user_id": "cnjdjd_66ea38a7829e1",
                        "action": 'query',
                        "original_product_id": "100148801459"
                    }
                ),
                Search(
                    name="get_gift_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100148801459"
                    }
                )
            ]
        )
    ),
    Task(
        annotator='50',
        user_id="cnjdjd_fvfvqajwvbaj",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction='\n### This is your profile:\n<Consumer Type>\nValue-for-money-oriented consumer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Positive and optimistic, fairly friendly toward customer service<\\Emotion>\n<Attentiveness>High; will ask in detail about the operating rules, and also has strong curiosity.<\\Attentiveness>\n<Patience>Relatively high, patiently waits for customer service replies.<\\Patience>\n<Trust Level>Medium; willing to communicate in depth with customer service to obtain more information, however, when some condition is mentioned that does not match known information, will ask about it<\\Trust Level>\n<Awareness of Rights>Average, will not take drastic measures.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and specific, clearly expresses their own needs<\\Questioning Style>\n<Speaking Style>The language style is fairly natural and relaxed, uses some informal expressions (such as "love you"), showing approachability, while still remaining polite and professional when discussing specific issues<\\Speaking Style>\n<Communication Rhythm>Stable, no obvious fluctuation in message length<\\Communication Rhythm>\n<\\Behavioral Traits>\n\n### These are your goals:\n<Intent 1>\nYou previously bought a product; the order status now shows "Shipped", and you want to know where this order has been delivered (Note: you do not know the order ID or the product ID, and you are forbidden from directly revealing this information to customer service; if customer service asks, answer "I don\'t know")\n<\\Intent 1>\n<Intent 2>\nIf it has not yet been delivered to "No. 1234 Kejiyuan Road", you will ask customer service to expedite it. (You are forbidden from revealing the information "No. 1234 Kejiyuan Road" to customer service)\n<\\Intent 2>\n<Intent 3>\nFinally, you hope customer service will issue an invoice for the order you just paid, as a \'Personal Invoice\'. (You are forbidden from revealing personal information such as name and phone number to customer service; if customer service asks you to provide them, have customer service look up the default information)\n<\\Intent 3>\n'  
,
        metadata=Validation(
            outputs=[],
            actions=[
            Action(
                    name="manage_urgent",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "order_id": "966768741700",
                        "user_id": "cnjdjd_fvfvqajwvbaj",
                    }
                ), 
            Action(
                name='manage_invoice',
                arguments={
                    "title":'Li Yutong',
                    "order_id":"238703475773",
                    "phone_number":"15923456789",
                    "invoice_type": 'personal_invoice'
                }
            )
            ],
            searches=[
                Search(
                    name="get_logistics_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "order_id": "966768741700",
                        "user_id": "cnjdjd_fvfvqajwvbaj",
                    }
                )
            ]
        )
    ),
    Task(
        annotator='51',
        user_id="cnjdjd_fvfvqajwvbaj",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction='\n### This is your profile:\n<Consumer Type>\nValue-for-money-oriented consumer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Positive and optimistic, fairly friendly toward customer service<\\Emotion>\n<Attentiveness>High; will ask in detail about the operating rules, and also has strong curiosity.<\\Attentiveness>\n<Patience>Relatively high, patiently waits for customer service replies.<\\Patience>\n<Trust Level>Medium; willing to communicate in depth with customer service to obtain more information, however, when some condition is mentioned that does not match known information, will ask about it<\\Trust Level>\n<Awareness of Rights>Average, will not take drastic measures.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and specific, clearly expresses their own needs<\\Questioning Style>\n<Speaking Style>The language style is fairly natural and relaxed, uses some informal expressions (such as "love you"), showing approachability, while still remaining polite and professional when discussing specific issues<\\Speaking Style>\n<Communication Rhythm>Stable, no obvious fluctuation in message length<\\Communication Rhythm>\n<\\Behavioral Traits>\n\n### These are your goals:\n<Intent 1>\nYou have just paid for an electric water heater, and you want to ask whether the gift for this product includes an air fryer (Note: you do not know the order ID or the product ID, and you are forbidden from revealing the fact that you do not know to customer service; if customer service asks, answer "I don\'t know")\n<\\Intent 1>\n<Intent 2>\nThen, you hope customer service will issue an invoice for the order you just bought, with type \'Personal Invoice\'. (You are forbidden from revealing personal information such as name and phone number to customer service; if customer service asks you to provide them, have customer service look up the default information)\n<\\Intent 2>\n<Intent 3>\nThen, you send an image: https://dd-static.jd.com/ddimg/jfs/t1/298651/16/8705/5580/682b2bfcF747a8e30/db631d46ad628e6d.jpg, and ask customer service to say whether the content of the image is genuine and what the specific process is (the content in the image is "post a photo and get a hair dryer", but you are forbidden from revealing the image content "post a photo and get a hair dryer" to customer service; if customer service does not explain the content in the image, you answer "Then I\'ll take another look later").\n<\\Intent 3>\n<Intent 4>\nFinally, you hope customer service will help you check where the shipped order has currently been delivered.\n<\\Intent 4>\n'  
,
        metadata=Validation(
            outputs=['Post a photo', 'hair dryer'],
            actions=[
            Action(
                name='manage_invoice',
                arguments={
                    "title":'Li Yutong',
                    "order_id":"238703475773",
                    "phone_number":"15923456789",
                    "invoice_type": 'personal_invoice'
                }
            )
            ],
            searches=[
                Search(
                    name='get_gift_info_tool',
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "product_id": "100192946480",
                    }
                    ),
                Search(
                    name="get_logistics_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "order_id": "966768741700",
                        "user_id": "cnjdjd_fvfvqajwvbaj",
                    }
                )
            ]
        )
    ),
    Task(
        annotator='52',
        user_id="cnjdjd_fvfvqajwvbaj",
        shop_id="5de650c946e7c3001814990f",
        platform="jd",
        instruction='\n### This is your profile:\n<Consumer Type>\nValue-for-money-oriented consumer\n<\\Consumer Type>\n\n<Personality Traits>\n<Emotion>Positive and optimistic, fairly friendly toward customer service<\\Emotion>\n<Attentiveness>High; will ask in detail about the operating rules, and also has strong curiosity.<\\Attentiveness>\n<Patience>Relatively high, patiently waits for customer service replies.<\\Patience>\n<Trust Level>Medium; willing to communicate in depth with customer service to obtain more information, however, when some condition is mentioned that does not match known information, will ask about it<\\Trust Level>\n<Awareness of Rights>Average, will not take drastic measures.<\\Awareness of Rights>\n<\\Personality Traits>\n\n<Behavioral Traits>\n<Questioning Style>Direct and specific, clearly expresses their own needs<\\Questioning Style>\n<Speaking Style>The language style is fairly natural and relaxed, uses some informal expressions (such as "love you"), showing approachability, while still remaining polite and professional when discussing specific issues<\\Speaking Style>\n<Communication Rhythm>Stable, no obvious fluctuation in message length<\\Communication Rhythm>\n<\\Behavioral Traits>\n\n### These are your goals:\n<Intent 1>\nYou previously bought a product (product ID: 100188628450); the order status now shows "Delivered", but you have not received a phone call to this day, so you want to ask where it has been delivered (Note: you do not know the order ID or the product ID, and you are forbidden from directly revealing this information to customer service; if customer service asks, answer "I don\'t know")\n<\\Intent 1>\n<Intent 2>\nThen, you want to check the delivery address of order ID: 238703475773; this product was bought for the company, and if it was delivered to "No. 1234 Kejiyuan Road", you will ask to change the order information, changing the address to "No. 3 Yuquan Road, Liancheng Community, Nantou Subdistrict". (You are forbidden from revealing the information "No. 1234 Kejiyuan Road" to customer service)\n<\\Intent 2>\n<Intent 3>\nFinally, you hope customer service will issue an invoice for this order delivered to the company, with type \'Corporate Invoice\' and title "Shanghai Technology Co., Ltd.". (You are forbidden from revealing personal information such as name and phone number to customer service; if customer service asks you to provide them, have customer service look up the default information)\n<\\Intent 3>\n'  
,
        metadata=Validation(
            outputs=[],
            actions=[
            Action(
                name='manage_order',
                arguments={
                    "platform": "jd",
                    "shop_id": "5de650c946e7c3001814990f",
                    "order_id": "238703475773",
                    "user_id": "cnjdjd_fvfvqajwvbaj",
                    "action": 'modify',
                    "address": 'No. 3 Yuquan Road, Liancheng Community, Nantou Subdistrict'
                }
            ),
            Action(
                name='manage_invoice',
                arguments={
                    "title":'Shanghai Technology Co., Ltd.',
                    "order_id":"238703475773",
                    "phone_number":"15923456789",
                    "invoice_type": 'corporate_invoice'
                }
            )
            ],
            searches=[
                Search(
                    name="get_logistics_info_tool",
                    arguments={
                        "platform": "jd",
                        "shop_id": "5de650c946e7c3001814990f",
                        "order_id": "115060910622",
                        "user_id": "cnjdjd_fvfvqajwvbaj",
                    }
                )
            ]
        )
    )
]