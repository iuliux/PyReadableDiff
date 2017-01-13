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
