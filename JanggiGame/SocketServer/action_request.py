from typing import List

from game import JanggiGame
from messages import Message, MessageData, MessageAction, GameStatus, PieceDestinations, PieceData
from dtos import PieceDTO


class ActionRequestHandler:
    def __init__(self, message, server):
        self.message = message
        self.server = server

    def handle_request(self):
        """
        Given a request Message, inspects the Message's Action attribute, performs requested Action if it is valid,
        and creates a response Message with optional Data to send back to client.
        """

        # create a response based on message content
        response: Message = Message(MessageAction.DEFAULT, MessageData())

        if self.message.Action is MessageAction.NEW_GAME:
            response = self.handle_new_game_request()
        elif self.message.Action is MessageAction.END_GAME:
            response = self.handle_end_game_request()
        elif self.message.Action is MessageAction.GET_GAME_STATUS:
            response = self.handle_game_status_request()
        elif self.message.Action is MessageAction.SETUP_COMPLETED:
            response = self.handle_setup_completed_request()
        elif self.message.Action is MessageAction.MOVE_COMPLETED:
            response = self.handle_move_request()
        elif self.message.Action is MessageAction.GET_PIECE_DESTINATIONS:
            response = self.handle_piece_destinations_request()

        # TODO: raise message action invalid if no match (or create response message with status as invalid).

        return response

    def handle_new_game_request(self) -> Message:
        """
        Create a new instance of a game and assign it to the server's game attribute.

        Return new Message object with starting data about each starting piece.
        """

        # Create new instance of game.
        self.server.game = JanggiGame()

        # Get data for every starting piece.
        pieces: List[PieceDTO] = list()
        for position, piece in self.server.game.board.coord_map.items():
            dto: PieceDTO = PieceDTO(
                Position=list(position),
                Color=piece.color.name,
                Category=piece.category.name
            )

            pieces.append(dto)

        return Message(MessageAction.GAME_STARTED, PieceData(pieces))

    def handle_end_game_request(self) -> Message:
        """
        End the current game instance by deleting any references to it.

        Return new Message object to confirm game has finished.
        """

        self.server.game = None

        return Message(MessageAction.GAME_OVER, MessageData())

    def handle_game_status_request(self) -> Message:
        """
        Return a new Message object containing the current game's status, namely game state, current player's turn,
        and if they are in check.
        """

        return Message(MessageAction.GAME_STATUS, GameStatus(**self.server.game.return_game_status()))

    def handle_piece_destinations_request(self) -> Message:
        """
        Given the coordinates of a piece, generate a list of coordinates it can visit given the game's rules.

        Return a new Message containing an array of all possible destinations, or an empty array if none exist.
        """

        destinations = self.server.game.return_piece_destinations(self.message.Data.Source)

        return Message(
            MessageAction.PIECE_DESTINATIONS,
            PieceDestinations(Source=self.message.Data.Source, Destinations=destinations)
        )

    def handle_move_request(self) -> Message:
        """
        Given a source and destination coordinate, perform the move in the game.

        Return a new Message object to confirm move has been completed.
        """

        src = self.server.game.coordinate_system_to_algebraic_notation(self.message.Data.Source)
        dst = self.server.game.coordinate_system_to_algebraic_notation(self.message.Data.Destination)
        self.server.game.make_move(src, dst)

        return  Message(MessageAction.MOVE_CONFIRMED, MessageData())

    def handle_setup_completed_request(self) -> Message:
        """
        For any horse-elephant transposition requested, update the game's board with the new transposition.

        Return a new Message object to confirm transposition has been completed.
        """

        self.server.game.transpose_pieces(self.message.Data.__dict__)

        return Message(MessageAction.SETUP_CONFIRMED, MessageData())
