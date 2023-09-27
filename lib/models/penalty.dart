import 'package:bioptim_gui/models/nodes.dart';
import 'package:bioptim_gui/models/quadrature_rules.dart';
import 'package:bioptim_gui/widgets/maximize_minimize_radio.dart';

enum PenaltyArgumentType {
  integer,
  float,
  string,
  array,
  ;

  @override
  String toString() {
    switch (this) {
      case integer:
        return 'Integer';
      case float:
        return 'Float';
      case string:
        return 'String';
      case array:
        return 'Array';
    }
  }

  RegExp get regexpValidator {
    switch (this) {
      case integer:
        return RegExp(r'[0-9]');
      case float:
        return RegExp(r'[0-9\.]');
      case string:
        return RegExp(r'[a-zA-Z0-9]');
      case array:
        return RegExp(r'[0-9\.,]');
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
  // regroup the objectives by arguments, then alphabetical order
  // (argument_name:type[ | type ][ =default_value ])

  // axes:tuple|list=None
  minimizeAngularMomentum,
  minimizeComPosition,
  minimizeComVelocity,
  minimizeLinearMomentum,

  // key:str
  minimizeControls,
  minimizePower,
  minimizeStates,

  // marker_index:tuple|list|int|str=None
  // axes:tuple|list=None
  // reference_jcs:str|int=None
  minimizeMarkers,
  minimizeMarkersAcceleration,
  minimizeMarkersVelocity,

  // segment:int|str
  // axes:tuple|list=None
  minimizeSegmentRotation,
  minimizeSegmentVelocity,

  // key:str
  // first_dof:int
  // second_dof:int
  // coef:float
  // first_dof_intercept:foat=0
  // second_dof_intercept:float=0
  proportionalControl,
  proportionalState,

  // first_marker:str|int
  // second_marker:str|int
  // axes:tuple|list=None
  superimposeMarkers,

  // marker:int|str
  // segment:int|str
  // axis:Axis
  trackMarkerWithSegmentAxis,

  // segment:int|str
  // rt:int
  trackSegmentWithCustomRT,

  // vector_0_marker_0:int|str
  // vector_0_marker_1:int|str
  // vector_1_marker_0:int|str
  // vector_1_marker_1:int|str
  trackVectorOrientationsFromMarkers,

  //
  minimizeQDot,
  minimizeTime,
  ;

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
      case minimizeAngularMomentum:
        return 'Minimize angular momentum';
      case minimizeComPosition:
        return 'Minimize CoM position';
      case minimizeComVelocity:
        return 'Minimize CoM velocity';
      case minimizeLinearMomentum:
        return 'Minimize linear momentum';
      case minimizeControls:
        return 'Minimize controls';
      case minimizePower:
        return 'Minimize power';
      case minimizeStates:
        return 'Minimize states';
      case minimizeMarkers:
        return 'Minimize markers';
      case minimizeMarkersAcceleration:
        return 'Minimize markers acceleration';
      case minimizeMarkersVelocity:
        return 'Minimize markers velocity';
      case minimizeSegmentRotation:
        return 'Minimize segment rotation';
      case minimizeSegmentVelocity:
        return 'Minimize segment velocity';
      case proportionalControl:
        return 'Proportional control';
      case proportionalState:
        return 'Proportional state';
      case superimposeMarkers:
        return 'Superimpose markers';
      case trackMarkerWithSegmentAxis:
        return 'Track marker with segment axis';
      case trackSegmentWithCustomRT:
        return 'Track segment with custom RT';
      case trackVectorOrientationsFromMarkers:
        return 'Track vector orientations from markers';
      case minimizeQDot:
        return 'Minimize qdot';
      case minimizeTime:
        return 'Minimize time';
    }
  }

