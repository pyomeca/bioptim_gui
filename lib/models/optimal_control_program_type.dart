enum OptimalControlProgramType {
  ocp;

  @override
  String toString() {
    switch (this) {
      case ocp:
        return 'Optimal control program';
    }
  }

  String toPythonString() {
    switch (this) {
      case ocp:
        return 'OptimalControlProgram';
    }
  }
}
