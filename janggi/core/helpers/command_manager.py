from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from command import ICommand
    from stack import Stack


class ICommandManager:
    """
    Interface for representing a Command Manager that is responsible for doing, undoing, and redoing move commands.

    Acts as an extension to the Command Pattern.
    """

    def __init__(self, undo_stack: Stack, redo_stack: Stack) -> None:
        """Create a new undo_stack and redo_stack to store undo commands and redo commands respectively."""

        self._undo_stack: Stack = undo_stack
        self._redo_stack: Stack = redo_stack

    def do(self, command: ICommand) -> None:
        pass

    def undo(self) -> None:
        pass

    def redo(self) -> None:
        pass


class MoveCommandManager(ICommandManager):
    """Responsible for doing, undoing, and redoing move commands."""

    def __init__(self, undo_stack: Stack, redo_stack: Stack) -> None:
        """Create a new undo_stack and redo_stack to store undo move commands and redo move commands respectively."""

        super().__init__(undo_stack, redo_stack)

    def do(self, command: ICommand) -> None:
        """
        Execute a command and push it onto the undo_stack.

        Flush the redo_stack since a new command has been added.

        :param command: Command to execute.
        """

        command.execute()
        self._undo_stack.push(command)
        self._redo_stack.flush()

    def undo(self) -> None:
        """Pop command off undo_stack and call its un_execute method. Then push it onto the redo stack."""

        if self._undo_stack.is_empty():
            return

        command = self._undo_stack.pop()
        self._redo_stack.push(command)
        command.un_execute()

    def redo(self) -> None:
        """Pop command off redo_stack and call its execute method. Then push it onto the undo_stack."""

        if self._redo_stack.is_empty():
            return

        command = self._redo_stack.pop()
        self._undo_stack.push(command)
        command.execute()
