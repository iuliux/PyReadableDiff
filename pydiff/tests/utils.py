import unittest

import pydiff


class TestBase(unittest.TestCase):
    """ Base class for testing all classes computing diffs. """

    def setUp(self):
        # Customize the differ object for subclasses
        self.differ = pydiff.Diff()

    def check_xml(self, old_string, new_string, expected_xml):
        changes = self.differ.diff(old_string, new_string)
        actual_xml = pydiff.convert_changes_to_xml(changes)
        self.assertEqual(expected_xml, actual_xml)
