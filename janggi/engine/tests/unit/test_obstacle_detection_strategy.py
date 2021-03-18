import unittest

import itertools

from janggi_piece import JanggiPiece, PieceCategory, PieceColor
from utils.point import Point2D
from utils.rectangle import Rectangle
from helpers.obstacle_detection_strategy import IllegalDestinationStrategy, IllegalPathStrategy, InsidePalaceStrategy
from helpers.path_generation_strategy import LinearDiagonalPathStrategy, LinearPathStrategy


class TestIObstacleDetectionStrategy(unittest.TestCase):
    def setUp(self) -> None:
        self.default_obstacle_strategy = dict(
            destination=IllegalDestinationStrategy(),
            path=IllegalPathStrategy(),
            palace=InsidePalaceStrategy()
        )
        self.gg_strat = [
            dict(
                default=None,
                palace=LinearDiagonalPathStrategy(
                    step_range=(1, 2), x_magnitudes={-1, 0, 1}, y_magnitudes={-1, 0, 1}, diag_limit=1
                ),
            ),
            self.default_obstacle_strategy
        ]
        self.cc_strat = [
            dict(
                default=LinearPathStrategy(step_range=(1, 10), x_magnitudes={0, 1}, y_magnitudes={-1, 1}),
                palace=LinearDiagonalPathStrategy(
                    step_range=(1, 10), x_magnitudes={-1, 0, 1}, y_magnitudes={-1, 0, 1}, diag_limit=2
            )),
            self.default_obstacle_strategy
        ]
        # Default pieces
        self.blue_general = JanggiPiece(PieceColor.BLUE, PieceCategory.GENERAL, Point2D(4, 2), self.gg_strat[0],
                                        self.gg_strat[1], True)
        self.blue_chariot = JanggiPiece(PieceColor.BLUE, PieceCategory.CHARIOT, Point2D(4, 2), self.cc_strat[0],
                                        self.cc_strat[1])
        self.red_soldier = JanggiPiece(PieceColor.RED, PieceCategory.SOLDIER, None, None, None)
        self.red_chariot = JanggiPiece(PieceColor.RED, PieceCategory.CHARIOT, None, None, None)
        self.blue_cannon = JanggiPiece(PieceColor.BLUE, PieceCategory.CANNON, None, None, None)
        self.red_cannon = JanggiPiece(PieceColor.RED, PieceCategory.CANNON, None, None, None)
        self.blue_horse = JanggiPiece(PieceColor.BLUE, PieceCategory.HORSE, None, None, None)
        self.red_horse = JanggiPiece(PieceColor.RED, PieceCategory.HORSE, None, None, None)
        self.red_elephant = JanggiPiece(PieceColor.RED, PieceCategory.ELEPHANT, None, None, None)

        # Palaces
        self.palaces = dict(
            blue=Rectangle([Point2D(3, 0), Point2D(3, 2), Point2D(5, 2), Point2D(5, 0)]),
            red=Rectangle([Point2D(3, 7), Point2D(3, 9), Point2D(5, 9), Point2D(5, 7)])
        )

        # Board coordinates
        self.blue_palace_walls = [
            Point2D(3, 0), Point2D(4, 0), Point2D(5, 0),
            Point2D(3, 1), Point2D(5, 1),
            Point2D(3, 2), Point2D(4, 2), Point2D(5, 2)
        ]

        self.blue_palace_coords = list(self.blue_palace_walls)
        self.blue_palace_coords.append(Point2D(4, 1))

        # Immediate coordinates 1 unit outside palace walls
        self.blue_outer_palace_coords = [
            Point2D(2, 0), Point2D(2, 1), Point2D(2, 2), Point2D(2, 3),
            Point2D(3, 3), Point2D(4, 3), Point2D(5, 3),
            Point2D(6, 3), Point2D(6, 2), Point2D(6, 1), Point2D(6, 0)
        ]

        self.in_out_paths = self.generate_all_paths_starting_from_palace_wall_and_ending_outside_palace()

    def generate_all_paths_starting_from_palace_wall_and_ending_outside_palace(self):
        """Generate all paths that leave palace walls for blue palace."""

        # Illegal paths for palace bound pieces
        blue_inner_outer_palace_coords = list(self.blue_palace_walls) + list(self.blue_outer_palace_coords)
        paths = list(map(list, itertools.permutations(blue_inner_outer_palace_coords, 2)))
        in_out_paths = list()

        blue_outer_palace_coords_tuple = [coord.to_tuple() for coord in self.blue_outer_palace_coords]
        blue_palace_coords_tuple = [coord.to_tuple() for coord in self.blue_palace_coords]

        for path in paths:

            # Don't add paths that originate outside palace
            if path[0].to_tuple() in blue_outer_palace_coords_tuple:
                continue

            # Don't add paths that start and end outside palace
            if path[0].to_tuple() in blue_outer_palace_coords_tuple \
                    and path[1].to_tuple() in blue_outer_palace_coords_tuple:
                continue

            # Don't add paths that end inside palace
            if path[1].to_tuple() in blue_palace_coords_tuple:
                continue

            # Don't add paths that are not 1 unit away from origin
            if abs(path[1].x - path[0].x) > 1 or abs(path[1].y - path[0].y) > 1:
                continue

            in_out_paths.append(path)

        return in_out_paths


