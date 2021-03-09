from __future__ import annotations

import abc
from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from janggi_piece import JanggiPiece, PieceCategory
    from utils.point import Point2D
    from utils.rectangle import Rectangle


class IObstacleDetectionStrategy(metaclass=abc.ABCMeta):
    """Interface for implementing the Strategy Pattern to detect any obstacles in a given path."""

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return (hasattr(subclass, "is_obstacle_in_path") and callable(subclass.is_obstacle_in_path) or
                NotImplemented)

    def __init__(self, **options):
        """Initialize object with optional keyword arguments."""

        self._options = options

    @property
    def options(self):
        return self._options

    @abc.abstractmethod
    def is_obstacle_in_path(self, **params) -> bool:
        """
        Return true if the path contains obstacles that can't be traversed past.

        Can accept optional parameters.
        """
        raise NotImplementedError


class InsidePalaceStrategy(IObstacleDetectionStrategy):
    """Obstacle detection strategies specific to pieces that are inside a palace."""

    def is_obstacle_in_path(self, **params) -> bool:
        """
        Given a path from originating from within a palace, determine if any obstacles exist on the path.

        For the General and Guards, they cannot leave the palace.
        For Soldiers, Cannons, and Chariots, they cannot move diagonally outside of a palace.
        For any piece, they cannot move diagonally if the path does not involve a palace corner.

        :keyword list[Point2D] path: A list of Point2D objects to denote a path from point source to destination.
        :keyword str color: The color of the piece at the source coordinate.
        :return: True if obstacles exist in path, False otherwise.
        """

        # Retrieve parameters.
        palace_bound: bool = self.options.get("palace_bound")
        palaces: Dict[str, Rectangle] = self.options.get("palace_corners")
        path: List[Point2D] = params.get("path")
        color: str = params.get("color")

        source: Point2D = path[0]
        destination: Point2D = path[-1]
        source_palace: str = "blue" if source in palaces["blue"] else "red"

        # Determine translation made from source to destination.
        translation: Point2D = destination - source

        # -----------------------CASE 1: Move not Across Diagonal Paths------------------------- #
        source_and_destination_checks = [
            destination == palaces[source_palace].top_left,
            destination == palaces[source_palace].bottom_left,
            destination == palaces[source_palace].top_right,
            destination == palaces[source_palace].bottom_right,
            source == palaces[source_palace].top_left,
            source == palaces[source_palace].bottom_left,
            source == palaces[source_palace].top_right,
            source == palaces[source_palace].bottom_right
        ]

        # Diagonal translation but neither source nor destination are the palace's corners.
        if not any(source_and_destination_checks):
            if abs(translation.x) >= 1 and abs(translation.y) >= 1:
                return True

        # --------------------------CASE 2: Locked in Palace------------------------------------ #
        if palace_bound:
            if destination not in palaces[color]:
                return True
            else:
                return False

        # --------------------------CASE 3: Limited Diagonal Movement---------------------------- #
        # Path does not leave past palace walls.
        if destination in palaces[source_palace]:
            return False

        # Path from source to destination involves a diagonal translation.
        if abs(translation.x) >= 1 and abs(translation.y) >= 1:
            return True

        return False


class IllegalDestinationStrategy(IObstacleDetectionStrategy):
    """Obstacle detection strategies specific to illegal path destinations."""

    def is_obstacle_in_path(self, **params) -> bool:
        """
        Determine if the destination contains a piece that can't be captured.

        For all piece, they cannot capture a friendly piece.
        For Cannons, in addition to friendly piece, they cannot capture another Cannon.

        :keyword JanggiPiece source_piece: The piece that is making the move.
        :keyword JanggiPiece target_piece: The piece that the source_piece want's to capture.
        :keyword bool category_restricted: Boolean value denoting whether the source piece can't capture another piece.
                 of the same category.
        :return: True if obstacles exist in path, False otherwise.
        """

        # Retrieve key args.
        source_piece: JanggiPiece = params.get("source_piece")
        target_piece: JanggiPiece = params.get("target_piece")
        category_restricted: bool = params.get("category_restricted")

        # No Piece at destination.
        if target_piece is None:
            return False

        # -----------------------CASE 1: Destination Friendly -------------------------- #
        if source_piece.color == target_piece.color:
            return True

        # -----------------------CASE 2: Destination Same Type ------------------------- #
        if category_restricted and source_piece.category == target_piece.category:
            return True

        return False


class IllegalPathStrategy(IObstacleDetectionStrategy):
    """Obstacle detection strategies specific to illegal paths between source and destination points."""

    def is_obstacle_in_path(self, **params) -> bool:
        """
        Determine if a path contains Pieces that cannot moved past.

        For all Pieces except for the Cannon, they cannot move past another Piece.
        For Cannons, exactly one Piece must exist in its path, and it cannot be another Cannon.

        :keyword List[Optional[JanggiPiece]] path_objects: A list of Piece objects (or None) on a path ordered from
                 start to finish.
        :keyword bool category_restricted: Boolean value denoting whether the source Piece can't pass another Piece
                 of the same category.
        :return: True if obstacles exist in path, False otherwise.
        """

        # Retrieve key args.
        path_objects: List[Optional[JanggiPiece]] = params.get("path_objects")
        category_restricted: bool = params.get("category_restricted")

        source_piece: JanggiPiece = path_objects[0]
        source_category: PieceCategory = source_piece.category
        categories: List[PieceCategory] = [obj.category for obj in path_objects[1:-1] if obj is not None]

        # -----------------------CASE 1: Category Restricted Piece -------------------------- #
        if category_restricted:

            # Cannon in path.
            if source_category in categories:
                return True

            # No Piece in path to hop over.
            if not any(isinstance(obj, JanggiPiece) for obj in path_objects[1: -1]):
                return True

            obj_count: int = 0
            for obj in path_objects[1:-1]:
                if isinstance(obj, JanggiPiece):
                    obj_count += 1

            # More than one Piece in path.
            if obj_count > 1:
                return True

            return False

        # ----------------------------- CASE 2: Piece in Path --------------------------------- #
        if any(isinstance(obj, JanggiPiece) for obj in path_objects[1: -1]):
            return True

        return False
