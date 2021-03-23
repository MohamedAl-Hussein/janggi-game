from __future__ import annotations

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from engine.utils.point import Point2D


class Rectangle:
    """A simple class to represent a rectangle."""

    def __init__(self, corners: List[Point2D]) -> None:
        """
        Initialize Rectangle object with four corners. The first corner will denote the bottom-left corner of a
        rectangle and remaining corners go clockwise from that position.

        :param corners: List of four Point2D objects to denote corners of a rectangle.
        """

        self._bottom_left: Point2D = corners[0]
        self._top_left: Point2D = corners[1]
        self._top_right: Point2D = corners[2]
        self._bottom_right: Point2D = corners[3]

    def __contains__(self, point: Point2D) -> bool:
        """
        Given a Point2D object, determine if it is inside the rectangle or not.

        :param point: Point to examine.
        :return: True if point in rectangle, False otherwise.
        """

        is_inside: List[bool] = [
            self.top_left.x <= point.x <= self.top_right.x,
            self.bottom_left.y <= point.y <= self.top_left.y
        ]

        return all(is_inside)

    @property
    def bottom_left(self) -> Point2D:
        return self._bottom_left

    @property
    def bottom_right(self) -> Point2D:
        return self._bottom_right

    @property
    def top_left(self) -> Point2D:
        return self._top_left

    @property
    def top_right(self) -> Point2D:
        return self._top_right
