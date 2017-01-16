from xml.sax.saxutils import escape as xml_escape


def _extended_xml_escape(string):
    # xml_escape only escapes <, &, and >,
    # so provide an additional mapping for ' and "
    return xml_escape(string, {'"': '&quot;', "'": "&apos;"})


def convert_changes_to_xml(changes):
    result = []
    for change in changes:
        if change.get('added'):
            result.append('<ins>')
        elif change.get('removed'):
            result.append('<del>')

        result.append(_extended_xml_escape(change['value']))

        if change.get('added'):
            result.append('</ins>')
        elif change.get('removed'):
            result.append('</del>')
    return ''.join(result)
