from .base import Diff


class WordDiff(Diff):
    pass


_word_diff = WordDiff()


def diff_words(old_string, new_string):
    return _word_diff.diff(old_string, new_string)
