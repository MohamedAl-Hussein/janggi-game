import asyncio

from server.app_server import AppServer

HOST = "127.0.0.1"
PORT = 9001


def main():
    server = AppServer(HOST, PORT)
    asyncio.run(server.run_server())


if __name__ == "__main__":
    main()
