import 'package:bioptim_gui/models/objective_type.dart';
import 'package:bioptim_gui/models/minimize_maximize.dart';
import 'package:bioptim_gui/models/nodes.dart';
import 'package:bioptim_gui/models/quadrature_rules.dart';

enum PenaltyArgumentType {
  integer,
  float,
  string,
  array,
  axis,
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
      case axis:
        return 'Axis';
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
      case axis:
        return RegExp(r'[XYZxyz]');
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

enum GenericFcn implements ObjectiveFcn {
  minimizeAngularMomentum,
  minimizeComPosition,
  minimizeComVelocity,
  minimizeLinearMomentum,
  minimizeControls,
  minimizePower,
  minimizeStates,
  minimizeMarkers,
  minimizeMarkersAcceleration,
  minimizeMarkersVelocity,
  minimizeSegmentRotation,
  minimizeSegmentVelocity,
  proportionalControl,
  proportionalState,
  superimposeMarkers,
  trackMarkerWithSegmentAxis,
  trackSegmentWithCustomRT,
  trackVectorOrientationsFromMarkers,
  minimizeTime,
  minimizeQDot,
  ;

  @override
  List<PenaltyFcn> get fcnValues {
    final out = <ObjectiveFcn>[];
    for (final obj in values) {
      out.add(obj);
    }
    return out;
  }

  @override
  String get penaltyTypeToString => 'Generic';

  @override
  String get penaltyType => 'Objective';

  @override
  String toPythonString() {
    return 'GenericFcn.toPythonString shoudn\'t be called';
  }

  @override
  List<PenaltyArgument> get mandatoryArguments {
    return [];
  }

  @override
  String toString() {
    switch (this) {
      case minimizeAngularMomentum:
        return 'Optimize angular momentum';
      case minimizeComPosition:
        return 'Optimize CoM position';
      case minimizeComVelocity:
        return 'Optimize CoM velocity';
      case minimizeLinearMomentum:
        return 'Optimize linear momentum';
      case minimizeControls:
        return 'Optimize controls';
      case minimizePower:
        return 'Optimize power';
      case minimizeStates:
        return 'Optimize states';
      case minimizeMarkers:
        return 'Optimize markers';
      case minimizeMarkersAcceleration:
        return 'Optimize markers acceleration';
      case minimizeMarkersVelocity:
        return 'Optimize markers velocity';
      case minimizeSegmentRotation:
        return 'Optimize segment rotation';
      case minimizeSegmentVelocity:
        return 'Optimize segment velocity';
      case proportionalControl:
        return 'Proportional control';
      case proportionalState:
        return 'Proportional state';
      case superimposeMarkers:
        return 'Marker distance';
      case trackMarkerWithSegmentAxis:
        return 'Track marker with segment axis';
      case trackSegmentWithCustomRT:
        return 'Track segment with custom RT';
      case trackVectorOrientationsFromMarkers:
        return 'Track vector orientations from markers';
      case minimizeQDot:
        return 'Optimize qdot';
      case minimizeTime:
        return 'Optimize time';
    }
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
          const PenaltyArgument(
              name: 'axis', dataType: PenaltyArgumentType.axis),
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
          const PenaltyArgument(
              name: 'axis', dataType: PenaltyArgumentType.axis),
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
  timeConstraint,
  continuity,
  ;

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
      case ConstraintFcn.continuity:
        return 'Continuity';
    }
  }

  @override
  String toPythonString() {
    switch (this) {
      case timeConstraint:
        return 'ConstraintFcn.TIME_CONSTRAINT';
      case ConstraintFcn.continuity:
        return 'ConstraintFcn.CONTINUITY';
    }
  }

