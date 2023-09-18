enum TrampoPosition {
  tuck,
  pike,
  straight,
  ;

  @override
  String toString() {
    switch (this) {
      case tuck:
        return 'Tuck';
      case pike:
        return 'Pike';
      case straight:
        return 'Straight';
    }
  }
}