  @override
  String toPythonString() {
    switch (this) {
      case minimizeAngularMomentum:
        return 'ObjectiveFcn.Lagrange.MINIMIZE_ANGULAR_MOMENTUM';
      case minimizeComPosition:
        return 'ObjectiveFcn.Lagrange.MINIMIZE_COM_POSITION';
      case minimizeComVelocity:
        return 'ObjectiveFcn.Lagrange.MINIMIZE_COM_VELOCITY';
      case minimizeLinearMomentum:
        return 'ObjectiveFcn.Lagrange.MINIMIZE_LINEAR_MOMENTUM';
      case minimizeControls:
        return 'ObjectiveFcn.Lagrange.MINIMIZE_CONTROL';
      case minimizePower:
        return 'ObjectiveFcn.Lagrange.MINIMIZE_POWER';
      case minimizeStates:
        return 'ObjectiveFcn.Lagrange.MINIMIZE_STATES';
      case minimizeMarkers:
        return 'ObjectiveFcn.Lagrange.MINIMIZE_MARKERS';
      case minimizeMarkersAcceleration:
        return 'ObjectiveFcn.Lagrange.MINIMIZE_MARKERS_ACCELERATION';
      case minimizeMarkersVelocity:
        return 'ObjectiveFcn.Lagrange.MINIMIZE_MARKERS_VELOCITY';
      case minimizeSegmentRotation:
        return 'ObjectiveFcn.Lagrange.MINIMIZE_SEGMENT_ROTATION';
      case minimizeSegmentVelocity:
        return 'ObjectiveFcn.Lagrange.MINIMIZE_SEGMENT_VELOCITY';
      case proportionalControl:
        return 'ObjectiveFcn.Lagrange.PROPORTIONAL_CONTROL';
      case proportionalState:
        return 'ObjectiveFcn.Lagrange.PROPORTIONAL_STATE';
      case superimposeMarkers:
        return 'ObjectiveFcn.Lagrange.SUPERIMPOSE_MARKERS';
      case trackMarkerWithSegmentAxis:
        return 'ObjectiveFcn.Lagrange.TRACK_MARKER_WITH_SEGMENT_AXIS';
      case trackSegmentWithCustomRT:
        return 'ObjectiveFcn.Lagrange.TRACK_SEGMENT_WITH_CUSTOM_RT';
      case trackVectorOrientationsFromMarkers:
        return 'ObjectiveFcn.Lagrange.TRACK_VECTOR_ORIENTATIONS_FROM_MARKERS';
      case minimizeQDot:
        return 'ObjectiveFcn.Lagrange.MINIMIZE_QDOT';
      case minimizeTime:
        return 'ObjectiveFcn.Lagrange.MINIMIZE_TIME';
    }
  }

