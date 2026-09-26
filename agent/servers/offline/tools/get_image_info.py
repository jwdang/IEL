from typing import List,Dict
from .apis import OnlineLLMApi


def get_image_info(data, summarized_query: str, needed_query:str, history_messages: str):
    """
    Returns:
        A formatted string with the image information
    """
    if not history_messages or len(history_messages)==0:
        return data, f"The parameter history_messages is invalid. Please try again."
    
    input_message = f'''
    "Understand the relationship between the image information and the text information sent in the conversation, and provide a description of the image that is related to the current main question.'
    Please describe the image content concisely and accurately, and follow the requirements below:
    1. Faithfully describe the main objects, scenes and other information in the image. If the image description contains text, please extract and return the text content.
    2. Reply to each question accordingly, and strictly follow the format:

    The format is as follows:
    ### Image description:
    {{description}}
    ### Answer to the question:
    {{answer}}
    ### Answer to the requirement:
    {{answer}}

    This is the conversation history:
    {history_messages}

    This is the user's current question:
    {summarized_query}
    
    This is the description of the requirement for the image content:
    {needed_query}
    '''
    online_llm_api = OnlineLLMApi()
    messages = [
        {'role': 'user', 'content': input_message}
    ]
    result = online_llm_api.generate_multimodal_response(messages).content
    print(f'result: {result}')
    return data, result
