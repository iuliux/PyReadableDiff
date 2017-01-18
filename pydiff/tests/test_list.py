import pydiff

import utils


class TestList(utils.TestBase):

    def setUp(self):
        super(TestList, self).setUp(pydiff.ListDiff)

    def test_diff_lists(self):
        a, b, c = {'a': 1}, {'b': 2}, {'c': 3}
        d, e, f = {'d': 4}, {'e': 5}, {'f': 6}

        old_list = [a, b, c, d, e]
        new_list = [a, c, d, f, e]

        expected_changes = [
            {'count': 1, 'value': [a]},
            {'count': 1, 'value': [b], 'removed': True, 'added': None},
            {'count': 2, 'value': [c, d]},
            {'count': 1, 'value': [f], 'removed': None, 'added': True},
            {'count': 1, 'value': [e]}
        ]

        # Any iterable with the same content (the order matters!) can be used
        # as an input and will produce the same output
        self.check_changes(old_list, tuple(new_list), expected_changes)
        self.check_changes(tuple(old_list), iter(new_list), expected_changes)
        self.check_changes(iter(old_list), new_list, expected_changes)
