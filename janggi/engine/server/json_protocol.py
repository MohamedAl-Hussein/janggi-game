import json
from json import JSONDecoder, JSONEncoder

from server.protocol import Protocol

from typing import Optional, Type


class JsonMessageProtocol(Protocol):
    def __init__(self, encoder: Optional[Type[JSONEncoder]] = None, decoder: Optional[Type[JSONDecoder]] = None) -> None:
        self.__encoder: Optional[Type[JSONEncoder]] = encoder
        self.__decoder: Optional[Type[JSONDecoder]] = decoder

    def encode_body(self, message):
        # Convert message to byte array
        if self.__encoder is None:
            return str(json.dumps(message)).encode('utf-8')

        return str(json.dumps(message, cls=self.__encoder)).encode('utf-8')

    def decode(self, message):
        # Convert bytes read to json
        if self.__decoder is None:
            return json.loads(message)

        return json.loads(message, cls=self.__decoder)
