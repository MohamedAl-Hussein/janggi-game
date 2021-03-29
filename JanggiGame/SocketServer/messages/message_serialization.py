import dataclasses
import json
from json import JSONEncoder, JSONDecoder
from typing import Any

from .message import Message
from .message_action import MessageAction
from .message_data import MessageData, SetupCompleted, PieceDestinations, MoveCompleted


class MessageEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Message):
            return {
                "Action": o.Action.name,
                "Data": dataclasses.asdict(o.Data)
            }

        return json.JSONEncoder.default(self, o)


class MessageDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if 'Action' in obj and 'Data' in obj:
            action = MessageAction[obj["Action"]]
            data = MessageData()

            if action is MessageAction.NEW_GAME:
                pass
            elif action is MessageAction.GET_GAME_STATUS:
                pass
            elif action is MessageAction.END_GAME:
                pass
            elif action is MessageAction.SETUP_COMPLETED:
                data = SetupCompleted(**obj["Data"])
            elif action is MessageAction.GET_PIECE_DESTINATIONS:
                data = PieceDestinations(**obj["Data"])
            elif action is MessageAction.MOVE_COMPLETED:
                data = MoveCompleted(**obj["Data"])
            else:
                return Message(MessageAction.DEFAULT, MessageData())

            return Message(action, data)
        return obj
