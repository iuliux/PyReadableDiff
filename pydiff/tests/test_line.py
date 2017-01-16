import pydiff

import utils


class TestLine(utils.TestBase):

    def setUp(self):
        super(TestLine, self).setUp(pydiff.LineDiff)

    def test_diff_lines_general(self):
        self.check_xml('line\nold value\nline', 'line\nnew value\nline',
                       'line\n<del>old value\n</del><ins>new value\n</ins>line')

        self.check_xml('line\nvalue\nline', 'line\nvalue\nline',
                       'line\nvalue\nline')

    def test_diff_lines_no_stripping(self):
        self.check_xml('line\nvalue \nline', 'line\n value\nline',
                       'line\n<del>value \n</del><ins> value\n</ins>line')

    def test_tokenize_various_linebreaks(self):
        self.assertEqual(['line\r', 'value\r\n', 'line\n'],
                         self.differ.tokenize('line\rvalue\r\nline\n'))

    def test_diff_lines_empty(self):
        self.check_xml('line\n\nold value\n\nline', '',
                       '<del>line\n\nold value\n\nline</del>')

        self.check_xml('', 'line\n\nnew value\n\nline',
                       '<ins>line\n\nnew value\n\nline</ins>')

        self.check_xml('line\n\nline', 'line\nnew value\nline',
                       'line\n<del>\n</del><ins>new value\n</ins>line')

        self.check_xml('line\nold value\nline', 'line\n\nline',
                       'line\n<del>old value\n</del><ins>\n</ins>line')


class TestStrippedLine(utils.TestBase):

    def setUp(self):
        super(TestStrippedLine, self).setUp(pydiff.StrippedLineDiff)

    def test_diff_lines_general(self):
        self.check_xml('line\nold value\nline', 'line\nnew value\nline',
                       'line\n<del>old value\n</del><ins>new value\n</ins>line')

        self.check_xml('line\nvalue\nline', 'line\nvalue\nline',
                       'line\nvalue\nline')

    def test_diff_lines_stripping(self):
        self.check_xml('line\nvalue \nline', 'line\n value\nline',
                       'line\nvalue\nline')

    def test_tokenize_various_linebreaks(self):
        self.assertEqual(['line\r', 'value\r\n', 'line\n'],
                         self.differ.tokenize('line\r \tvalue\t \r\nline\n'))

    def test_diff_lines_empty(self):
        self.check_xml('line\n\nold value\n\nline', '',
                       '<del>line\n\nold value\n\nline</del>')

        self.check_xml('', 'line\n\nnew value\n\nline',
                       '<ins>line\n\nnew value\n\nline</ins>')

        self.check_xml('line\n\nline', 'line\n new value \nline',
                       'line\n<del>\n</del><ins>new value\n</ins>line')

        self.check_xml('line\n old value \nline', 'line\n\nline',
                       'line\n<del>old value\n</del><ins>\n</ins>line')
