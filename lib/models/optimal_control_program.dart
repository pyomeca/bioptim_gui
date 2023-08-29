import 'dart:io';

import 'package:bioptim_gui/models/bio_model.dart';
import 'package:bioptim_gui/models/dynamics.dart';
import 'package:bioptim_gui/models/global.dart';
import 'package:bioptim_gui/models/optimal_control_program_type.dart';
import 'package:bioptim_gui/models/optimization_variable.dart';
import 'package:bioptim_gui/models/penalty.dart';
import 'package:bioptim_gui/models/solver.dart';

class OptimalControlProgram {
  ///
  /// Constructor

  OptimalControlProgram({
    OptimalControlProgramType ocpType = OptimalControlProgramType.ocp,
    BioModel bioModel = BioModel.biorbd,
    String modelPath = '',
    int nbShootingPoints = 50,
    double phaseTime = 1.0,
    Dynamics dynamics =
        const Dynamics(type: DynamicsType.torqueDriven, isExpanded: true),
    bool useSx = true,
    Solver solver = const Solver(type: SolverType.ipopt),
  })  : _ocpType = ocpType,
        _bioModel = bioModel,
        _modelPath = modelPath,
        _nbShootingPoints = nbShootingPoints,
        _phaseTime = phaseTime,
        _dynamics = dynamics,
        _solver = solver,
        _useSx = useSx;

  ///
  /// Setters and Getters

  bool _hasPendingChanges = true;
  bool get hasPendingChanges => _hasPendingChanges;

  OptimalControlProgramType _ocpType;
  OptimalControlProgramType get ocpType => _ocpType;
  set ocpType(OptimalControlProgramType value) {
    _ocpType = value;
    _hasPendingChanges = true;
  }

  BioModel _bioModel;
  BioModel get bioModel => _bioModel;
  set bioModel(BioModel value) {
    _bioModel = value;
    _hasPendingChanges = true;
  }

  String _modelPath;
  String get modelPath => _modelPath;
  set modelPath(String value) {
    _modelPath = value;
    _hasPendingChanges = true;
  }

  int _nbShootingPoints;
  int get nbShootingPoints => _nbShootingPoints;
  set nbShootingPoints(int value) {
    _nbShootingPoints = value;
    _hasPendingChanges = true;
  }

  double _phaseTime;
  double get phaseTime => _phaseTime;
  set phaseTime(double value) {
    _phaseTime = value;
    _hasPendingChanges = true;
  }

  Dynamics _dynamics;
  Dynamics get dynamics => _dynamics;
  set dynamic(Dynamics value) {
    _dynamics = value;
    _hasPendingChanges = true;
  }

  final OptimizationVariableMap _stateVariables =
      OptimizationVariableMap(OptimizationVariableType.state);
  final OptimizationVariableMap _controlVariables =
      OptimizationVariableMap(OptimizationVariableType.control);

  OptimizationVariableMap variableMap(
      {required OptimizationVariableType from}) {
    switch (from) {
      case OptimizationVariableType.state:
        return _stateVariables;
      case OptimizationVariableType.control:
        return _controlVariables;
    }
  }

  OptimizationVariable variable(String name,
          {required OptimizationVariableType from}) =>
      variableMap(from: from)[name];

  void addVariable(OptimizationVariable value,
      {required OptimizationVariableType from}) {
    variableMap(from: from).addVariable(value);
    _hasPendingChanges = true;
  }

  void fillBound(
    String name, {
    required List<double> min,
    required List<double> max,
    required OptimizationVariableType from,
    int? rowIndex,
    int? colIndex,
  }) {
    variableMap(from: from).fillBound(name,
        min: min, max: max, rowIndex: rowIndex, colIndex: colIndex);
    _hasPendingChanges = true;
  }

  void fillInitialGuess(String name,
      {required List<double> guess, required OptimizationVariableType from}) {
    variableMap(from: from).fillInitialGuess(name, guess: guess);
    _hasPendingChanges = true;
  }

  void replaceVariable(OptimizationVariable value,
      {required OptimizationVariableType from}) {
    variableMap(from: from).replaceVariable(value);
    _hasPendingChanges = true;
  }

  void removeVariable(String name, {required OptimizationVariableType from}) {
    variableMap(from: from).removeVariable(name);
    _hasPendingChanges = true;
  }

  final List<Objective> _objectives = [];
  Objective objective(int index) => _objectives[index];
  void addObjective(Objective value) {
    _objectives.add(value);
    _hasPendingChanges = true;
  }

  void replaceObjective(int index, Objective value) {
    _objectives[index] = value;
    _hasPendingChanges = true;
  }

  void removeObjectives(int index) {
    _objectives.removeAt(index);
    _hasPendingChanges = true;
  }

  final List<Constraint> _constraints = [];
  Constraint constraint(int index) => _constraints[index];
  void addConstraint(Constraint value) {
    _constraints.add(value);
    _hasPendingChanges = true;
  }

  void replaceConstraint(int index, Constraint value) {
    _constraints[index] = value;
    _hasPendingChanges = true;
  }

  void removeConstraint(int index) {
    _constraints.removeAt(index);
    _hasPendingChanges = true;
  }

  bool _useSx;
  bool get useSx => _useSx;
  set useSx(bool value) {
    _useSx = value;
    _hasPendingChanges = true;
  }

  Solver _solver;
  Solver get solver => _solver;
  set solver(Solver value) {
    _solver = value;
    _hasPendingChanges = true;
  }

