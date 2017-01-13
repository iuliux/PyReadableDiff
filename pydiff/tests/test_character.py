import pydiff

import utils


class TestCharacter(utils.TestBase):

    def setUp(self):
        self.differ = pydiff.CharacterDiff()

    def test_diff_characters(self):
        self.check_xml('New Value.', 'New ValueMoreData.',
                       'New Value<ins>MoreData</ins>.')

        self.check_xml('New ValueMoreData.', 'New Value.',
                       'New Value<del>MoreData</del>.')

        self.check_xml(' helloworld ', 'Hello, world',
                       '<del> h</del><ins>H</ins>ello<ins>, </ins>world<del> </del>')

        # Some corner cases

        self.check_xml('New Value', 'New Value', 'New Value')

        self.check_xml('', '', '')

        self.check_xml('New Value', '', '<del>New Value</del>')

        self.check_xml('', 'New Value', '<ins>New Value</ins>')
