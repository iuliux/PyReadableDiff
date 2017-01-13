# PyReadableDiff
Intuitive human-readable diff for text.

The [pydiff](https://github.com/BeagleInc/PyReadableDiff)
library was inspired by the [jsdiff](https://github.com/kpdecker/jsdiff)
library, and it tries to port as much functionality from JS to Python as possible,
though the APIs may differ.

## API

* `pydiff.diff_characters(old_string, new_string)` - diffs two blocks of text, comparing character by character.

    Returns a list of change dicts (see below).

* `pydiff.diff_words(old_string, new_string)` - diffs two blocks of text, comparing word by word, ignoring whitespaces.

    Returns a list of change dicts (see below).

* `pydiff.convert_changes_to_xml(changes)` - converts a list of changes to a serialized XML format.

### Change Dicts

Many of the methods above return change dicts. These dicts consist of the following keys:

* `value`: text content
* `count`: number of tokens merged together in order to form the given value
* `added`: `True` if the value was inserted into the new string (`None` or absent otherwise)
* `removed`: `True` of the value was removed from the old string (`None` or absent otherwise)

Note that some cases may omit a particular flag key. Comparison on the flag keys should always be done in a truthy or falsy manner.
We suggest using the `.get(key)` method of dicts for this purpose, e.g.:
```python
if change.get('added'):
    # handle an inserted part
    ...
elif change.get('removed'):
    # handle a deleted part
    ...
else:
    # handle an unchanged part
    ...
```

## Custom Diffs

If you need more customization for your diffs, you can inherit from the `pydiff.Diff` base class and override the following available public methods:

* `preprocess(self, string)` - prepares an input string for processing (is used on `old_string` and `new_string` prior to running the main diff computing algorithm).
By default does nothing and simply returns the same string back.

* `tokenize(self, string)` - splits the preprocessed input string into atomic parts, which are compared with each other during the diffing.
By default uses characters as tokens.

* `join(self, tokens)` - merges tokens into bigger strings, which then form text values of resultant change dicts.
By default simply concatenates all tokens using an empty string as a separator.

* `are_equal(self, left_token, right_token)` - compares two tokens returning `True` or `False`.
By default uses the built-in `==` operator. For example, if you want your diffs to be case insensitive, you may define this method in a following manner:

```python
import pydiff

class CustomDiff(pydiff.Diff):
    ...

    def are_equal(self, left_token, right_token):
        return left_token.lower() == right_token.lower()

    ...
```

After that actual diffs can be computed via the inherited `.diff(old_string, new_string)` method of instances of your newly created subclass.
