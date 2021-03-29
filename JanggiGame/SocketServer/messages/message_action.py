from enum import auto, Enum


class MessageAction(Enum):
    NEW_GAME = auto()
    GAME_STARTED = auto()
    SETUP_COMPLETED = auto()
    SETUP_CONFIRMED = auto()
    GET_GAME_STATUS = auto()
    GAME_STATUS = auto()
    GET_PIECE_DESTINATIONS = auto()
    PIECE_DESTINATIONS = auto()
    MOVE_COMPLETED = auto()
    MOVE_CONFIRMED = auto()
    END_GAME = auto()
    GAME_OVER = auto()
    DEFAULT = auto()
