def arg_to_string(argument: dict) -> str:
    """
    Stringify an objective/constraint argument to go into the generated code.

    Parameters
    ----------
    argument: dict
        The argument to stringify.

    Returns
    -------
    str
        The stringified argument.
    """
    name, arg_type, value = argument["name"], argument["type"], argument["value"]
    if arg_type in ["int", "float", "list", "function"]:
        return f"{name}={value}"
    else:
        return f'{name}="{value}"'


def format_2d_array(array, indent: int = 8) -> str:
    """
    Format a 2D array to go into the generated code. Each list is on an indented new line.
    Values are rounded to 2 decimals for readability.

    Parameters
    ----------
    array: list
        The array to format.
    indent: int
        The number of spaces to indent the array.

    Returns
    -------
    str
        The formatted array.
    """
    res = " [\n"
    for arr in array:
        res += f"{' ' * (indent + 4)}[{', '.join([str(round(value, 2)) for value in arr])}],\n"
    res += f"{' ' * indent}]"
    return res


def invert_min_max(bounds: list, index: int) -> None:
    """
    Invert the min and max of the bounds at the given index.

    Example:
    index = 1
    { "min": [0, 0, 0], "max": [1, 1, 1] } -> { "min": [0, -1, 0], "max": [1, 0, 1] }

    Parameters
    ----------
    bounds: list
        The bounds to invert.
    index: int
        The index of the bounds to invert.

    Returns
    -------
    None
    """
    for i in range(len(bounds)):
        tmp = bounds[i]["min"][index].copy()
        bounds[i]["min"][index] = -bounds[i]["max"][index]
        bounds[i]["max"][index] = -tmp


def indent_lines(text: str, indent: int = 4) -> str:
    """
    Indent each line of the given text by the given number of spaces. Ignore beginning and trailing new lines.

    Parameters
    ----------
    text: str
        The text to indent.
    indent: int
        The number of spaces to indent the text.

    Returns
    -------
    str
        The indented text.
    """
    lines = text.split("\n")
    res = ""
    for line in lines:
        if line:
            res += f"{' ' * indent}{line}\n"
        else:
            res += "\n"

    # remove trailing new line
    res = res[:-1]

    return res
