import abc
import struct


class Protocol(metaclass=abc.ABCMeta):
    """Base class for sending/receiving messages between sockets."""

    HEADER_SIZE = 4
    HEADER_FORMAT = "!I"

    async def receive_async(self, reader):
        body_len = await self.read_header(reader)
        msg = await self.read_body(reader, body_len)

        return msg

    async def send_async(self, writer, message):
        response = self.encode(message)

        writer.write(response)
        await writer.drain()

        print("Close the connection")
        writer.close()

    async def read_header(self, reader):
        # Read header to get body length
        header_bytes = await reader.read(self.HEADER_SIZE)
        body_len = struct.unpack(self.HEADER_FORMAT, bytearray(header_bytes))[0]

        return body_len

    async def read_body(self, reader, length):
        # Read body length bytes
        data = await reader.read(length)
        message = data.decode()

        return self.decode(message)

    def encode(self, message):
        body_bytes = self.encode_body(message)

        # Get message length and convert to 4 bytes
        header_bytes = struct.pack(self.HEADER_FORMAT, len(body_bytes))

        return header_bytes + body_bytes

    @abc.abstractmethod
    def encode_body(self, message):
        pass

    @abc.abstractmethod
    def decode(self, message):
        pass