class TestInsidePalaceStrategy(TestIObstacleDetectionStrategy):
    def setUp(self) -> None:
        super().setUp()

        self.bound_strat = InsidePalaceStrategy()
        self.unbound_strat = InsidePalaceStrategy()

    def test_palace_bound_or_unbound_piece_can_move_freely_within_palace(self):
        # -------------------- Arrange -------------------- #
        # Assume paths for blue piece inside blue palace as it shouldn't matter which color they are or what palace
        # they are within.
        color: PieceColor = PieceColor.BLUE
        in_palace_paths = list(map(list, itertools.permutations(self.blue_palace_coords, 2)))

        # Invalid diagonal movement inside blue palace
        invalid_paths = [
            [Point2D(4, 2), Point2D(5, 1)],
            [Point2D(4, 2), Point2D(3, 1)],
            [Point2D(4, 0), Point2D(5, 1)],
            [Point2D(4, 0), Point2D(3, 1)],
            [Point2D(3, 1), Point2D(4, 2)],
            [Point2D(3, 1), Point2D(4, 0)],
            [Point2D(5, 1), Point2D(4, 2)],
            [Point2D(5, 1), Point2D(4, 0)]
        ]

        valid_paths = list()
        for path in in_palace_paths:

            # Don't add paths that are not 1 unit away from origin
            if abs(path[1].x - path[0].x) > 1 or abs(path[1].y - path[0].y) > 1:
                continue

            # Don't add paths that do not travel across palace diagonal.
            if path in invalid_paths:
                continue

            valid_paths.append(path)

        # -------------------- Act/Assert -------------------- #
        for path in valid_paths:
            with self.subTest(path=path, color=color):
                # Bounded piece can move freely inside palace
                self.assertFalse(self.blue_general.is_obstacle_in_path(
                    in_palace=True, path_objects=[self.blue_general, None], path=path, blue_palace=self.palaces["blue"],
                    red_palace=self.palaces["red"]
                ))

                # Unbounded piece can move freely inside palace
                self.assertFalse(self.blue_chariot.is_obstacle_in_path(
                    in_palace=True, path_objects=[self.blue_chariot, None], path=path, blue_palace=self.palaces["blue"],
                    red_palace=self.palaces["red"]
                ))

    def test_palace_bound_piece_cannot_leave_palace(self):
        # -------------------- Arrange -------------------- #
        color: PieceColor = PieceColor.BLUE

        # -------------------- Act/Assert -------------------- #
        for path in self.in_out_paths:
            with self.subTest(path=path, color=color):
                self.assertTrue(self.blue_general.is_obstacle_in_path(
                    in_palace=True, path_objects=[self.blue_general, None], path=path, blue_palace=self.palaces["blue"],
                    red_palace=self.palaces["red"]
                ))

    def test_palace_unbound_piece_can_leave_palace_horizontally_or_vertically(self):
        # -------------------- Arrange -------------------- #
        color: PieceColor = PieceColor.BLUE

        # Filter paths that traverse horizontally or vertically outside palace walls.
        paths = list()
        for path in self.in_out_paths:
            translation = path[1] - path[0]

            # Path involves diagonal move.
            if abs(translation.x) >= 1 and abs(translation.y) >= 1:
                continue

            paths.append(path)

        # -------------------- Act/Assert -------------------- #
        for path in paths:
            with self.subTest(path=path, color=color):
                self.assertFalse(self.blue_chariot.is_obstacle_in_path(
                    in_palace=True, path_objects=[self.blue_chariot, None], path=path, blue_palace=self.palaces["blue"],
                    red_palace=self.palaces["red"]
                ))

    def test_palace_unbound_piece_cannot_leave_palace_diagonally(self):
        # -------------------- Arrange -------------------- #
        color: PieceColor = PieceColor.BLUE

        # Filter paths that traverse diagonally outside palace walls.
        illegal_paths = list()
        for path in self.in_out_paths:
            translation = path[1] - path[0]

            # Path does not involve diagonal move.
            if not(abs(translation.x) >= 1 and abs(translation.y) >= 1):
                continue

            illegal_paths.append(path)

        # -------------------- Act/Assert -------------------- #
        for path in illegal_paths:
            with self.subTest(path=path, color=color):
                self.assertTrue(self.blue_chariot.is_obstacle_in_path(
                    in_palace=True, path_objects=[self.blue_chariot, None], path=path, blue_palace=self.palaces["blue"],
                    red_palace=self.palaces["red"]
                ))


