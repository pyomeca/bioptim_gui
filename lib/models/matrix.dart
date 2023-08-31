class Matrix {
  int nbRows;
  int nbCols;
  List<double> values;
  Matrix.zeros({required this.nbRows, required this.nbCols})
      : values = List<double>.filled(nbRows * nbCols, 0, growable: false);

  Matrix.fromValues({
    required List<double> values,
    required this.nbRows,
    required this.nbCols,
  }) : values = List.from(values, growable: false);

  void changeNbRows(int value) {
    if (nbRows == value) return;
    // If we are changing the number of rows, we must reset the values,
    nbRows = value;
    values = List<double>.filled(nbRows * nbCols, 0, growable: false);
  }

  void changeNbCols(int value) {
    if (nbCols == value) return;
    // If we are changing the number of rows, we must reset the values,
    nbCols = value;
    values = List<double>.filled(nbRows * nbCols, 0, growable: false);
  }

  void fill(List<double> values, {int? rowIndex, int? colIndex}) {
    if (colIndex != null && rowIndex != null) {
      throw '[rowIndex] and [colIndex] can\' be simultaneously set when filling the matrix.';
    } else if (rowIndex != null) {
      _fillRow(rowIndex, values);
    } else if (colIndex != null) {
      _fillCol(colIndex, values);
    } else {
      _fillAll(values);
    }
  }

  void _fillAll(List<double> values) {
    if (values.length != this.values.length) {
      throw 'Wrong dimensions in filling matrix.\n'
          'Expected ${this.values.length}, but got ${values.length})';
    }

    for (int i = 0; i < values.length; i++) {
      this.values[i] = values[i];
    }
  }

  void _fillRow(int rowIndex, List<double> values) {
    if (values.length != nbCols) {
      throw 'Wrong dimensions in filling matrix row.\n'
          'Expected $nbCols, but got ${values.length})';
    }

    for (int i = 0; i < values.length; i++) {
      this.values[rowIndex * nbCols + i] = values[i];
    }
  }

  void _fillCol(int colIndex, List<double> values) {
    if (values.length != nbRows) {
      throw 'Wrong dimensions in filling matrix column.\n'
          'Expected $nbRows, but got ${values.length})';
    }

    for (int i = 0; i < values.length; i++) {
      this.values[i * nbCols + colIndex] = values[i];
    }
  }

  List<double> row(int rowIndex) {
    final out = <double>[];
    for (int i = 0; i < nbCols; i++) {
      out.add(values[rowIndex * nbCols + i]);
    }
    return out;
  }

  List<double> col(int colIndex) {
    final out = <double>[];
    for (int i = 0; i < nbRows; i++) {
      out.add(values[i * nbCols + colIndex]);
    }
    return out;
  }

  @override
  String toString() {
    final List<String> tp = [];
    for (int rowIndex = 0; rowIndex < nbRows; rowIndex++) {
      tp.add('[${row(rowIndex).join(', ')}]');
    }
    return '[${tp.join(', ')}]';
  }
}
