import asyncio

from channel import Channel
from json_protocol import JsonMessageProtocol

HOST = "127.0.0.1"
PORT = 9001


async def main():
    channel = Channel(JsonMessageProtocol())
    server = await asyncio.start_server(channel.handle_conn, HOST, PORT)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
