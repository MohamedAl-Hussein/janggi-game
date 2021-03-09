from __future__ import annotations

from typing import Union


class Point2D:
    """A class representing a 2D point in space."""

    def __init__(self, x: Union[int, float], y: Union[int, float]) -> None:
        """
        Initialize a Point2D object with x and y coordinates.

        :param x: The x coordinate of the point.
        :param y: The y coordinate of the point.
        """

        self._x = x
        self._y = y

    @property
    def x(self) -> Union[int, float]:
        return self._x

    @property
    def y(self) -> Union[int, float]:
        return self._y

    def __add__(self, other: Point2D):
        """Override addition operator to assist in performing vector addition."""

        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point2D):
        """Override subtraction operator to assist in performing vector subtraction."""

        return Point2D(self.x - other.x, self.y - other.y)

    def __eq__(self, other: Point2D):
        """Override the equality operator to assist in comparing two points by their x andy attributes."""

        return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other: Point2D):
        """Override the inequality operator to assist in comparing two points by they x and y attributes."""
        return (self.x, self.y) != (other.x, other.y)

    def to_tuple(self):
        return self.x, self.y
