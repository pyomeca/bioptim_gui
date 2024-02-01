import pytest

from bioptim_gui_api.utils.format_utils import format_2d_array, arg_to_string, indent_lines


def test_format_2d_array():
    array = [[1, 2, 3], [4, 5, 6]]
    expected = """ [
            [1, 2, 3],
            [4, 5, 6],
        ]"""
    assert format_2d_array(array, indent=8) == expected


@pytest.mark.parametrize(
    "argument, expected",
    [
        ({"name": "x", "type": "float", "value": 1.2}, "x=1.2"),
        ({"name": "x", "type": "int", "value": 0}, "x=0"),
        ({"name": "x", "type": "str", "value": "0"}, 'x="0"'),
    ],
)
def test_arg_to_string(argument, expected):
    assert arg_to_string(argument) == expected


def test_indent_simple():
    text = """
    haha
        hope it works
"""

    expected = """
        haha
            hope it works
"""

    assert indent_lines(text, 4) == expected


def test_indent_no_beginning_new_line():
    text = """    haha
        hope it works
"""

    expected = """        haha
            hope it works
"""

    assert indent_lines(text, 4) == expected


def test_indent_no_trailing_new_line():
    text = """
    haha
        hope it works"""

    expected = """
        haha
            hope it works"""

    assert indent_lines(text, 4) == expected


def test_multiple_newline_in_middle():
    text = """
    haha


        hope it works
        
"""

    expected = """
        haha


            hope it works
            
"""

    assert indent_lines(text, 4) == expected
