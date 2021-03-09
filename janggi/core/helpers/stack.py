from typing import Any, Optional


class Stack:
    """Class representing Stack ADT."""

    def __init__(self) -> None:
        """Initialize the stack as a list."""

        self._list = list()

    def push(self, data: Any) -> None:
        """Push item to top of stack."""

        self._list.append(data)

    def pop(self) -> Any:
        """Pop the topmost item off the stack."""

        return self._list.pop()

    def peek(self) -> Optional[Any]:
        """Return the topmost item on the stack without popping it. If the stack is empty, return None."""

        if not self.is_empty():
            return self._list[-1]

    def is_empty(self) -> bool:
        """
        Check if the stack is empty.

        :return: True if stack is empty, False otherwise.
        """

        return len(self._list) == 0

    def flush(self) -> None:
        """Empty the stack."""

        self._list.clear()
