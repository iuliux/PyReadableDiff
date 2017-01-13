import pydiff

import utils


class TestWord(utils.TestBase):

    def setUp(self):
        self.differ = pydiff.WordDiff()

    def test_diff_words_whitespaces(self):
        self.check_xml('New Value', 'New  ValueMoreData',
                       'New  <del>Value</del><ins>ValueMoreData</ins>')

        self.check_xml('New Value  ', 'New  ValueMoreData ',
                       'New  <del>Value</del><ins>ValueMoreData</ins> ')

    def test_diff_words_boundaries(self):
        self.check_xml('New :Value:Test', 'New  ValueMoreData ',
                       'New  <del>:Value:Test</del><ins>ValueMoreData </ins>')

        self.check_xml('New Value:Test', 'New  Value:MoreData ',
                       'New  Value:<del>Test</del><ins>MoreData </ins>')

        self.check_xml('New Value-Test', 'New  Value:MoreData ',
                       'New  Value<del>-Test</del><ins>:MoreData </ins>')

        self.check_xml('New Value', 'New  Value:MoreData ',
                       'New  Value<ins>:MoreData </ins>')

    def test_diff_words_no_changes(self):
        self.check_xml('New Value', 'New Value', 'New Value')

        self.check_xml('', '', '')

        self.check_xml('New Value', 'New  Value', 'New  Value')

    def test_diff_words_empty(self):
        self.check_xml('New Value', '',
                       '<del>New Value</del>')

        self.check_xml('', 'New Value',
                       '<ins>New Value</ins>')

    def test_diff_words_no_anchor(self):
        self.check_xml('New Value New Value', 'Value Value New New',
                       '<del>New</del><ins>Value</ins> Value New <del>Value</del><ins>New</ins>')
