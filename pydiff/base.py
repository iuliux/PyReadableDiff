from collections import defaultdict


class Diff(object):

    # Public methods (can be overridden by subclasses
    # for computing customized diffs)

    def preprocess(self, string):
        return string

    def tokenize(self, string):
        return list(string)

    def join(self, tokens):
        return ''.join(tokens)

    def are_equal(self, left_token, right_token):
        return left_token == right_token

    # Actual implementation of diff computing algorithm (though this method
    # is also public, it shouldn't be changed unless you want to implement
    # and use another algorithm instead of the current one)

    def diff(self, old_string, new_string):
        # Preprocess the input strings prior to running
        old_string = self.preprocess(old_string)
        new_string = self.preprocess(new_string)

        # Split the already processed strings into tokens
        old_tokens = self.tokenize(old_string)
        new_tokens = self.tokenize(new_string)

        old_len = len(old_tokens)
        new_len = len(new_tokens)

        furthest_paths = defaultdict(lambda: None)
        furthest_paths[0] = {'new_pos': -1, 'components': []}

        # Seed the case when edit_dist = 0, i.e. the strings are considered
        # to be equal, but we take the most recent version
        old_pos, new_pos = self._extend_path(furthest_paths[0],
                                             old_tokens, new_tokens, 0)
        if old_pos + 1 >= old_len and new_pos + 1 >= new_len:
            return [{'value': self.join(new_tokens), 'count': new_len}]

        max_edit_dist = new_len + old_len
        for edit_dist in range(1, max_edit_dist + 1):
            for diag in range(-edit_dist, edit_dist + 1, 2):
                add_path = furthest_paths[diag - 1]
                remove_path = furthest_paths[diag + 1]

                # Select the diagonal that we want to branch from.
                # We select the previous path whose endpoint in the old string
                # is the farthest from the origin and does not pass the bounds
                # of the diff (a.k.a edit) graph. Notice, that we tend to
                # perform removals first (as many as possible) and then
                # insertions in order to follow the common convention and also
                # to get slightly better diffs with bigger groups of
                # removed/added tokens rather than several smaller alternating
                # ones.
                if diag == -edit_dist or diag != edit_dist and \
                        self._get_endpoint(add_path, diag - 1)[0] <= \
                        self._get_endpoint(remove_path, diag + 1)[0]:
                    path = self._copy_path(remove_path)
                    self._push_component(path['components'], removed=True)
                else:
                    path = self._copy_path(add_path)
                    path['new_pos'] += 1
                    self._push_component(path['components'], added=True)

                # Try to extend the current path by matching as many tokens
                # as possible
                old_pos, new_pos = \
                    self._extend_path(path, old_tokens, new_tokens, diag)

                # If we have hit the ends of both strings, then we are done,
                # since a shortest path (i.e. with the minimum number of
                # editions) has just been found
                if old_pos + 1 >= old_len and new_pos + 1 >= new_len:
                    return self._build_values_from_components(
                        path['components'], old_tokens, new_tokens
                    )
                else:
                    # Otherwise track this path as a potential candidate
                    # and proceed to the next iteration
                    furthest_paths[diag] = path

    # Private utility methods (for internal usage only)

    def _get_endpoint(self, path, diag):
        new_pos = path['new_pos']
        old_pos = new_pos - diag
        return old_pos, new_pos

    def _extend_path(self, path, old_string, new_string, diag):
        old_len = len(old_string)
        new_len = len(new_string)

        old_pos, new_pos = self._get_endpoint(path, diag)

        count = 0
        while old_pos + 1 < old_len and new_pos + 1 < new_len and \
                self.are_equal(old_string[old_pos + 1],
                               new_string[new_pos + 1]):
            old_pos += 1
            new_pos += 1
            count += 1

        if count:
            path['components'].append({'count': count})

        path['new_pos'] = new_pos
        return old_pos, new_pos

    def _push_component(self, components, added=None, removed=None):
        last_component = components[-1] if components else None
        if last_component and last_component.get('added') == added and \
                last_component.get('removed') == removed:
            last_component = last_component.copy()
            last_component['count'] += 1
            components[-1] = last_component
        else:
            components.append({'count': 1, 'added': added, 'removed': removed})

    def _copy_path(self, path):
        return {'new_pos': path['new_pos'],
                'components': list(path['components'])}

    def _build_values_from_components(self, components,
                                      old_tokens, new_tokens):
        old_pos = 0
        new_pos = 0

        for component in components:
            if not component.get('removed'):
                component['value'] = self.join(
                    new_tokens[new_pos:(new_pos + component['count'])]
                )
                new_pos += component['count']
                # The component is neither removed, nor added,
                # i.e. it is unchanged, so we have to increment both indices
                if not component.get('added'):
                    old_pos += component['count']
            else:
                component['value'] = self.join(
                    old_tokens[old_pos:(old_pos + component['count'])]
                )
                old_pos += component['count']

        # Handle the special case when the last change is dropped and
        # the last component is appended to the previous one
        last_component = components[-1]
        added_or_removed = \
            last_component.get('added') or last_component.get('removed')
        if len(components) > 1 and added_or_removed and \
                self.are_equal('', last_component['value']):
            components[-2]['value'] += last_component['value']
            components.pop()

        return components
