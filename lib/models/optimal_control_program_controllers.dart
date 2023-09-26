import 'dart:math';

import 'package:bioptim_gui/models/bio_model.dart';
import 'package:bioptim_gui/models/dynamics.dart';
import 'package:bioptim_gui/models/matrix.dart';
import 'package:bioptim_gui/models/optimal_control_program_type.dart';
import 'package:bioptim_gui/models/optimal_control_program.dart';
import 'package:bioptim_gui/models/decision_variables.dart';
import 'package:bioptim_gui/models/penalty.dart';
import 'package:flutter/material.dart';

class PenaltyInterface {
  const PenaltyInterface({
    required this.create,
    required this.fetch,
    required this.fetchAll,
    required this.update,
    required this.remove,
    this.weightController,
    required this.argumentController,
  });

  final Function() create;
  final Penalty Function({required int penaltyIndex}) fetch;
  final List<Penalty> Function() fetchAll;
  final Function(Penalty penalty, {required int penaltyIndex}) update;
  final Function({required int penaltyIndex}) remove;

  final TextEditingController Function({required int penaltyIndex})?
      weightController;

  final TextEditingController Function(
      {required int penaltyIndex,
      required int argumentIndex}) argumentController;
}

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
    if (value == _ocp.phases[phaseIndex].nbShootingPoints) return;

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
    if (value == _ocp.phases[phaseIndex].duration) return;

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
    if (value.type == _ocp.phases[phaseIndex].dynamics.type) return;

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
    final bounds =
        _ocp.variable(name, from: from, phaseIndex: phaseIndex).bounds;
    if (value == bounds.interpolation) return;

    bounds.interpolation = value;
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
    final initialGuess =
        _ocp.variable(name, from: from, phaseIndex: phaseIndex).initialGuess;
    if (value == initialGuess.interpolation) return;

    initialGuess.interpolation = value;
    _variableController(name: name, from: from, phaseIndex: phaseIndex)
        ._updateInitialGuess();
    _notifyListeners();
  }

  ///
  /// Here are some generic methods for penalties (declared later)
  void _createPenalty(
    Penalty penalty, {
    required List<_PenaltyTextEditingControllers> controllers,
    required List<Penalty> penalties,
  }) {
    penalties.add(penalty);
    controllers.add(_PenaltyTextEditingControllers(penalties.last));
    controllers.last._updateWeight();
    controllers.last._updateArguments();
    _notifyListeners();
  }

  void _updatePenalty(
    Penalty penalty, {
    required List<_PenaltyTextEditingControllers> controllers,
    required List<Penalty> penalties,
    required int penaltyIndex,
  }) {
    penalties[penaltyIndex] = penalty;
    controllers[penaltyIndex]._penalty = penalty;
    controllers[penaltyIndex]._updateWeight();
    controllers[penaltyIndex]._updateArguments();
    _notifyListeners();
  }

  void _removePenalty({
    required List<_PenaltyTextEditingControllers> controllers,
    required List<Penalty> penalties,
    required int penaltyIndex,
  }) {
    penalties.removeAt(penaltyIndex);
    controllers[penaltyIndex].dispose();
    controllers.removeAt(penaltyIndex);
    _notifyListeners();
  }

  ///
  /// Here are the objective function methods
  final List<List<_PenaltyTextEditingControllers>> _objectiveControllers = [];

  List<TextEditingController> getObjectiveArgumentsControllers(
          {required int penaltyIndex, required int phaseIndex}) =>
      _objectiveControllers[phaseIndex][penaltyIndex].arguments;

  PenaltyInterface objectives({required int phaseIndex}) => PenaltyInterface(
      create: () => _createObjective(phaseIndex: phaseIndex),
      fetch: ({required penaltyIndex}) =>
          _getObjectives(phaseIndex: phaseIndex)[penaltyIndex],
      fetchAll: () => _getObjectives(phaseIndex: phaseIndex),
      update: (penalty, {required penaltyIndex}) => _updateObjective(penalty,
          penaltyIndex: penaltyIndex, phaseIndex: phaseIndex),
      remove: ({required penaltyIndex}) =>
          _removeObjective(penaltyIndex: penaltyIndex, phaseIndex: phaseIndex),
      weightController: ({required penaltyIndex}) =>
          _objectiveControllers[phaseIndex][penaltyIndex].weight,
      argumentController: ({required penaltyIndex, required argumentIndex}) =>
          _objectiveControllers[phaseIndex][penaltyIndex]
              .arguments[argumentIndex]);

  List<Penalty> _getObjectives({required int phaseIndex}) =>
      _ocp.phases[phaseIndex].objectives;

  void _createObjective({required int phaseIndex}) =>
      _createPenalty(Objective.generic(),
          controllers: _objectiveControllers[phaseIndex],
          penalties: _ocp.phases[phaseIndex].objectives);

  void _updateObjective(Penalty penalty,
          {required int penaltyIndex, required int phaseIndex}) =>
      _updatePenalty(penalty,
          controllers: _objectiveControllers[phaseIndex],
          penalties: _ocp.phases[phaseIndex].objectives,
          penaltyIndex: penaltyIndex);

  void _removeObjective({required int penaltyIndex, required int phaseIndex}) =>
      _removePenalty(
          controllers: _objectiveControllers[phaseIndex],
          penalties: _ocp.phases[phaseIndex].objectives,
          penaltyIndex: penaltyIndex);

  ///
  /// Here are all the constraint methods
  final List<List<_PenaltyTextEditingControllers>> _constraintControllers = [];

  List<TextEditingController> getConstraintArgumentsControllers(
          {required int penaltyIndex, required int phaseIndex}) =>
      _constraintControllers[phaseIndex][penaltyIndex].arguments;

  PenaltyInterface constraints({required int phaseIndex}) => PenaltyInterface(
      create: () => _createConstraint(phaseIndex: phaseIndex),
      fetch: ({required penaltyIndex}) =>
          _getConstraints(phaseIndex: phaseIndex)[penaltyIndex],
      fetchAll: () => _getConstraints(phaseIndex: phaseIndex),
      update: (penalty, {required penaltyIndex}) => _updateConstraint(penalty,
          penaltyIndex: penaltyIndex, phaseIndex: phaseIndex),
      remove: ({required penaltyIndex}) =>
          _removeConstraint(penaltyIndex: penaltyIndex, phaseIndex: phaseIndex),
      argumentController: ({required penaltyIndex, required argumentIndex}) =>
          _constraintControllers[phaseIndex][penaltyIndex]
              .arguments[argumentIndex]);

  List<Penalty> _getConstraints({required int phaseIndex}) =>
      _ocp.phases[phaseIndex].constraints;

  void _createConstraint({required int phaseIndex}) =>
      _createPenalty(Constraint.generic(),
          controllers: _constraintControllers[phaseIndex],
          penalties: _ocp.phases[phaseIndex].constraints);

  void _updateConstraint(Penalty penalty,
          {required int penaltyIndex, required int phaseIndex}) =>
      _updatePenalty(penalty,
          controllers: _constraintControllers[phaseIndex],
          penalties: _ocp.phases[phaseIndex].constraints,
          penaltyIndex: penaltyIndex);

  void _removeConstraint(
          {required int penaltyIndex, required int phaseIndex}) =>
      _removePenalty(
          controllers: _constraintControllers[phaseIndex],
          penalties: _ocp.phases[phaseIndex].constraints,
          penaltyIndex: penaltyIndex);

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

    _updatePenaltyControllers(_objectiveControllers);
    _updatePenaltyControllers(_constraintControllers);
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
      for (int i = controllers.length - 1; i >= nbPhases; i--) {
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
      for (int i = controllers.length - 1; i >= nbPhases; i--) {
        for (final key in controllers[i].keys) {
          controllers[i][key]!.dispose();
        }
        controllers.removeAt(i);
      }
    } else {
      // Do not change anything if we already have the right number of phases
    }
  }

  void _updatePenaltyControllers(
      List<List<_PenaltyTextEditingControllers>> controllers) {
    if (controllers.length < nbPhases) {
      // For each of the new phases, declare all the required variables
      for (int i = controllers.length; i < nbPhases; i++) {
        controllers.add([]);
      }
    } else if (controllers.length > nbPhases) {
      for (int i = controllers.length - 1; i >= nbPhases; i--) {
        for (final controller in controllers[i]) {
          controller.dispose();
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

class _PenaltyTextEditingControllers {
  final weight = TextEditingController(text: '1.0');

  Penalty _penalty;
  final arguments = <TextEditingController>[];

  _PenaltyTextEditingControllers(this._penalty) {
    weight.addListener(() {
      if (_penalty.runtimeType != Objective) return;
      final newWeight = double.tryParse(weight.text);
      if (newWeight == null || newWeight == (_penalty as Objective).weight) {
        return;
      }

      (_penalty as Objective).weight = newWeight;

      OptimalControlProgramControllers.instance._notifyListeners();
    });
    _updateArguments();
  }

  void _updateWeight() {
    if (_penalty.runtimeType != Objective) return;
    weight.text = (_penalty as Objective).weight.toString();
  }

  void _updateArguments() {
    _disposeArguments();
    final names = _penalty.arguments.keys.toList();
    for (int i = 0; i < _penalty.arguments.length; i++) {
      final name = names[i];

      arguments.add(TextEditingController(
          text: _penalty.arguments[name]?.toString() ?? ''));
      arguments[i].addListener(() {
        final value = arguments[i].text;
        if (value == _penalty.arguments[name].toString()) return;
        _penalty.arguments[name] = value;
        OptimalControlProgramControllers.instance._notifyListeners();
      });
    }
  }

  void _disposeArguments() {
    for (final controller in arguments) {
      controller.dispose();
    }
    arguments.clear();
  }

  void dispose() {
    weight.dispose();
    _disposeArguments();
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
