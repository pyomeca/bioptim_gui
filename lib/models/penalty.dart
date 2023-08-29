mixin _PenaltyFcn {
  ///
  /// The objective function as it should be written in Python
  String toPythonString();

  ///
  /// The type of penalty (Mayer, Lagrange or Constraint)
  String get penaltyTypeToString;

  ///
  /// The name of the penalty (objective or constraint)
  String get penaltyType;

  ///
  /// The list of mandatory arguments in this objective function
  List<String> get mandatoryArguments;
}

mixin ObjectiveFcn implements _PenaltyFcn {}

enum LagrangeFcn implements ObjectiveFcn {
  minimizeControls;

  @override
  String get penaltyTypeToString => 'Lagrange';

  @override
  String get penaltyType => 'objective';

  @override
  String toString() {
    switch (this) {
      case minimizeControls:
        return 'Minimize control';
    }
  }

  @override
  String toPythonString() {
    switch (this) {
      case minimizeControls:
        return 'ObjectiveFcn.Lagrange.MINIMIZE_CONTROL';
    }
  }

  @override
  List<String> get mandatoryArguments {
    switch (this) {
      case minimizeControls:
        return ['key'];
    }
  }
}

enum MayerFcn implements _PenaltyFcn {
  minimizeTime;

  @override
  String get penaltyTypeToString => 'Mayer';

  @override
  String get penaltyType => 'objective';

  @override
  String toString() {
    switch (this) {
      case minimizeTime:
        return 'Minimize time';
    }
  }

  @override
  String toPythonString() {
    switch (this) {
      case minimizeTime:
        return 'ObjectiveFcn.Mayer.MINIMIZE_TIME';
    }
  }

  @override
  List<String> get mandatoryArguments {
    switch (this) {
      case minimizeTime:
        return [];
    }
  }
}

enum ConstraintFcn implements _PenaltyFcn {
  timeConstraint;

  @override
  String get penaltyTypeToString => 'Constraint';

  @override
  String get penaltyType => 'constraint';

  @override
  String toString() {
    switch (this) {
      case timeConstraint:
        return 'Time constraint';
    }
  }

  @override
  String toPythonString() {
    switch (this) {
      case timeConstraint:
        return 'ConstraintFcn.TIME_CONSTRAINT';
    }
  }

  @override
  List<String> get mandatoryArguments {
    switch (this) {
      case timeConstraint:
        return [];
    }
  }
}

class _Penalty {
  final _PenaltyFcn fcn;
  final Map<String, dynamic> _arguments;

  Iterable<String> get argumentKeys => _arguments.keys;

  String argumentToPythonString(String key) {
    final argument = _arguments[key];
    if (argument == null) throw 'The key $key is not in the argument list';

    switch (argument.runtimeType) {
      case String:
        return '$key="$argument"';
      default:
        throw 'The type ${argument.runtimeType} is not supported.\n'
            'Please contact the developpers for more assistance';
    }
  }

  _Penalty(this.fcn, {required Map<String, dynamic> arguments})
      : _arguments = arguments {
    for (final argument in _arguments.keys) {
      if (!fcn.mandatoryArguments.contains(argument)) {
        throw 'The ${fcn.penaltyType} $fcn requires $argument';
      }
    }
  }
}

class Objective extends _Penalty {
  Objective(ObjectiveFcn fcn, {required Map<String, dynamic> arguments})
      : super(fcn, arguments: arguments);
}

class Constraint extends _Penalty {
  Constraint(ConstraintFcn fcn, {required Map<String, dynamic> arguments})
      : super(fcn, arguments: arguments);
}
