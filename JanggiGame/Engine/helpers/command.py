from __future__ import annotations

import abc
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from utils import Point2D
    from board import JanggiBoard
    from game import GameState
    from piece import JanggiPiece


class ICommand(metaclass=abc.ABCMeta):
    """Interface representing Command class for implementing the Command Pattern."""

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return (hasattr(subclass, "execute") and callable(subclass.execute) and
                hasattr(subclass, "un_execute") and callable(subclass.un_execute) or
                NotImplemented)

    @abc.abstractmethod
    def execute(self) -> None:
        """Execute a command."""
        raise NotImplementedError

    @abc.abstractmethod
    def un_execute(self) -> None:
        """Execute the inverse of a command."""
        raise NotImplementedError


class MoveCommand(ICommand):
    """Store the state of a move request made by a JanggiGame instance."""

    def __init__(self, source: Point2D, destination: Point2D, board: JanggiBoard, game_state: GameState) -> None:
        """
        Create new instance of object and save source, destination, and board state.

        Create property for storing piece that was removed as a result of calling this command.

        :param source: Source coordinate.
        :param destination: Destination coordinate.
        :param board: Game board map.
        """

        self.__source: Point2D = source
        self.__destination: Point2D = destination
        self.__board: JanggiBoard = board
        self.__game_state: GameState = game_state
        self.__removed_piece: Optional[JanggiPiece] = None

    @property
    def source(self) -> Point2D:
        return self.__source

    @property
    def destination(self) -> Point2D:
        return self.__destination

    @property
    def board(self) -> JanggiBoard:
        return self.__board

    @property
    def game_state(self) -> GameState:
        return self.__game_state

    @game_state.setter
    def game_state(self, value: GameState) -> None:
        self.__game_state = value

    @property
    def removed_piece(self) -> Optional[JanggiPiece]:
        return self.__removed_piece

    @removed_piece.setter
    def removed_piece(self, value: Optional[JanggiPiece]) -> None:
        self.__removed_piece = value

    def execute(self) -> None:
        """Move object from source to destination."""

        self.removed_piece = self.board.coord_map.get(self.destination.to_tuple())
        self.board.move(self.source, self.destination)

    def un_execute(self) -> None:
        """Move object from destination to source."""

        self.board.move(self.destination, self.source)

        # Return removed piece back to its original location (if one existed).
        if self.removed_piece is not None:
            self.board.coord_map[self.destination.to_tuple()] = self.removed_piece
            self.removed_piece = None
