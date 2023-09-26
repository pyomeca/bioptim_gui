import 'dart:math';

import 'package:bioptim_gui/models/acrobatics_ocp.dart';
import 'package:bioptim_gui/models/acrobatics_position.dart';
import 'package:bioptim_gui/models/acrobatics_sport_type.dart';
import 'package:bioptim_gui/models/acrobatics_twist_side.dart';
import 'package:bioptim_gui/models/bio_model.dart';
import 'package:bioptim_gui/models/dynamics.dart';
import 'package:bioptim_gui/models/matrix.dart';
import 'package:bioptim_gui/models/optimal_control_program.dart';
import 'package:bioptim_gui/models/decision_variables.dart';
import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:bioptim_gui/models/penalty.dart';
import 'package:flutter/material.dart';

///
/// This class mimics the strcture of the [OptimalControlProgram] class but in
/// a UI perspective. It creates all the required Controllers as well as it gets
/// or updates the values.
class AcrobaticsOCPControllers {
  static final AcrobaticsOCPControllers _instance =
      AcrobaticsOCPControllers._internal();
  static AcrobaticsOCPControllers get instance => _instance;
  AcrobaticsOCPControllers._internal() {
    _updateAllControllers();
  }

  Function(String path) get exportScript => _ocp.exportScript;
  bool get mustExport => _ocp.mustExport;

  final _ocp = AcrobaticsOCPProgram();
  // This is to keep track of how many controllers we have because we don't
  // delete them if we reduce _nbSomersaults
  int _nbSomersaultsMax = 1;

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
  /// All methods related to controlling the number of somersaults
  late final nbSomersaultsController = TextEditingController(text: '1')
    ..addListener(_nbSomersaultsControllerListener);
  int get nbSomersaults => _ocp.generic.nbSomersaults;
  void setNbSomersaults(int value) {
    _ocp.generic.nbSomersaults = value;
    _ocp.updateSomersaults();
    _nbSomersaultsMax = max(nbSomersaults, _nbSomersaultsMax);
    if (nbSomersaultsController.text != nbSomersaults.toString()) {
      // This if case is to ensure non recursive calls
      nbSomersaultsController.text = nbSomersaults.toString();
    }
    // Wait for one frame so the the UI is updated
    WidgetsBinding.instance.addPostFrameCallback((timeStamp) {
      _updateAllControllers();
      _notifyListeners();
    });
  }

  void _nbSomersaultsControllerListener() {
    final tp = int.tryParse(nbSomersaultsController.text);
    if (tp == null || tp < 1 || tp == nbSomersaults) return;
    setNbSomersaults(tp);
  }

  ///
  /// All the methods related to the dynamic model
  BioModel getBioModel() => _ocp.generic.bioModel;
  void setBioModel(BioModel value) {
    _ocp.generic.bioModel = value;
    _notifyListeners();
  }

  ///
  /// All the methods related to the model path
  String getModelPath() => _ocp.generic.modelPath;
  void setModelPath(String value) {
    _ocp.generic.modelPath = value;
    _notifyListeners();
  }

  ///
  /// All the methods related to the final time margin
  late final finalTimeMarginController = TextEditingController(text: '0.1')
    ..addListener(_finalTimeMarginControllerListener);
  double get finalTimeMargin => _ocp.generic.finalTimeMargin;
  void setFinalTimeMargin(double value) {
    _ocp.generic.finalTimeMargin = value;
    // Wait for one frame so the the UI is updated
    WidgetsBinding.instance.addPostFrameCallback((timeStamp) {
      _updateAllControllers();
      _notifyListeners();
    });
  }

  void _finalTimeMarginControllerListener() {
    final tp = double.tryParse(finalTimeMarginController.text);
    if (tp == null) return;
    setFinalTimeMargin(tp);
  }

  ///
  /// All the methods related to the final time
  late final finalTimeController = TextEditingController(text: '1.0')
    ..addListener(_finalTimeControllerListener);
  double get finalTime => _ocp.generic.finalTime;
  void setFinalTime(double value) {
    _ocp.generic.finalTime = value;
    // Wait for one frame so the the UI is updated
    WidgetsBinding.instance.addPostFrameCallback((timeStamp) {
      _updateAllControllers();
      _notifyListeners();
    });
  }

  void _finalTimeControllerListener() {
    final tp = double.tryParse(finalTimeController.text);
    if (tp == null) return;
    setFinalTime(tp);
  }

