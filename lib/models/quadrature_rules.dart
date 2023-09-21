enum QuadratureRules {
  defaultQuadraticRule,
  rectangleLeft,
  rectangleRight,
  midPoint,
  approximateTrapezoidal,
  trapezoidal,
  ;

  String toPythonString() {
    switch (this) {
      case defaultQuadraticRule:
        return 'QuadratureRule.DEFAULT';
      case rectangleLeft:
        return 'QuadratureRule.RECTANGLE_LEFT';
      case rectangleRight:
        return 'QuadratureRule.RECTANGLE_RIGHT';
      case midPoint:
        return 'QuadratureRule.MIDPOINT';
      case approximateTrapezoidal:
        return 'QuadratureRule.APPROXIMATE_TRAPEZOIDAL';
      case trapezoidal:
        return 'QuadratureRule.TRAPEZOIDAL';
    }
  }

  @override
  String toString() {
    switch (this) {
      case defaultQuadraticRule:
        return 'Default';
      case rectangleLeft:
        return 'Rectangle left';
      case rectangleRight:
        return 'Rectangle right';
      case midPoint:
        return 'Midpoint';
      case approximateTrapezoidal:
        return 'Approximate trapezoidal';
      case trapezoidal:
        return 'Trapezoidal';
    }
  }
}
