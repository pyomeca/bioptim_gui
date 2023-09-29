enum SolverType {
  ipopt,
  ;

  @override
  String toString() {
    switch (this) {
      case ipopt:
        return 'Ipopt';
    }
  }

  String toPythonString() {
    switch (this) {
      case ipopt:
        return 'Solver.IPOPT';
    }
  }
}

class Solver {
  final SolverType type;

  const Solver({
    required this.type,
  });
}
