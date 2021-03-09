from __future__ import annotations

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.point import Point2D
    from janggi_board import JanggiBoard


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

    def __init__(self, source: Point2D, destination: Point2D, board: JanggiBoard) -> None:
        """
        Create new instance of a move command and save the source, destination, and board state.

        :param source: Source coordinate.
        :param destination: Destination coordinate.
        :param board: Game board.
        """

        self._source: Point2D = source
        self._destination: Point2D = destination
        self._board: JanggiBoard = board

    @property
    def source(self) -> Point2D:
        return self._source

    @property
    def destination(self) -> Point2D:
        return self._destination

    @property
    def board(self) -> JanggiBoard:
        return self._board

    def execute(self) -> None:
        """Call move on the board object to signify a move from source to destination."""

        self.board.move(self.source, self.destination)

    def un_execute(self) -> None:
        """Call move on the board object to signify a move from destination to source."""

        self.board.move(self.destination, self.source)