  @override
  List<PenaltyArgument> get mandatoryArguments {
    switch (this) {
      case timeConstraint || continuity:
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
          case PenaltyArgumentType.axis:
            return '$key=Axis.${argument.toUpperCase()}';
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
  ObjectiveType objectiveType;
  GenericFcn genericFcn;

  Objective.generic(
      {ObjectiveFcn fcn = LagrangeFcn.minimizeControls,
      super.nodes = Nodes.all,
      super.quadratureRules = QuadratureRules.rectangleLeft,
      super.quadratic = true,
      super.expand = true,
      super.target = 'None',
      super.derivative = false,
      super.multiThread = false,
      this.weight = 1,
      this.minimizeOrMaximize = MinMax.minimize,
      this.objectiveType = ObjectiveType.lagrange,
      this.genericFcn = GenericFcn.minimizeControls,
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
      super.multiThread = false,
      this.weight = 100,
      this.minimizeOrMaximize = MinMax.minimize,
      this.objectiveType = ObjectiveType.lagrange,
      this.genericFcn = GenericFcn.minimizeControls,
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
      super.multiThread = false,
      this.weight = 1,
      this.minimizeOrMaximize = MinMax.minimize,
      this.objectiveType = ObjectiveType.mayer,
      this.genericFcn = GenericFcn.minimizeTime,
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
      super.multiThread = false,
      this.weight = 1,
      this.minimizeOrMaximize = MinMax.minimize,
      this.objectiveType = ObjectiveType.lagrange,
      this.genericFcn = GenericFcn.minimizeControls,
      Map<String, dynamic>? arguments})
      : super(fcn, arguments: arguments ?? {});

  Objective.mayer(MayerFcn fcn,
      {super.nodes = Nodes.end,
      super.quadratureRules = QuadratureRules.rectangleLeft,
      super.quadratic = true,
      super.expand = true,
      super.target = 'None',
      super.derivative = false,
      super.multiThread = false,
      this.weight = 1,
      this.minimizeOrMaximize = MinMax.minimize,
      this.objectiveType = ObjectiveType.mayer,
      this.genericFcn = GenericFcn.minimizeControls,
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
      super.multiThread = false,
      Map<String, dynamic>? arguments})
      : super(fcn, arguments: arguments ?? {});
}

ObjectiveFcn? genericFcn2ObjectiveFcn(
    GenericFcn genericFcn, ObjectiveType objectiveType) {
  if (objectiveType == ObjectiveType.mayer) {
    switch (genericFcn) {
      case GenericFcn.minimizeAngularMomentum:
        return MayerFcn.minimizeAngularMomentum;
      case GenericFcn.minimizeComPosition:
        return MayerFcn.minimizeComPosition;
      case GenericFcn.minimizeComVelocity:
        return MayerFcn.minimizeComVelocity;
      case GenericFcn.minimizeLinearMomentum:
        return MayerFcn.minimizeLinearMomentum;
      case GenericFcn.minimizeControls:
        return MayerFcn.minimizeControls;
      case GenericFcn.minimizePower:
        return MayerFcn.minimizePower;
      case GenericFcn.minimizeStates:
        return MayerFcn.minimizeStates;
      case GenericFcn.minimizeMarkers:
        return MayerFcn.minimizeMarkers;
      case GenericFcn.minimizeMarkersAcceleration:
        return MayerFcn.minimizeMarkersAcceleration;
      case GenericFcn.minimizeMarkersVelocity:
        return MayerFcn.minimizeMarkersVelocity;
      case GenericFcn.minimizeSegmentRotation:
        return MayerFcn.minimizeSegmentRotation;
      case GenericFcn.minimizeSegmentVelocity:
        return MayerFcn.minimizeSegmentVelocity;
      case GenericFcn.proportionalControl:
        return MayerFcn.proportionalControl;
      case GenericFcn.proportionalState:
        return MayerFcn.proportionalState;
      case GenericFcn.superimposeMarkers:
        return MayerFcn.superimposeMarkers;
      case GenericFcn.trackMarkerWithSegmentAxis:
        return MayerFcn.trackMarkerWithSegmentAxis;
      case GenericFcn.trackSegmentWithCustomRT:
        return MayerFcn.trackSegmentWithCustomRT;
      case GenericFcn.trackVectorOrientationsFromMarkers:
        return MayerFcn.trackVectorOrientationsFromMarkers;
      case GenericFcn.minimizeQDot:
        return MayerFcn.minimizeQDot;
      case GenericFcn.minimizeTime:
        return MayerFcn.minimizeTime;
    }
  } else if (objectiveType == ObjectiveType.lagrange) {
    switch (genericFcn) {
      case GenericFcn.minimizeAngularMomentum:
        return LagrangeFcn.minimizeAngularMomentum;
      case GenericFcn.minimizeComPosition:
        return LagrangeFcn.minimizeComPosition;
      case GenericFcn.minimizeComVelocity:
        return LagrangeFcn.minimizeComVelocity;
      case GenericFcn.minimizeLinearMomentum:
        return LagrangeFcn.minimizeLinearMomentum;
      case GenericFcn.minimizeControls:
        return LagrangeFcn.minimizeControls;
      case GenericFcn.minimizePower:
        return LagrangeFcn.minimizePower;
      case GenericFcn.minimizeStates:
        return LagrangeFcn.minimizeStates;
      case GenericFcn.minimizeMarkers:
        return LagrangeFcn.minimizeMarkers;
      case GenericFcn.minimizeMarkersAcceleration:
        return LagrangeFcn.minimizeMarkersAcceleration;
      case GenericFcn.minimizeMarkersVelocity:
        return LagrangeFcn.minimizeMarkersVelocity;
      case GenericFcn.minimizeSegmentRotation:
        return LagrangeFcn.minimizeSegmentRotation;
      case GenericFcn.minimizeSegmentVelocity:
        return LagrangeFcn.minimizeSegmentVelocity;
      case GenericFcn.proportionalControl:
        return LagrangeFcn.proportionalControl;
      case GenericFcn.proportionalState:
        return LagrangeFcn.proportionalState;
      case GenericFcn.superimposeMarkers:
        return LagrangeFcn.superimposeMarkers;
      case GenericFcn.trackMarkerWithSegmentAxis:
        return LagrangeFcn.trackMarkerWithSegmentAxis;
      case GenericFcn.trackSegmentWithCustomRT:
        return LagrangeFcn.trackSegmentWithCustomRT;
      case GenericFcn.trackVectorOrientationsFromMarkers:
        return LagrangeFcn.trackVectorOrientationsFromMarkers;
      case GenericFcn.minimizeQDot:
        return LagrangeFcn.minimizeQDot;
      case GenericFcn.minimizeTime:
        return LagrangeFcn.minimizeTime;
    }
  }
  return null;
}

GenericFcn? objectiveFcn2GenericFcn(ObjectiveFcn objectiveFcn) {
  if (objectiveFcn.runtimeType == GenericFcn) return objectiveFcn as GenericFcn;

  if (objectiveFcn.runtimeType == LagrangeFcn) {
    switch (objectiveFcn as LagrangeFcn) {
      case LagrangeFcn.minimizeAngularMomentum:
        return GenericFcn.minimizeAngularMomentum;
      case LagrangeFcn.minimizeComPosition:
        return GenericFcn.minimizeComPosition;
      case LagrangeFcn.minimizeComVelocity:
        return GenericFcn.minimizeComVelocity;
      case LagrangeFcn.minimizeLinearMomentum:
        return GenericFcn.minimizeLinearMomentum;
      case LagrangeFcn.minimizeControls:
        return GenericFcn.minimizeControls;
      case LagrangeFcn.minimizePower:
        return GenericFcn.minimizePower;
      case LagrangeFcn.minimizeStates:
        return GenericFcn.minimizeStates;
      case LagrangeFcn.minimizeMarkers:
        return GenericFcn.minimizeMarkers;
      case LagrangeFcn.minimizeMarkersAcceleration:
        return GenericFcn.minimizeMarkersAcceleration;
      case LagrangeFcn.minimizeMarkersVelocity:
        return GenericFcn.minimizeMarkersVelocity;
      case LagrangeFcn.minimizeSegmentRotation:
        return GenericFcn.minimizeSegmentRotation;
      case LagrangeFcn.minimizeSegmentVelocity:
        return GenericFcn.minimizeSegmentVelocity;
      case LagrangeFcn.proportionalControl:
        return GenericFcn.proportionalControl;
      case LagrangeFcn.proportionalState:
        return GenericFcn.proportionalState;
      case LagrangeFcn.superimposeMarkers:
        return GenericFcn.superimposeMarkers;
      case LagrangeFcn.trackMarkerWithSegmentAxis:
        return GenericFcn.trackMarkerWithSegmentAxis;
      case LagrangeFcn.trackSegmentWithCustomRT:
        return GenericFcn.trackSegmentWithCustomRT;
      case LagrangeFcn.trackVectorOrientationsFromMarkers:
        return GenericFcn.trackVectorOrientationsFromMarkers;
      case LagrangeFcn.minimizeQDot:
        return GenericFcn.minimizeQDot;
      case LagrangeFcn.minimizeTime:
        return GenericFcn.minimizeTime;
    }
  } else {
    if (objectiveFcn.runtimeType == MayerFcn) {
      switch (objectiveFcn as MayerFcn) {
        case MayerFcn.minimizeAngularMomentum:
          return GenericFcn.minimizeAngularMomentum;
        case MayerFcn.minimizeComPosition:
          return GenericFcn.minimizeComPosition;
        case MayerFcn.minimizeComVelocity:
          return GenericFcn.minimizeComVelocity;
        case MayerFcn.minimizeLinearMomentum:
          return GenericFcn.minimizeLinearMomentum;
        case MayerFcn.minimizeControls:
          return GenericFcn.minimizeControls;
        case MayerFcn.minimizePower:
          return GenericFcn.minimizePower;
        case MayerFcn.minimizeStates:
          return GenericFcn.minimizeStates;
        case MayerFcn.minimizeMarkers:
          return GenericFcn.minimizeMarkers;
        case MayerFcn.minimizeMarkersAcceleration:
          return GenericFcn.minimizeMarkersAcceleration;
        case MayerFcn.minimizeMarkersVelocity:
          return GenericFcn.minimizeMarkersVelocity;
        case MayerFcn.minimizeSegmentRotation:
          return GenericFcn.minimizeSegmentRotation;
        case MayerFcn.minimizeSegmentVelocity:
          return GenericFcn.minimizeSegmentVelocity;
        case MayerFcn.proportionalControl:
          return GenericFcn.proportionalControl;
        case MayerFcn.proportionalState:
          return GenericFcn.proportionalState;
        case MayerFcn.superimposeMarkers:
          return GenericFcn.superimposeMarkers;
        case MayerFcn.trackMarkerWithSegmentAxis:
          return GenericFcn.trackMarkerWithSegmentAxis;
        case MayerFcn.trackSegmentWithCustomRT:
          return GenericFcn.trackSegmentWithCustomRT;
        case MayerFcn.trackVectorOrientationsFromMarkers:
          return GenericFcn.trackVectorOrientationsFromMarkers;
        case MayerFcn.minimizeQDot:
          return GenericFcn.minimizeQDot;
        case MayerFcn.minimizeTime:
          return GenericFcn.minimizeTime;
      }
    }
  }
  return null;
}
