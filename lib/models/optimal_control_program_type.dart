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
        return 'Acrobatics optimal control program';
    }
  }

  String toPythonString() {
    switch (this) {
      case ocp:
        return 'OptimalControlProgram';
      case abrobaticsOCP:
        return 'OptimalControlProgram';
    }
  }
}
