from __future__ import annotations

import abc
from typing import Iterator, List, Set, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from utils.point import Point2D


class IPathGenerationStrategy(metaclass=abc.ABCMeta):
    """Interface for implementing the Strategy Pattern to generate paths starting from a given point of origin."""

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return (hasattr(subclass, "path_generator") and callable(subclass.path_generator) or
                NotImplemented)

    def __init__(self, **options) -> None:
        """Initialize object with optional keyword arguments."""

        self._options = options

    @property
    def options(self):
        return self._options

    @abc.abstractmethod
    def path_generator(self, **params) -> Iterator[List[Point2D]]:
        """
        Return a generator that produces a new path starting from an origin point on every iteration.

        Can accept optional parameters.
        """
        raise NotImplementedError

    def vector_array_to_path(self, vector_array: List[Point2D]) -> List[Point2D]:
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

    def path_generator(self, **params) -> Iterator[List[Point2D]]:
        """
        Given an origin point and parameters specifying path length, and x and y magnitudes; return a generator that
        produces all combinations of paths from the origin point.

        For Soldiers: x_magnitudes = {-1, 0, 1}, y_magnitudes = {[-1 or 1]}.
        For Chariots/Cannons: x_magnitudes = {0, 1}, y_magnitudes = {-1, 1}.
        For multi-step moves: step_range[1] > 2.

        :keyword Point2D source: The origin point to move from.
        :keyword tuple[int, int] step_range: The minimum and maximum path lengths.
        :keyword set[int, ...] x_magnitudes: A combination of magnitudes to be applied to the x-axis for each vector.
        :keyword set[int, ...] y_magnitudes: A combination of magnitudes to be applied to the y-axis for each vector.
        :return: Generator object that returns a new path on each iteration.
        """

        # Retrieve key args.
        source = params.get("source")
        step_range = self.options.get("step_range")
        x_magnitudes = self.options.get("x_magnitudes")
        y_magnitudes = self.options.get("y_magnitudes")

        # Create combination pairs to be used for path generation at next step.
        # If x and y are equal to 0, it's the same as not moving so skip and continue.
        combinations = [(s, x, y)
                        for s in range(*step_range)
                        for x in x_magnitudes
                        for y in y_magnitudes
                        if not (x == 0 == y)]

        # For each combination, calculate the vector array from source and convert them to a path.
        for s, x, y in combinations:
            vector_array = [source] + s * [Point2D(x * y, int(not x) * y)]
            path = self.vector_array_to_path(vector_array)

            yield path


class LinearDiagonalPathStrategy(IPathGenerationStrategy):
    """Path generation strategy specific to paths that move on the axis or diagonally away from an origin point."""

    def path_generator(self, **params) -> Iterator[List[Point2D]]:
        """
        Given an origin point and parameters specifying path length, x and y magnitudes, and diagonal movement
        limitations; return a generator that produces all combinations of paths from the origin point.

        For Generals/Guards: x_magnitudes = {-1, 0, 1}, y_magnitudes = {-1, 0, 1}.
        For Soldiers (inside palace only): x_magnitudes = {-1, 0, 1}, y_magnitudes = {0, [1 or -1]}.
        For multi-step moves (Cannons/Chariots inside palace only): step_range[1] > 2.
        For Cannons/Chariots inside palace: diag_limit = 2.

        :keyword Point2D source: The origin point to move from.
        :keyword tuple[int, int] step_range: The minimum and maximum path lengths.
        :keyword set[int, ...] x_magnitudes: A combination of magnitudes to be applied to the x-axis for each vector.
        :keyword set[int, ...] y_magnitudes: A combination of magnitudes to be applied to the y-axis for each vector.
        :keyword int diag_limit: An imposed limit for diagonal path lengths for when inside a palace.
        :return: Generator object that returns a new path on each iteration.
        """

        # Retrieve key args.
        source = params.get("source")
        step_range = self.options.get("step_range")
        x_magnitudes = self.options.get("x_magnitudes")
        y_magnitudes = self.options.get("y_magnitudes")

        # Default diag_limit to maximum steps piece can take.
        diag_limit = self.options.get("diag_limit", step_range[1])

        # Create combination pairs to be used for path generation at next step.
        # If x and y are equal to 0, it's the same as not moving so skip and continue.
        combinations = [(s, x, y)
                        for s in range(*step_range)
                        for x in x_magnitudes
                        for y in y_magnitudes
                        if not (x == 0 == y)
                        if not (abs(x) == abs(y) and s > diag_limit)]

        # For each combination, calculate the vector array from source and convert them to a path.
        for s, x, y in combinations:
            vector_array = [source] + s * [Point2D(x, y)]
            path = self.vector_array_to_path(vector_array)

            yield path


class BranchPathStrategy(IPathGenerationStrategy):
    """Path generation strategy specific to paths that change direction multiple times."""

    def path_generator(self, **params) -> Iterator[List[Point2D]]:
        """
        Given an origin point and parameters specifying path length, a set of scalars, and x and y magnitudes; return a
        generator that produces all combinations of paths from the origin point.

        For Horse/Elephant: x_magnitudes = {-1, 1}, y_magnitudes = {-1, 1}, magnitudes = {0, 1}.
        For multi-step moves: step_range = (2, 3).

        :keyword Point2D source: The origin point to move from.
        :keyword tuple[int, int] step_range: The minimum and maximum path lengths.
        :keyword set[int, ...] scalars: A combination of scalars to assist in generating branches.
        :keyword set[int, ...] x_magnitudes: A combination of magnitudes to be applied to the x-axis for each vector.
        :keyword set[int, ...] y_magnitudes: A combination of magnitudes to be applied to the y-axis for each vector.
        :return: Generator object that returns a new list of Point2D objects denoting a path on each iteration.
        """

        # Retrieve key args.
        source: Point2D = params.get("source")
        step_range: Tuple[int, int] = self.options.get("step_range")
        scalars: Set[int, ...] = self.options.get("magnitudes")
        x_magnitudes: Set[int, ...] = self.options.get("x_magnitudes")
        y_magnitudes: Set[int, ...] = self.options.get("y_magnitudes")

        # Create combination pairs to be used for path generation at next step.
        # If x and y are equal to 0, it's the same as not moving so skip and continue.
        combinations = [(s, m, x, y)
                        for s in range(*step_range)
                        for m in scalars
                        for x in x_magnitudes
                        for y in y_magnitudes
                        if not (x == 0 == y)]

        # For each combination, calculate the vector array from source and convert them to a path.
        for s, m, x, y in combinations:
            vector_array = [source, Point2D(m * x, int(not m) * y)] + s * [Point2D(x, y)]
            path = self.vector_array_to_path(vector_array)

            yield path