  @override
  List<PenaltyArgument> get mandatoryArguments {
    switch (this) {
      // the arguments that can be multiple are set to string for now

      // axes:tuple|list=None
      case minimizeAngularMomentum ||
            minimizeComPosition ||
            minimizeComVelocity ||
            minimizeLinearMomentum:
        return [
          const PenaltyArgument(
              name: 'axes', dataType: PenaltyArgumentType.array),
        ];

      // key:str
      case minimizeControls || minimizePower || minimizeStates:
        return [
          const PenaltyArgument(
              name: 'key', dataType: PenaltyArgumentType.string),
        ];

      // marker_index:tuple|list|int|str=None
      // axes:tuple|list=None
      // reference_jcs:str|int=None
      case minimizeMarkers ||
            minimizeMarkersAcceleration ||
            minimizeMarkersVelocity:
        return [
          const PenaltyArgument(
              name: 'marker_index', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'axes', dataType: PenaltyArgumentType.array),
          const PenaltyArgument(
              name: 'reference_jcs', dataType: PenaltyArgumentType.string),
        ];

      // segment:int|str
      // axes:tuple|list=None
      case minimizeSegmentRotation || minimizeSegmentVelocity:
        return [
          const PenaltyArgument(
              name: 'segment', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'axes', dataType: PenaltyArgumentType.array),
        ];

      // key:str
      // first_dof:int
      // second_dof:int
      // coef:float
      // first_dof_intercept:foat=0
      // second_dof_intercept:float=0
      case proportionalControl || proportionalState:
        return [
          const PenaltyArgument(
              name: 'key', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'first_dof', dataType: PenaltyArgumentType.integer),
          const PenaltyArgument(
              name: 'second_dof', dataType: PenaltyArgumentType.integer),
          const PenaltyArgument(
              name: 'coef', dataType: PenaltyArgumentType.float),
          const PenaltyArgument(
              name: 'first_dof_intercept', dataType: PenaltyArgumentType.float),
          const PenaltyArgument(
              name: 'second_dof_intercept',
              dataType: PenaltyArgumentType.float),
        ];

      // first_marker:str|int
      // second_marker:str|int
      // axes:tuple|list=None
      case superimposeMarkers:
        return [
          const PenaltyArgument(
              name: 'first_marker', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'second_marker', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'axes', dataType: PenaltyArgumentType.array),
        ];

      // marker:int|str
      // segment:int|str
      // axis:Axis
      case trackMarkerWithSegmentAxis:
        return [
          const PenaltyArgument(
              name: 'marker', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'segment', dataType: PenaltyArgumentType.string),
          // TODO implement argument
          // const PenaltyArgument(
          //    name: 'axis', dataType: PenaltyArgumentType.string),
        ];

      // segment:int|str
      // rt:int
      case trackSegmentWithCustomRT:
        return [
          const PenaltyArgument(
              name: 'segment', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'rt', dataType: PenaltyArgumentType.integer),
        ];

      // vector_0_marker_0:int|str
      // vector_0_marker_1:int|str
      // vector_1_marker_0:int|str
      // vector_1_marker_1:int|str
      case trackVectorOrientationsFromMarkers:
        return [
          const PenaltyArgument(
              name: 'vector_0_marker_0', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'vector_0_marker_1', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'vector_1_marker_0', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'vector_1_marker_1', dataType: PenaltyArgumentType.string),
        ];

      //
      case minimizeQDot || minimizeTime:
        return [];
    }
  }
}

enum MayerFcn implements ObjectiveFcn {
  // regroup the objectives by arguments, then alphabetical order
  // (argument_name:type[ | type ][ =default_value ])

  // axes:tuple|list=None
  minimizeAngularMomentum,
  minimizeComPosition,
  minimizeComVelocity,
  minimizeLinearMomentum,

  // key:str
  minimizeControls,
  minimizePower,
  minimizeStates,

  // marker_index:tuple|list|int|str=None
  // axes:tuple|list=None
  // reference_jcs:str|int=None
  minimizeMarkers,
  minimizeMarkersAcceleration,
  minimizeMarkersVelocity,

  // segment:int|str
  // axes:tuple|list=None
  minimizeSegmentRotation,
  minimizeSegmentVelocity,

  // key:str
  // first_dof:int
  // second_dof:int
  // coef:float
  // first_dof_intercept:foat=0
  // second_dof_intercept:float=0
  proportionalControl,
  proportionalState,

  // first_marker:str|int
  // second_marker:str|int
  // axes:tuple|list=None
  superimposeMarkers,

  // marker:int|str
  // segment:int|str
  // axis:Axis
  trackMarkerWithSegmentAxis,

  // segment:int|str
  // rt:int
  trackSegmentWithCustomRT,

  // vector_0_marker_0:int|str
  // vector_0_marker_1:int|str
  // vector_1_marker_0:int|str
  // vector_1_marker_1:int|str
  trackVectorOrientationsFromMarkers,

  // min_bound:float=None
  // max_bound:float=None
  minimizeTime,

