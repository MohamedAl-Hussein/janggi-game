import enum

# from ..engine.janggi_game import JanggiGame


class ActionRequestHandler:
    def __init__(self, action, message):
        self.action = action
        self.message = message

    def handle_request(self):
        if self.action is ActionRequest.INVALID_REQUEST:
            raise

        if self.action == ActionRequest.NEW_GAME:
            pass
            # return JanggiGame()
        elif self.action == ActionRequest.UPDATE_START_LAYOUT:
            pass
        elif self.action == ActionRequest.GET_GAME_STATE:
            pass
        elif self.action == ActionRequest.GET_DESTINATIONS:
            pass
        elif self.action == ActionRequest.PROCESS_MOVE:
            pass
        elif self.action == ActionRequest.END_GAME:
            pass



class ActionRequest(enum.Enum):
    NEW_GAME = enum.auto()
    UPDATE_START_LAYOUT = enum.auto()
    GET_GAME_STATE = enum.auto()
    GET_DESTINATIONS = enum.auto()
    PROCESS_MOVE = enum.auto()
    END_GAME = enum.auto()
    INVALID_REQUEST = enum.auto()
