import re
from openai import OpenAI

from llm_config import get_llm_config
from llm_retry import call_with_retry


class ChatCompletionMessage:
    def __init__(self, content, role='assistant', refusal=None, audio=None, function_call=None, tool_calls=None):
        self.content = content
        self.role = role
        self.refusal = refusal
        self.audio = audio
        self.function_call = function_call
        self.tool_calls = tool_calls
    
    def __str__(self):
        return f"ChatCompletionMessage(content='{self.content}', refusal={self.refusal}, role='{self.role}', audio={self.audio}, function_call={self.function_call}, tool_calls={self.tool_calls})"

    def model_dump(self):
        return {
            "role": self.role,
            "content": self.content,
            "refusal": self.refusal,
            "audio": self.audio,
            "function_call": self.function_call,
            "tool_calls": self.tool_calls
        }
        

class MultimodalModelClient:
    def __init__(self, console=None):
        self.console = console
        self.url_pattern = r'https?://[^\s<>"]+?(?:jpg|jpeg|gif|png|webp)'

        config = get_llm_config("vlm")
        self.model = config.model
        self.client = OpenAI(base_url=config.base_url, api_key=config.api_key, max_retries=3)

    def create_response(self, messages, tools=None, temperature=0.0, top_p=0.2, max_tokens=128, presence_penalty=1.0, frequency_penalty=1.0, repetition_penalty=1.2):
        parsed_messages = self._prepare_messages(messages)
        self.console.log("Sending request to multimodal model.")
        response = call_with_retry(
            lambda: self.client.chat.completions.create(
                model=self.model,
                messages=parsed_messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty
            ),
            description="vlm.create_response",
        )
        if response.choices and len(response.choices) > 0:
            try:
                multimodal_reply = response.choices[0].message.content
                response_obj = ChatCompletionMessage(
                    content=multimodal_reply,
                    role='assistant',
                    refusal=None,
                    audio=None,
                    function_call=None,
                    tool_calls=None
                )
                return response_obj
            except Exception as e:
                self.console.log(f"Error parsing response: {e}")
                return ChatCompletionMessage(
                    content='Sorry, an error occurred while processing the request.',
                    role='assistant'
                )
        else:
            self.console.log(f"Request failed with status code: {response.status_code}")
            return ChatCompletionMessage(
                content=f"Request failed (status code: {response.status_code})",
                role='assistant'
            )
            
    def _prepare_messages(self, messages):
        parsed_messages = []
        # This method can be implemented to process messages before sending
        for message in messages:
            if not isinstance(message.get('content'), str):
                continue
            text = message.get("content", "")
            role = message.get("role", "user")
            image_match = re.findall(self.url_pattern, text)
            if image_match:
                for url in image_match:
                    text = text.replace(url, '[IMAGE_URL]')
                text = text.strip()
                if role == "user":
                    parsed_messages.append({
                        "role": role,
                        "content": [
                            {
                                "type": "text",
                                "text": text
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_match[0],
                                    "detail": "high"
                                }
                            }
                            ]
                    })
                else:
                    parsed_messages.append({
                        "role": role,
                        "content": text
                    })
            else:
                if role == "user":
                    parsed_messages.append({
                        "role": role,
                        "list_contents": [
                            {
                                "type": "text",
                                "text": text
                            }
                        ]
                    })
                else:
                    parsed_messages.append({
                        "role": role,
                        "content": text
                    })
        return parsed_messages
