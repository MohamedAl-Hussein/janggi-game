from __future__ import annotations

from typing import TYPE_CHECKING

from server.action_request import ActionRequest, ActionRequestHandler
from server.message import MessageDTO
from engine.core.janggi_game import JanggiGame

if TYPE_CHECKING:
    from protocol import Protocol


class Channel:
    def __init__(self, server, protocol: Protocol):
        self.server = server
        self.protocol: Protocol = protocol

    async def handle_conn(self, reader, writer):
        # process request
        msg = await self.receive_async(reader)

        addr = writer.get_extra_info('peername')
        print(f"Received {msg} from {addr!r}")

        # prepare response
        response_body = self.create_response(msg.copy())

        # return response
        print(f"Send: {response_body}")
        await self.send_async(writer, response_body)

    async def receive_async(self, reader):
        msg = await self.protocol.receive_async(reader)
        return msg

    async def send_async(self, writer, message):
        await self.protocol.send_async(writer, message)

    def create_response(self, message):
        """
        MESSAGE:

        { action: ActionRequest,
          data: MessageDTO }

        """

        # create a response based on message content

        # get message action request
        action: ActionRequest = ActionRequest[message.get("action", "INVALID_REQUEST")]
        message: MessageDTO = message.get("data", MessageDTO())

        if action is ActionRequest.NEW_GAME:
            self.server.game = JanggiGame()
        elif action is ActionRequest.END_GAME:
            del self.server.game

        handler = ActionRequestHandler(action, message)
        response = handler.handle_request()

        return response
