from __future__ import annotations

import unittest
from typing import List, TYPE_CHECKING

from engine.helpers import BranchPathStrategy, LinearDiagonalPathStrategy, LinearPathStrategy
from engine.utils import Point2D

if TYPE_CHECKING:
    from engine.helpers import IPathGenerationStrategy


class TestIPathGenerationStrategy(unittest.TestCase):
    pass


class TestLinearDiagonalPathStrategy(unittest.TestCase):
    def setUp(self) -> None:
        self.general_guard_strat: IPathGenerationStrategy = LinearDiagonalPathStrategy(
            step_range=(1, 2), x_magnitudes={-1, 0, 1}, y_magnitudes={-1, 0, 1}, diag_limit=1
        )
        self.blue_soldier_in_palace_strat: IPathGenerationStrategy = LinearDiagonalPathStrategy(
            step_range=(1, 2), x_magnitudes={-1, 0, 1}, y_magnitudes={0, 1}, diag_limit=1
        )
        self.red_soldier_in_palace_strat: IPathGenerationStrategy = LinearDiagonalPathStrategy(
            step_range=(1, 2), x_magnitudes={-1, 0, 1}, y_magnitudes={0, -1}, diag_limit=1
        )
        self.chariot_cannon_in_palace_strat: IPathGenerationStrategy = LinearDiagonalPathStrategy(
            step_range=(1, 10), x_magnitudes={-1, 0, 1}, y_magnitudes={-1, 0, 1}, diag_limit=2
        )

        self.chariot_cannon_expected_paths: List[List[Point2D]] = [
            [Point2D(0, 0), Point2D(0, 1)],
            [Point2D(0, 0), Point2D(0, -1)],
            [Point2D(0, 0), Point2D(1, 0)],
            [Point2D(0, 0), Point2D(-1, 0)],
            [Point2D(0, 0), Point2D(0, 1), Point2D(0, 2)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(0, -2)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, 0)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, 0)],
            [Point2D(0, 0), Point2D(0, 1), Point2D(0, 2), Point2D(0, 3)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(0, -2), Point2D(0, -3)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, 0), Point2D(3, 0)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, 0), Point2D(-3, 0)],
            [Point2D(0, 0), Point2D(0, 1), Point2D(0, 2), Point2D(0, 3), Point2D(0, 4)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(0, -2), Point2D(0, -3), Point2D(0, -4)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, 0), Point2D(3, 0), Point2D(4, 0)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, 0), Point2D(-3, 0), Point2D(-4, 0)],
            [Point2D(0, 0), Point2D(0, 1), Point2D(0, 2), Point2D(0, 3), Point2D(0, 4), Point2D(0, 5)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(0, -2), Point2D(0, -3), Point2D(0, -4), Point2D(0, -5)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, 0), Point2D(3, 0), Point2D(4, 0), Point2D(5, 0)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, 0), Point2D(-3, 0), Point2D(-4, 0), Point2D(-5, 0)],
            [Point2D(0, 0), Point2D(0, 1), Point2D(0, 2), Point2D(0, 3), Point2D(0, 4), Point2D(0, 5),
             Point2D(0, 6)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(0, -2), Point2D(0, -3), Point2D(0, -4), Point2D(0, -5),
             Point2D(0, -6)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, 0), Point2D(3, 0), Point2D(4, 0), Point2D(5, 0),
             Point2D(6, 0)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, 0), Point2D(-3, 0), Point2D(-4, 0), Point2D(-5, 0),
             Point2D(-6, 0)],
            [Point2D(0, 0), Point2D(0, 1), Point2D(0, 2), Point2D(0, 3), Point2D(0, 4), Point2D(0, 5),
             Point2D(0, 6), Point2D(0, 7)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(0, -2), Point2D(0, -3), Point2D(0, -4), Point2D(0, -5),
             Point2D(0, -6), Point2D(0, -7)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, 0), Point2D(3, 0), Point2D(4, 0), Point2D(5, 0),
             Point2D(6, 0), Point2D(7, 0)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, 0), Point2D(-3, 0), Point2D(-4, 0), Point2D(-5, 0),
             Point2D(-6, 0), Point2D(-7, 0)],
            [Point2D(0, 0), Point2D(0, 1), Point2D(0, 2), Point2D(0, 3), Point2D(0, 4), Point2D(0, 5),
             Point2D(0, 6), Point2D(0, 7), Point2D(0, 8)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(0, -2), Point2D(0, -3), Point2D(0, -4), Point2D(0, -5),
             Point2D(0, -6), Point2D(0, -7), Point2D(0, -8)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, 0), Point2D(3, 0), Point2D(4, 0), Point2D(5, 0),
             Point2D(6, 0), Point2D(7, 0), Point2D(8, 0)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, 0), Point2D(-3, 0), Point2D(-4, 0), Point2D(-5, 0),
             Point2D(-6, 0), Point2D(-7, 0), Point2D(-8, 0)],
            [Point2D(0, 0), Point2D(0, 1), Point2D(0, 2), Point2D(0, 3), Point2D(0, 4), Point2D(0, 5),
             Point2D(0, 6), Point2D(0, 7), Point2D(0, 8), Point2D(0, 9)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(0, -2), Point2D(0, -3), Point2D(0, -4), Point2D(0, -5),
             Point2D(0, -6), Point2D(0, -7), Point2D(0, -8), Point2D(0, -9)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, 0), Point2D(3, 0), Point2D(4, 0), Point2D(5, 0),
             Point2D(6, 0), Point2D(7, 0), Point2D(8, 0), Point2D(9, 0)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, 0), Point2D(-3, 0), Point2D(-4, 0), Point2D(-5, 0),
             Point2D(-6, 0), Point2D(-7, 0), Point2D(-8, 0), Point2D(-9, 0)],
            [Point2D(0, 0), Point2D(1, 1)],
            [Point2D(0, 0), Point2D(-1, -1)],
            [Point2D(0, 0), Point2D(1, -1)],
            [Point2D(0, 0), Point2D(-1, 1)],
            [Point2D(0, 0), Point2D(1, 1), Point2D(2, 2)],
            [Point2D(0, 0), Point2D(-1, -1), Point2D(-2, -2)],
            [Point2D(0, 0), Point2D(1, -1), Point2D(2, -2)],
            [Point2D(0, 0), Point2D(-1, 1), Point2D(-2, 2)]
        ]

    def test_path_generator_returns_all_paths_for_general_or_guard(self) -> None:
        # -------------------- Arrange -------------------- #
        # All paths starting at origin.
        # Only need to test for one source position as paths go in all directions.
        starting_coord: Point2D = Point2D(0, 0)
        expected_paths: List[List[Point2D]] = [
            [Point2D(0, 0), Point2D(1, 0)],
            [Point2D(0, 0), Point2D(1, -1)],
            [Point2D(0, 0), Point2D(0, -1)],
            [Point2D(0, 0), Point2D(-1, -1)],
            [Point2D(0, 0), Point2D(-1, 0)],
            [Point2D(0, 0), Point2D(-1, 1)],
            [Point2D(0, 0), Point2D(0, 1)],
            [Point2D(0, 0), Point2D(1, 1)]
        ]

        # -------------------- Act -------------------- #
        # Generate all paths starting at origin.
        paths: List[List[Point2D]] = list(self.general_guard_strat.path_generator(source=starting_coord))

        # -------------------- Assert -------------------- #
        self.assertCountEqual(expected_paths, paths)

    def test_path_generator_returns_all_paths_for_blue_soldier_in_palace(self) -> None:
        # -------------------- Arrange -------------------- #
        # All paths starting at origin.
        # Only need to test for one source position as paths go in all directions.
        starting_coord: Point2D = Point2D(0, 0)
        expected_paths: List[List[Point2D]] = [
            [Point2D(0, 0), Point2D(1, 0)],
            [Point2D(0, 0), Point2D(-1, 0)],
            [Point2D(0, 0), Point2D(-1, 1)],
            [Point2D(0, 0), Point2D(0, 1)],
            [Point2D(0, 0), Point2D(1, 1)]
        ]

        # -------------------- Act -------------------- #
        # Generate all paths starting at origin.
        paths: List[List[Point2D]] = list(self.blue_soldier_in_palace_strat.path_generator(source=starting_coord))

        # -------------------- Assert -------------------- #
        self.assertCountEqual(expected_paths, paths)

    def test_path_generator_returns_all_paths_for_red_soldier_in_palace(self) -> None:
        # -------------------- Arrange -------------------- #
        # All paths starting at origin.
        # Only need to test for one source position as paths go in all directions.
        starting_coord: Point2D = Point2D(0, 0)
        expected_paths: List[List[Point2D]] = [
            [Point2D(0, 0), Point2D(1, 0)],
            [Point2D(0, 0), Point2D(1, -1)],
            [Point2D(0, 0), Point2D(0, -1)],
            [Point2D(0, 0), Point2D(-1, -1)],
            [Point2D(0, 0), Point2D(-1, 0)]
        ]

        # -------------------- Act -------------------- #
        # Generate all paths starting at origin.
        paths: List[List[Point2D]] = list(self.red_soldier_in_palace_strat.path_generator(source=starting_coord))

        # -------------------- Assert -------------------- #
        self.assertCountEqual(expected_paths, paths)

    def test_path_generator_returns_all_paths_for_chariot_or_cannon_in_palace(self) -> None:
        # -------------------- Arrange -------------------- #
        # All paths starting at origin.
        # Only need to test for one source position as paths go in all directions.
        starting_coord: Point2D = Point2D(0, 0)

        # -------------------- Act -------------------- #
        # Generate all paths starting at origin.
        paths: List[List[Point2D]] = list(self.chariot_cannon_in_palace_strat.path_generator(source=starting_coord))

        # -------------------- Assert -------------------- #
        self.assertCountEqual(self.chariot_cannon_expected_paths, paths)


