import dataclasses
import json
from json import JSONEncoder, JSONDecoder
from typing import Any

from server.message import Message,MessageAction, SetupCompleted, PieceDestinations, MessageData, MoveCompleted


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

            d = obj["Data"]
            # if obj["Data"] is not None:
            #     d = json.loads(obj["Data"])

            if action is MessageAction.NEW_GAME:
                pass
            elif action is MessageAction.GET_GAME_STATUS:
                pass
            elif action is MessageAction.END_GAME:
                pass
            elif action is MessageAction.SETUP_COMPLETED:
                data = SetupCompleted(**d)
            elif action is MessageAction.GET_PIECE_DESTINATIONS:
                data = PieceDestinations(**d)
            elif action is MessageAction.MOVE_COMPLETED:
                data = MoveCompleted(**d)
            else:
                return Message(MessageAction.DEFAULT, MessageData())

            return Message(action, data)
        return obj
