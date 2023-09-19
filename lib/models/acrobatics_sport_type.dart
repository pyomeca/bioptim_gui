enum AcrobaticsSportType {
  trampoline,
  ;

  @override
  String toString() {
    switch (this) {
      case trampoline:
        return 'Trampoline';
    }
  }

  String toPythonString() {
    switch (this) {
      case trampoline:
        return 'Trampoline';
    }
  }
}
