from .models import MultimodalModelClient
from .console import console_model


class OnlineLLMApi:
    """Entry point for image understanding; the model configuration comes from the
    VLM_* set in .env."""

    def __init__(self):
        self.console = console_model
        self.multimodal_client = MultimodalModelClient(console=self.console)

    def generate_multimodal_response(self, messages, tools=None):
        return self.multimodal_client.create_response(messages, tools)


if __name__ == "__main__":
    api = OnlineLLMApi()
    messages = [{'role': 'system', 'content': f'''

"You are a senior e-commerce customer service agent. You need to understand the relationship between the image information and the text information sent in the conversation, and provide a description of the image that is related to the current main question.'

Please describe the image content concisely and accurately, and follow the requirements below:

1. Faithfully describe the main objects, scenes and other information in the image. If the image description contains text, please extract and return the text content.
                    2.
Try to output only information that is related to the user's main question, and keep it brief and clear, no more than 100 characters."
                   '''}, {'role': 'user', 'content':f'''
'https://chat-img.pddugc.com/chat-pic-mall-user-v1/2025-04-06/7a963da6-a2e4-4340-aa88-10c008c6fb9c.jpeg
The dimensions shown in this image seem to be different from what you said."'''}]
    response = api.generate_multimodal_response(messages)
    print(response)
