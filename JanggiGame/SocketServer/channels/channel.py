from __future__ import annotations

from typing import TYPE_CHECKING

from action_request import ActionRequestHandler

if TYPE_CHECKING:
    from messages import Message
    from protocols.protocol import Protocol


class Channel:
    def __init__(self, server, protocol: Protocol):
        self.server = server
        self.protocol: Protocol = protocol

    async def handle_conn(self, reader, writer):
        # process request
        msg = await self.receive_async(reader)

        addr = writer.get_extra_info('peername')
        print(f"Received: {msg} from {addr!r}")

        # perform action and return result
        action_handler: ActionRequestHandler = ActionRequestHandler(msg, self.server)
        response: Message = action_handler.handle_request()

        # return response
        print(f"Send: {response}")
        await self.send_async(writer, response)

    async def receive_async(self, reader):
        msg = await self.protocol.receive_async(reader)
        return msg

    async def send_async(self, writer, message):
        await self.protocol.send_async(writer, message)
