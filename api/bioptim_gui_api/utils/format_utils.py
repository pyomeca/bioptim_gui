def arg_to_string(argument: dict) -> str:
    name, arg_type, value = argument["name"], argument["type"], argument["value"]
    if arg_type in ["int", "float", "list"]:
        return f"{name}={value}"
    else:
        return f'{name}="{value}"'


def format_2d_array(array, indent: int = 8) -> str:
    res = " [\n"
    for arr in array:
        res += f"{' ' * (indent + 4)}[{', '.join([str(round(value, 2)) for value in arr])}],\n"
    res += f"{' ' * indent}]"
    return res
