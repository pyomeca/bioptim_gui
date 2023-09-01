import 'dart:math';

import 'package:bioptim_gui/models/bio_model.dart';
import 'package:bioptim_gui/models/dynamics.dart';
import 'package:bioptim_gui/models/matrix.dart';
import 'package:bioptim_gui/models/optimal_control_program_type.dart';
import 'package:bioptim_gui/models/optimal_control_program.dart';
import 'package:bioptim_gui/models/decision_variables.dart';
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

  final _ocp = OptimalControlProgram();
  // This is to keep track of how many controllers we have because we don't
  // delete them if we reduce _nbPhases
  int _nbPhasesMax = 1;

  ///
  /// This callback can be used so the UI is updated on any change
  void _notifyListeners() {
    if (_hasChanged != null) _hasChanged!();
    _ocp.notifyThatModelHasChanged();
  }

  void Function()? _hasChanged;
  void registerToStatusChanged(Function() callback) {
    _hasChanged = callback;
    _updateAllControllers();
    _notifyListeners();
  }

  ///
  /// All methods related to controlling the ocp type
  OptimalControlProgramType get ocpType => _ocp.generic.ocpType;
  void setOcpType(OptimalControlProgramType value) {
    _ocp.generic.ocpType = value;
    _notifyListeners();
  }

  ///
  /// All methods related to controlling the number of phases
  late final nbPhasesController = TextEditingController(text: '1')
    ..addListener(_nbPhasesControllerListener);
  int get nbPhases => _ocp.generic.nbPhases;
  void setNbPhases(int value) {
    _ocp.generic.nbPhases = value;
    _ocp.updatePhases();
    _nbPhasesMax = max(nbPhases, _nbPhasesMax);
    if (nbPhasesController.text != nbPhases.toString()) {
      // This if case is to ensure non recursive calls
      nbPhasesController.text = nbPhases.toString();
    }
    // Wait for one frame so the the UI is updated
    WidgetsBinding.instance.addPostFrameCallback((timeStamp) {
      _updateAllControllers();
      _notifyListeners();
    });
  }

  void _nbPhasesControllerListener() {
    final tp = int.tryParse(nbPhasesController.text);
    if (tp == null || tp < 1 || tp == nbPhases) return;
    setNbPhases(tp);
  }

  ///
  /// All the methods related to the dynamic model
  BioModel getBioModel({required int phaseIndex}) =>
      _ocp.phases[phaseIndex].bioModel;
  void setBioModel(BioModel value, {required int phaseIndex}) {
    _ocp.phases[phaseIndex].bioModel = value;
    _notifyListeners();
  }

  ///
  /// All the methods related to the model path
  String getModelPath({required int phaseIndex}) =>
      _ocp.phases[phaseIndex].modelPath;
  void setModelPath(String value, {required int phaseIndex}) {
    _ocp.phases[phaseIndex].modelPath = value;
    _notifyListeners();
  }

  ///
  /// All methods related to the number of shooting points
  final nbShootingPointsControllers = <TextEditingController>[];
  int getNbShootingPoints({required int phaseIndex}) =>
      _ocp.phases[phaseIndex].nbShootingPoints;
  void setNbShootingPoints(int value, {required int phaseIndex}) {
    _ocp.phases[phaseIndex].nbShootingPoints = value;
    _notifyListeners();
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
      _ocp.phases[phaseIndex].duration;
  void setPhaseDuration(double value, {required int phaseIndex}) {
    _ocp.phases[phaseIndex].duration = value;
    _notifyListeners();
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
      _ocp.phases[phaseIndex].dynamics;
  void setDynamics(Dynamics value, {required int phaseIndex}) {
    _ocp.phases[phaseIndex].dynamics = value;
    _ocp.resetVariables(phaseIndex: phaseIndex);

    for (final key in _states[phaseIndex].keys) {
      _states[phaseIndex][key]!.dispose();
    }
    _states[phaseIndex] = {};
    _createVariableControllers(_states[phaseIndex],
        from: DecisionVariableType.state, phaseIndex: phaseIndex);

    for (final key in _controls[phaseIndex].keys) {
      _controls[phaseIndex][key]!.dispose();
    }
    _controls[phaseIndex] = {};
    _createVariableControllers(_controls[phaseIndex],
        from: DecisionVariableType.control, phaseIndex: phaseIndex);

    _notifyListeners();
  }

  ///
  /// All methods related to the state and control variables
  final List<Map<String, _VariableTextEditingControllers>> _states = [];
  final List<Map<String, _VariableTextEditingControllers>> _controls = [];
  _VariableTextEditingControllers _variableController(
      {required String name,
      required DecisionVariableType from,
      required int phaseIndex}) {
    switch (from) {
      case DecisionVariableType.state:
        return _states[phaseIndex][name]!;
      case DecisionVariableType.control:
        return _controls[phaseIndex][name]!;
    }
  }

  /// Warning, even though this allows to modify values, getVariable should
  /// NOT be used as such. That is because other functions must be called
  /// each time a variable is updated. Consider this [getVariable] interface
  /// as a readonly interface.
  DecisionVariable getVariable(
          {required String name,
          required int phaseIndex,
          required DecisionVariableType from}) =>
      _ocp.variable(name, from: from, phaseIndex: phaseIndex);

  List<String> getVariableNames(
          {required int phaseIndex, required DecisionVariableType from}) =>
      _ocp.variables(from: from, phaseIndex: phaseIndex).names;

  TextEditingController getVariableNameController(
          {required String name,
          required int phaseIndex,
          required DecisionVariableType from}) =>
      _variableController(name: name, from: from, phaseIndex: phaseIndex).name;

  TextEditingController getVariableDimensionController({
    required String name,
    required int phaseIndex,
    required DecisionVariableType from,
  }) =>
      _variableController(name: name, from: from, phaseIndex: phaseIndex)
          .dimension;

  void setVariableDimension(
    int value, {
    required String name,
    required int phaseIndex,
    required DecisionVariableType from,
  }) {
    _ocp
        .variable(name, from: from, phaseIndex: phaseIndex)
        .changeDimension(value);
    _variableController(name: name, from: from, phaseIndex: phaseIndex)
        ._updateBounds();
    _variableController(name: name, from: from, phaseIndex: phaseIndex)
        ._updateInitialGuess();
    _notifyListeners();
  }

  Map<String, List<TextEditingController>> getVariableBoundsControllers({
    required String name,
    required int phaseIndex,
    required DecisionVariableType from,
  }) =>
      {
        'minBounds':
            _variableController(name: name, from: from, phaseIndex: phaseIndex)
                .minBounds,
        'maxBounds':
            _variableController(name: name, from: from, phaseIndex: phaseIndex)
                .maxBounds,
      };

  void setVariableBoundsInterpolation(
    Interpolation value, {
    required String name,
    required int phaseIndex,
    required DecisionVariableType from,
  }) {
    _ocp
        .variable(name, from: from, phaseIndex: phaseIndex)
        .bounds
        .interpolation = value;
    _variableController(name: name, from: from, phaseIndex: phaseIndex)
        ._updateBounds();
    _notifyListeners();
  }

  List<TextEditingController> getVariableInitialGuessControllers({
    required String name,
    required int phaseIndex,
    required DecisionVariableType from,
  }) =>
      _variableController(name: name, from: from, phaseIndex: phaseIndex)
          .initialGuess;

  void setVariableInitialGuessInterpolation(
    Interpolation value, {
    required String name,
    required int phaseIndex,
    required DecisionVariableType from,
  }) {
    _ocp
        .variable(name, from: from, phaseIndex: phaseIndex)
        .initialGuess
        .interpolation = value;
    _variableController(name: name, from: from, phaseIndex: phaseIndex)
        ._updateInitialGuess();
    _notifyListeners();
  }

  ///
  /// Here are the internal methods that ensures all the controllers are sane
  void _updateAllControllers() {
    _updateTextControllers(
      nbShootingPointsControllers,
      initialValue: _nbShootingPointsInitialValues,
      onChanged: _nbShootingPointsListener,
    );
    _updateTextControllers(
      phaseDurationControllers,
      initialValue: _phaseDurationInitialValues,
      onChanged: _phaseDurationListener,
    );

    _updateVariableController(_states, from: DecisionVariableType.state);
    _updateVariableController(_controls, from: DecisionVariableType.control);
  }

  void _updateTextControllers(List<TextEditingController> controllers,
      {required List<String> initialValue,
      required Function(String value, {required int phaseIndex}) onChanged}) {
    if (controllers.length < nbPhases) {
      for (int i = controllers.length; i < nbPhases; i++) {
        controllers.add(TextEditingController());
        controllers[i].text = initialValue[i];
        controllers[i]
            .addListener(() => onChanged(controllers[i].text, phaseIndex: i));
      }
    } else if (controllers.length > nbPhases) {
      for (int i = controllers.length - 1; i >= nbPhases; i++) {
        controllers[i].dispose();
        controllers.removeAt(i);
      }
    } else {
      // Do not change anything if we already have the right number of phases
    }
  }

  void _updateVariableController(
    List<Map<String, _VariableTextEditingControllers>> controllers, {
    required DecisionVariableType from,
  }) {
    if (controllers.length < nbPhases) {
      // For each of the new phases, declare all the required variables
      for (int i = controllers.length; i < nbPhases; i++) {
        controllers.add({});
        _createVariableControllers(controllers[i], from: from, phaseIndex: i);
      }
    } else if (controllers.length > nbPhases) {
      for (int i = controllers.length - 1; i >= nbPhases; i++) {
        for (final key in controllers[i].keys) {
          controllers[i][key]!.dispose();
        }
        controllers.removeAt(i);
      }
    } else {
      // Do not change anything if we already have the right number of phases
    }
  }

  void _createVariableControllers(
    Map<String, _VariableTextEditingControllers> controllers, {
    required DecisionVariableType from,
    required int phaseIndex,
  }) {
    for (final name in getVariableNames(from: from, phaseIndex: phaseIndex)) {
      controllers[name] = _VariableTextEditingControllers(
        getVariable(
          name: name,
          phaseIndex: phaseIndex,
          from: from,
        ),
        setDimensionCallback: (value) => setVariableDimension(value,
            name: name, from: from, phaseIndex: phaseIndex),
      );
    }
  }

  void dispose() {
    nbPhasesController.dispose();
    for (final controller in nbShootingPointsControllers) {
      controller.dispose();
    }
    nbShootingPointsControllers.clear();
    for (final controller in phaseDurationControllers) {
      controller.dispose();
    }
    phaseDurationControllers.clear();

    for (final phaseVariables in _states) {
      for (final key in phaseVariables.keys) {
        phaseVariables[key]!.dispose();
      }
      phaseVariables.clear();
    }
    _states.clear();

    for (final phaseVariables in _controls) {
      for (final key in phaseVariables.keys) {
        phaseVariables[key]!.dispose();
      }
      phaseVariables.clear();
    }
    _controls.clear();
  }
}

class _VariableTextEditingControllers {
  // TODO Add the capability to automatically fill end phase continuity with starting of next phase
  final DecisionVariable _variable;

  final name = TextEditingController(); // Add setter (and listener)

  final dimension = TextEditingController(text: '1');
  final Function(int value) setDimensionCallback;

  final minBounds = <TextEditingController>[];
  final maxBounds = <TextEditingController>[];
  // TODO By adding a boundHasChangedCallback it could be possible to set values accross phases
  final initialGuess = <TextEditingController>[];
  // TODO By adding a initialGuessHasChangedCallback it could be possible to set values accross phases

  _VariableTextEditingControllers(
    this._variable, {
    required this.setDimensionCallback,
  }) {
    name.text = _variable.name;

    _updateBounds();
    _updateInitialGuess();

    dimension.addListener(() {
      // The text field of dimension should only be positive integers
      final value = int.tryParse(dimension.text);
      if (value == null || value < 1 || value == _variable.dimension) return;

      setDimensionCallback(value);
      // No need to update the bounds or the initial guess because the
      // [setDimensionCallback] is expected to do so if required
    });
  }

  void _updateBounds() {
    // We have to reset all the controllers since we don't know if the number of
    // dimension or column changed. This would make the textfield bouncing around
    // randomly.
    _disposeBounds();
    final minValues = _variable.bounds.min.values;
    final maxValues = _variable.bounds.max.values;
    for (int i = 0; i < _variable.bounds.length; i++) {
      minBounds.add(TextEditingController(text: minValues[i].toString()));
      minBounds[i].addListener(
          () => _updateMatrixValue(_variable.bounds.min, i, minBounds[i].text));
      maxBounds.add(TextEditingController(text: maxValues[i].toString()));
      maxBounds[i].addListener(
          () => _updateMatrixValue(_variable.bounds.max, i, maxBounds[i].text));
    }
  }

  void _updateInitialGuess() {
    // We have to reset all the controllers since we don't know if the number of
    // dimension or column changed. This would make the textfield bouncing around
    // randomly.
    _disposeInitialGuess();
    final guessValues = _variable.initialGuess.guess.values;
    for (int i = 0; i < _variable.initialGuess.length; i++) {
      initialGuess.add(TextEditingController(text: guessValues[i].toString()));
      initialGuess[i].addListener(() => _updateMatrixValue(
          _variable.initialGuess.guess, i, initialGuess[i].text));
    }
  }

  void _updateMatrixValue(Matrix matrix, int index, String valueAsString) {
    final value = double.tryParse(valueAsString);
    if (value == null || value == matrix.values[index]) return;
    matrix.values[index] = value;
    OptimalControlProgramControllers.instance._notifyListeners();
  }

  void _disposeBounds() {
    for (final bound in minBounds) {
      bound.dispose();
    }
    for (final bound in maxBounds) {
      bound.dispose();
    }
    minBounds.clear();
    maxBounds.clear();
  }

  void _disposeInitialGuess() {
    for (final guess in initialGuess) {
      guess.dispose();
    }
    initialGuess.clear();
  }

  void dispose() {
    name.dispose();
    dimension.dispose();
    _disposeBounds();
    _disposeInitialGuess();
  }
}
