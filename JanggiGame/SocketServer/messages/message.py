import dataclasses

from .message_action import MessageAction
from .message_data import MessageData


@dataclasses.dataclass
class Message:
    Action: MessageAction
    Data: MessageData
