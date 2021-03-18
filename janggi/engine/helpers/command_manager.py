from __future__ import annotations

from typing import Optional,TYPE_CHECKING

if TYPE_CHECKING:
    from command import ICommand
    from stack import Stack


class CommandManager:
    """Responsible for doing, undoing, and redoing commands."""

    def __init__(self, undo_stack: Stack, redo_stack: Stack) -> None:
        """
        Create a new undo_stack and redo_stack to store undo commands and redo commands respectively.

        :param undo_stack: Instance of stack for storing undo commands.
        :param redo_stack: Instance of stack for storing redo commands.
        """

        self.__undo_stack: Stack = undo_stack
        self.__redo_stack: Stack = redo_stack
        self.__last_command: Optional[ICommand] = None

    @property
    def last_command(self) -> Optional[ICommand]:
        return self.__last_command

    @last_command.setter
    def last_command(self, value: ICommand) -> None:
        self.__last_command = value

    def do(self, command: ICommand) -> None:
        """
        Execute a command and push it onto the undo_stack.

        Flush the redo_stack since a new command has been added.

        :param command: Command to execute.
        """

        command.execute()
        self.__undo_stack.push(command)
        self.__redo_stack.flush()

        self.last_command = command

    def undo(self) -> None:
        """Pop command off undo_stack and call its un_execute method. Then push it onto the redo stack."""

        if self.__undo_stack.is_empty():
            return

        command = self.__undo_stack.pop()
        self.__redo_stack.push(command)
        command.un_execute()

        self.last_command = command

    def redo(self) -> None:
        """Pop command off redo_stack and call its execute method. Then push it onto the undo_stack."""

        if self.__redo_stack.is_empty():
            return

        command = self.__redo_stack.pop()
        self.__undo_stack.push(command)
        command.execute()

        self.last_command = command
