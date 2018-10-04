"""This module contains functions that retrieve a specific text field form a html formatted buffer
"""


def find_text_in_tag(data, tag, possible_values):
    """Method to find text under a specified tag in the provided html formatted data

    args:
        :data: The html data you want to parse
        :tag: The tag under which the field should be
        :possible_values: Dictionary with keys = identifier and values = identifier values for the field you search.
        E.g. {'class': 'my-class', 'class': 'my-2nd-class'} would mean we search for a field with
        class == my-class or class == 'my-2nd-class'

    returns: Value of the field formatted as text

    raises: ValueError if we didn't find a match
    """
    for key in possible_values.keys():
        try:
            field = data.find(tag, {key: possible_values[key]}).text.strip()
            break
        except Exception:
            continue
    else:
        raise ValueError('Could not find the expected text in the html buffer')
    return field
