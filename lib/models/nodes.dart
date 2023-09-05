enum Nodes {
  start,
  end,
  all;

  String toPythonString() {
    switch (this) {
      case start:
        return 'Node.START';
      case end:
        return 'Node.END';
      case all:
        return 'Node.ALL';
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
    }
  }
}
