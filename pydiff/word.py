import re

from .base import Diff


class WordDiff(Diff):

    # Words are considered to be separated with multiple whitespaces or
    # single non-alphanumeric and non-underscore characters
    _word_split_re = re.compile(r'(\s+|\W)', re.UNICODE)

    def tokenize(self, string):
        return [token for token in self._word_split_re.split(string) if token]

    def _is_space(self, string):
        # Empty strings should also be treated as containing only whitespaces
        return not string or string.isspace()

    def are_equal(self, left_token, right_token):
        # Strings consisting of only whitespaces are considered equivalent
        return left_token == right_token or \
               (self._is_space(left_token) and self._is_space(right_token))


class WordWithSpaceDiff(WordDiff):

    def are_equal(self, left_token, right_token):
        # Whitespaces are not ignored anymore here,
        # so override the parent's method
        return left_token == right_token


_word_diff = WordDiff()
_word_with_space_diff = WordWithSpaceDiff()


def diff_words(old_string, new_string):
    return _word_diff.diff(old_string, new_string)


def diff_words_with_spaces(old_string, new_string):
    return _word_with_space_diff.diff(old_string, new_string)
