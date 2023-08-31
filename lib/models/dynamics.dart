enum DynamicsType {
  // TODO Transform this enum into a json reader so when the BioModel is loaded, we automatically retrieve everything that is needed
  torqueDriven,
  dummy;

  @override
  String toString() {
    switch (this) {
      case torqueDriven:
        return 'Torque driven';
      case dummy:
        return 'Dummy';
    }
  }

  String toPythonString() {
    switch (this) {
      case torqueDriven:
        return 'DynamicsFcn.TORQUE_DRIVEN';
      case dummy:
        return 'DynamicsFcn.DUMMY';
    }
  }

  List<String> get states {
    switch (this) {
      case torqueDriven:
        return ['q', 'qdot'];
      case dummy:
        return ['tata'];
    }
  }

  // TODO Call python so it automatically gets the dimensions of variables
  List<String> get stateDimensions {
    switch (this) {
      case torqueDriven:
        return ['nb_q', 'nb_qdot'];
      case dummy:
        return ['nb_tata'];
    }
  }

  List<String> get controls {
    switch (this) {
      case torqueDriven:
        return ['tau'];
      case dummy:
        return ['coucou'];
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
