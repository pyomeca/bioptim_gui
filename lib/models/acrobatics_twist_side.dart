enum PreferredTwistSide {
  left,
  right,
  ;

  @override
  String toString() {
    switch (this) {
      case left:
        return 'Left';
      case right:
        return 'Right';
    }
  }

  String toPythonString() {
    switch (this) {
      case left:
        return 'PreferredTwistSide.LEFT';
      case right:
        return 'PreferredTwistSide.RIGHT';
    }
  }
}