  ///
  /// All methods related to the number of shooting points
  final nbShootingPointsControllers = <TextEditingController>[];
  int getNbShootingPoints({required int somersaultIndex}) =>
      _ocp.somersaults[somersaultIndex].nbShootingPoints;
  void setNbShootingPoints(int value, {required int somersaultIndex}) {
    if (value == _ocp.somersaults[somersaultIndex].nbShootingPoints) return;

    _ocp.somersaults[somersaultIndex].nbShootingPoints = value;
    _notifyListeners();
  }

  List<String> get _nbShootingPointsInitialValues => [
        for (int i = 0; i < nbSomersaults; i++)
          getNbShootingPoints(somersaultIndex: i).toString()
      ];
  void _nbShootingPointsListener(String value,
          {required int somersaultIndex}) =>
      setNbShootingPoints(int.tryParse(value) ?? -1,
          somersaultIndex: somersaultIndex);

  ///
  /// All methods related to the number of half twists
  final nbHalfTwistsControllers = <TextEditingController>[];
  int getNbHalfTwists({required int somersaultIndex}) =>
      _ocp.somersaults[somersaultIndex].nbHalfTwists;
  void setNbHalfTwists(int value, {required int somersaultIndex}) {
    if (value == _ocp.somersaults[somersaultIndex].nbHalfTwists) return;

    _ocp.somersaults[somersaultIndex].nbHalfTwists = value;
    _notifyListeners();
  }

  List<String> get _nbHalfTwistsInitialValues => [
        for (int i = 0; i < nbSomersaults; i++)
          getNbHalfTwists(somersaultIndex: i).toString()
      ];
  void _nbHalfTwistsListener(String value, {required int somersaultIndex}) =>
      setNbHalfTwists(int.tryParse(value) ?? -1,
          somersaultIndex: somersaultIndex);

  ///
  /// All methods related to the somersault duration
  final somersaultDurationControllers = <TextEditingController>[];
  double getSomersaultDuration({required int somersaultIndex}) =>
      _ocp.somersaults[somersaultIndex].duration;
  void setSomersaultDuration(double value, {required int somersaultIndex}) {
    if (value == _ocp.somersaults[somersaultIndex].duration) return;

    _ocp.somersaults[somersaultIndex].duration = value;
    _notifyListeners();
  }

  List<String> get _somersaultDurationInitialValues => [
        for (int i = 0; i < nbSomersaults; i++)
          getSomersaultDuration(somersaultIndex: i).toString()
      ];

  void _somersaultDurationListener(String value,
          {required int somersaultIndex}) =>
      setSomersaultDuration(double.tryParse(value) ?? -1.0,
          somersaultIndex: somersaultIndex);

  ///
  /// All methods related to controlling the acrobatics position
  AcrobaticsPosition get position => _ocp.generic.position;
  void setPosition(AcrobaticsPosition value) {
    _ocp.generic.position = value;
    _notifyListeners();
  }

  ///
  /// All methods related to controlling the sport type
  AcrobaticsSportType get sportType => _ocp.generic.sportType;
  void setSportType(AcrobaticsSportType value) {
    _ocp.generic.sportType = value;
    _notifyListeners();
  }

  ///
  /// All methods related to controlling the twist side
  PreferredTwistSide get preferredTwistSide => _ocp.generic.preferredTwistSide;
  void setPreferredTwistSide(PreferredTwistSide value) {
    _ocp.generic.preferredTwistSide = value;
    _notifyListeners();
  }

  ///
  /// All methods related to the dynamics equation
  Dynamics getDynamics({required int somersaultIndex}) =>
      _ocp.somersaults[somersaultIndex].dynamics;
  void setDynamics(Dynamics value, {required int somersaultIndex}) {
    if (value.type == _ocp.somersaults[somersaultIndex].dynamics.type) return;

    _ocp.somersaults[somersaultIndex].dynamics = value;
    _ocp.resetVariables(somersaultIndex: somersaultIndex);

    for (final key in _states[somersaultIndex].keys) {
      _states[somersaultIndex][key]!.dispose();
    }
    _states[somersaultIndex] = {};
    _createVariableControllers(_states[somersaultIndex],
        from: DecisionVariableType.state, somersaultIndex: somersaultIndex);

    for (final key in _controls[somersaultIndex].keys) {
      _controls[somersaultIndex][key]!.dispose();
    }
    _controls[somersaultIndex] = {};
    _createVariableControllers(_controls[somersaultIndex],
        from: DecisionVariableType.control, somersaultIndex: somersaultIndex);

    _notifyListeners();
  }

