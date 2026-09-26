from typing import List, Dict
import json
import re
import os
from datetime import datetime
from itertools import count
from langchain_openai import ChatOpenAI

from llm_retry import invoke_with_retry
from llm_config import get_llm_config

_MM_DEBUG_COUNTER = count(1)


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
        self.client = ChatOpenAI(
            base_url=config.base_url,
            api_key=config.api_key,
            model=config.model,
            temperature=0.3,
            max_retries=3,
        )

    def create_response(self, messages, model, tools=None, temperature=0.0, top_p=0.2, max_tokens=128,
                        presence_penalty=1.0, frequency_penalty=1.0, repetition_penalty=1.2):
        """Kept as a placeholder; not used directly in the mock scenario. Prefer calling
        it through ChatOpenAI.invoke."""
        parsed_messages = self._prepare_messages(messages)
        # print(f"parsed_messages: {parsed_messages}")
        # ChatOpenAI is itself a LangChain Runnable, so .invoke(messages) is the
        # recommended way to call it. Here we simply serialize the parsed messages into a
        # single text input.
        text_input = json.dumps(parsed_messages, ensure_ascii=False)
        llm_response = invoke_with_retry(
            self.client, text_input, description="vlm.create_response"
        )
        _print_mm_llm_debug(
            stage="get_image_info_mock.create_response",
            model_name=str(getattr(self.client, "model_name", "unknown")),
            input_payload=text_input,
            output_payload=getattr(llm_response, "content", str(llm_response)),
        )
        content = getattr(llm_response, "content", str(llm_response))
        return ChatCompletionMessage(content=content, role='assistant')
            
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



CAPTIONS_PATH = os.path.join(os.path.dirname(__file__), "img_cache", "captions.jsonl")


def read_captions():
    file_path = CAPTIONS_PATH
    captions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                json_data = json.loads(line)
                captions.append(json_data)
            except json.JSONDecodeError as e:
                print(f"Failed to parse line {line_num}: {e}")
    return captions


def get_image_info(data, summarized_query: str, needed_query: str, history_messages: str, model: str='DeepSeek-V3'):
    """
    Entry point:
    1. Find the image URL in history_messages;
    2. Use the URL's file name to find the matching caption in captions.jsonl;
    3. Assemble the caption, the conversation and the request into a prompt;
    4. Send it to self.client (ChatOpenAI) to get an answer;

    Returns:
        data (returned unchanged), plus a formatted string with the image information
    """
    if not history_messages or len(history_messages) == 0:
        return data, 'The parameter history_messages is invalid. Please try again.'

    # 1. Extract the image URL from the conversation history
    url_pattern = r'https?://[^\s<>"]+?(?:jpg|jpeg|gif|png|webp)'
    matches = re.findall(url_pattern, history_messages)
    if not matches:
        return data, 'No image link found in the conversation. Please make sure history_messages contains the full image URL.'
    img_url = matches[0]
    img_name = img_url.split("/")[-1]

    # 2. Look up the caption of the corresponding image in captions.jsonl
    captions = read_captions()
    curr_caption = None
    for cap in captions:
        if cap.get("name") == img_name:
            curr_caption = cap
            break

    if not curr_caption or "caption" not in curr_caption:
        return data, f"Not found: caption for image {img_name}. Please generate it first and write it into captions.jsonl."

    # 3. Assemble the prompt, packing in the caption, the conversation history and the
    # request
    input_message = f"""
You are an e-commerce customer service assistant. You need to understand the relationship between the image information and the text information, and answer the content related to the current question.
Based on the image description, reply to each question accordingly, and strictly follow the format below:

The format is as follows:
### Answer to the question:
{{answer}}
### Answer to the requirement:
{{answer}}

Below is the image description (caption):
{curr_caption['caption']}

Below is the conversation history (which may contain image links):
{history_messages}

This is the user's current question:
{summarized_query}

This is the specific requirement description for the image content:
{needed_query}
"""
    
    # 4. Send it to self.client (ChatOpenAI) to get an answer
    config = get_llm_config("agent")
    llm = ChatOpenAI(
        base_url=config.base_url,
        api_key=config.api_key,
        model=config.model,
        temperature=0.3,
        max_retries=3,
    )
    try:
        llm_response = invoke_with_retry(
            llm, input_message, description="vlm.get_image_info"
        )
        _print_mm_llm_debug(
            stage="get_image_info_mock.get_image_info",
            model_name=str(getattr(llm, "model_name", "unknown")),
            input_payload=input_message,
            output_payload=getattr(llm_response, "content", str(llm_response)),
        )
        result_text = getattr(llm_response, "content", str(llm_response))
    except Exception as e:
        result_text = f"Failed to call the image understanding model: {e}"

    return data, result_text


def _is_mm_debug_enabled() -> bool:
    value = os.getenv("ECOM_DEBUG_LLM_IO", "0").strip().lower()
    return value in {"1", "true", "yes", "y", "on"}


def _print_mm_llm_debug(stage: str, model_name: str, input_payload: str, output_payload: str) -> None:
    if not _is_mm_debug_enabled():
        return
    call_id = next(_MM_DEBUG_COUNTER)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n" + "=" * 100)
    print(f"[LLM DEBUG MM #{call_id}] Time: {ts} | Stage: {stage} | Model: {model_name}")
    print("-" * 100)
    # print("[INPUT]")
    # print(f"[human] {input_payload}")
    print("[INPUT] (omitted)")
    print("-" * 100)
    print("[OUTPUT]")
    print(f"[ai] {output_payload}")
    print("=" * 100)
