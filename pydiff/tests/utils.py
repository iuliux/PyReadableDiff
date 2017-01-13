import unittest

import pydiff


class TestBase(unittest.TestCase):
    """ Base class for testing all classes computing diffs. """

    def setUp(self, diff_class=None):
        super(TestBase, self).setUp()
        # Differ can be customized for testing specific subclasses
        self.differ = (diff_class or pydiff.Diff)()

    def check_changes(self, old_string, new_string, expected_changes):
        actual_changes = self.differ.diff(old_string, new_string)
        self.assertEqual(expected_changes, actual_changes)

    def check_xml(self, old_string, new_string, expected_xml):
        actual_changes = self.differ.diff(old_string, new_string)
        actual_xml = pydiff.convert_changes_to_xml(actual_changes)
        self.assertEqual(expected_xml, actual_xml)
