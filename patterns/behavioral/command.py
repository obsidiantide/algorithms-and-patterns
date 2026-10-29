"""Command Pattern implementation with undo, redo, and macro command support."""
from abc import ABC, abstractmethod
from typing import List, Optional


class Command(ABC):
    """Abstract base class representing an executable command."""

    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""

    @abstractmethod
    def undo(self) -> None:
        """Undo the effect of the command."""


class MacroCommand(Command):
    """Composite command that executes a sequence of commands."""

    def __init__(self, commands: Optional[List[Command]] = None) -> None:
        self.commands: List[Command] = list(commands or [])

    def add(self, command: Command) -> None:
        """Append a command to the macro sequence."""
        self.commands.append(command)

    def execute(self) -> None:
        """Execute all commands in sequential order."""
        for cmd in self.commands:
            cmd.execute()

    def undo(self) -> None:
        """Undo all commands in reverse order."""
        for cmd in reversed(self.commands):
            cmd.undo()

    def __len__(self) -> int:
        return len(self.commands)


class CommandManager:
    """Invoker that manages command execution history with undo and redo."""

    def __init__(self) -> None:
        self._undo_stack: List[Command] = []
        self._redo_stack: List[Command] = []

    @property
    def can_undo(self) -> bool:
        return bool(self._undo_stack)

    @property
    def can_redo(self) -> bool:
        return bool(self._redo_stack)

    def execute(self, command: Command) -> None:
        """Execute command and record it in undo history."""
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()

    def undo(self) -> bool:
        """Undo most recent command; returns True if successful."""
        if not self._undo_stack:
            return False
        cmd = self._undo_stack.pop()
        cmd.undo()
        self._redo_stack.append(cmd)
        return True

    def redo(self) -> bool:
        """Redo most recently undone command; returns True if successful."""
        if not self._redo_stack:
            return False
        cmd = self._redo_stack.pop()
        cmd.execute()
        self._undo_stack.append(cmd)
        return True

    def clear(self) -> None:
        """Clear both undo and redo histories."""
        self._undo_stack.clear()
        self._redo_stack.clear()
