import 'dart:math';

import 'package:bioptim_gui/models/bio_model.dart';
import 'package:bioptim_gui/models/dynamics.dart';
import 'package:bioptim_gui/models/optimal_control_program_type.dart';
import 'package:bioptim_gui/models/optimal_control_program.dart';
import 'package:bioptim_gui/models/optimization_variable.dart';
import 'package:flutter/material.dart';

///
/// This class mimics the strcture of the [OptimalControlProgram] class but in
/// a UI perspective. It creates all the required Controllers as well as it gets
/// or updates the values.
class OptimalControlProgramControllers {
  static final OptimalControlProgramControllers _instance =
      OptimalControlProgramControllers._internal();
  static OptimalControlProgramControllers get instance => _instance;
  OptimalControlProgramControllers._internal() {
    _updateAllControllers();
  }

  Function(String path) get exportScript => _ocp.exportScript;
  bool get mustExport => _ocp.mustExport;

  void dispose() {
    nbPhasesController.dispose();
    for (int i = 0; i < _nbPhasesMax; i++) {
      nbShootingPointsControllers[i].dispose();
      phaseDurationControllers[i].dispose();
    }
  }

  final _ocp = OptimalControlProgram();
  // This is to keep track of how many controllers we have because we don't
  // delete them if we reduce _nbPhases
  int _nbPhasesMax = 1;

  ///
  /// This callback can be used so the UI is updated on any change
  void Function()? _hasChanged;
  void registerToStatusChanged(Function() callback) {
    _hasChanged = callback;
    _updateAllControllers();
    if (_hasChanged != null) _hasChanged!();
  }

  ///
  /// All methods related to controlling the ocp type
  OptimalControlProgramType get ocpType => _ocp.ocpType;
  set ocpType(OptimalControlProgramType value) {
    _ocp.ocpType = value;
    if (_hasChanged != null) _hasChanged!();
  }

  ///
  /// All methods related to controlling the number of phases
  late final nbPhasesController = TextEditingController(text: '1')
    ..addListener(_nbPhasesControllerListener);
  int get nbPhases => _ocp.nbPhases;
  set nbPhases(int value) {
    _ocp.nbPhases = value;
    _nbPhasesMax = max(nbPhases, _nbPhasesMax);
    if (nbPhasesController.text != nbPhases.toString()) {
      // This if case is to ensure non recursive calls
      nbPhasesController.text = nbPhases.toString();
    }
    // Wait for one frame so the the UI is updated
    WidgetsBinding.instance.addPostFrameCallback((timeStamp) {
      _updateAllControllers();
      if (_hasChanged != null) _hasChanged!();
    });
  }

  void _nbPhasesControllerListener() {
    final tp = int.tryParse(nbPhasesController.text);
    if (tp == null || tp < 1 || tp == nbPhases) return;
    nbPhases = tp;
  }

  ///
  /// All the methods related to the dynamic model
  BioModel getBioModel({required int phaseIndex}) =>
      _ocp.getBioModel(phaseIndex: phaseIndex);
  void setBioModel(BioModel value, {required int phaseIndex}) {
    _ocp.setBioModel(value, phaseIndex: phaseIndex);
    if (_hasChanged != null) _hasChanged!();
  }

  ///
  /// All the methods related to the model path
  String getModelPath({required int phaseIndex}) =>
      _ocp.getModelPath(phaseIndex: phaseIndex);
  void setModelPath(String value, {required int phaseIndex}) {
    _ocp.setModelPath(value, phaseIndex: phaseIndex);
    if (_hasChanged != null) _hasChanged!();
  }

  ///
  /// All methods related to the number of shooting points
  final nbShootingPointsControllers = <TextEditingController>[];
  int getNbShootingPoints({required int phaseIndex}) =>
      _ocp.getNbShootingPoints(phaseIndex: phaseIndex);
  void setNbShootingPoints(int value, {required int phaseIndex}) {
    _ocp.setNbShootingPoints(value, phaseIndex: phaseIndex);
    if (_hasChanged != null) _hasChanged!();
  }

