import 'package:bioptim_gui/models/matrix.dart';

enum Interpolation {
  constant,
  constantWithFirstAndLastDifferent;

  @override
  String toString() {
    switch (this) {
      case constant:
        return 'Constant';
      case constantWithFirstAndLastDifferent:
        return 'Constant except for first and last points';
    }
  }

  String toPythonString() {
    switch (this) {
      case constant:
        return 'InterpolationType.CONSTANT';
      case constantWithFirstAndLastDifferent:
        return 'InterpolationType.CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT';
    }
  }

  int get nbCols {
    switch (this) {
      case constant:
        return 1;
      case constantWithFirstAndLastDifferent:
        return 3;
    }
  }
}

class Bound {
  final Matrix min;
  final Matrix max;
  Interpolation _interpolation;
  Interpolation get interpolation => _interpolation;
  set interpolation(Interpolation value) {
    _interpolation = value;
    min.changeNbRows(_interpolation.nbCols);
    max.changeNbRows(_interpolation.nbCols);
  }

  int get nbRows => min.nbRows;
  int get nbCols => min.nbCols;

  void changeDimension(int value) {
    min.changeNbRows(value);
    max.changeNbRows(value);
  }

  Bound({required int nbElements, required Interpolation interpolation})
      : min = Matrix.zeros(nbRows: nbElements, nbCols: interpolation.nbCols),
        max = Matrix.zeros(nbRows: nbElements, nbCols: interpolation.nbCols),
        _interpolation = interpolation;
}

class InitialGuess {
  final Matrix guess;
  final Interpolation interpolation;

  int get nbRows => guess.nbRows;
  int get nbCols => guess.nbCols;

  void changeDimension(int value) {
    guess.changeNbRows(value);
  }

  InitialGuess({required int nbElements, required this.interpolation})
      : guess = Matrix.zeros(nbRows: nbElements, nbCols: interpolation.nbCols);
}

class OptimizationVariable {
  final String name;
  final Bound bounds;
  final InitialGuess initialGuess;

  int get dimension => initialGuess.nbRows;
  int get nbRows => dimension;

  void changeDimension(int value) {
    bounds.changeDimension(value);
    initialGuess.changeDimension(value);
  }

  void fillInitialGuess(String name, {required List<double> guess}) {
    initialGuess.guess.fill(guess);
  }

  void fillBounds({
    required List<double> min,
    required List<double> max,
    int? rowIndex,
    int? colIndex,
  }) {
    bounds.min.fill(min, rowIndex: rowIndex, colIndex: colIndex);
    bounds.max.fill(max, rowIndex: rowIndex, colIndex: colIndex);
  }

  const OptimizationVariable({
    required this.name,
    required this.bounds,
    required this.initialGuess,
  });
}

enum OptimizationVariableType {
  state,
  control;

  @override
  String toString() {
    switch (this) {
      case state:
        return 'State';
      case control:
        return 'Control';
    }
  }

  String toPythonString() {
    switch (this) {
      case state:
        return 'x';
      case control:
        return 'u';
    }
  }
}

class OptimizationVariableMap {
  final Map<String, OptimizationVariable> _elements = {};

  final OptimizationVariableType type;
  OptimizationVariableMap(this.type);

  OptimizationVariable operator [](String name) {
    if (_elements[name] == null) {
      throw '$type $name not found';
    }
    return _elements[name]!;
  }

  List<String> get names => _elements.keys.toList();

  void addVariable(OptimizationVariable value) => _elements[value.name] = value;

  void clearVariables() => _elements.clear();

  void replaceVariable(OptimizationVariable value) =>
      _elements[value.name] = value;

  void removeVariable(String name) {
    if (_elements[name] == null) return;
    _elements.remove(name);
  }
}
