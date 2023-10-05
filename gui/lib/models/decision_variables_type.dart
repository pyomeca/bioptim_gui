enum DecisionVariableType {
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
