import unittest

import pydiff


class ConvertTest(unittest.TestCase):

    def test_conversion_to_xml(self):
        changes = [
            {'value': 'I '},
            {'value': 'hate', 'removed': True}, {'value': 'love', 'added': True},
            {'value': ' '},
            {'value': 'JS', 'removed': True}, {'value': 'Python', 'added': True},
            {'value': '!'}
        ]
        expected_xml = 'I <del>hate</del><ins>love</ins> <del>JS</del><ins>Python</ins>!'
        actual_xml = pydiff.convert_changes_to_xml(changes)
        self.assertEqual(expected_xml, actual_xml)


class BaseTest(unittest.TestCase):

    def check_xml(self, old_string, new_string, expected_xml):
        changes = self.compute_diff(old_string, new_string)
        actual_xml = pydiff.convert_changes_to_xml(changes)
        self.assertEqual(expected_xml, actual_xml)

    def compute_diff(self, old_string, new_string):
        raise NotImplementedError('base class cannot compute diffs')


class CharacterTest(BaseTest):

    def compute_diff(self, old_string, new_string):
        return pydiff.diff_characters(old_string, new_string)

    def test_diff_characters(self):
        self.check_xml('New Value.', 'New ValueMoreData.',
                       'New Value<ins>MoreData</ins>.')
        self.check_xml('New ValueMoreData.', 'New Value.',
                       'New Value<del>MoreData</del>.')
        self.check_xml(' helloworld ', 'Hello, world',
                       '<del> h</del><ins>H</ins>ello<ins>, </ins>world<del> </del>')


class WordTest(BaseTest):

    def compute_diff(self, old_string, new_string):
        return pydiff.diff_words(old_string, new_string)


if __name__ == '__main__':
    unittest.main()
