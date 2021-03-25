from __future__ import annotations

import dataclasses
from enum import auto, Enum
from typing import List

from SocketServer.piece_dto import PieceDTO


@dataclasses.dataclass
class Message:
    Action: MessageAction
    Data: MessageData


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


@dataclasses.dataclass
class MessageData:
    pass


@dataclasses.dataclass
class GameStatus(MessageData):
    GameState: str
    PlayerTurn: str
    IsChecked: bool


@dataclasses.dataclass
class PieceDestinations(MessageData):
    Source: List[int]
    Destinations: List[List[int]]


@dataclasses.dataclass
class SetupCompleted(MessageData):
    BlueLeftTransposed: bool
    BlueRightTransposed: bool
    RedLeftTransposed: bool
    RedRightTransposed: bool


@dataclasses.dataclass
class MoveCompleted(MessageData):
    Source: List[int]
    Destination: List[int]


@dataclasses.dataclass
class PieceData(MessageData):
    Pieces: List[PieceDTO]
