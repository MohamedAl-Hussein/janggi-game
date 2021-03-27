import asyncio

from channels import Channel
from protocols import JsonMessageProtocol
from messages import MessageEncoder, MessageDecoder

HOST = "127.0.0.1"
PORT = 9001


def main():
    server = Server(HOST, PORT)
    asyncio.run(server.run_server())


class Server:
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


if __name__ == "__main__":
    main()