  ///
  /// All methods related to the state and control variables
  final List<Map<String, _VariableTextEditingControllers>> _states = [];
  final List<Map<String, _VariableTextEditingControllers>> _controls = [];
  _VariableTextEditingControllers _variableController(
      {required String name,
      required DecisionVariableType from,
      required int somersaultIndex}) {
    switch (from) {
      case DecisionVariableType.state:
        return _states[somersaultIndex][name]!;
      case DecisionVariableType.control:
        return _controls[somersaultIndex][name]!;
    }
  }

  /// Warning, even though this allows to modify values, getVariable should
  /// NOT be used as such. That is because other functions must be called
  /// each time a variable is updated. Consider this [getVariable] interface
  /// as a readonly interface.
  DecisionVariable getVariable(
          {required String name,
          required int somersaultIndex,
          required DecisionVariableType from}) =>
      _ocp.variable(name, from: from, somersaultIndex: somersaultIndex);

  List<String> getVariableNames(
          {required int somersaultIndex, required DecisionVariableType from}) =>
      _ocp.variables(from: from, somersaultIndex: somersaultIndex).names;

  TextEditingController getVariableNameController(
          {required String name,
          required int somersaultIndex,
          required DecisionVariableType from}) =>
      _variableController(
              name: name, from: from, somersaultIndex: somersaultIndex)
          .name;

  TextEditingController getVariableDimensionController({
    required String name,
    required int somersaultIndex,
    required DecisionVariableType from,
  }) =>
      _variableController(
              name: name, from: from, somersaultIndex: somersaultIndex)
          .dimension;

  void setVariableDimension(
    int value, {
    required String name,
    required int somersaultIndex,
    required DecisionVariableType from,
  }) {
    _ocp
        .variable(name, from: from, somersaultIndex: somersaultIndex)
        .changeDimension(value);
    _variableController(
            name: name, from: from, somersaultIndex: somersaultIndex)
        ._updateBounds();
    _variableController(
            name: name, from: from, somersaultIndex: somersaultIndex)
        ._updateInitialGuess();
    _notifyListeners();
  }

  Map<String, List<TextEditingController>> getVariableBoundsControllers({
    required String name,
    required int somersaultIndex,
    required DecisionVariableType from,
  }) =>
      {
        'minBounds': _variableController(
                name: name, from: from, somersaultIndex: somersaultIndex)
            .minBounds,
        'maxBounds': _variableController(
                name: name, from: from, somersaultIndex: somersaultIndex)
            .maxBounds,
      };

  void setVariableBoundsInterpolation(
    Interpolation value, {
    required String name,
    required int somersaultIndex,
    required DecisionVariableType from,
  }) {
    final bounds = _ocp
        .variable(name, from: from, somersaultIndex: somersaultIndex)
        .bounds;
    if (value == bounds.interpolation) return;

    bounds.interpolation = value;
    _variableController(
            name: name, from: from, somersaultIndex: somersaultIndex)
        ._updateBounds();
    _notifyListeners();
  }

  List<TextEditingController> getVariableInitialGuessControllers({
    required String name,
    required int somersaultIndex,
    required DecisionVariableType from,
  }) =>
      _variableController(
              name: name, from: from, somersaultIndex: somersaultIndex)
          .initialGuess;

  void setVariableInitialGuessInterpolation(
    Interpolation value, {
    required String name,
    required int somersaultIndex,
    required DecisionVariableType from,
  }) {
    final initialGuess = _ocp
        .variable(name, from: from, somersaultIndex: somersaultIndex)
        .initialGuess;
    if (value == initialGuess.interpolation) return;

    initialGuess.interpolation = value;
    _variableController(
            name: name, from: from, somersaultIndex: somersaultIndex)
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
          {required int penaltyIndex, required int somersaultIndex}) =>
      _objectiveControllers[somersaultIndex][penaltyIndex].arguments;

  PenaltyInterface objectives({required int somersaultIndex}) =>
      PenaltyInterface(
          create: () => _createObjective(somersaultIndex: somersaultIndex),
          fetch: ({required penaltyIndex}) =>
              _getObjectives(somersaultIndex: somersaultIndex)[penaltyIndex],
          fetchAll: () => _getObjectives(somersaultIndex: somersaultIndex),
          update: (penalty, {required penaltyIndex}) => _updateObjective(
              penalty,
              penaltyIndex: penaltyIndex,
              somersaultIndex: somersaultIndex),
          remove: ({required penaltyIndex}) => _removeObjective(
              penaltyIndex: penaltyIndex, somersaultIndex: somersaultIndex),
          weightController: ({required penaltyIndex}) =>
              _objectiveControllers[somersaultIndex][penaltyIndex].weight,
          argumentController: (
                  {required penaltyIndex, required argumentIndex}) =>
              _objectiveControllers[somersaultIndex][penaltyIndex]
                  .arguments[argumentIndex]);

