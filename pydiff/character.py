from .base import Diff


class CharacterDiff(Diff):
    pass


_character_diff = CharacterDiff()


def diff_characters(old_string, new_string):
    return _character_diff.diff(old_string, new_string)
