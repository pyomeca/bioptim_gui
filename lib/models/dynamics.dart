enum DynamicsType {
  torqueDriven;

  @override
  String toString() {
    switch (this) {
      case torqueDriven:
        return 'Torque driven';
    }
  }

  String toPythonString() {
    switch (this) {
      case torqueDriven:
        return 'DynamicsFcn.TORQUE_DRIVEN';
    }
  }

  List<String> get states {
    switch (this) {
      case torqueDriven:
        return ['q', 'qdot'];
    }
  }

  List<String> get controls {
    switch (this) {
      case torqueDriven:
        return ['tau'];
    }
  }
}

class Dynamics {
  final DynamicsType type;
  final bool isExpanded;

  const Dynamics({
    required this.type,
    required this.isExpanded,
  });
}