  List<Penalty> _getObjectives({required int somersaultIndex}) =>
      _ocp.somersaults[somersaultIndex].objectives;

  void _createObjective({required int somersaultIndex}) =>
      _createPenalty(Objective.generic(),
          controllers: _objectiveControllers[somersaultIndex],
          penalties: _ocp.somersaults[somersaultIndex].objectives);

  void _updateObjective(Penalty penalty,
          {required int penaltyIndex, required int somersaultIndex}) =>
      _updatePenalty(penalty,
          controllers: _objectiveControllers[somersaultIndex],
          penalties: _ocp.somersaults[somersaultIndex].objectives,
          penaltyIndex: penaltyIndex);

  void _removeObjective(
          {required int penaltyIndex, required int somersaultIndex}) =>
      _removePenalty(
          controllers: _objectiveControllers[somersaultIndex],
          penalties: _ocp.somersaults[somersaultIndex].objectives,
          penaltyIndex: penaltyIndex);

  ///
  /// Here are all the constraint methods
  final List<List<_PenaltyTextEditingControllers>> _constraintControllers = [];

  List<TextEditingController> getConstraintArgumentsControllers(
          {required int penaltyIndex, required int somersaultIndex}) =>
      _constraintControllers[somersaultIndex][penaltyIndex].arguments;

  PenaltyInterface constraints({required int somersaultIndex}) =>
      PenaltyInterface(
          create: () => _createConstraint(somersaultIndex: somersaultIndex),
          fetch: ({required penaltyIndex}) =>
              _getConstraints(somersaultIndex: somersaultIndex)[penaltyIndex],
          fetchAll: () => _getConstraints(somersaultIndex: somersaultIndex),
          update: (penalty, {required penaltyIndex}) => _updateConstraint(
              penalty,
              penaltyIndex: penaltyIndex,
              somersaultIndex: somersaultIndex),
          remove: ({required penaltyIndex}) => _removeConstraint(
              penaltyIndex: penaltyIndex, somersaultIndex: somersaultIndex),
          argumentController: (
                  {required penaltyIndex, required argumentIndex}) =>
              _constraintControllers[somersaultIndex][penaltyIndex]
                  .arguments[argumentIndex]);

  List<Penalty> _getConstraints({required int somersaultIndex}) =>
      _ocp.somersaults[somersaultIndex].constraints;

  void _createConstraint({required int somersaultIndex}) =>
      _createPenalty(Constraint.generic(),
          controllers: _constraintControllers[somersaultIndex],
          penalties: _ocp.somersaults[somersaultIndex].constraints);

  void _updateConstraint(Penalty penalty,
          {required int penaltyIndex, required int somersaultIndex}) =>
      _updatePenalty(penalty,
          controllers: _constraintControllers[somersaultIndex],
          penalties: _ocp.somersaults[somersaultIndex].constraints,
          penaltyIndex: penaltyIndex);

  void _removeConstraint(
          {required int penaltyIndex, required int somersaultIndex}) =>
      _removePenalty(
          controllers: _constraintControllers[somersaultIndex],
          penalties: _ocp.somersaults[somersaultIndex].constraints,
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
      nbHalfTwistsControllers,
      initialValue: _nbHalfTwistsInitialValues,
      onChanged: _nbHalfTwistsListener,
    );
    _updateTextControllers(
      somersaultDurationControllers,
      initialValue: _somersaultDurationInitialValues,
      onChanged: _somersaultDurationListener,
    );

    _updateVariableController(_states, from: DecisionVariableType.state);
    _updateVariableController(_controls, from: DecisionVariableType.control);