  ///
  /// Main interface

  void exportScript(String path) {
    _hasPendingChanges = false;

    final file = File(path);

    // Write the header
    file.writeAsStringSync('"""\n'
        'This file was automatically generated using BioptimGUI version $biotimGuiVersion\n'
        '"""\n'
        '\n'
        'from bioptim import *  # TODO Pariterre - Do not import "*"\n'
        '\n'
        '\n');

    // Write the docstring of the prepare_ocp section
    file.writeAsStringSync(
        'def prepare_ocp():\n'
        '    """\n'
        '    This function build an optimal control program and instantiate it.\n'
        '    It can be seen as a factory for the OptimalControlProgram class.\n'
        '\n'
        '    Parameters\n'
        '    ----------\n'
        '    # TODO fill this section\n'
        '\n'
        '    Returns\n'
        '    -------\n'
        '    The OptimalControlProgram ready to be solved\n'
        '    """\n'
        '\n',
        mode: FileMode.append);

    // Write the Generic section
    file.writeAsStringSync(
        '    # Declaration of generic elements\n'
        '    bio_model = ${bioModel.toPythonString()}(r"$modelPath")\n'
        '    n_shooting = $nbShootingPoints\n'
        '    phase_time = $phaseTime\n'
        '\n',
        mode: FileMode.append);

    // Write the dynamics section
    file.writeAsStringSync(
        '    # Declaration of the dynamics function used during integration\n'
        '    dynamics = Dynamics(${dynamics.type.toPythonString()}, '
        'expand=${dynamics.isExpanded ? 'True' : 'False'})\n'
        '\n',
        mode: FileMode.append);

    // Write the variable section
    file.writeAsStringSync(
        '    # Declaration of optimization variables bounds and initial guesses\n',
        mode: FileMode.append);

    for (final variableType in OptimizationVariableType.values) {
      final allVariables = variableMap(from: variableType);
      final basename = allVariables.type.toPythonString();

      file.writeAsStringSync(
          '    ${basename}_bounds = BoundsList()\n'
          '    ${basename}_initial_guesses = InitialGuessList()\n'
          '\n',
          mode: FileMode.append);

      for (final name in allVariables.names) {
        final variable = allVariables[name];
        file.writeAsStringSync(
            '    ${basename}_bounds.add(\n'
            '        "${variable.name}",\n'
            '        min_bound=${variable.bounds.min},\n'
            '        max_bound=${variable.bounds.max},\n'
            '        interpolation=${variable.bounds.interpolation.toPythonString()},\n'
            '        phase=${variable.phase},\n'
            '    )'
            '\n'
            '    ${basename}_initial_guesses.add(\n'
            '        "${variable.name}",\n'
            '        initial_guess=${variable.initialGuess.guess},\n'
            '        interpolation=${variable.initialGuess.interpolation.toPythonString()},\n'
            '        phase=${variable.phase},\n'
            '    )\n'
            '\n',
            mode: FileMode.append);
      }
    }

    // Write the constraints
    file.writeAsStringSync(
        '    # Declaration of the constraints of the ocp\n'
        '    constraints = ConstraintList()\n',
        mode: FileMode.append);
    for (final constraint in _constraints) {
      file.writeAsStringSync(
          '    constraints.add(\n'
          '        constraint=${constraint.fcn.toPythonString()},\n'
          '    )\n',
          mode: FileMode.append);
    }
    file.writeAsStringSync('\n', mode: FileMode.append);

    // Write the objective functions
    file.writeAsStringSync(
        '    # Declaration of the objectives of the ocp\n'
        '    objective_functions = ObjectiveList()\n',
        mode: FileMode.append);
    for (final objective in _objectives) {
      file.writeAsStringSync(
          '    objective_functions.add(\n'
          '        objective=${objective.fcn.toPythonString()},\n'
          '${objective.argumentKeys.map((key) => '        ${objective.argumentToPythonString(key)},').join('\n')}\n'
          '    )\n',
          mode: FileMode.append);
    }
    file.writeAsStringSync('\n', mode: FileMode.append);

    // Write the return section
    file.writeAsStringSync(
        '    # Construct and return the optimal control program (OCP)\n'
        '    return ${ocpType.toPythonString()}(\n'
        '        bio_model=bio_model,\n'
        '        n_shooting=n_shooting,\n'
        '        phase_time=phase_time,\n'
        '        dynamics=dynamics,\n'
        '        x_bounds=x_bounds,\n'
        '        u_bounds=u_bounds,\n'
        '        x_init=x_initial_guesses,\n'
        '        u_init=u_initial_guesses,\n'
        '        constraints=constraints,\n'
        '        objective_functions=objective_functions,\n'
        '        use_sx=${useSx ? 'True' : 'False'},\n'
        '    )\n'
        '\n'
        '\n',
        mode: FileMode.append);

    // Write run as a script section
    file.writeAsStringSync(
        'def main():\n'
        '    """\n'
        '    If this file is run, then it will perform the optimization\n'
        '    """\n'
        '\n'
        '    # --- Prepare the ocp --- #\n'
        '    ocp = prepare_ocp()\n'
        '\n'
        '    # --- Solve the ocp --- #\n'
        '    sol = ocp.solve(solver=${solver.type.toPythonString()}())\n'
        '    sol.animate()\n'
        '\n'
        '\n'
        'if __name__ == "__main__":\n'
        '    main()\n',
        mode: FileMode.append);
  }
}
