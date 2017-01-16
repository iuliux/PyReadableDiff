from .base import Diff

from .character import CharacterDiff, \
                       diff_characters

from .word import WordDiff, WordWithSpaceDiff, \
                  diff_words, diff_words_with_spaces

from .line import LineDiff, StrippedLineDiff,\
                  diff_lines, diff_stripped_lines

from .convert import convert_changes_to_xml


__version__ = '0.1.0'