class TestLinearPathStrategy(unittest.TestCase):
    def setUp(self) -> None:
        self.blue_soldier_strat: IPathGenerationStrategy = LinearPathStrategy(
            step_range=(1, 2), x_magnitudes={-1, 0, 1}, y_magnitudes={1}
        )
        self.red_soldier_strat: IPathGenerationStrategy = LinearPathStrategy(
            step_range=(1, 2), x_magnitudes={-1, 0, 1}, y_magnitudes={-1}
        )
        self.chariot_cannon_strat: IPathGenerationStrategy = LinearPathStrategy(
            step_range=(1, 10), x_magnitudes={0, 1}, y_magnitudes={-1, 1}
        )

        self.chariot_cannon_expected_paths: List[List[Point2D]] = [
            [Point2D(0, 0), Point2D(0, 1)],
            [Point2D(0, 0), Point2D(0, -1)],
            [Point2D(0, 0), Point2D(1, 0)],
            [Point2D(0, 0), Point2D(-1, 0)],
            [Point2D(0, 0), Point2D(0, 1), Point2D(0, 2)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(0, -2)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, 0)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, 0)],
            [Point2D(0, 0), Point2D(0, 1), Point2D(0, 2), Point2D(0, 3)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(0, -2), Point2D(0, -3)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, 0), Point2D(3, 0)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, 0), Point2D(-3, 0)],
            [Point2D(0, 0), Point2D(0, 1), Point2D(0, 2), Point2D(0, 3), Point2D(0, 4)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(0, -2), Point2D(0, -3), Point2D(0, -4)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, 0), Point2D(3, 0), Point2D(4, 0)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, 0), Point2D(-3, 0), Point2D(-4, 0)],
            [Point2D(0, 0), Point2D(0, 1), Point2D(0, 2), Point2D(0, 3), Point2D(0, 4), Point2D(0, 5)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(0, -2), Point2D(0, -3), Point2D(0, -4), Point2D(0, -5)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, 0), Point2D(3, 0), Point2D(4, 0), Point2D(5, 0)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, 0), Point2D(-3, 0), Point2D(-4, 0), Point2D(-5, 0)],
            [Point2D(0, 0), Point2D(0, 1), Point2D(0, 2), Point2D(0, 3), Point2D(0, 4), Point2D(0, 5),
             Point2D(0, 6)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(0, -2), Point2D(0, -3), Point2D(0, -4), Point2D(0, -5),
             Point2D(0, -6)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, 0), Point2D(3, 0), Point2D(4, 0), Point2D(5, 0),
             Point2D(6, 0)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, 0), Point2D(-3, 0), Point2D(-4, 0), Point2D(-5, 0),
             Point2D(-6, 0)],
            [Point2D(0, 0), Point2D(0, 1), Point2D(0, 2), Point2D(0, 3), Point2D(0, 4), Point2D(0, 5),
             Point2D(0, 6), Point2D(0, 7)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(0, -2), Point2D(0, -3), Point2D(0, -4), Point2D(0, -5),
             Point2D(0, -6), Point2D(0, -7)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, 0), Point2D(3, 0), Point2D(4, 0), Point2D(5, 0),
             Point2D(6, 0), Point2D(7, 0)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, 0), Point2D(-3, 0), Point2D(-4, 0), Point2D(-5, 0),
             Point2D(-6, 0), Point2D(-7, 0)],
            [Point2D(0, 0), Point2D(0, 1), Point2D(0, 2), Point2D(0, 3), Point2D(0, 4), Point2D(0, 5),
             Point2D(0, 6), Point2D(0, 7), Point2D(0, 8)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(0, -2), Point2D(0, -3), Point2D(0, -4), Point2D(0, -5),
             Point2D(0, -6), Point2D(0, -7), Point2D(0, -8)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, 0), Point2D(3, 0), Point2D(4, 0), Point2D(5, 0),
             Point2D(6, 0), Point2D(7, 0), Point2D(8, 0)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, 0), Point2D(-3, 0), Point2D(-4, 0), Point2D(-5, 0),
             Point2D(-6, 0), Point2D(-7, 0), Point2D(-8, 0)],
            [Point2D(0, 0), Point2D(0, 1), Point2D(0, 2), Point2D(0, 3), Point2D(0, 4), Point2D(0, 5),
             Point2D(0, 6), Point2D(0, 7), Point2D(0, 8), Point2D(0, 9)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(0, -2), Point2D(0, -3), Point2D(0, -4), Point2D(0, -5),
             Point2D(0, -6), Point2D(0, -7), Point2D(0, -8), Point2D(0, -9)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, 0), Point2D(3, 0), Point2D(4, 0), Point2D(5, 0),
             Point2D(6, 0), Point2D(7, 0), Point2D(8, 0), Point2D(9, 0)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, 0), Point2D(-3, 0), Point2D(-4, 0), Point2D(-5, 0),
             Point2D(-6, 0), Point2D(-7, 0), Point2D(-8, 0), Point2D(-9, 0)]
        ]

    def test_path_generator_returns_all_paths_for_blue_soldier(self) -> None:
        # -------------------- Arrange -------------------- #
        # All paths starting at origin.
        # Only need to test for one source position as paths go in all directions.
        starting_coord: Point2D = Point2D(0, 0)
        expected_paths: List[List[Point2D]] = [
            [Point2D(0, 0), Point2D(0, 1)],
            [Point2D(0, 0), Point2D(1, 0)],
            [Point2D(0, 0), Point2D(-1, 0)]
        ]

        # -------------------- Act -------------------- #
        # Generate all paths starting at origin.
        paths: List[List[Point2D]] = list(self.blue_soldier_strat.path_generator(source=starting_coord))

        # -------------------- Assert -------------------- #
        self.assertCountEqual(expected_paths, paths)

    def test_path_generator_returns_all_paths_for_red_soldier(self) -> None:
        # -------------------- Arrange -------------------- #
        # All paths starting at origin.
        # Only need to test for one source position as paths go in all directions.
        starting_coord: Point2D = Point2D(0, 0)
        expected_paths: List[List[Point2D]] = [
            [Point2D(0, 0), Point2D(0, -1)],
            [Point2D(0, 0), Point2D(1, 0)],
            [Point2D(0, 0), Point2D(-1, 0)]
        ]

        # -------------------- Act -------------------- #
        # Generate all paths starting at origin.
        paths: List[List[Point2D]] = list(self.red_soldier_strat.path_generator(source=starting_coord))

        # -------------------- Assert -------------------- #
        self.assertCountEqual(expected_paths, paths)

    def test_path_generator_returns_all_paths_for_chariot_or_cannon(self) -> None:
        # -------------------- Arrange -------------------- #
        # All paths starting at origin.
        # Only need to test for one source position as paths go in all directions.
        starting_coord: Point2D = Point2D(0, 0)

        # -------------------- Act -------------------- #
        # Generate all paths starting at origin.
        paths: List[List[Point2D]] = list(self.chariot_cannon_strat.path_generator(source=starting_coord))

        # -------------------- Assert -------------------- #
        self.assertCountEqual(self.chariot_cannon_expected_paths, paths)


