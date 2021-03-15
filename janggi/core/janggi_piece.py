from __future__ import annotations

import enum
from typing import Dict, Iterator, List, TYPE_CHECKING

if TYPE_CHECKING:
    from helpers.obstacle_detection_strategy import IObstacleDetectionStrategy
    from helpers.path_generation_strategy import IPathGenerationStrategy
    from utils.point import Point2D


class JanggiPiece:
    """Class representing a single janggi piece."""

    def __init__(self,
                 color: PieceColor,
                 category: PieceCategory,
                 position: Point2D,
                 path_generation_strategies: Dict[str, IPathGenerationStrategy],
                 obstacle_detection_strategies: Dict[str, IObstacleDetectionStrategy]) -> None:

        """
        Create a new Piece object with color, category, position, path strategy, and move strategy.

        :param color: The piece's color.
        :param category: The piece's category.
        :param position: The piece's starting position.
        :param path_generation_strategies: A dictionary of path generation strategies for various scenarios.
        :param obstacle_detection_strategies: A dictionary of obstacle detection strategies for various scenarios.
        """

        self._color: PieceColor = color
        self._position: Point2D = position
        self._category: PieceCategory = category
        self._path_generation_strategies: Dict[str, IPathGenerationStrategy] = path_generation_strategies
        self._obstacle_detection_strategies: Dict[str, IObstacleDetectionStrategy] = obstacle_detection_strategies

    @property
    def color(self) -> PieceColor:
        return self._color

    @color.setter
    def color(self, value) -> None:
        self._color = value

    @property
    def category(self) -> PieceCategory:
        return self._category

    @property
    def position(self) -> Point2D:
        return self._position

    @position.setter
    def position(self, value) -> None:
        self._position = value

    def generate_path(self, **params) -> Iterator[List[Point2D]]:
        """
        Return a generator that produces a new path starting from the piece's current position on every iteration.

        :keyword bool in_palace: Whether or not the piece is currently within the boundaries of a palace.
        :keyword Point2D source: The origin point to move from.
        :keyword tuple[int, int] step_range: The minimum and maximum path lengths.
        :keyword set[int, ...] x_magnitudes: A combination of magnitudes to be applied to the x-axis for each vector.
        :keyword set[int, ...] y_magnitudes: A combination of magnitudes to be applied to the y-axis for each vector.
        :keyword set[int, ...] scalars: A combination of scalars to assist in generating branches.
        :keyword int diag_limit: An imposed limit for diagonal path lengths for when inside a palace.
        :return: Generator object that returns a new path on each iteration.
        """

        # Determine which strategy to use based on the location of the piece relative to a palace.
        if params["in_palace"]:
            return self._path_generation_strategies["palace"].path_generator(**params)

        return self._path_generation_strategies["default"].path_generator(**params)

    def is_obstacle_in_path(self, **params) -> bool:
        """
        Determine if the piece has any obstacles in its chosen path that it can't traverse past.

        :keyword bool in_palace: Whether or not the piece is currently within the boundaries of a palace.
        :keyword list[Point2D] path: A list of Point2D objects to denote a path from point source to destination.
        :keyword str color: The color of the piece at the source coordinate.
        :keyword JanggiPiece source_piece: The piece that is making the move.
        :keyword JanggiPiece target_piece: The piece that the source_piece want's to capture.
        :keyword bool category_restricted: Boolean value denoting whether the source piece can't capture another piece.
                 of the same category.
        :keyword List[Optional[JanggiPiece]] path_objects: A list of Piece objects (or None) on a path ordered from
                 start to finish.
        :return: True if any obstacles exist that can't be traversed past, False otherwise.
        """

        # Create an array of obstacle detection strategies to implement for the given piece.
        has_obstacles: List[bool] = [
            self._obstacle_detection_strategies.get("path").is_obstacle_in_path(**params),
            self._obstacle_detection_strategies.get("destination").is_obstacle_in_path(**params)
        ]

        # Piece not in palace.
        if not params["in_palace"]:
            return any(has_obstacles)

        # Horse and Elephant do not have palace-specific moves.
        if self._obstacle_detection_strategies.get("palace") is not None:
            has_obstacles.append(
                params["in_palace"] and self._obstacle_detection_strategies.get("palace").is_obstacle_in_path(**params)
            )

        return any(has_obstacles)


class PieceColor(enum.Enum):
    """Enum class representing various colors a janggi piece can have."""

    BLUE = enum.auto()
    RED = enum.auto()


class PieceCategory(enum.Enum):
    """Enum class representing the various categories a janggi piece can belong to."""

    GENERAL = 9
    GUARD = 19
    HORSE = 29
    ELEPHANT = 39
    CHARIOT = 49
    CANNON = 59
    SOLDIER = 69
