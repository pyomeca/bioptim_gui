enum AcrobaticsPosition {
  straight,
  tuck,
  pike,
  ;

  @override
  String toString() {
    switch (this) {
      case straight:
        return 'Straight';
      case tuck:
        return 'Tuck';
      case pike:
        return 'Pike';
    }
  }
}
