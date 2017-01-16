import re

from .base import Diff


class LineDiff(Diff):

    _line_split_re = re.compile(r'(\r\n|\r|\n)')

    def tokenize(self, string):
        lines_and_linebreaks = self._line_split_re.split(string)

        # Discard the final empty token which appears
        # if the string ends with line-break characters
        if lines_and_linebreaks and not lines_and_linebreaks[-1]:
            lines_and_linebreaks.pop()

        tokens = []
        for index, entry in enumerate(lines_and_linebreaks):
            if index % 2 and tokens:
                # Append the line-break to the previous line
                tokens[-1] += entry
            else:
                # Preprocess the line before adding to other tokens
                # (a token is a (line + line-break) combination, so we have to
                # another function for this purpose instead of public
                # self.preprocess(string), which serves for another purpose)
                tokens.append(self._preprocess(entry))
        return tokens

    def _preprocess(self, line):
        # Nothing to do here
        return line


class StrippedLineDiff(LineDiff):

    def _preprocess(self, line):
        # Override the parent's method
        return line.strip()


_line_diff = LineDiff()
_stripped_line_diff = StrippedLineDiff()


def diff_lines(old_string, new_string):
    return _line_diff.diff(old_string, new_string)


def diff_stripped_lines(old_string, new_string):
    return _stripped_line_diff.diff(old_string, new_string)
