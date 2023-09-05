enum Nodes {
  start,
  end,
  all,
  allShooting;

  String toPythonString() {
    switch (this) {
      case start:
        return 'Node.START';
      case end:
        return 'Node.END';
      case all:
        return 'Node.ALL';
      case allShooting:
        return 'Node.ALL_SHOOTING';
    }
  }

  @override
  String toString() {
    switch (this) {
      case start:
        return 'Starting node';
      case end:
        return 'Last node';
      case all:
        return 'All nodes';
      case allShooting:
        return 'All shooting nodes';
    }
  }
}
