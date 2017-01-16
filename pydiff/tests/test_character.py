import pydiff

import utils


class TestCharacter(utils.TestBase):

    def setUp(self):
        super(TestCharacter, self).setUp(pydiff.CharacterDiff)

    def test_diff_characters_general(self):
        self.check_xml('New Value.', 'New ValueMoreData.',
                       'New Value<ins>MoreData</ins>.')

        self.check_xml('New ValueMoreData.', 'New Value.',
                       'New Value<del>MoreData</del>.')

        self.check_xml(' helloworld ', 'Hello, world',
                       '<del> h</del><ins>H</ins>ello<ins>, </ins>world<del> </del>')

        self.check_xml('restaura', 'aurant',
                       '<del>rest</del>aura<ins>nt</ins>')

    def test_diff_characters_corner_cases(self):
        self.check_xml('New Value', 'New Value', 'New Value')

        self.check_xml('', '', '')

        self.check_xml('New Value', '', '<del>New Value</del>')

        self.check_xml('', 'New Value', '<ins>New Value</ins>')

        self.check_xml('abc', 'xyz', '<del>abc</del><ins>xyz</ins>')

    def test_diff_characters_additional(self):
        self.check_changes(
            'y' + 'a' * 1000 + 'x' + 'b' * 1000,
                  'a' * 1000 + 'y' + 'b' * 1000 + 'x',
            [{'count': 1, 'value': 'y', 'removed': True, 'added': None},
             {'count': 1000, 'value': 'a' * 1000},
             {'count': 1, 'value': 'x', 'removed': True, 'added': None},
             {'count': 1, 'value': 'y', 'removed': None, 'added': True},
             {'count': 1000, 'value': 'b' * 1000},
             {'count': 1, 'value': 'x', 'removed': None, 'added': True}]
        )
