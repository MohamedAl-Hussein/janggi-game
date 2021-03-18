from __future__ import annotations

import abc
from typing import Iterator, List, Set, Tuple

from utils.point import Point2D


class IPathGenerationStrategy(metaclass=abc.ABCMeta):
    """Interface for implementing the Strategy Pattern to generate paths starting from a given point of origin."""

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return (hasattr(subclass, "path_generator") and callable(subclass.path_generator) or
                NotImplemented)

    def __init__(self, **kwargs) -> None:
        """
        Initialize PathGenerationStrategy instance.

        :keyword tuple[int, int] step_range: The minimum and maximum path lengths.
        :keyword set[int, ...] scalars: A combination of scalars to assist in generating branches.
        :keyword set[int, ...] x_magnitudes: A combination of magnitudes to be applied to the x-axis for each vector.
        :keyword set[int, ...] y_magnitudes: A combination of magnitudes to be applied to the y-axis for each vector.
        :keyword int diag_limit: An imposed limit for diagonal path lengths for when inside a palace.
        """

        self.__step_range: Tuple[int, int] = kwargs.get("step_range")
        self.__scalars: Set[int, ...] = kwargs.get("scalars")
        self.__x_magnitudes: Set[int, ...] = kwargs.get("x_magnitudes")
        self.__y_magnitudes: Set[int, ...] = kwargs.get("y_magnitudes")
        self.__diag_limit: int = kwargs.get("diag_limit", self.__step_range[1])

    @property
    def step_range(self) -> Tuple[int, int]:
        return self.__step_range

    @property
    def scalars(self) -> Set[int, ...]:
        return self.__scalars

    @property
    def x_magnitudes(self) -> Set[int, ...]:
        return self.__x_magnitudes

    @property
    def y_magnitudes(self) -> Set[int, ...]:
        return self.__y_magnitudes

    @property
    def diag_limit(self) -> int:
        return self.__diag_limit

    @abc.abstractmethod
    def path_generator(self, source: Point2D) -> Iterator[List[Point2D]]:
        """
        Return a generator that produces a new path starting from an origin point on every iteration.

        :param source: The origin point to move from.
        """
        raise NotImplementedError

    @staticmethod
    def vector_array_to_path(vector_array: List[Point2D]) -> List[Point2D]:
        """
        Convert an array of vectors into a path by adding each vector to the previous one.

        The end result will be a series of points representing a path originating from one point, traversing across a
        series of points in between, and ending at a final point.

        :param vector_array: An array of Point2D objects representing a series of vector transformations.
        :return: An array of Point2D objects representing a path.
        """

        path = list(vector_array)
        for index in range(1, len(path)):
            path[index] = path[index] + path[index - 1]

        return path


class LinearPathStrategy(IPathGenerationStrategy):
    """Path generation strategy specific to paths that move on the axis away from an origin point."""

    def path_generator(self, source: Point2D) -> Iterator[List[Point2D]]:
        """
        Given an origin point and parameters specifying path length, and x and y magnitudes; return a generator that
        produces all combinations of paths from the origin point.

        For Soldiers: x_magnitudes = {-1, 0, 1}, y_magnitudes = {[-1 or 1]}.
        For Chariots/Cannons: x_magnitudes = {0, 1}, y_magnitudes = {-1, 1}.
        For multi-step moves: step_range[1] > 2.

        :param source: The origin point to move from.
        :return: Generator object that returns a new path on each iteration.
        """

        # Create combination pairs to be used for path generation at next step.
        # If x and y are equal to 0, it's the same as not moving so skip and continue.
        combinations = [(s, x, y)
                        for s in range(*self.step_range)
                        for x in self.x_magnitudes
                        for y in self.y_magnitudes
                        if not (x == 0 == y)]

        # For each combination, calculate the vector array from source and convert them to a path.
        for s, x, y in combinations:
            vector_array = [source] + s * [Point2D(x * y, int(not x) * y)]
            path = IPathGenerationStrategy.vector_array_to_path(vector_array)

            yield path


class LinearDiagonalPathStrategy(IPathGenerationStrategy):
    """Path generation strategy specific to paths that move on the axis or diagonally away from an origin point."""

    def path_generator(self, source: Point2D) -> Iterator[List[Point2D]]:
        """
        Given an origin point and parameters specifying path length, x and y magnitudes, and diagonal movement
        limitations; return a generator that produces all combinations of paths from the origin point.

        For Generals/Guards: x_magnitudes = {-1, 0, 1}, y_magnitudes = {-1, 0, 1}.
        For Soldiers (inside palace only): x_magnitudes = {-1, 0, 1}, y_magnitudes = {0, [1 or -1]}.
        For multi-step moves (Cannons/Chariots inside palace only): step_range[1] > 2.
        For Cannons/Chariots inside palace: diag_limit = 2.

        :keyword Point2D source: The origin point to move from.
        :return: Generator object that returns a new path on each iteration.
        """

        # Create combination pairs to be used for path generation at next step.
        # If x and y are equal to 0, it's the same as not moving so skip and continue.
        combinations = [(s, x, y)
                        for s in range(*self.step_range)
                        for x in self.x_magnitudes
                        for y in self.y_magnitudes
                        if not (x == 0 == y)
                        if not (abs(x) == abs(y) and s > self.diag_limit)]

        # For each combination, calculate the vector array from source and convert them to a path.
        for s, x, y in combinations:
            vector_array = [source] + s * [Point2D(x, y)]
            path = IPathGenerationStrategy.vector_array_to_path(vector_array)

            yield path


class BranchPathStrategy(IPathGenerationStrategy):
    """Path generation strategy specific to paths that change direction multiple times."""

    def path_generator(self, source: Point2D) -> Iterator[List[Point2D]]:
        """
        Given an origin point and parameters specifying path length, a set of scalars, and x and y magnitudes; return a
        generator that produces all combinations of paths from the origin point.

        For Horse/Elephant: x_magnitudes = {-1, 1}, y_magnitudes = {-1, 1}, magnitudes = {0, 1}.
        For multi-step moves: step_range = (2, 3).

        :keyword Point2D source: The origin point to move from.
        :return: Generator object that returns a new list of Point2D objects denoting a path on each iteration.
        """

        # Create combination pairs to be used for path generation at next step.
        # If x and y are equal to 0, it's the same as not moving so skip and continue.
        combinations = [(s, m, x, y)
                        for s in range(*self.step_range)
                        for m in self.scalars
                        for x in self.x_magnitudes
                        for y in self.y_magnitudes
                        if not (x == 0 == y)]

        # For each combination, calculate the vector array from source and convert them to a path.
        for s, m, x, y in combinations:
            vector_array = [source, Point2D(m * x, int(not m) * y)] + s * [Point2D(x, y)]
            path = IPathGenerationStrategy.vector_array_to_path(vector_array)

            yield path
