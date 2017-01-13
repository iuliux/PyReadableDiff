class _AssociativeArray(object):

    def __init__(self, data={}):
        self._data = data.copy()

    def __getitem__(self, key):
        return self._data.get(key)

    def __setitem__(self, key, value):
        self._data[key] = value


class Diff(object):

    def diff(self, old_string, new_string):
        # Allow subclasses to massage the input prior to running
        old_string = self.preprocess(old_string)
        new_string = self.preprocess(new_string)

        old_string = self.tokenize(old_string)
        new_string = self.tokenize(new_string)

        new_len = len(new_string)
        old_len = len(old_string)
        max_edit_length = new_len + old_len
        best_path = _AssociativeArray({0: {'new_pos': -1, 'components': []}})

        # Seed edit_length = 0, i.e. the content starts with the same values
        old_pos = self._extract_common(best_path[0], new_string, old_string, 0)
        if best_path[0]['new_pos'] + 1 >= new_len and old_pos + 1 >= old_len:
            # Identity per the equality and tokenizer
            return [{'value': self.join(new_string), 'count': new_len}]

        for edit_length in range(1, max_edit_length + 1):
            # Check all permutations of a given edit length for acceptance
            for diagonal_path in range(-1 * edit_length, edit_length + 1, 2):
                add_path = best_path[diagonal_path - 1]
                remove_path = best_path[diagonal_path + 1]
                old_pos = (remove_path['new_pos'] if remove_path else 0) - diagonal_path
                if add_path:
                    # No one else is going to attempt to use this value, clear it
                    best_path[diagonal_path - 1] = None

                can_add = add_path and add_path['new_pos'] + 1 < new_len
                can_remove = remove_path and 0 <= old_pos < old_len
                if not (can_add or can_remove):
                    # If this path is a terminal then prune
                    best_path[diagonal_path] = None
                    continue

                # Select the diagonal that we want to branch from. We select the prior
                # path whose position in the new string is the farthest from the origin
                # and does not pass the bounds of the diff graph
                if not can_add or (can_remove and add_path['new_pos'] < remove_path['new_pos']):
                    base_path = self._clone_path(remove_path)
                    self._push_component(base_path['components'], None, True)
                else:
                    base_path = add_path  # No need to clone, we've pulled it from the list
                    base_path['new_pos'] += 1
                    self._push_component(base_path['components'], True, None)

                old_pos = self._extract_common(base_path, new_string, old_string, diagonal_path)

                # If we have hit the end of both strings, then we are done
                if base_path['new_pos'] + 1 >= new_len and old_pos + 1 >= old_len:
                    return self._build_values(base_path['components'], new_string, old_string)
                else:
                    # Otherwise track this path as a potential candidate and continue
                    best_path[diagonal_path] = base_path

    # Public methods (can be overwritten by subclasses for computing customized diffs)

    def preprocess(self, string):
        return string

    def tokenize(self, string):
        return list(string)

    def join(self, tokens):
        return ''.join(tokens)

    def are_equal(self, left_token, right_token):
        return left_token == right_token

    # Private methods (for internal usage only)

    def _extract_common(self, base_path, new_string, old_string, diagonal_path):
        new_len = len(new_string)
        old_len = len(old_string)
        new_pos = base_path['new_pos']
        old_pos = new_pos - diagonal_path

        common_count = 0
        while new_pos + 1 < new_len and old_pos + 1 < old_len and self.equals(new_string[new_pos + 1], old_string[old_pos + 1]):
            new_pos += 1
            old_pos += 1
            common_count += 1

        if common_count:
            base_path['components'].append({'count': common_count})

        base_path['new_pos'] = new_pos
        return old_pos

    def _push_component(self, components, added, removed):
        last = components[-1] if components else None
        if last and last.get('added') == added and last.get('removed') == removed:
            new_last = last.copy()
            new_last['count'] += 1
            components[-1] = new_last
        else:
            components.append({'count': 1, 'added': added, 'removed': removed})

    def _clone_path(self, path):
        return {'new_pos': path['new_pos'], 'components': list(path['components'])}

    def _build_values(self, components, new_string, old_string):
        component_len = len(components)
        new_pos = 0
        old_pos = 0

        for component_pos in range(component_len):
            component = components[component_pos]
            if not component.get('removed'):
                component['value'] = self.join(new_string[new_pos : new_pos + component['count']])
                new_pos += component['count']

                # Common case
                if not component.get('added'):
                    old_pos += component['count']
            else:
                component['value'] = self.join(old_string[old_pos : old_pos + component['count']])
                old_pos += component['count']

                # Reverse add and remove so removes are output first to match common convention.
                # The diffing algorithm is tied to add then remove output and this is the simplest
                # route to get the desired output with minimal overhead
                if component_pos and components[component_pos - 1].get('added'):
                    components[component_pos], components[component_pos - 1] = components[component_pos - 1], components[component_pos]

        # Special case handle for when one terminal is ignored. For this case we merge the
        # terminal into the prior string and drop the change
        last_component = components[component_len - 1]
        if component_len > 1 and (last_component.get('added') or last_component.get('removed')) and self.equals('', last_component['value']):
            components[component_len - 2]['value'] += last_component['value']
            components.pop()

        return components
