import unittest
from unittest.mock import patch

from engine.janggi_game import GameState, JanggiGame
from engine.janggi_piece import PieceColor
from engine.utils import Point2D


class TestJanggiGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = JanggiGame()

    def test_change_player_alternated_player_turn(self) -> None:
        """Calling set_player_turn should set player_turn to opposing player."""

        # -------------------- Arrange -------------------- #
        expected_turn1 = PieceColor.BLUE
        expected_turn2 = PieceColor.RED

        # -------------------- Act/Assert -------------------- #
        # Initial turn on game start should be BLUE
        turn = self.game.player_turn
        self.assertEqual(expected_turn1, turn)

        # After setting turn, next turn should be RED
        self.game.change_player()
        turn = self.game.player_turn
        self.assertEqual(expected_turn2, turn)

        # After setting turn, next turn should be BLUE
        self.game.change_player()
        turn = self.game.player_turn
        self.assertEqual(expected_turn1, turn)

    def test_make_move_returns_false_if_player_tries_to_pass_turn_while_they_are_in_check(self):
        # -------------------- Arrange -------------------- #
        # Move red soldier to put blue general in check.
        self.game.move(Point2D(0, 6), Point2D(3, 2))

        # Reset turn to blue player.
        self.game.change_player()

        # -------------------- Act/Assert -------------------- #
        msg = "BLUE tries to pass turn while their General is in check by RED Soldier."
        can_move = self.game.make_move("a10", "a10")
        self.assertFalse(can_move, msg)

    def test_make_move_returns_true_if_player_tries_to_pass_turn_while_they_are_not_in_check(self):
        # -------------------- Act/Assert -------------------- #
        msg = "BLUE tries to pass turn on first turn."
        can_move = self.game.make_move("a10", "a10")
        self.assertTrue(can_move, msg)

    @patch("janggi_game.JanggiGame.is_move_valid")
    @patch("janggi_game.JanggiGame.is_in_check")
    @patch("janggi_game.JanggiGame.is_checkmate")
    def test_make_move_updates_game_state_if_checkmate(self, validation_mock, in_check_mock, checkmate_mock):
        # -------------------- Arrange -------------------- #
        # Assume move is valid and results in a checkmate.
        validation_mock.return_value = True
        checkmate_mock.return_value = True
        in_check_mock.return_value = True

        # -------------------- Act ------------------------ #
        self.game.make_move("a10", "a10")
        expected_state = GameState.BLUE_WON
        state = self.game.game_state

        # -------------------- Assert --------------------- #
        self.assertEqual(expected_state, state)

    def test_is_move_valid_returns_false_if_game_is_over(self):
        # -------------------- Arrange -------------------- #
        self.game.game_state = GameState.BLUE_WON

        # -------------------- Act ------------------------ #
        is_valid = self.game.is_move_valid(Point2D(4, 1), Point2D(4, 1))

        # -------------------- Assert --------------------- #
        self.assertFalse(is_valid)

    def test_make_move_returns_false_if_not_current_players_turn(self) -> None:
        """
        Calling make_move should return false if the piece that is being moved is not same color as current player
        whose turn it is to move.
        """

        # -------------------- Arrange -------------------- #
        # RED player piece: chariot at position A1 requests move one unit forward to A2
        source1 = "a1"
        destination1 = "a2"

        # BLUE player piece: chariot at position A10 requests move one unit forward to A9
        source2 = "a10"
        destination2 = "a9"

        # -------------------- Act/Assert -------------------- #
        # At game start, it is the BLUE player's turn
        result = self.game.make_move(source1, destination1)
        self.assertFalse(result)

        self.game.change_player()

        # Now it is the RED player's turn
        result = self.game.make_move(source2, destination2)
        self.assertFalse(result)

    def test_make_move_returns_true_if_current_players_turn(self) -> None:
        """
        Calling make_move should return true if the piece that is being moved is the same color as current player
        whose turn it is to move.
        """

        # -------------------- Arrange -------------------- #
        # RED player piece: chariot at position A1 requests move one unit forward to A2
        source1 = "a1"
        destination1 = "a2"

        # BLUE player piece: chariot at position A10 requests move one unit forward to A9
        source2 = "a10"
        destination2 = "a9"

        # -------------------- Act/Assert -------------------- #
        # At game start, it is the BLUE player's turn
        result = self.game.make_move(source2, destination2)
        self.assertTrue(result)

        # Now it is the RED player's turn
        result = self.game.make_move(source1, destination1)
        self.assertTrue(result)

    def test_is_in_check_returns_true_if_player_in_check(self):
        # -------------------- Arrange -------------------- #
        # Place red soldier on diagonal in palace across blue general that is in the center.
        self.game.board.move(Point2D(0, 6), Point2D(5, 2))

        # ------------------------ Act ----------------------- #
        in_check = self.game.is_in_check(PieceColor.BLUE)

        # -------------------- Act/Assert -------------------- #
        self.assertTrue(in_check)

    def test_is_in_check_returns_false_if_player_not_in_check(self):
        # ------------------------ Act ----------------------- #
        in_check = self.game.is_in_check(PieceColor.BLUE)

        # -------------------- Act/Assert -------------------- #
        self.assertFalse(in_check)

    def test_is_checkmate_returns_true_if_player_has_been_checkmated(self) -> None:
        # -------------------- Arrange -------------------- #
        # Move blue general to top left corner of palace.
        self.game.move(Point2D(4, 1), Point2D(3, 2))

        # Move blue soldier 1 below general
        self.game.move(Point2D(2, 3), Point2D(3, 1))

        # Move blue soldier 2 to the right of general
        self.game.move(Point2D(4, 3), Point2D(4, 2))

        # Move blue elephant to center of palace
        self.game.move(Point2D(1, 0), Point2D(4, 1))

        # Move red chariot to be above blue general (but can't be captured).
        self.game.move(Point2D(0, 9), Point2D(3, 6))

        with self.subTest("SCENARIO 1: Blue General cornered by own pieces in checkmate by red Cannon."):
            # -------------------- Act/Assert -------------------- #
            checkmate: bool = self.game.is_checkmate(PieceColor.BLUE)
            self.assertTrue(checkmate)

        with self.subTest("SCENARIO 2: Blue General cornered by own pieces in checkmate by red Cannon and red horse."):
            # -------------------- Arrange -------------------- #
            # Move red horse to be on path to blue general.
            self.game.move(Point2D(2, 9), Point2D(2, 4))

            # -------------------- Act/Assert -------------------- #
            checkmate: bool = self.game.is_checkmate(PieceColor.BLUE)
            self.assertTrue(checkmate)

        with self.subTest("SCENARIO 3: Blue General cornered by own pieces in check by red horse. If blue soldier moves"
                          " to capture/block red horse, it opens a pathway for red chariot to capture general."):

            # -------------------- Arrange -------------------- #
            # Move red horse to be on path to blue general.
            self.game.move(Point2D(2, 4), Point2D(5, 3))

            # Move blue soldier 3 so that red horse can only be captured by blue soldier 1.
            self.game.move(Point2D(6, 3), Point2D(7, 3))

            # Move red chariot to be able to attack general once red soldier moves to defend.
            self.game.move(Point2D(3, 6), Point2D(5, 2))

            # -------------------- Act/Assert -------------------- #
            checkmate: bool = self.game.is_checkmate(PieceColor.BLUE)
            self.assertTrue(checkmate)

    def test_is_checkmate_returns_false_if_player_has_not_been_checkmated(self) -> None:
        # -------------------- Arrange -------------------- #
        # Move blue general to top left corner of palace.
        self.game.move(Point2D(4, 1), Point2D(3, 2))

        # Move blue soldier 1 below general
        self.game.move(Point2D(2, 3), Point2D(3, 1))

        # Move blue soldier 2 to the right of general
        self.game.move(Point2D(4, 3), Point2D(4, 2))

        # Move red chariot to be above blue general (but can't be captured).
        self.game.move(Point2D(0, 9), Point2D(3, 6))

        with self.subTest("SCENARIO 1: Blue General in check by Red Chariot; but can escape the check."):
            # -------------------- Act/Assert -------------------- #
            checkmate: bool = self.game.is_checkmate(PieceColor.BLUE)
            self.assertFalse(checkmate)

        with self.subTest("SCENARIO 2: Blue General cornered by own pieces in check by Red Horse; but red soldier "
                          "to right of Blue General can move to block the attack."):

            # -------------------- Arrange -------------------- #
            # Move blue elephant to center of palace
            self.game.move(Point2D(1, 0), Point2D(4, 1))

            # Move red chariot out of way so it can't attack blue general.
            self.game.move(Point2D(3, 6), Point2D(7, 6))

            # Move red horse to be on path to blue general.
            self.game.move(Point2D(2, 9), Point2D(5, 3))

            # Move blue soldier 3 so that red horse can only be captured by blue soldier 1.
            self.game.move(Point2D(6, 3), Point2D(7, 3))

            # Move blue elephant so that it can't intercept red horse.
            self.game.move(Point2D(6, 0), Point2D(0, 1))

            # -------------------- Act/Assert -------------------- #
            checkmate: bool = self.game.is_checkmate(PieceColor.BLUE)
            self.assertFalse(checkmate)


if __name__ == "__main__":
    unittest.main()
