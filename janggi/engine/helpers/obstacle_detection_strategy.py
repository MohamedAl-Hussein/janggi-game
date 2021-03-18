from __future__ import annotations

import abc
from typing import List, Optional, TYPE_CHECKING

from janggi_piece import JanggiPiece, PieceCategory, PieceColor

if TYPE_CHECKING:
    from utils.point import Point2D
    from utils.rectangle import Rectangle


class IObstacleDetectionStrategy(metaclass=abc.ABCMeta):
    """Interface for implementing the Strategy Pattern to detect any obstacles in a given path."""

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return (hasattr(subclass, "is_obstacle_in_path") and callable(subclass.is_obstacle_in_path) or
                NotImplemented)

    @abc.abstractmethod
    def is_obstacle_in_path(self,
                            path_objects: List[Optional[JanggiPiece]],
                            path: List[Point2D] = None,
                            blue_palace: Rectangle = None,
                            red_palace: Rectangle = None
                            ) -> bool:
        """
        Return true if the path contains obstacles that can't be traversed past.

        :param path_objects: A list of Piece objects (or None) on a path ordered from start to finish.
        :param path: A list of Point2D objects to denote a path from point source to destination.
        :param blue_palace: Instance of blue palace.
        :param red_palace: Instance of red palace.
        :return: True if obstacles exist in path, False otherwise.
        """
        raise NotImplementedError


class InsidePalaceStrategy(IObstacleDetectionStrategy):
    """Obstacle detection strategies specific to pieces that are inside a palace."""

    def is_obstacle_in_path(self,
                            path_objects: List[Optional[JanggiPiece]],
                            path: List[Point2D] = None,
                            blue_palace: Rectangle = None,
                            red_palace: Rectangle = None
                            ) -> bool:
        """
        Given a path from originating from within a palace, determine if any obstacles exist on the path.

        For the General and Guards, they cannot leave the palace.
        For Soldiers, Cannons, and Chariots, they cannot move diagonally outside of a palace.
        For any piece, they cannot move diagonally if the path does not involve a palace corner.

        :param path_objects: A list of Piece objects (or None) on a path ordered from start to finish.
        :param path: A list of Point2D objects to denote a path from point source to destination.
        :param blue_palace: Instance of blue palace.
        :param red_palace: Instance of red palace.
        :return: True if obstacles exist in path, False otherwise.
        """

        # Retrieve parameters.
        palace_bound: bool = path_objects[0].palace_bound
        color: PieceColor = path_objects[0].color
        source: Point2D = path[0]
        destination: Point2D = path[-1]

        source_palace: Rectangle = blue_palace if source in blue_palace else red_palace
        local_palace: Rectangle = blue_palace if color is PieceColor.BLUE else red_palace

        # Determine translation made from source to destination.
        translation: Point2D = destination - source

        # -----------------------CASE 1: Move not Across Diagonal Paths------------------------- #
        source_and_destination_checks = [
            destination == source_palace.top_left,
            destination == source_palace.bottom_left,
            destination == source_palace.top_right,
            destination == source_palace.bottom_right,
            source == source_palace.top_left,
            source == source_palace.bottom_left,
            source == source_palace.top_right,
            source == source_palace.bottom_right
        ]

        # Diagonal translation but neither source nor destination are the palace's corners.
        if not any(source_and_destination_checks):
            if abs(translation.x) >= 1 and abs(translation.y) >= 1:
                return True

        # --------------------------CASE 2: Locked in Palace------------------------------------ #
        if palace_bound:
            if destination not in local_palace:
                return True
            else:
                return False

        # --------------------------CASE 3: Limited Diagonal Movement---------------------------- #
        # Path does not leave past palace walls.
        if destination in source_palace:
            return False

        # Path from source to destination involves a diagonal translation.
        if abs(translation.x) >= 1 and abs(translation.y) >= 1:
            return True

        return False


class IllegalDestinationStrategy(IObstacleDetectionStrategy):
    """Obstacle detection strategies specific to illegal path destinations."""

    def is_obstacle_in_path(self,
                            path_objects: List[Optional[JanggiPiece]],
                            path: List[Point2D] = None,
                            blue_palace: Rectangle = None,
                            red_palace: Rectangle = None
                            ) -> bool:
        """
        Determine if the destination contains a piece that can't be captured.

        For all piece, they cannot capture a friendly piece.
        For Cannons, in addition to friendly piece, they cannot capture another Cannon.

        :param path_objects: A list of Piece objects (or None) on a path ordered from start to finish.
        :param path: A list of Point2D objects to denote a path from point source to destination.
        :param blue_palace: Instance of blue palace.
        :param red_palace: Instance of red palace.
        :return: True if obstacles exist in path, False otherwise.
        """

        # Retrieve key args.
        source_piece: JanggiPiece = path_objects[0]
        target_piece: JanggiPiece = path_objects[-1]
        category_restricted = True if source_piece.category is PieceCategory.CANNON else False

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

    def is_obstacle_in_path(self,
                            path_objects: List[Optional[JanggiPiece]],
                            path: List[Point2D] = None,
                            blue_palace: Rectangle = None,
                            red_palace: Rectangle = None
                            ) -> bool:
        """
        Determine if a path contains Pieces that cannot moved past.

        For all Pieces except for the Cannon, they cannot move past another Piece.
        For Cannons, exactly one Piece must exist in its path, and it cannot be another Cannon.

        :param path_objects: A list of Piece objects (or None) on a path ordered from start to finish.
        :param path: A list of Point2D objects to denote a path from point source to destination.
        :param blue_palace: Instance of blue palace.
        :param red_palace: Instance of red palace.
        :return: True if obstacles exist in path, False otherwise.
        """

        source_piece: JanggiPiece = path_objects[0]
        source_category: PieceCategory = source_piece.category
        category_restricted = True if source_category is PieceCategory.CANNON else False
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