  List<String> get _nbShootingPointsInitialValues => [
        for (int i = 0; i < nbPhases; i++)
          getNbShootingPoints(phaseIndex: i).toString()
      ];
  void _nbShootingPointsListener(String value, {required int phaseIndex}) =>
      setNbShootingPoints(int.tryParse(value) ?? -1, phaseIndex: phaseIndex);

  ///
  /// All methods related to the phase duration
  final phaseDurationControllers = <TextEditingController>[];
  double getPhaseDuration({required int phaseIndex}) =>
      _ocp.getPhaseDuration(phaseIndex: phaseIndex);
  void setPhaseDuration(double value, {required int phaseIndex}) {
    _ocp.setPhaseDuration(value, phaseIndex: phaseIndex);
    if (_hasChanged != null) _hasChanged!();
  }

  List<String> get _phaseDurationInitialValues => [
        for (int i = 0; i < nbPhases; i++)
          getPhaseDuration(phaseIndex: i).toString()
      ];

  void _phaseDurationListener(String value, {required int phaseIndex}) =>
      setPhaseDuration(double.tryParse(value) ?? -1.0, phaseIndex: phaseIndex);

  ///
  /// All methods related to the dynamics equation
  Dynamics getDynamics({required int phaseIndex}) =>
      _ocp.getDynamics(phaseIndex: phaseIndex);
  void setDynamics(Dynamics value, {required int phaseIndex}) {
    // TODO add?  setVariables(value, phaseIndex: phaseIndex);
    _ocp.setDynamic(value, phaseIndex: phaseIndex);
    if (_hasChanged != null) _hasChanged!();
  }

  ///
  /// All methods related to the state and control variables
  final List<Map<String, _VariableTextEditingControllers>> _states = [];
  final List<Map<String, _VariableTextEditingControllers>> _controls = [];
  _VariableTextEditingControllers _variableController(
      {required String name,
      required OptimizationVariableType from,
      required int phaseIndex}) {
    switch (from) {
      case OptimizationVariableType.state:
        return _states[phaseIndex][name]!;
      case OptimizationVariableType.control:
        return _controls[phaseIndex][name]!;
    }
  }

  /// Warning, even though this allows to modify values, getVariable should
  /// NOT be used as such. That is because other functions must be called
  /// each time a variable is updated. Consider this [getVariable] interface
  /// as a readonly interface.
  OptimizationVariable getVariable(
          {required String name,
          required int phaseIndex,
          required OptimizationVariableType from}) =>
      _ocp.variable(name, from: from, phaseIndex: phaseIndex);

  List<String> getVariableNames(
          {required int phaseIndex, required OptimizationVariableType from}) =>
      _ocp.variableNames(from: from, phaseIndex: phaseIndex);

  TextEditingController getVariableNameController(
          {required String name,
          required int phaseIndex,
          required OptimizationVariableType from}) =>
      _variableController(name: name, from: from, phaseIndex: phaseIndex).name;

  TextEditingController getVariableDimensionController({
    required String name,
    required int phaseIndex,
    required OptimizationVariableType from,
  }) =>
      _variableController(name: name, from: from, phaseIndex: phaseIndex)
          .dimension;

  void setVariableDimension(
    int value, {
    required String name,
    required int phaseIndex,
    required OptimizationVariableType from,
  }) {
    _ocp.changeVariableDimension(value,
        name: name, from: from, phaseIndex: phaseIndex);
    if (_hasChanged != null) _hasChanged!();
  }

  void setVariableBoundsInterpolation(
    Interpolation value, {
    required String name,
    required int phaseIndex,
    required OptimizationVariableType from,
  }) {
    _ocp.changeVariableBoundsInterpolation(value,
        name: name, from: from, phaseIndex: phaseIndex);
    if (_hasChanged != null) _hasChanged!();
  }