class TestIllegalDestinationStrategy(TestIObstacleDetectionStrategy):
    def setUp(self) -> None:
        super().setUp()

        self.dest_strat = IllegalDestinationStrategy()

    def test_piece_can_move_to_empty_coord(self):
        """
        Test if a piece can move to an empty position on the board.

        Choose blue general in blue palace, as the piece category, color, or position does not matter in these tests.
        """

        # -------------------- Arrange -------------------- #
        # Assume paths for blue piece inside blue palace as it shouldn't matter which color they are or what palace
        # they are within.
        color: PieceColor = PieceColor.BLUE

        # Place blue general in center of blue palace
        self.blue_general.position = Point2D(4, 1)
        destination = Point2D(4, 2)

        # -------------------- Act/Assert -------------------- #
        with self.subTest(msg="Piece can move to empty spot.", path=destination, color=color):
            self.assertFalse(self.dest_strat.is_obstacle_in_path(path_objects=[self.blue_general, None]))

    def test_piece_can_capture_enemy_of_same_category_if_not_category_restricted(self):
        """
        Test if a piece can capture an enemy piece of same category if they're not category restricted.

        Choose blue general in blue palace, as the piece category, color, or position does not matter in these tests.
        """

        # -------------------- Arrange -------------------- #
        # Place general at center of palace
        self.blue_general.position = Point2D(4, 1)

        # Create enemy for general to capture.
        enemy = JanggiPiece(PieceColor.RED, PieceCategory.GENERAL, Point2D(4, 2), None, None, True)

        # -------------------- Act/Assert -------------------- #
        self.assertFalse(
            self.dest_strat.is_obstacle_in_path(path_objects=[self.blue_general, enemy]),
            msg="Piece can capture same category if it is not category restricted."
        )

    def test_piece_cannot_capture_enemy_of_same_category_if_category_restricted(self):
        """
        Test if a piece cannot capture an enemy piece of same category if they're category restricted.

        Choose blue general in blue palace, as the piece category, color, or position does not matter in these tests.
        """

        # -------------------- Arrange -------------------- #
        # Place general at center of palace
        self.blue_cannon.position = Point2D(4, 1)

        # Create enemy for general to capture.
        enemy = JanggiPiece(PieceColor.RED, PieceCategory.CANNON, Point2D(4, 2), None, None, True)

        # -------------------- Act/Assert -------------------- #
        # Can't capture enemy of same type if category restricted.
        self.assertTrue(self.dest_strat.is_obstacle_in_path(path_objects=[self.blue_cannon, enemy]))

    def test_piece_cannot_capture_teammate(self):
        """
        Test if a piece can't capture teammate.

        Choose blue general in blue palace, as the piece category, color, or position does not matter in these tests.
        """

        # -------------------- Arrange -------------------- #
        # Place general at center of palace
        self.blue_general.position = Point2D(4, 1)

        # Create enemy for general to capture.
        teammate = JanggiPiece(PieceColor.BLUE, PieceCategory.GENERAL, Point2D(4, 2),None, None, True)

        # -------------------- Act/Assert -------------------- #
        # Can't capture enemy of same type if category restricted.
        self.assertTrue(self.dest_strat.is_obstacle_in_path(path_objects=[self.blue_general, teammate]))