class TestBranchPathStrategy(unittest.TestCase):
    def setUp(self) -> None:
        self.horse_strat: IPathGenerationStrategy = BranchPathStrategy(
            step_range=(1, 2), scalars={0, 1}, x_magnitudes={-1, 1}, y_magnitudes={-1, 1}
        )
        self.elephant_strat: IPathGenerationStrategy = BranchPathStrategy(
            step_range=(2, 3), scalars={0, 1}, x_magnitudes={-1, 1}, y_magnitudes={-1, 1}
        )

    def test_path_generator_returns_all_paths_for_horse(self) -> None:
        # -------------------- Arrange -------------------- #
        # All paths starting at origin.
        # Only need to test for one source position as paths go in all directions.
        starting_coord: Point2D = Point2D(0, 0)
        expected_paths: List[List[Point2D]] = [
            [Point2D(0, 0), Point2D(0, 1), Point2D(1, 2)],
            [Point2D(0, 0), Point2D(0, 1), Point2D(-1, 2)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(1, -2)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(-1, -2)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, 1)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, -1)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, 1)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, -1)]
        ]

        # -------------------- Act -------------------- #
        # Generate all paths starting at origin.
        paths: List[List[Point2D]] = list(self.horse_strat.path_generator(source=starting_coord))

        # -------------------- Assert -------------------- #
        self.assertCountEqual(expected_paths, paths)

    def test_path_generator_returns_all_paths_for_elephant(self) -> None:
        # -------------------- Arrange -------------------- #
        # All paths starting at origin.
        # Only need to test for one source position as paths go in all directions.
        starting_coord: Point2D = Point2D(0, 0)
        expected_paths: List[List[Point2D]] = [
            [Point2D(0, 0), Point2D(0, 1), Point2D(1, 2), Point2D(2, 3)],
            [Point2D(0, 0), Point2D(0, 1), Point2D(-1, 2), Point2D(-2, 3)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(1, -2), Point2D(2, -3)],
            [Point2D(0, 0), Point2D(0, -1), Point2D(-1, -2), Point2D(-2, -3)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, 1), Point2D(3, 2)],
            [Point2D(0, 0), Point2D(1, 0), Point2D(2, -1), Point2D(3, -2)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, 1), Point2D(-3, 2)],
            [Point2D(0, 0), Point2D(-1, 0), Point2D(-2, -1), Point2D(-3, -2)]
        ]

        # -------------------- Act -------------------- #
        # Generate all paths starting at origin.
        paths: List[List[Point2D]] = list(self.elephant_strat.path_generator(source=starting_coord))

        # -------------------- Assert -------------------- #
        self.assertCountEqual(expected_paths, paths)


if __name__ == "__main__":
    unittest.main()
