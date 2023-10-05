enum BioModel {
  biorbd,
  dummy;

  @override
  String toString() {
    switch (this) {
      case biorbd:
        return 'Biorbd';
      case dummy:
        return 'Dummy';
    }
  }

  String toPythonString() {
    switch (this) {
      case biorbd:
        return 'BiorbdModel';
      case dummy:
        return 'Dummy';
    }
  }

  String get extension {
    switch (this) {
      case biorbd:
        return 'bioMod';
      case dummy:
        return 'dummy';
    }
  }
}
