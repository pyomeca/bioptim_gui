extension BoolToPythonString on bool {
  String toPythonString() {
    return this ? 'True' : 'False';
  }
}
