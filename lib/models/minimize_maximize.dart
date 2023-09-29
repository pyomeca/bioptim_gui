enum MinMax {
  maximize,
  minimize,
  ;

  @override
  String toString() {
    switch (this) {
      case MinMax.maximize:
        return 'Maximize';
      case MinMax.minimize:
        return 'Minimize';
    }
  }

  String toPythonString() {
    switch (this) {
      case MinMax.maximize:
        return '-'; // will be used to negate the weight for maximizing
      case MinMax.minimize:
        return '';
    }
  }
}
