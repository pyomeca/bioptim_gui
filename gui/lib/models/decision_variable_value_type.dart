enum DecisionVariableValueType {
  minBound,
  maxBound,
  initGuess;

  String toPythonString() {
    switch (this) {
      case DecisionVariableValueType.minBound:
        return "min_bounds";
      case DecisionVariableValueType.maxBound:
        return "max_bounds";
      case DecisionVariableValueType.initGuess:
        return "initial_guess";
    }
  }
}
