from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from protocol import Protocol


class Channel:
    def __init__(self, protocol: Protocol):
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
        message["stringProperty"] = "Goodbye World"

        return message
