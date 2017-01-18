from .base import Diff


class ListDiff(Diff):

    def join(self, tokens):
        # Tokens are stored internally as lists, so there is no need in any
        # additional transformations
        return tokens


_list_diff = ListDiff()


def diff_lists(old_list, new_list):
    return _list_diff.diff(old_list, new_list)
