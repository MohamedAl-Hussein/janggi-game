from __future__ import annotations

import enum
from typing import Dict, Iterator, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from engine.helpers.obstacle_detection_strategy import IObstacleDetectionStrategy
    from engine.helpers.path_generation_strategy import IPathGenerationStrategy
    from engine.utils.point import Point2D
    from engine.utils.rectangle import Rectangle


class JanggiPiece:
    """Class representing a single janggi piece."""

    def __init__(self,
                 color: PieceColor,
                 category: PieceCategory,
                 position: Point2D,
                 path_strategies: Dict[str, IPathGenerationStrategy],
                 obstacle_strategies: Dict[str, IObstacleDetectionStrategy],
                 palace_bound: bool = False) -> None:
        """
        Create a new Piece object with color, category, position, path strategy, obstacle strategy and palace_bound
        trait.

        :param color: The piece's color.
        :param category: The piece's category.
        :param position: The piece's starting position.
        :param path_strategies: A dictionary of path generation strategies for various scenarios.
        :param obstacle_strategies: A dictionary of obstacle detection strategies for various scenarios.
        :param palace_bound: Whether the piece is bound by its palace.
        """

        self.__color: PieceColor = color
        self.__category: PieceCategory = category
        self.__position: Point2D = position
        self.__path_strategies: Dict[str, IPathGenerationStrategy] = path_strategies
        self.__obstacle_strategies: Dict[str, IObstacleDetectionStrategy] = obstacle_strategies
        self.__palace_bound: bool = palace_bound

    @property
    def color(self) -> PieceColor:
        return self.__color

    @color.setter
    def color(self, value) -> None:
        self.__color = value

    @property
    def category(self) -> PieceCategory:
        return self.__category

    @property
    def position(self) -> Point2D:
        return self.__position

    @position.setter
    def position(self, value) -> None:
        self.__position = value

    @property
    def palace_bound(self) -> bool:
        return self.__palace_bound

    def generate_path(self, source: Point2D, in_palace: bool = False) -> Iterator[List[Point2D]]:
        """
        Return a generator that produces a new path starting from the piece's current position on every iteration.

        :param in_palace: Whether or not the piece is currently within the boundaries of a palace.
        :param source: The origin point to move from.
        :return: Generator object that returns a new path on each iteration.
        """

        # Determine which strategy to use based on the location of the piece relative to a palace.
        if in_palace:
            return self.__path_strategies["palace"].path_generator(source)

        return self.__path_strategies["default"].path_generator(source)

    def is_obstacle_in_path(self,
                            in_palace: bool,
                            path_objects: List[Optional[JanggiPiece]],
                            path: List[Point2D] = None,
                            blue_palace: Rectangle = None,
                            red_palace: Rectangle = None
                            ) -> bool:
        """
        Determine if the piece has any obstacles in its chosen path that it can't traverse past.

        :param in_palace: If the piece is inside a palace or not.
        :param path_objects: A list of Piece objects (or None) on a path ordered from start to finish.
        :param path: A list of Point2D objects to denote a path from point source to destination.
        :param blue_palace: Instance of blue palace.
        :param red_palace: Instance of red palace.
        :return: True if obstacles exist in path, False otherwise.
        """

        # Create an array of obstacle detection strategies to implement for the given piece.
        has_obstacles: List[bool] = [
            self.__obstacle_strategies.get("path").is_obstacle_in_path(path_objects, path, blue_palace, red_palace),
            self.__obstacle_strategies.get("destination").is_obstacle_in_path(
                path_objects, path, blue_palace, red_palace
            )
        ]

        # Piece not in palace.
        if not in_palace:
            return any(has_obstacles)

        # Horse and Elephant do not have palace-specific moves.
        if self.__obstacle_strategies.get("palace") is not None:
            has_obstacles.append(
                self.__obstacle_strategies.get("palace").is_obstacle_in_path(
                    path_objects, path, blue_palace, red_palace
                )
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
