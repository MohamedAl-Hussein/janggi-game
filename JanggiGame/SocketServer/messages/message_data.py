import dataclasses
from typing import List

from dtos.piece_dto import PieceDTO


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
