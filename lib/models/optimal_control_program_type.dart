enum OptimalControlProgramType {
  ocp,
  abrobaticsOCP,
  ;

  @override
  String toString() {
    switch (this) {
      case ocp:
        return 'Optimal control program';
      case abrobaticsOCP:
        return 'Abrobatics optimal control program';
    }
  }

  String toPythonString() {
    switch (this) {
      case ocp:
        return 'OptimalControlProgram';
      case abrobaticsOCP:
        return 'AbrobaticsOptimalControlProgram'; // TODO check if right String
    }
  }
}
