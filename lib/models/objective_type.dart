enum ObjectiveType {
  mayer,
  lagrange,
  ;

  @override
  String toString() {
    switch (this) {
      case mayer:
        return '\u2133'; // German mark M
      case lagrange:
        return '\u2112'; // Laplace L
    }
  }
}
