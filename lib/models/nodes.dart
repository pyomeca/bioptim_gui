enum Nodes {
  start,
  mid,
  intermediates,
  penultimate,
  end,
  all,
  allShooting,
  transition,
  multinode,
  defaultNode,
  ;

  String toPythonString() {
    switch (this) {
      case start:
        return 'Node.START';
      case mid:
        return 'Node.MID';
      case intermediates:
        return 'Node.INTERMEDIATES';
      case penultimate:
        return 'Node.PENULTIMATE';
      case end:
        return 'Node.END';
      case all:
        return 'Node.ALL';
      case allShooting:
        return 'Node.ALL_SHOOTING';
      case transition:
        return 'Node.TRANSITION';
      case multinode:
        return 'Node.MULTINODE';
      case defaultNode:
        return 'Node.DEFAULT';
    }
  }

  @override
  String toString() {
    switch (this) {
      case start:
        return 'Starting node';
      case mid:
        return 'Mid node';
      case intermediates:
        return 'Intermediate nodes';
      case penultimate:
        return 'Penultimate node';
      case end:
        return 'Last node';
      case all:
        return 'All nodes ';
      case allShooting:
        return 'All shooting nodes';
      case transition:
        return 'Transition nodes';
      case multinode:
        return 'Multinode';
      case defaultNode:
        return 'Default node';
    }
  }
}
