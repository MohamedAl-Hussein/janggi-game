import json

from .protocol import Protocol


class JsonMessageProtocol(Protocol):
    def encode_body(self, message):
        # Convert message to byte array
        return str(json.dumps(message)).encode('utf-8')

    def decode(self, message):
        # Convert bytes read to json
        return json.loads(message)
