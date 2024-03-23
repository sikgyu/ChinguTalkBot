import os
from typing import List
import logging

from repositories.model import MessageModel

logger = logging.getLogger(__name__)

def is_running_on_lambda():
    in_lambda = 'AWS_EXECUTION_ENV' in os.environ
    logger.info(f'Running on Lambda: {in_lambda}')
    return in_lambda

def get_buffer_string(conversations: List[MessageModel]) -> str:
    string_messages = []
    for conversation in conversations:
        if conversation.role == "assistant":
            prefix = "Assistant: "
        elif conversation.role == "user":
            prefix = "Human: "
        else:
            raise ValueError(f"Unsupported role: {conversation.role}")
        message = f"{prefix}{conversation.content.body}"
        string_messages.append(message)

    # 最後のメッセージがユーザーからのものである場合、prefixを追加します。
    # Ref: https://docs.anthropic.com/claude/docs/introduction-to-prompt-design#human--assistant-formatting
    if conversations[-1].role == "user":
        string_messages.append("Assistant: ")

    return "\n".join(string_messages)