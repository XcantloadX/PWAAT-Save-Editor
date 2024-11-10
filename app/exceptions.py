from typing import TYPE_CHECKING

from gettext import gettext as _

if TYPE_CHECKING:
    from app.editor.save_editor import SaveType

class PWAATEditorError(Exception):
    pass

class GameNotFoundError(PWAATEditorError):
    def __init__(self) -> None:
        super().__init__(_("Game not found. Have you installed the game?"))


class GameFileMissingError(PWAATEditorError):
    def __init__(self, file: str) -> None:
        self.file = file
        super().__init__(_(
            "Game file missing: {}. "
            "Make sure you've installed Steam/Xbox version of game. "
            "Try to check game integrity."
        ).format(file))

class InvalidSaveLengthError(PWAATEditorError):
    """存档实际长度与预期长度不正确"""
    def __init__(self, path: str, expected: int, actual: int):
        self.path = path
        self.expected = expected
        self.actual = actual
        super().__init__(_(
            'Invalid save file length: {path}, expected {expected}, got {actual}.  '
            'This might be caused by corrupted save file or save type mismatch.'
        ).format(path=path, expected=expected, actual=actual))

class NoOpenSaveFileError(PWAATEditorError):
    pass

class NoGameFoundError(PWAATEditorError):
    pass

class IncompatibleSlotError(PWAATEditorError):
    def __init__(self, left_type: 'SaveType', right_type: 'SaveType') -> None:
        self.left_type = left_type
        self.right_type = right_type
        super().__init__(_(
            'Incompatible slot types: '
            'left is {left_type} and right is {right_type}'
        ).format(left_type=left_type, right_type=right_type))

if __name__ == "__main__":
    raise GameNotFoundError()