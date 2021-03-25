from typing import List

from engine.core.janggi_game import JanggiGame
from server.message import Message, MessageData, MessageAction, GameStatus, PieceDestinations, PieceDTO, PieceData


class ActionRequestHandler:
    def __init__(self, message, server):
        self.message = message
        self.server = server

    def create_response(self):
        # create a response based on message content
        response = Message(MessageAction.DEFAULT, MessageData())

        if self.message.Action is MessageAction.DEFAULT:
            pass

        if self.message.Action is MessageAction.NEW_GAME:
            self.server.game = JanggiGame()

            pieces: List[PieceDTO] = list()
            for position, piece in self.server.game.board.coord_map.items():
                dto: PieceDTO = PieceDTO(
                    Position=list(position),
                    Color=piece.color.name,
                    Category=piece.category.name
                )

                pieces.append(dto)
            response = Message(MessageAction.GAME_STARTED, PieceData(pieces))
        elif self.message.Action is MessageAction.END_GAME:
            self.server.game = None
            response = Message(MessageAction.GAME_OVER, MessageData())
        elif self.message.Action is MessageAction.GET_GAME_STATUS:
            response = Message(MessageAction.GAME_STATUS, GameStatus(**self.server.game.return_game_status()))
        elif self.message.Action is MessageAction.SETUP_COMPLETED:
            self.server.game.transpose_pieces(self.message.Data.__dict__)
            response = Message(MessageAction.SETUP_CONFIRMED, MessageData())
        elif self.message.Action is MessageAction.MOVE_COMPLETED:
            self.server.game.perform_move_using_tuple_coords(self.message.Data.Source, self.message.Data.Destination)
            response = Message(MessageAction.MOVE_CONFIRMED, MessageData())
        elif self.message.Action is MessageAction.GET_PIECE_DESTINATIONS:
            destinations = self.server.game.return_piece_destinations(self.message.Data.Source)
            response = Message(
                MessageAction.PIECE_DESTINATIONS,
                PieceDestinations(Source=self.message.Data.Source, Destinations=destinations)
            )

        return response
