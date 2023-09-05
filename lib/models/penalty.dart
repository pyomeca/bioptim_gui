import 'package:bioptim_gui/models/nodes.dart';

enum PenaltyArgumentType {
  integer,
  float,
  string;

  @override
  String toString() {
    switch (this) {
      case integer:
        return 'Integer';
      case float:
        return 'Float';
      case string:
        return 'String';
    }
  }

  RegExp get regexpValidator {
    switch (this) {
      case integer:
        return RegExp(r'[0-9]');
      case float:
        return RegExp(r'[0-9\.]');
      case string:
        return RegExp(r'[a-zA-Z]');
    }
  }
}

class PenaltyArgument {
  final String name;
  final PenaltyArgumentType dataType;
  const PenaltyArgument({required this.name, required this.dataType});
}

mixin PenaltyFcn {
  ///
  /// The objective function as it should be written in Python
  String toPythonString();

  ///
  /// Interface to [values]
  List<PenaltyFcn> get fcnValues;

  ///
  /// The type of penalty (Mayer, Lagrange or Constraint)
  String get penaltyTypeToString;

  ///
  /// The name of the penalty (objective or constraint)
  String get penaltyType;

  ///
  /// The list of mandatory arguments in this objective function
  List<PenaltyArgument> get mandatoryArguments;
}

mixin ObjectiveFcn implements PenaltyFcn {
  @override
  List<PenaltyFcn> get fcnValues {
    final out = <ObjectiveFcn>[];
    for (final obj in LagrangeFcn.values) {
      out.add(obj);
    }
    for (final obj in MayerFcn.values) {
      out.add(obj);
    }
    return out;
  }
}

enum LagrangeFcn implements ObjectiveFcn {
  minimizeControls,
  minimizeStates;

  @override
  List<PenaltyFcn> get fcnValues {
    final out = <ObjectiveFcn>[];
    for (final obj in LagrangeFcn.values) {
      out.add(obj);
    }
    for (final obj in MayerFcn.values) {
      out.add(obj);
    }
    return out;
  }

  @override
  String get penaltyTypeToString => 'Lagrange';

  @override
  String get penaltyType => 'Objective';

  @override
  String toString() {
    switch (this) {
      case minimizeControls:
        return 'Minimize controls';
      case minimizeStates:
        return 'Minimize states';
    }
  }

  @override
  String toPythonString() {
    switch (this) {
      case minimizeControls:
        return 'ObjectiveFcn.Lagrange.MINIMIZE_CONTROL';
      case minimizeStates:
        return 'ObjectiveFcn.Lagrange.MINIMIZE_STATE';
    }
  }

  @override
  List<PenaltyArgument> get mandatoryArguments {
    switch (this) {
      case minimizeControls:
        return [
          const PenaltyArgument(
              name: 'key', dataType: PenaltyArgumentType.string),
        ];
      case minimizeStates:
        return [
          const PenaltyArgument(
              name: 'key', dataType: PenaltyArgumentType.string),
        ];
    }
  }
}

enum MayerFcn implements ObjectiveFcn {
  minimizeTime;

  @override
  List<PenaltyFcn> get fcnValues {
    final out = <ObjectiveFcn>[];
    for (final obj in LagrangeFcn.values) {
      out.add(obj);
    }
    for (final obj in MayerFcn.values) {
      out.add(obj);
    }
    return out;
  }

  @override
  String get penaltyTypeToString => 'Mayer';

  @override
  String get penaltyType => 'Objective';

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
  List<PenaltyArgument> get mandatoryArguments {
    switch (this) {
      case minimizeTime:
        return [];
    }
  }
}

enum ConstraintFcn implements PenaltyFcn {
  timeConstraint;

  @override
  List<PenaltyFcn> get fcnValues {
    return ConstraintFcn.values;
  }

  @override
  String get penaltyTypeToString => 'Constraint';

  @override
  String get penaltyType => 'Constraint';

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
  List<PenaltyArgument> get mandatoryArguments {
    switch (this) {
      case timeConstraint:
        return [];
    }
  }
}

abstract class Penalty {
  final PenaltyFcn fcn;
  final Map<String, dynamic> arguments;

  final Nodes nodes;

  String argumentToPythonString(String key) {
    final argument = arguments[key];
    if (argument == null) throw 'The key $key is not in the argument list';

    switch (argument.runtimeType) {
      case String:
        return '$key="$argument"';
      default:
        throw 'The type ${argument.runtimeType} is not supported.\n'
            'Please contact the developpers for more assistance';
    }
  }

  Penalty(this.fcn, {required this.nodes, required this.arguments}) {
    final argumentNames = fcn.mandatoryArguments.map((e) => e.name);

    // Do not allow non mandatory arguments
    for (final argument in arguments.keys) {
      if (!argumentNames.contains(argument)) {
        throw 'The ${fcn.penaltyType} $fcn requires $argument';
      }
    }

    // Initialize if not all mandatory arguments are present
    for (final name in argumentNames) {
      if (!arguments.containsKey(name)) {
        arguments[name] = null;
      }
    }
  }
}

class Objective extends Penalty {
  double weight;
  Objective.generic(
      {ObjectiveFcn fcn = LagrangeFcn.minimizeControls,
      super.nodes = Nodes.all,
      this.weight = 1,
      Map<String, dynamic>? arguments})
      : super(fcn, arguments: arguments ?? {});

  Objective.lagrange(LagrangeFcn fcn,
      {super.nodes = Nodes.all,
      this.weight = 1,
      Map<String, dynamic>? arguments})
      : super(fcn, arguments: arguments ?? {});
  Objective.mayer(MayerFcn fcn,
      {super.nodes = Nodes.all,
      this.weight = 1,
      Map<String, dynamic>? arguments})
      : super(fcn, arguments: arguments ?? {});
}

class Constraint extends Penalty {
  Constraint(ConstraintFcn fcn,
      {super.nodes = Nodes.end, Map<String, dynamic>? arguments})
      : super(fcn, arguments: arguments ?? {});
}
