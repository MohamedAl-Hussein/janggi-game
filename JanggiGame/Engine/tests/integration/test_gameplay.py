import unittest

from game import GameState, JanggiGame


class TestGamePlay(unittest.TestCase):
    def setUp(self) -> None:
        self.game = JanggiGame()

    def test_gameplay_sequences_scenario_one(self) -> None:
        """
        SCENARIO 01

        Each player moves a piece on every turn, making sure every piece is moved exactly once.
        Then proceed to capture as many pieces as possible.
        """

        # ---------------------- PHASE 1: Move Every Piece ----------------------- #

        src, dst = "a7", "a6"
        with self.subTest(msg=f"001: BLUE moves Soldier from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "a4", "a5"
        with self.subTest(msg=f"002: RED moves Soldier from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "i7", "i6"
        with self.subTest(msg=f"003: BLUE moves Soldier from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "i4", "i5"
        with self.subTest(msg=f"004: RED moves Soldier from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "c7", "c6"
        with self.subTest(msg=f"005: BLUE moves Soldier from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "c4", "c5"
        with self.subTest(msg=f"006: RED moves Soldier from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "g7", "g6"
        with self.subTest(msg=f"007: BLUE moves Soldier from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "g4", "g5"
        with self.subTest(msg=f"008: RED moves Soldier from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "e7", "e6"
        with self.subTest(msg=f"009: BLUE moves Soldier from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "e4", "e5"
        with self.subTest(msg=f"010: RED moves Soldier from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "a10", "a7"
        with self.subTest(msg=f"011: BLUE moves Chariot from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "a1", "a4"
        with self.subTest(msg=f"012: RED moves Chariot from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "i10", "i7"
        with self.subTest(msg=f"013: BLUE moves Chariot from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "i1", "i4"
        with self.subTest(msg=f"014: RED moves Chariot from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "b10", "d7"
        with self.subTest(msg=f"015: BLUE moves Elephant from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "b1", "d4"
        with self.subTest(msg=f"016: RED moves Elephant from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "g10", "e7"
        with self.subTest(msg=f"017: BLUE moves Elephant from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "g1", "e4"
        with self.subTest(msg=f"018: RED moves Elephant from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "c10", "d8"
        with self.subTest(msg=f"019: BLUE moves Horse from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "c1", "d3"
        with self.subTest(msg=f"020: RED moves Horse from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "h10", "g8"
        with self.subTest(msg=f"021: BLUE moves Horse from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "h1", "g3"
        with self.subTest(msg=f"022: RED moves Horse from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "b8", "e8"
        with self.subTest(msg=f"023: BLUE moves Cannon from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "b3", "e3"
        with self.subTest(msg=f"024: RED moves Cannon from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "h8", "f8"
        with self.subTest(msg=f"025: BLUE moves Cannon from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "h3", "f3"
        with self.subTest(msg=f"026: RED moves Cannon from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "d10", "d9"
        with self.subTest(msg=f"027: BLUE moves Guard from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "d1", "d2"
        with self.subTest(msg=f"028: RED moves Guard from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "f10", "f9"
        with self.subTest(msg=f"029: BLUE moves Guard from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "f1", "f2"
        with self.subTest(msg=f"030: RED moves Guard from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "e9", "e10"
        with self.subTest(msg=f"031: BLUE moves General from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "e2", "e1"
        with self.subTest(msg=f"032: RED moves General from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        # Check to see if all pieces still remain on board.
        piece_count = len(self.game.board.coord_map)
        expected_piece_count = 32
        self.assertEqual(expected_piece_count, piece_count)

        # ---------------------- PHASE 2: Capture Pieces ----------------------- #

        src, dst = "a6", "a5"
        with self.subTest(msg=f"033: BLUE moves Soldier from {src} to {dst} to capture RED Soldier."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "i5", "i6"
        with self.subTest(msg=f"034: RED moves Soldier from {src} to {dst} to capture BLUE Soldier."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "c6", "c5"
        with self.subTest(msg=f"035: BLUE moves Soldier from {src} to {dst} to capture RED Soldier."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "g5", "g6"
        with self.subTest(msg=f"036: RED moves Soldier from {src} to {dst} to capture BLUE Soldier."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "e6", "e5"
        with self.subTest(msg=f"037: BLUE moves Soldier from {src} to {dst} to capture RED Soldier."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "a4", "a5"
        with self.subTest(msg=f"038: RED moves Chariot from {src} to {dst} to capture BLUE Soldier."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "i7", "i6"
        with self.subTest(msg=f"039: BLUE moves Chariot from {src} to {dst} to capture RED Soldier."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "a5", "c5"
        with self.subTest(msg=f"040: RED moves Chariot from {src} to {dst} to capture BLUE Soldier."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "i6", "g6"
        with self.subTest(msg=f"041: BLUE moves Chariot from {src} to {dst} to capture RED Soldier."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "e3", "e5"
        with self.subTest(msg=f"042: RED moves Cannon from {src} to {dst} to capture BLUE Soldier."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "g6", "g3"
        with self.subTest(msg=f"043: BLUE moves Chariot from {src} to {dst} to capture RED Horse."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "c5", "c4"
        with self.subTest(msg=f"044: RED moves Chariot from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "e7", "c4"
        with self.subTest(msg=f"045: BLUE moves Elephant from {src} to {dst} to capture RED Chariot."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "e1", "e1"
        with self.subTest(msg=f"046: RED moves General from {src} to {dst} to pass their turn."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "g3", "f3"
        with self.subTest(msg=f"047: BLUE moves Chariot from {src} to {dst} to capture RED Cannon."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "e1", "e1"
        with self.subTest(msg=f"048: RED moves General from {src} to {dst} to pass their turn."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "f8", "f2"
        with self.subTest(msg=f"049: BLUE moves Cannon from {src} to {dst} to capture RED Guard."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "e1", "f2"
        with self.subTest(msg=f"050: RED tries to move General from {src} to {dst} to capture BLUE Cannon but can't"
                              f"as it will be captured on next turn by BLUE Chariot."):
            self.assertFalse(self.game.make_move(src, dst))

        src, dst = "d3", "f2"
        with self.subTest(msg=f"051: RED moves Horse from {src} to {dst} to capture BLUE Cannon."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "f3", "f2"
        with self.subTest(msg=f"052: BLUE moves Chariot from {src} to {dst} to capture RED Horse and puts RED General"
                              f"in check."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "e1", "f2"
        with self.subTest(msg=f"053: RED tries to move General from {src} to {dst} to capture BLUE Chariot but can't as"
                              f" it is the move does not involve the palace's diagonal lines."):
            self.assertFalse(self.game.make_move(src, dst))

        src, dst = "i4", "i10"
        with self.subTest(msg=f"054: RED moves Chariot from {src} to {dst} and puts BLUE General in check."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "e10", "e10"
        with self.subTest(msg=f"055: BLUE tries to move General from {src} to {dst} to pass their turn but can't as "
                              f"they are in check by RED Chariot"):
            self.assertFalse(self.game.make_move(src, dst))

        src, dst = "f9", "f10"
        with self.subTest(msg=f"056: BLUE moves Guard from {src} to {dst} to intercept check made by RED Chariot "
                              f"by blocking their path."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "i10", "f10"
        with self.subTest(msg=f"057: RED moves Chariot from {src} to {dst} to capture BLUE Guard and put BLUE General"
                              f" in check."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "g8", "f10"
        with self.subTest(msg=f"058: BLUE moves Horse from {src} to {dst} to intercept check made by RED Chariot by"
                              f" capturing RED chariot."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "d4", "f7"
        with self.subTest(msg=f"059: RED moves Elephant from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "d9", "d10"
        with self.subTest(msg=f"060: BLUE moves Guard from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "f7", "d10"
        with self.subTest(msg=f"061: RED moves Elephant from {src} to {dst} to capture BLUE Guard."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "e8", "c8"
        with self.subTest(msg=f"062: BLUE moves Cannon from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "e1", "d1"
        with self.subTest(msg=f"063: RED moves General from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "f10", "e8"
        with self.subTest(msg=f"064: BLUE tries to move Horse from {src} to {dst} but can't because RED Cannon would "
                              f"be able to capture BLUE General on next move."):
            self.assertFalse(self.game.make_move(src, dst))

        src, dst = "c8", "c1"
        with self.subTest(msg=f"065: BLUE moves Cannon from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "d2", "e2"
        with self.subTest(msg=f"066: RED moves Guard from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "e10", "e10"
        with self.subTest(msg=f"067: BLUE moves General from {src} to {dst} to pass their turn."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "e5", "e3"
        with self.subTest(msg=f"068: RED moves Cannon from {src} to {dst} to put BLUE General in check."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "f2", "f1"
        with self.subTest(msg=f"069: BLUE tries to move Chariot from {src} to {dst} to put RED General in check but "
                              f"can't because BLUE General is already in check by RED Cannon."):
            self.assertFalse(self.game.make_move(src, dst))

        src, dst = "e10", "d10"
        with self.subTest(msg=f"070: BLUE moves General from {src} to {dst} to escape check and captures RED "
                              f"Elephant."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "e2", "e1"
        with self.subTest(msg=f"071: RED moves Guard from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "c4", "e1"
        with self.subTest(msg=f"072: BLUE moves Elephant from {src} to {dst} to capture RED Guard."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "e3", "e10"
        with self.subTest(msg=f"073: RED moves Cannon from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "a7", "a2"
        with self.subTest(msg=f"074: BLUE moves Chariot from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "e4", "c7"
        with self.subTest(msg=f"075: RED moves Elephant from {src} to {dst}."):
            self.assertTrue(self.game.make_move(src, dst))

        src, dst = "f2", "e2"
        with self.subTest(msg=f"076: BLUE moves Chariot from {src} to {dst} to force a checkmate."):
            self.assertTrue(self.game.make_move(src, dst))

        # Check if game state updated to show that BLUE won.
        state = self.game.game_state
        expected_state = GameState.BLUE_WON
        self.assertEqual(expected_state, state)

        # Make sure no other moves can be made.
        src, dst = "d1", "d2"
        with self.subTest(msg=f"077: RED tries to move General from {src} to {dst} to capture BLUE Elephant, but "
                              f"the game is over and no more moves can be made."):
            self.assertFalse(self.game.make_move(src, dst))

        src, dst = "e2", "d1"
        with self.subTest(msg=f"078: BLUE tries to move Chariot from {src} to {dst} to capture RED General, but "
                              f"the game is over and no more moves can be made."):
            self.assertFalse(self.game.make_move(src, dst))

    def test_gameplay_sequences_scenario_two(self) -> None:
        """
        SCENARIO 2

        Sequence of moves that leads to RED winning.
        """

        # -------------------- Act ------------------------ #
        self.game.make_move('a7', 'b7')
        self.game.make_move('i4', 'h4')
        self.game.make_move('h10', 'g8')
        self.game.make_move('c1', 'd3')
        self.game.make_move('h8', 'e8')
        self.game.make_move('i1', 'i2')
        self.game.make_move('e7', 'f7')
        self.game.make_move('b3', 'e3')
        self.game.make_move('g10', 'e7')
        self.game.make_move('e4', 'd4')
        self.game.make_move('c10', 'd8')
        self.game.make_move('g1', 'e4')
        self.game.make_move('f10', 'f9')
        self.game.make_move('h1', 'g3')
        self.game.make_move('a10', 'a6')
        self.game.make_move('d4', 'd5')
        self.game.make_move('e9', 'f10')
        self.game.make_move('h3', 'f3')
        self.game.make_move('e8', 'h8')
        self.game.make_move('i2', 'h2')
        self.game.make_move('h8', 'f8')
        self.game.make_move('f1', 'f2')
        self.game.make_move('b8', 'e8')
        self.game.make_move('f3', 'f1')
        self.game.make_move('i7', 'h7')
        self.game.make_move('f1', 'c1')
        self.game.make_move('d10', 'e9')
        self.game.make_move('a4', 'b4')
        self.game.make_move('a6', 'a1')
        self.game.make_move('c1', 'a1')
        self.game.make_move('f8', 'd10')
        self.game.make_move('d5', 'c5')
        self.game.make_move('i10', 'i6')
        self.game.make_move('b1', 'd4')
        self.game.make_move('c7', 'c6')
        self.game.make_move('c5', 'b5')
        self.game.make_move('b10', 'd7')
        self.game.make_move('d4', 'f7')
        self.game.make_move('g7', 'f7')
        self.game.make_move('a1', 'f1')
        self.game.make_move('g8', 'f6')
        self.game.make_move('f1', 'f5')
        self.game.make_move('f6', 'd5')
        self.game.make_move('e3', 'e5')
        self.game.make_move('f7', 'f6')
        self.game.make_move('f5', 'f7')
        self.game.make_move('f10', 'e10')
        self.game.make_move('e2', 'f1')
        self.game.make_move('i6', 'i3')
        self.game.make_move('h2', 'g2')
        self.game.make_move('i3', 'i1')
        self.game.make_move('f1', 'e2')
        self.game.make_move('f6', 'f5')
        self.game.make_move('c4', 'd4')
        self.game.make_move('f5', 'e5')
        self.game.make_move('f7', 'd7')
        self.game.make_move('e7', 'g4')
        self.game.make_move('d4', 'd5')
        self.game.make_move('e5', 'e4')
        self.game.make_move('d3', 'e5')
        self.game.make_move('e4', 'e3')
        self.game.make_move('e2', 'd2')
        self.game.make_move('e3', 'e2')
        self.game.make_move('d2', 'd3')
        self.game.make_move('e8', 'e4')
        self.game.make_move('f2', 'e2')
        self.game.make_move('i1', 'd1')
        self.game.make_move('e2', 'd2')
        self.game.make_move('d1', 'f3')

        # -------------------- Assert --------------------- #
        state = self.game.game_state
        expected_state = GameState.BLUE_WON
        self.assertEqual(expected_state, state)

    def test_gameplay_sequences_scenario_three(self) -> None:
        """
        SCENARIO 3:

        Sequence of moves that leads to BLUE cannon performing a checkmate on RED General.
        """

        # -------------------- Act ------------------------ #
        self.game.make_move('e7', 'e6')
        self.game.make_move('e2', 'e2')
        self.game.make_move('e6', 'e5')
        self.game.make_move('e2', 'e2')
        self.game.make_move('e5', 'e4')
        self.game.make_move('e2', 'e2')
        self.game.make_move('e4', 'd4')
        self.game.make_move('e2', 'e2')
        self.game.make_move('d4', 'c4')
        self.game.make_move('e2', 'e2')
        self.game.make_move('a10', 'a9')
        self.game.make_move('e2', 'e2')
        self.game.make_move('a9', 'd9')
        self.game.make_move('e2', 'e2')
        self.game.make_move('d9', 'd8')
        self.game.make_move('i1', 'i2')
        self.game.make_move('e9', 'e9')
        self.game.make_move('i2', 'g2')
        self.game.make_move('e9', 'e9')
        self.game.make_move('i4', 'h4')
        self.game.make_move('e9', 'e9')
        self.game.make_move('h3', 'h5')
        self.game.make_move('i10', 'i9')
        self.game.make_move('e2', 'e2')
        self.game.make_move('i9', 'g9')
        self.game.make_move('e2', 'e2')
        self.game.make_move('g9', 'g8')
        self.game.make_move('e2', 'e2')
        self.game.make_move('h8', 'f8')
        self.game.make_move('f1', 'e1')
        self.game.make_move('g7', 'f7')
        self.game.make_move('g4', 'f4')
        self.game.make_move('e9', 'e9')
        self.game.make_move('f4', 'e4')
        self.game.make_move('b8', 'e8')

        # -------------------- Assert --------------------- #
        state = self.game.game_state
        expected_state = GameState.BLUE_WON
        self.assertEqual(expected_state, state)

    def test_gameplay_sequence_scenario_four(self) -> None:
        """
        SCENARIO 4:

        Sequences of moves that puts RED General in a checkmate. Tests for ability to pass a move if every other move
        is a check.
        """

        # -------------------- Act ------------------------ #
        self.game.make_move('e7', 'e6')
        self.game.make_move('e2', 'e2')
        self.game.make_move('e6', 'e5')
        self.game.make_move('e2', 'e2')
        self.game.make_move('e5', 'e4')
        self.game.make_move('e2', 'e2')
        self.game.make_move('e4', 'd4')
        self.game.make_move('e2', 'e2')
        self.game.make_move('d4', 'c4')
        self.game.make_move('e2', 'e2')
        self.game.make_move('a10', 'a9')
        self.game.make_move('e2', 'e2')
        self.game.make_move('a9', 'd9')
        self.game.make_move('e2', 'e2')
        self.game.make_move('d9', 'd8')
        self.game.make_move('e2', 'e2')
        self.game.make_move('d8', 'd7')
        self.game.make_move('e2', 'e2')
        self.game.make_move('d7', 'd6')
        self.game.make_move('i1', 'i2')
        self.game.make_move('e9', 'e9')
        self.game.make_move('i2', 'g2')
        self.game.make_move('e9', 'e9')
        self.game.make_move('i4', 'h4')
        self.game.make_move('e9', 'e9')
        self.game.make_move('h3', 'h5')
        self.game.make_move('i10', 'i9')
        self.game.make_move('e2', 'e2')
        self.game.make_move('i9', 'g9')
        self.game.make_move('e2', 'e2')
        self.game.make_move('g9', 'g8')
        self.game.make_move('e2', 'e2')
        self.game.make_move('h8', 'f8')
        self.game.make_move('f1', 'e1')
        self.game.make_move('g7', 'f7')
        self.game.make_move('e2', 'e2')
        self.game.make_move('i7', 'i6')
        self.game.make_move('e2', 'e2')
        self.game.make_move('g10', 'i7')
        self.game.make_move('e2', 'e2')
        self.game.make_move('i7', 'f5')
        self.game.make_move('e2', 'e2')
        self.game.make_move('f5', 'd8')
        self.game.make_move('e2', 'e2')
        self.game.make_move('d8', 'b5')
        self.game.make_move('e2', 'e2')
        self.game.make_move('c4', 'd4')
        self.game.make_move('e2', 'e2')
        self.game.make_move('d4', 'e4')
        self.game.make_move('e2', 'e2')
        self.game.make_move('e4', 'e3')

        # -------------------- Assert --------------------- #
        state = self.game.game_state
        expected_state = GameState.BLUE_WON
        self.assertEqual(expected_state, state)


if __name__ == "__main__":
    unittest.main()
