"""Unit tests for the Command Pattern implementation."""
import pytest
from patterns.behavioral.command import Command, CommandManager, MacroCommand


class Editor:
    def __init__(self) -> None:
        self.text: str = ""


class InsertCommand(Command):
    def __init__(self, editor: Editor, text: str) -> None:
        self.editor = editor
        self.text = text

    def execute(self) -> None:
        self.editor.text += self.text

    def undo(self) -> None:
        self.editor.text = self.editor.text[: -len(self.text)]


def test_cannot_instantiate_abstract_command():
    with pytest.raises(TypeError):
        Command()  # type: ignore[abstract]


def test_command_execution_and_undo():
    editor = Editor()
    cmd = InsertCommand(editor, "hello")
    cmd.execute()
    assert editor.text == "hello"
    cmd.undo()
    assert editor.text == ""


def test_command_manager_lifecycle():
    manager = CommandManager()
    editor = Editor()
    assert not manager.can_undo and not manager.can_redo
    assert manager.undo() is False and manager.redo() is False

    manager.execute(InsertCommand(editor, "foo"))
    manager.execute(InsertCommand(editor, "bar"))
    assert editor.text == "foobar"
    assert manager.undo() is True and editor.text == "foo"
    assert manager.redo() is True and editor.text == "foobar"

    # New command invalidates redo stack
    manager.undo()
    manager.execute(InsertCommand(editor, "baz"))
    assert not manager.can_redo and editor.text == "foobaz"
    manager.clear()
    assert not manager.can_undo and not manager.can_redo


def test_macro_command():
    editor = Editor()
    macro = MacroCommand([InsertCommand(editor, "a")])
    macro.add(InsertCommand(editor, "b"))
    assert len(macro) == 2
    macro.execute()
    assert editor.text == "ab"
    macro.undo()
    assert editor.text == ""
