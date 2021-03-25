import asyncio

from server.channel import Channel
from server.json_protocol import JsonMessageProtocol
from server.message_serialization import MessageEncoder, MessageDecoder


class AppServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.game = None

    async def run_server(self):
        channel = Channel(self, JsonMessageProtocol(MessageEncoder, MessageDecoder))
        server = await asyncio.start_server(channel.handle_conn, self.host, self.port)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()