class TestIllegalPathStrategy(TestIObstacleDetectionStrategy):
    def setUp(self) -> None:
        super().setUp()

        self.strat = IllegalPathStrategy()

    def test_category_restricted_piece_cannot_move_if_not_exactly_one_piece_in_path(self):
        # -------------------- Arrange -------------------- #
        path_objects1 = [self.blue_cannon, None, self.red_horse]
        path_objects2 = [self.blue_cannon, self.red_horse]
        path_objects3 = [self.blue_cannon, self.red_horse, self.red_elephant, self.red_horse]

        # -------------------- Act/Assert -------------------- #
        with self.subTest(msg="Cannon tries to capture horse with no piece in between."):
            self.assertTrue(self.strat.is_obstacle_in_path(path_objects1))

        with self.subTest(msg="Cannon tries to capture horse directly in front of it."):
            self.assertTrue(self.strat.is_obstacle_in_path(path_objects2))

        with self.subTest(msg="Cannon tries to capture horse with more than one piece in its path."):
            self.assertTrue(self.strat.is_obstacle_in_path(path_objects3))

    def test_category_restricted_piece_cannot_move_if_exactly_one_piece_in_path_that_is_same_category(self):
        # -------------------- Arrange -------------------- #
        path_objects = [self.blue_cannon, self.red_cannon, self.red_horse]

        # -------------------- Act/Assert -------------------- #
        with self.subTest(msg="Cannon tries to capture horse with cannon in its path."):
            self.assertTrue(self.strat.is_obstacle_in_path(path_objects))

    def test_category_restricted_piece_can_move_if_exactly_one_piece_in_path_that_is_not_same_category(self):
        # -------------------- Arrange -------------------- #
        path_objects = [self.blue_cannon, self.blue_horse, self.red_horse]

        # -------------------- Act/Assert -------------------- #
        with self.subTest(msg="Cannon tries to capture horse with one horse in its path."):
            self.assertFalse(self.strat.is_obstacle_in_path(path_objects))

    def test_non_category_restricted_piece_cannot_move_if_one_or_more_pieces_in_path(self):
        # -------------------- Arrange -------------------- #
        path_objects = [self.blue_chariot, self.red_soldier, self.red_horse]

        # -------------------- Act/Assert -------------------- #
        with self.subTest(msg="Chariot tries to capture horse with one soldier in its path."):
            self.assertTrue(self.strat.is_obstacle_in_path(path_objects))

    def test_non_category_restricted_piece_can_move_if_no_pieces_in_path(self):
        # -------------------- Arrange -------------------- #
        path_objects1 = [self.blue_chariot, self.red_chariot]
        path_objects2 = [self.blue_chariot, None, None, self.red_chariot]

        # -------------------- Act/Assert -------------------- #
        with self.subTest(msg="Chariot tries to capture enemy chariot directly in front of it."):
            self.assertFalse(self.strat.is_obstacle_in_path(path_objects1))

        with self.subTest(msg="Chariot tries to capture enemy chariot with no piece in its path."):
            self.assertFalse(self.strat.is_obstacle_in_path(path_objects2))


if __name__ == "__main__":
    unittest.main()
