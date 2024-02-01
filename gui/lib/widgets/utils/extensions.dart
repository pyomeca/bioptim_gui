extension BoolToPythonString on bool {
  String toPythonString() {
    return this ? 'True' : 'False';
  }
}

extension StringExtension on String {
  String capitalize() {
    return "${this[0].toUpperCase()}${substring(1).toLowerCase()}";
  }

  List<double>? tryParseDoubleList() {
    var input = trim();

    if (input.startsWith('[') && input.endsWith(']')) {
      input = input.substring(1, input.length - 1);
    }

    if (input.isEmpty) {
      return null;
    }

    var valueStrings = input.split(',');

    var intValues = valueStrings.map((value) {
      return double.parse(value);
    }).toList();

    return intValues;
  }
}
