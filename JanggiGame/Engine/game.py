from __future__ import annotations

import enum
from typing import Dict, List, Optional, Tuple, TYPE_CHECKING

from board import JanggiBoard
from piece import JanggiPiece, PieceCategory, PieceColor
from helpers import CommandManager, MoveCommand, Stack, IllegalDestinationStrategy, IllegalPathStrategy, \
    InsidePalaceStrategy, BranchPathStrategy, LinearDiagonalPathStrategy, LinearPathStrategy
from utils import Point2D, Rectangle

if TYPE_CHECKING:
    from helpers.command import ICommand


class JanggiGame:
    """
    Class representing a JanggiGame object. Responsible for performing the core actions for a traditional game of
    Janggi.

    Creating an instance of this class starts a new game. Each player can take turns making a move until a player
    wins; there are no draws.

    Class methods will determine whose turn it is; if the game is finished; or if the move is valid. They will also
    perform the move should it be validated.
    """

    # region Constructor

    def __init__(self) -> None:
        """
        Initializes an instance of the JanggiGame object. Symbolizes the creation of a new game.

        The class constructor performs the following actions:
            1. Set _game_state to UNFINISHED.
            2. Create a JanggiBoard instance to store Piece objects by their coordinate positions, including palaces
               and board boundaries.
            3. Create a collection of Piece objects, configuring their color, position, and strategies; then adding
               them to the JanggiBoard instance.
            4. Create Rectangle objects holding palace coordinates and board boundaries and assign them to the
               JanggiBoard instance.
            5. Create a CommandManger object to allow undoing/redoing moves.
            6. Initialize the starting player's turn to BLUE.

        Calls __setup() to perform tasks 3 and 4.
        """

        self.__game_state: GameState = GameState.UNFINISHED
        self.__player_turn: PieceColor = PieceColor.BLUE
        self.__command_manager: CommandManager = CommandManager(undo_stack=Stack(), redo_stack=Stack())
        self.__board: Optional[JanggiBoard] = None
        self.__setup()

    def __setup(self) -> None:
        """
        Called by constructor to aid in game setup.

        Initializes board pieces, board boundaries, and both palaces. Then assigns them to a new JanggiBoard instance
        that can be accessed as a class attribute.
        """

        params = dict()

        # Create game palaces.
        blue_palace, red_palace = self.__create_palaces()

        # Create and configure game pieces.
        pieces = self.__create_pieces()

        # Place pieces on the game board.
        coord_map = self.__create_coord_map(pieces)

        # Configure board boundaries
        boundaries: Rectangle = Rectangle([Point2D(0, 0), Point2D(0, 9), Point2D(8, 9), Point2D(8, 0)])

        # Create new JanggiBoard instance using the parameters created above.
        self.__board = JanggiBoard(coord_map, blue_palace, red_palace, boundaries)

    def __create_pieces(self) -> List[JanggiPiece]:
        """
        Called during the constructor step.

        Creates and configures Piece objects for all board pieces for both blue and red players and returns the Piece
        objects as a list to the caller.

        Piece objects have their path and move strategies configured during this step. These strategies are later
        used by the game to create paths and detect obstacles within them.

        Each Piece is configured with a color, category, position, custom path strategy instance, and a custom move
        strategy instance. The parameters for the strategy instances are configured for the different Piece categories
        and occasionally Piece colors.

        :return: A list of Piece objects configured for a new game.
        """

        # Configure path and move strategies for the different piece types/colors.
        chariot_cannon_path_strategy = dict(
            default=LinearPathStrategy(step_range=(1, 10), x_magnitudes={0, 1}, y_magnitudes={-1, 1}),
            palace=LinearDiagonalPathStrategy(
                step_range=(1, 10), x_magnitudes={-1, 0, 1}, y_magnitudes={-1, 0, 1}, diag_limit=2
            )
        )
        horse_path_strategy = dict(
            default=BranchPathStrategy(
                step_range=(1, 2), scalars={0, 1}, x_magnitudes={-1, 1}, y_magnitudes={-1, 1}
            ),
            palace=BranchPathStrategy(step_range=(1, 2), scalars={0, 1}, x_magnitudes={-1, 1}, y_magnitudes={-1, 1})
        )
        elephant_path_strategy = dict(
            default=BranchPathStrategy(
                step_range=(2, 3), scalars={0, 1}, x_magnitudes={-1, 1}, y_magnitudes={-1, 1}
            ),
            palace=BranchPathStrategy(step_range=(2, 3), scalars={0, 1}, x_magnitudes={-1, 1}, y_magnitudes={-1, 1})
        )
        blue_soldier_path_strategy = dict(
            default=LinearPathStrategy(step_range=(1, 2), x_magnitudes={-1, 0, 1}, y_magnitudes={1}),
            palace=LinearDiagonalPathStrategy(
                step_range=(1, 2), x_magnitudes={-1, 0, 1}, y_magnitudes={0, 1}, diag_limit=1
            )
        )
        red_soldier_path_strategy = dict(
            default=LinearPathStrategy(step_range=(1, 2), x_magnitudes={-1, 0, 1}, y_magnitudes={-1}),
            palace=LinearDiagonalPathStrategy(
                step_range=(1, 2), x_magnitudes={-1, 0, 1}, y_magnitudes={0, -1}, diag_limit=1
            )
        )
        general_guard_path_strategy = dict(
            default=None,
            palace=LinearDiagonalPathStrategy(
                step_range=(1, 2), x_magnitudes={-1, 0, 1}, y_magnitudes={-1, 0, 1}, diag_limit=1
            )
        )
        default_obstacle_strategy = dict(
            destination=IllegalDestinationStrategy(),
            path=IllegalPathStrategy(),
            palace=InsidePalaceStrategy()
        )
        horse_elephant_obstacle_strategy = dict(
            destination=IllegalDestinationStrategy(),
            path=IllegalPathStrategy(),
            palace=None
        )

        cc_strat = [chariot_cannon_path_strategy, default_obstacle_strategy]
        elephant_strat = [elephant_path_strategy, horse_elephant_obstacle_strategy]
        horse_strat = [horse_path_strategy, horse_elephant_obstacle_strategy]
        gg_strat = [general_guard_path_strategy, default_obstacle_strategy]
        b_soldier_strat = [blue_soldier_path_strategy, default_obstacle_strategy]
        r_soldier_strat = [red_soldier_path_strategy, default_obstacle_strategy]

        # Initialize the pieces.
        pieces = [
            JanggiPiece(PieceColor.BLUE, PieceCategory.CHARIOT, Point2D(0, 0), cc_strat[0], cc_strat[1]),
            JanggiPiece(PieceColor.BLUE, PieceCategory.CHARIOT, Point2D(8, 0), cc_strat[0], cc_strat[1]),
            JanggiPiece(PieceColor.RED, PieceCategory.CHARIOT, Point2D(0, 9), cc_strat[0], cc_strat[1]),
            JanggiPiece(PieceColor.RED, PieceCategory.CHARIOT, Point2D(8, 9), cc_strat[0], cc_strat[1]),
            JanggiPiece(PieceColor.BLUE, PieceCategory.ELEPHANT, Point2D(1, 0), elephant_strat[0], elephant_strat[1]),
            JanggiPiece(PieceColor.BLUE, PieceCategory.ELEPHANT, Point2D(6, 0), elephant_strat[0], elephant_strat[1]),
            JanggiPiece(PieceColor.RED, PieceCategory.ELEPHANT, Point2D(1, 9), elephant_strat[0], elephant_strat[1]),
            JanggiPiece(PieceColor.RED, PieceCategory.ELEPHANT, Point2D(6, 9), elephant_strat[0], elephant_strat[1]),
            JanggiPiece(PieceColor.BLUE, PieceCategory.HORSE, Point2D(2, 0), horse_strat[0], horse_strat[1]),
            JanggiPiece(PieceColor.BLUE, PieceCategory.HORSE, Point2D(7, 0), horse_strat[0], horse_strat[1]),
            JanggiPiece(PieceColor.RED, PieceCategory.HORSE, Point2D(2, 9), horse_strat[0], horse_strat[1]),
            JanggiPiece(PieceColor.RED, PieceCategory.HORSE, Point2D(7, 9), horse_strat[0], horse_strat[1]),
            JanggiPiece(PieceColor.BLUE, PieceCategory.CANNON, Point2D(1, 2), cc_strat[0], cc_strat[1]),
            JanggiPiece(PieceColor.BLUE, PieceCategory.CANNON, Point2D(7, 2), cc_strat[0], cc_strat[1]),
            JanggiPiece(PieceColor.RED, PieceCategory.CANNON, Point2D(1, 7), cc_strat[0], cc_strat[1]),
            JanggiPiece(PieceColor.RED, PieceCategory.CANNON, Point2D(7, 7), cc_strat[0], cc_strat[1]),
            JanggiPiece(PieceColor.BLUE, PieceCategory.GUARD, Point2D(3, 0), gg_strat[0], gg_strat[1], True),
            JanggiPiece(PieceColor.BLUE, PieceCategory.GUARD, Point2D(5, 0), gg_strat[0], gg_strat[1], True),
            JanggiPiece(PieceColor.RED, PieceCategory.GUARD, Point2D(3, 9), gg_strat[0], gg_strat[1], True),
            JanggiPiece(PieceColor.RED, PieceCategory.GUARD, Point2D(5, 9), gg_strat[0], gg_strat[1], True),
            JanggiPiece(PieceColor.BLUE, PieceCategory.SOLDIER, Point2D(0, 3), b_soldier_strat[0], b_soldier_strat[1]),
            JanggiPiece(PieceColor.BLUE, PieceCategory.SOLDIER, Point2D(2, 3), b_soldier_strat[0], b_soldier_strat[1]),
            JanggiPiece(PieceColor.BLUE, PieceCategory.SOLDIER, Point2D(4, 3), b_soldier_strat[0], b_soldier_strat[1]),
            JanggiPiece(PieceColor.BLUE, PieceCategory.SOLDIER, Point2D(6, 3), b_soldier_strat[0], b_soldier_strat[1]),
            JanggiPiece(PieceColor.BLUE, PieceCategory.SOLDIER, Point2D(8, 3), b_soldier_strat[0], b_soldier_strat[1]),
            JanggiPiece(PieceColor.RED, PieceCategory.SOLDIER, Point2D(0, 6), r_soldier_strat[0], r_soldier_strat[1]),
            JanggiPiece(PieceColor.RED, PieceCategory.SOLDIER, Point2D(2, 6), r_soldier_strat[0], r_soldier_strat[1]),
            JanggiPiece(PieceColor.RED, PieceCategory.SOLDIER, Point2D(4, 6), r_soldier_strat[0], r_soldier_strat[1]),
            JanggiPiece(PieceColor.RED, PieceCategory.SOLDIER, Point2D(6, 6), r_soldier_strat[0], r_soldier_strat[1]),
            JanggiPiece(PieceColor.RED, PieceCategory.SOLDIER, Point2D(8, 6), r_soldier_strat[0], r_soldier_strat[1]),
            JanggiPiece(PieceColor.BLUE, PieceCategory.GENERAL, Point2D(4, 1), gg_strat[0], gg_strat[1], True),
            JanggiPiece(PieceColor.RED, PieceCategory.GENERAL, Point2D(4, 8), gg_strat[0], gg_strat[1], True)
        ]

        return pieces

    def __create_coord_map(self, pieces: List[JanggiPiece]) -> Dict[Tuple[int, int], JanggiPiece]:
        """
        This method is called during the constructor step, after the individual Piece objects have been created.

        Creates a coordinate-map for the JanggiBoard instance identifying Piece objects by their x and y coordinates.

        This map is later used as a quick lookup-table to determine if a space is occupied, and for updating occupants
        of a position after a move and/or capture.

        :param pieces: A list of Piece objects configured for the game.
        :return: A dictionary with key-value pairs of tuple coordinates and Piece objects.
        """

        coord_map = dict()

        for piece in pieces:
            coord_map[piece.position.to_tuple()] = piece

        return coord_map

    def __create_palaces(self) -> Tuple[Rectangle, Rectangle]:
        """
        This method is called during the constructor step.

        Creates a palace-map containing the palaces as Rectangle objects with x and y coordinates for each corner.

        The purpose of the palace-map is for detecting illegal moves that may occur within a palace.

        :return: A tuple object containing both palaces as Rectangle objects.
        """

        blue_palace: Rectangle = Rectangle([Point2D(3, 0), Point2D(3, 2), Point2D(5, 2), Point2D(5, 0)])
        red_palace: Rectangle = Rectangle([Point2D(3, 7), Point2D(3, 9), Point2D(5, 9), Point2D(5, 7)])

        return blue_palace, red_palace

    # endregion

    # region Getters/Setters

    @property
    def board(self):
        return self.__board

    @property
    def command_manager(self):
        return self.__command_manager

    @property
    def game_state(self) -> GameState:
        return self.__game_state

    @game_state.setter
    def game_state(self, value: GameState) -> None:
        self.__game_state = value

    @property
    def player_turn(self) -> PieceColor:
        return self.__player_turn

    @player_turn.setter
    def player_turn(self, value: PieceColor) -> None:
        self.__player_turn = value

    # endregion

    def make_move(self, source: str, destination: str) -> bool:
        """
        Given a source and destination coordinate, validates move and performs it if it is legal.

        :param source: Algebraic notation of source position.
        :param destination: Algebraic notation of destination position.
        :return: True if success, False if failure.
        """

        # Convert algebraic notation to Point2D objects.
        src: Point2D = self.algebraic_notation_to_coordinate_system(source)
        dst: Point2D = self.algebraic_notation_to_coordinate_system(destination)

        # Check if the move is valid.
        if not self.is_move_valid(src, dst):
            return False

        # If we reach this point, it means that the move is legal; so perform the move.
        self.move(src, dst)

        # Check if opponent is in check and if so test for a checkmate.
        if self.is_in_check(self.player_turn) and self.is_checkmate(self.player_turn):

            # Checkmate! Set game state to denote the winning player.
            self.game_state = GameState.BLUE_WON if self.player_turn is PieceColor.RED else GameState.RED_WON

            # Store new game state on command stack in case we want to undo then redo a move again.
            self.command_manager.last_command.game_state = self.game_state

        return True

    def is_move_valid(self, source: Point2D, destination: Point2D) -> bool:
        """
        Performs move validation for every request made through make_move().

        A move is illegal if:
            1. The game is already over.
            2. The source does not contain a piece.
            3. The source piece does not belong to current player.
            4. The player requested to pass their turn but their General is in check.
            5. There is no path for the piece from source to destination.
            6. The path to the destination contains obstacles that the piece cannot overcome.
            7. The move will put/leave the current player's General in check.

        :param source: Point2D object representing the source position.
        :param destination: Point2D object representing the destination position.
        :return: True if move is valid, False otherwise.
        """

        # Game is already over.
        if self.game_state is not GameState.UNFINISHED:
            return False

        piece: JanggiPiece = self.board.coord_map.get(source.to_tuple())

        # Source does not contain a piece or not player's turn.
        if piece is None or piece.color != self.player_turn:
            return False

        # Player requests to pass turn. Allow it if their General isn't in check.
        if source == destination:
            return not self.is_in_check(self.player_turn)

        path = self.board.find_path(source, destination)

        # There is no path from source to destination and if there is a path it contains obstacles that can't be passed.
        if len(path) == 0 or self.board.find_obstacles(path):
            return False

        # Move leave/puts player's General in check.
        if self.move_results_in_check(source, destination):
            return False

        return True

    def move_results_in_check(self, source, destination):
        turn: PieceColor = self.player_turn
        self.move(source, destination)
        in_check: bool = self.is_in_check(turn)
        self.undo_move()

        return in_check

    def is_in_check(self, color: PieceColor) -> bool:
        """
        Determine if current player's General is in check.

        A General is in check if the it can be captured on the next turn.

        Used to determine if the move is legal, as a player can't place/leave their General in check.

        :param color: The player we are examining to see if they are in check.
        :return: True if in check, False otherwise.
        """

        # Generate all paths for opponent.
        opponent = PieceColor.BLUE if color is PieceColor.RED else PieceColor.RED
        opponent_pieces = self.board.search(opponent)
        opponent_paths = self.board.generate_paths(*opponent_pieces)

        # Search for the current player's General.
        general = self.board.search(color, PieceCategory.GENERAL)[0]

        # For each opponent piece, check if any one of their paths will end on current player's General.
        intersecting_paths = [path for path in opponent_paths if path[-1] == general.position]

        # If one or more opponents can reach the General, then the player is in check.
        return len(intersecting_paths) > 0

    def is_checkmate(self, color: PieceColor) -> bool:
        """
        Given the player's color, determine if they are in checkmate.

        A player is in checkmate if their General cannot make any move to escape a check; and neither of the player's
        pieces can block the check or capture the attacking piece.

        :param color: PieceColor of player we want to investigate to see if they are in a checkmate.
        :return: True if player is in a checkmate, False otherwise.
        """

        opponent_color = PieceColor.BLUE if color == PieceColor.RED else PieceColor.RED

        # ---------------------------------------STEP 1---------------------------------------------- #
        # Generate all paths for player's General.
        general: JanggiPiece = self.board.search(color, PieceCategory.GENERAL)[0]
        general_paths: List[List[Point2D]] = self.board.generate_paths(general)

        # Check if the General can move to any of the paths available to it to escape a check.
        for path in general_paths:
            self.move(general.position, path[-1])
            in_check = self.is_in_check(color)
            self.undo_move()

            # General can escape the check.
            if not in_check:
                return False

        # ---------------------------------------STEP 2---------------------------------------------- #
        # If we reach this point, it means the General can't escape the check. So now we look for which attack vectors
        # can capture the General at its current position.
        attack_vectors: List[List[Point2D]] = list()
        opponent_pieces: List[JanggiPiece] = self.board.search(opponent_color)
        opponent_paths: List[List[Point2D]] = self.board.generate_paths(*opponent_pieces)

        # Save all paths that lead to the player's General.
        for path in opponent_paths:
            if path[-1] == general.position:
                attack_vectors.append(path)

        # If there is more than one attack vector, then it's a double-check and it can't be stopped, so return True.
        if len(attack_vectors) > 1:
            return True

        # ---------------------------------------STEP 3---------------------------------------------- #
        # If we reach this point, it means that there is only one attack vector, so we will try to block it.
        pieces: List[JanggiPiece] = self.board.search(color)
        paths: List[List[Point2D]] = self.board.generate_paths(*pieces)

        # Find a path that can block the attack.
        for path in paths:
            if path[-1] in attack_vectors[0][:-1]:

                # Check if attempt by opponent to intercept attack does not put their general in check.
                self.move(path[0], path[-1])
                in_check = self.is_in_check(color)
                self.undo_move()

                # The attack can be blocked so that the player's General is no longer in check.
                if not in_check:
                    return False

        # ---------------------------------------STEP 4---------------------------------------------- #
        # If we reach this point, it means that there is no way to block attack vector, so it's a checkmate.
        return True

    def move(self, source: Point2D, destination: Point2D) -> None:
        """
        Performs a move by updating Piece positions on the game board and assigning turn to next player.

        Stores move as a command to be later retrieved for undo/redo operations.

        :param source: Source coordinate.
        :param destination: Destination coordinate.
        """

        command: ICommand = MoveCommand(source, destination, self.board, self.game_state)
        self.command_manager.do(command)
        self.change_player()

    def undo_move(self) -> None:
        """
        Reverse the actions of the previous move by un-executing a command.

        Proceeds to assign turn to next player and updates the game state (in case method was called after the game
        had been finished).
        """

        self.command_manager.undo()
        self.change_player()
        command: Optional[MoveCommand] = self.command_manager.last_command

        if command is not None:
            self.game_state = command.game_state

    def redo_move(self) -> None:
        """
        Redo actions of previously undone move.

        Proceeds to assign turn to next player and updates the game state (in case move was the final one in a game).
        """

        self.command_manager.redo()
        self.change_player()
        command: Optional[MoveCommand] = self.command_manager.last_command

        if command is not None:
            self.game_state = command.game_state

    def change_player(self) -> None:
        """Sets the player turn to the opposing color."""

        if self.player_turn == PieceColor.BLUE:
            self.player_turn = PieceColor.RED
        else:
            self.player_turn = PieceColor.BLUE

    def algebraic_notation_to_coordinate_system(self, position: str) -> Point2D:
        """
        Translates algebraic coordinate notation to a Point2D object.

        The notation may start with letters a through i, and end with a digit 1 through 10.

        The letters are mapped to integers, with a set to 0 and i set to 8.
        The numbers are translated by subtracting them from 10, in order to position the origin of the game board
        at the bottom left corner where BLUE's chariot would reside.

        :param position: Algebraic position string.
        :return: Point2D translation of position.
        """

        column_map = dict(a=0, b=1, c=2, d=3, e=4, f=5, g=6, h=7, i=8)

        x_coord = column_map.get(position[0])
        y_coord = 10 - int(position[1:])

        return Point2D(x_coord, y_coord)

    def coordinate_system_to_algebraic_notation(self, position: Tuple[int, int]) -> str:
        """
        Converts a tuple coordinate into an algebraic coordinate.
        """

        column_map = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i'}

        return column_map[position[0]] + str(10 + position[1])

    def transpose_pieces(self, transpositions: Dict[str, bool]) -> None:
        """
        Transposes the horse and elephant for each player if requested to do so.

        Called before first move is made.
        """

        blue_left_pairs = (Point2D(1, 0), Point2D(2, 0))
        blue_right_pairs = (Point2D(6, 0), Point2D(7, 0))
        red_left_pairs = (Point2D(6, 9), Point2D(7, 9))
        red_right_pairs = (Point2D(1, 9), Point2D(2, 9))

        if transpositions.get("blue_left_transposed"):
            self.board.swap(*blue_left_pairs)

        if transpositions.get("blue_right_transposed"):
            self.board.swap(*blue_right_pairs)

        if transpositions.get("red_left_transposed"):
            self.board.swap(*red_left_pairs)

        if transpositions.get("red_right_transposed"):
            self.board.swap(*red_right_pairs)

    def return_game_status(self):
        return dict(
            GameState=self.game_state.name,
            PlayerTurn=self.player_turn.name,
            IsChecked=self.is_in_check(self.player_turn)
        )

    def perform_move_using_tuple_coords(self, start_coord, end_coord):
        self.make_move(
            self.coordinate_system_to_algebraic_notation(start_coord),
            self.coordinate_system_to_algebraic_notation(end_coord)
        )

    def return_piece_destinations(self, source):
        piece = self.board.coord_map[tuple(source)]
        destinations = [
            list(path[-1].to_tuple())
            for path
            in self.board.generate_paths(piece)
            if not self.move_results_in_check(piece.position, path[-1])
        ]

        return destinations


class GameState(enum.Enum):
    """Enum class representing possible game states."""

    UNFINISHED = enum.auto()
    BLUE_WON = enum.auto()
    RED_WON = enum.auto()