  ///
  /// Here are the internal methods that ensures all the controllers are sane
  void _updateAllControllers() {
    _updateController(
      nbShootingPointsControllers,
      initialValue: _nbShootingPointsInitialValues,
      onChanged: _nbShootingPointsListener,
    );
    _updateController(
      phaseDurationControllers,
      initialValue: _phaseDurationInitialValues,
      onChanged: _phaseDurationListener,
    );

    _updateVariableController(
      _states,
      variableNames: ({required phaseIndex}) => getVariableNames(
          phaseIndex: phaseIndex, from: OptimizationVariableType.state),
      setDimension: (value, {required name, required phaseIndex}) =>
          setVariableDimension(value,
              name: name,
              phaseIndex: phaseIndex,
              from: OptimizationVariableType.state),
      getNumberOfBoundsColumns: ({required name, required phaseIndex}) =>
          getVariable(
                  name: name,
                  phaseIndex: phaseIndex,
                  from: OptimizationVariableType.state)
              .bounds
              .nbCols,
    );
    _updateVariableController(
      _controls,
      variableNames: ({required phaseIndex}) => getVariableNames(
          phaseIndex: phaseIndex, from: OptimizationVariableType.control),
      setDimension: (value, {required name, required phaseIndex}) =>
          setVariableDimension(value,
              name: name,
              phaseIndex: phaseIndex,
              from: OptimizationVariableType.control),
      getNumberOfBoundsColumns: ({required name, required phaseIndex}) =>
          getVariable(
                  name: name,
                  phaseIndex: phaseIndex,
                  from: OptimizationVariableType.control)
              .bounds
              .nbCols,
    );
  }

  void _updateController(List<TextEditingController> controllers,
      {required List<String> initialValue,
      required Function(String value, {required int phaseIndex}) onChanged}) {
    if (controllers.length < nbPhases) {
      for (int i = controllers.length; i < nbPhases; i++) {
        controllers.add(TextEditingController());
        controllers[i].text = initialValue[i];
        controllers[i]
            .addListener(() => onChanged(controllers[i].text, phaseIndex: i));
      }
    } else {
      // Do not change anything if we already have the right number of phases

      // Also we don't mind having to much controllers declared so keep the
      // previously declared if we removed controllers
    }
  }

  void _updateVariableController(
      List<Map<String, _VariableTextEditingControllers>> controllers,
      {required List<String> Function({required int phaseIndex}) variableNames,
      required Function(int value,
              {required String name, required int phaseIndex})
          setDimension,
      required int Function({required String name, required int phaseIndex})
          getNumberOfBoundsColumns}) {
    if (controllers.length < nbPhases) {
      // For each of the new phases, declare all the required variables
      for (int i = controllers.length; i < nbPhases; i++) {
        Map<String, _VariableTextEditingControllers> tp = {};
        for (final name in variableNames(phaseIndex: i)) {
          tp[name] = _VariableTextEditingControllers(name,
              setDimension: (value) =>
                  setDimension(value, name: name, phaseIndex: i),
              getNumberOfBoundsColumns: () =>
                  getNumberOfBoundsColumns(name: name, phaseIndex: i));
        }
        controllers.add(tp);
      }
    } else {
      // Do not change anything if we already have the right number of phases

      // Also we don't mind having to much controllers declared so keep the
      // previously declared if we removed controllers
    }
  }
}

class _VariableTextEditingControllers {
  // TODO Add the capability to automatically fill end phase continuity with starting of next phase
  final name = TextEditingController();
  final dimension = TextEditingController(text: '1');
  void Function(int value) setDimension;

  int Function() getNumberOfBoundsColumns;
  final bounds = <TextEditingController>[];

  _VariableTextEditingControllers(String name,
      {required this.setDimension, required this.getNumberOfBoundsColumns}) {
    this.name.text = name;
    _updateBounds(getNumberOfBoundsColumns());

    dimension.addListener(() {
      // The text field of dimension should only be positive integers
      final value = int.tryParse(dimension.text);
      if (value == null || value < 1) return;

      setDimension(value);
      _updateBounds(value * getNumberOfBoundsColumns());
    });
  }

  void _updateBounds(int length) {
    // We have to reset all the controllers since we don't know if the number of
    // dimension or column changed. This would make the textfield bouncing around
    // randomly.
    _disposeBounds();
    for (int i = 0; i < length; i++) {
      bounds.add(TextEditingController());
    }
  }

  void _disposeBounds() {
    for (final bound in bounds) {
      bound.dispose();
    }
    bounds.clear();
  }

  void dispose() {
    name.dispose();
    dimension.dispose();
    _disposeBounds();
  }
}
