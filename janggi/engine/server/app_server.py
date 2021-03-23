import asyncio

from .channel import Channel
from .json_protocol import JsonMessageProtocol


class AppServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.game = None

    async def run_server(self):
        channel = Channel(self, JsonMessageProtocol())
        server = await asyncio.start_server(channel.handle_conn, self.host, self.port)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()
