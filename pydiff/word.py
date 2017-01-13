import re

from .base import Diff


class WordDiff(Diff):

    # Words are considered to be separated with multiple whitespaces or
    # single non-alphanumeric and non-underscore characters
    _word_split_re = re.compile(r'(\s+|\W)', re.UNICODE)

    def tokenize(self, string):
        return [token for token in self._word_split_re.split(string) if token]


_word_diff = WordDiff()


def diff_words(old_string, new_string):
    return _word_diff.diff(old_string, new_string)