    _updatePenaltyControllers(_objectiveControllers);
    _updatePenaltyControllers(_constraintControllers);
  }

  void _updateTextControllers(List<TextEditingController> controllers,
      {required List<String> initialValue,
      required Function(String value, {required int somersaultIndex})
          onChanged}) {
    if (controllers.length < nbSomersaults) {
      for (int i = controllers.length; i < nbSomersaults; i++) {
        controllers.add(TextEditingController());
        controllers[i].text = initialValue[i];
        controllers[i].addListener(
            () => onChanged(controllers[i].text, somersaultIndex: i));
      }
    } else if (controllers.length > nbSomersaults) {
      for (int i = controllers.length - 1; i >= nbSomersaults; i--) {
        controllers[i].dispose();
        controllers.removeAt(i);
      }
    } else {
      // Do not change anything if we already have the right number of somersaults
    }
  }

  void _updateVariableController(
    List<Map<String, _VariableTextEditingControllers>> controllers, {
    required DecisionVariableType from,
  }) {
    if (controllers.length < nbSomersaults) {
      // For each of the new somersaults, declare all the required variables
      for (int i = controllers.length; i < nbSomersaults; i++) {
        controllers.add({});
        _createVariableControllers(controllers[i],
            from: from, somersaultIndex: i);
      }
    } else if (controllers.length > nbSomersaults) {
      for (int i = controllers.length - 1; i >= nbSomersaults; i--) {
        for (final key in controllers[i].keys) {
          controllers[i][key]!.dispose();
        }
        controllers.removeAt(i);
      }
    } else {
      // Do not change anything if we already have the right number of somersaults
    }
  }

  void _updatePenaltyControllers(
      List<List<_PenaltyTextEditingControllers>> controllers) {
    if (controllers.length < nbSomersaults) {
      // For each of the new somersaults, declare all the required variables
      for (int i = controllers.length; i < nbSomersaults; i++) {
        controllers.add([]);

        // adding default penalties, that will be added for each somersault
        if (_objectiveControllers[i].isEmpty) {
          _createPenalty(Objective.acrobaticGenericLagrangeMinimizeControls(),
              controllers: _objectiveControllers[i],
              penalties: _ocp.somersaults[i].objectives);

          _createPenalty(
              Objective.acrobaticGenericMayerMinimizeTime(
                  minBound:
                      double.parse(somersaultDurationControllers[i].text) -
                          finalTimeMargin,
                  maxBound:
                      double.parse(somersaultDurationControllers[i].text) +
                          finalTimeMargin),
              controllers: _objectiveControllers[i],
              penalties: _ocp.somersaults[i].objectives);
        }
      }
    } else if (controllers.length > nbSomersaults) {
      for (int i = controllers.length - 1; i >= nbSomersaults; i--) {
        for (final controller in controllers[i]) {
          controller.dispose();
        }
        controllers.removeAt(i);
      }
    } else {
      // Do not change anything if we already have the right number of somersaults
    }
  }

  void _createVariableControllers(
    Map<String, _VariableTextEditingControllers> controllers, {
    required DecisionVariableType from,
    required int somersaultIndex,
  }) {
    for (final name
        in getVariableNames(from: from, somersaultIndex: somersaultIndex)) {
      controllers[name] = _VariableTextEditingControllers(
        getVariable(
          name: name,
          somersaultIndex: somersaultIndex,
          from: from,
        ),
        setDimensionCallback: (value) => setVariableDimension(value,
            name: name, from: from, somersaultIndex: somersaultIndex),
      );
    }
  }

  void dispose() {
    nbSomersaultsController.dispose();
    for (final controller in nbShootingPointsControllers) {
      controller.dispose();
    }
    nbShootingPointsControllers.clear();
    for (final controller in somersaultDurationControllers) {
      controller.dispose();
    }
    somersaultDurationControllers.clear();

    for (final somersaultVariables in _states) {
      for (final key in somersaultVariables.keys) {
        somersaultVariables[key]!.dispose();
      }
      somersaultVariables.clear();
    }
    _states.clear();

    for (final somersaultVariables in _controls) {
      for (final key in somersaultVariables.keys) {
        somersaultVariables[key]!.dispose();
      }
      somersaultVariables.clear();
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
      AcrobaticsOCPControllers.instance._notifyListeners();
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
        AcrobaticsOCPControllers.instance._notifyListeners();
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
  // TODO Add the capability to automatically fill end somersault continuity with starting of next somersault
  final DecisionVariable _variable;

  final name = TextEditingController(); // Add setter (and listener)

  final dimension = TextEditingController(text: '1');
  final Function(int value) setDimensionCallback;

  final minBounds = <TextEditingController>[];
  final maxBounds = <TextEditingController>[];
  // TODO By adding a boundHasChangedCallback it could be possible to set values accross somersaults
  final initialGuess = <TextEditingController>[];
  // TODO By adding a initialGuessHasChangedCallback it could be possible to set values accross somersaults

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
    AcrobaticsOCPControllers.instance._notifyListeners();
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