  //
  minimizeQDot,
  ;

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
      case minimizeAngularMomentum:
        return 'Minimize angular momentum';
      case minimizeComPosition:
        return 'Minimize CoM position';
      case minimizeComVelocity:
        return 'Minimize CoM velocity';
      case minimizeLinearMomentum:
        return 'Minimize linear momentum';
      case minimizeControls:
        return 'Minimize controls';
      case minimizePower:
        return 'Minimize power';
      case minimizeStates:
        return 'Minimize states';
      case minimizeMarkers:
        return 'Minimize markers';
      case minimizeMarkersAcceleration:
        return 'Minimize markers acceleration';
      case minimizeMarkersVelocity:
        return 'Minimize markers velocity';
      case minimizeSegmentRotation:
        return 'Minimize segment rotation';
      case minimizeSegmentVelocity:
        return 'Minimize segment velocity';
      case proportionalControl:
        return 'Proportional control';
      case proportionalState:
        return 'Proportional state';
      case superimposeMarkers:
        return 'Superimpose markers';
      case trackMarkerWithSegmentAxis:
        return 'Track marker with segment axis';
      case trackSegmentWithCustomRT:
        return 'Track segment with custom RT';
      case trackVectorOrientationsFromMarkers:
        return 'Track vector orientations from markers';
      case minimizeQDot:
        return 'Minimize qdot';
      case minimizeTime:
        return 'Minimize time';
    }
  }

  @override
  String toPythonString() {
    switch (this) {
      case minimizeAngularMomentum:
        return 'ObjectiveFcn.Mayer.MINIMIZE_ANGULAR_MOMENTUM';
      case minimizeComPosition:
        return 'ObjectiveFcn.Mayer.MINIMIZE_COM_POSITION';
      case minimizeComVelocity:
        return 'ObjectiveFcn.Mayer.MINIMIZE_COM_VELOCITY';
      case minimizeLinearMomentum:
        return 'ObjectiveFcn.Mayer.MINIMIZE_LINEAR_MOMENTUM';
      case minimizeControls:
        return 'ObjectiveFcn.Mayer.MINIMIZE_CONTROL';
      case minimizePower:
        return 'ObjectiveFcn.Mayer.MINIMIZE_POWER';
      case minimizeStates:
        return 'ObjectiveFcn.Mayer.MINIMIZE_STATES';
      case minimizeMarkers:
        return 'ObjectiveFcn.Mayer.MINIMIZE_MARKERS';
      case minimizeMarkersAcceleration:
        return 'ObjectiveFcn.Mayer.MINIMIZE_MARKERS_ACCELERATION';
      case minimizeMarkersVelocity:
        return 'ObjectiveFcn.Mayer.MINIMIZE_MARKERS_VELOCITY';
      case minimizeSegmentRotation:
        return 'ObjectiveFcn.Mayer.MINIMIZE_SEGMENT_ROTATION';
      case minimizeSegmentVelocity:
        return 'ObjectiveFcn.Mayer.MINIMIZE_SEGMENT_VELOCITY';
      case proportionalControl:
        return 'ObjectiveFcn.Mayer.PROPORTIONAL_CONTROL';
      case proportionalState:
        return 'ObjectiveFcn.Mayer.PROPORTIONAL_STATE';
      case superimposeMarkers:
        return 'ObjectiveFcn.Mayer.SUPERIMPOSE_MARKERS';
      case trackMarkerWithSegmentAxis:
        return 'ObjectiveFcn.Mayer.TRACK_MARKER_WITH_SEGMENT_AXIS';
      case trackSegmentWithCustomRT:
        return 'ObjectiveFcn.Mayer.TRACK_SEGMENT_WITH_CUSTOM_RT';
      case trackVectorOrientationsFromMarkers:
        return 'ObjectiveFcn.Mayer.TRACK_VECTOR_ORIENTATIONS_FROM_MARKERS';
      case minimizeQDot:
        return 'ObjectiveFcn.Mayer.MINIMIZE_QDOT';
      case minimizeTime:
        return 'ObjectiveFcn.Mayer.MINIMIZE_TIME';
    }
  }

  @override
  List<PenaltyArgument> get mandatoryArguments {
    switch (this) {
      // axes:tuple|list=None
      case minimizeAngularMomentum ||
            minimizeComPosition ||
            minimizeComVelocity ||
            minimizeLinearMomentum:
        return [
          const PenaltyArgument(
              name: 'axes', dataType: PenaltyArgumentType.array),
        ];

      // key:str
      case minimizeControls || minimizePower || minimizeStates:
        return [
          const PenaltyArgument(
              name: 'key', dataType: PenaltyArgumentType.string),
        ];

      // marker_index:tuple|list|int|str=None
      // axes:tuple|list=None
      // reference_jcs:str|int=None
      case minimizeMarkers ||
            minimizeMarkersAcceleration ||
            minimizeMarkersVelocity:
        return [
          // TODO adapt argument type, set to string for now
          const PenaltyArgument(
              name: 'marker_index', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'axes', dataType: PenaltyArgumentType.array),
          const PenaltyArgument(
              name: 'reference_jcs', dataType: PenaltyArgumentType.string),
        ];

      // segment:int|str
      // axes:tuple|list=None
      case minimizeSegmentRotation || minimizeSegmentVelocity:
        return [
          const PenaltyArgument(
              name: 'segment', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'axes', dataType: PenaltyArgumentType.array),
        ];

      // key:str
      // first_dof:int
      // second_dof:int
      // coef:float
      // first_dof_intercept:foat=0
      // second_dof_intercept:float=0
      case proportionalControl || proportionalState:
        return [
          const PenaltyArgument(
              name: 'key', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'first_dof', dataType: PenaltyArgumentType.integer),
          const PenaltyArgument(
              name: 'second_dof', dataType: PenaltyArgumentType.integer),
          const PenaltyArgument(
              name: 'coef', dataType: PenaltyArgumentType.float),
          const PenaltyArgument(
              name: 'first_dof_intercept', dataType: PenaltyArgumentType.float),
          const PenaltyArgument(
              name: 'second_dof_intercept',
              dataType: PenaltyArgumentType.float),
        ];

      // first_marker:str|int
      // second_marker:str|int
      // axes:tuple|list=None
      case superimposeMarkers:
        return [
          const PenaltyArgument(
              name: 'first_marker', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'second_marker', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'axes', dataType: PenaltyArgumentType.array),
        ];

      // marker:int|str
      // segment:int|str
      // axis:Axis
      case trackMarkerWithSegmentAxis:
        return [
          const PenaltyArgument(
              name: 'marker', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'segment', dataType: PenaltyArgumentType.string),
          // TODO implement argument
          // const PenaltyArgument(
          //    name: 'axis', dataType: PenaltyArgumentType.string),
        ];

      // segment:int|str
      // rt:int
      case trackSegmentWithCustomRT:
        return [
          const PenaltyArgument(
              name: 'segment', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'rt', dataType: PenaltyArgumentType.integer),
        ];

      // vector_0_marker_0:int|str
      // vector_0_marker_1:int|str
      // vector_1_marker_0:int|str
      // vector_1_marker_1:int|str
      case trackVectorOrientationsFromMarkers:
        return [
          const PenaltyArgument(
              name: 'vector_0_marker_0', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'vector_0_marker_1', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'vector_1_marker_0', dataType: PenaltyArgumentType.string),
          const PenaltyArgument(
              name: 'vector_1_marker_1', dataType: PenaltyArgumentType.string),
        ];

      // min_bound:float=None
      // max_bound:float=None
      case minimizeTime:
        return [
          const PenaltyArgument(
              name: 'min_bound', dataType: PenaltyArgumentType.float),
          const PenaltyArgument(
              name: 'max_bound', dataType: PenaltyArgumentType.float),
        ];

      //
      case minimizeQDot:
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
  final bool quadratic;
  final bool expand;
  String target;
  final bool derivative;
  final bool explicitDerivative;
  final QuadratureRules quadratureRules;
  final bool multiThread;

  String argumentToPythonString(String key) {
    final argument = arguments[key] ?? 'to_be_specified';
    switch (argument.runtimeType) {
      case String:
        switch (fcn.mandatoryArguments
            .firstWhere((element) => element.name == key)
            .dataType) {
          case PenaltyArgumentType.array:
            return '$key=np.array([$argument])';
          default:
            return '$key="$argument"';
        }
      case double || int:
        return '$key=$argument';
      case bool:
        return argument ? '$key=True' : '$key=False';
      default:
        throw 'The type ${argument.runtimeType} is not supported.\n'
            'Please contact the developpers for more assistance';
    }
  }

  Penalty(this.fcn,
      {required this.nodes,
      required this.quadratic,
      required this.expand,
      required this.target,
      required this.derivative,
      required this.explicitDerivative,
      required this.multiThread,
      required this.quadratureRules,
      required this.arguments}) {
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
  MinMax minimizeOrMaximize;
  Objective.generic(
      {ObjectiveFcn fcn = LagrangeFcn.minimizeControls,
      super.nodes = Nodes.all,
      super.quadratureRules = QuadratureRules.rectangleLeft,
      super.quadratic = true,
      super.expand = true,
      super.target = 'None',
      super.derivative = false,
      super.explicitDerivative = false,
      super.multiThread = false,
      this.weight = 1,
      this.minimizeOrMaximize = MinMax.minimize,
      Map<String, dynamic>? arguments})
      : super(fcn, arguments: arguments ?? {});

  Objective.acrobaticGenericLagrangeMinimizeControls(
      {ObjectiveFcn fcn = LagrangeFcn.minimizeControls,
      super.nodes = Nodes.allShooting,
      super.quadratureRules = QuadratureRules.rectangleLeft,
      super.quadratic = true,
      super.expand = true,
      super.target = 'None',
      super.derivative = false,
      super.explicitDerivative = false,
      super.multiThread = false,
      this.weight = 100,
      this.minimizeOrMaximize = MinMax.minimize,
      Map<String, dynamic>? arguments})
      : super(fcn,
            arguments: arguments ??
                {
                  'key': 'tau',
                });

  Objective.acrobaticGenericMayerMinimizeTime(
      {ObjectiveFcn fcn = MayerFcn.minimizeTime,
      super.nodes = Nodes.end,
      super.quadratureRules = QuadratureRules.rectangleLeft,
      super.quadratic = true,
      super.expand = true,
      super.target = 'None',
      super.derivative = false,
      super.explicitDerivative = false,
      super.multiThread = false,
      this.weight = 1,
      this.minimizeOrMaximize = MinMax.minimize,
      Map<String, dynamic>? arguments,
      required double minBound,
      required double maxBound})
      : super(fcn,
            arguments: arguments ??
                {
                  'min_bound': minBound,
                  'max_bound': maxBound,
                });

  Objective.lagrange(LagrangeFcn fcn,
      {super.nodes = Nodes.allShooting,
      super.quadratureRules = QuadratureRules.rectangleLeft,
      super.quadratic = true,
      super.expand = true,
      super.target = 'None',
      super.derivative = false,
      super.explicitDerivative = false,
      super.multiThread = false,
      this.weight = 1,
      this.minimizeOrMaximize = MinMax.minimize,
      Map<String, dynamic>? arguments})
      : super(fcn, arguments: arguments ?? {});

  Objective.mayer(MayerFcn fcn,
      {super.nodes = Nodes.end,
      super.quadratureRules = QuadratureRules.rectangleLeft,
      super.quadratic = true,
      super.expand = true,
      super.target = 'None',
      super.derivative = false,
      super.explicitDerivative = false,
      super.multiThread = false,
      this.weight = 1,
      this.minimizeOrMaximize = MinMax.minimize,
      Map<String, dynamic>? arguments})
      : super(fcn, arguments: arguments ?? {});
}

class Constraint extends Penalty {
  Constraint.generic(
      {ConstraintFcn fcn = ConstraintFcn.timeConstraint,
      super.nodes = Nodes.end,
      super.quadratureRules = QuadratureRules.rectangleLeft,
      super.quadratic = true,
      super.expand = true,
      super.target = 'None',
      super.derivative = false,
      super.explicitDerivative = false,
      super.multiThread = false,
      Map<String, dynamic>? arguments})
      : super(fcn, arguments: arguments ?? {});
}
