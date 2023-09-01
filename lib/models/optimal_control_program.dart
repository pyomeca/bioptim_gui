import 'dart:io';

import 'package:bioptim_gui/models/bio_model.dart';
import 'package:bioptim_gui/models/dynamics.dart';
import 'package:bioptim_gui/models/generic_ocp_config.dart';
import 'package:bioptim_gui/models/global.dart';
import 'package:bioptim_gui/models/decision_variables.dart';
import 'package:bioptim_gui/models/penalty.dart';

class _Phase {
  int phaseIndex;
  BioModel bioModel;
  String modelPath;
  int nbShootingPoints;
  double duration;
  Dynamics dynamics;

  DecisionVariables stateVariables =
      DecisionVariables(DecisionVariableType.state);
  DecisionVariables controlVariables =
      DecisionVariables(DecisionVariableType.control);

  _Phase({
    required this.phaseIndex,
    required this.bioModel,
    required this.modelPath,
    required this.nbShootingPoints,
    required this.duration,
    required this.dynamics,
  });
}

///
/// This is the main class holder for the model. Nevertheless, this class should
/// not be instantiated manually but only by the [OptimalControlProgramController].
/// Similarly, it should not be directly access (except from the said calss).
class OptimalControlProgram {
  ///
  /// Constructor

  OptimalControlProgram() {
    updatePhases();
  }

  ///
  /// Setters and Getters

  bool _hasPendingChanges = true;
  void notifyThatModelHasChanged() => _hasPendingChanges = true;
  bool get mustExport => _hasPendingChanges;

  GenericOptimalControlProgram generic = GenericOptimalControlProgram();

  final phases = <_Phase>[];
  void updatePhases() {
    // TODO protected?
    if (phases.length < generic.nbPhases) {
      for (int i = phases.length; i < generic.nbPhases; i++) {
        phases.add(_Phase(
            phaseIndex: i,
            bioModel: BioModel.biorbd,
            modelPath: '',
            duration: 1.0,
            nbShootingPoints: 50,
            dynamics: const Dynamics(
                type: DynamicsType.torqueDriven, isExpanded: true)));
        resetVariables(phaseIndex: i);
      }
    } else {
      // Do not change anything if we already have the right number of phases

      // Do not remove the phases if they are removed from the GUI, so it can
      // be reinstated prefilled with previous data
    }
    _hasPendingChanges = true;
  }

  void resetVariables({required int phaseIndex}) {
    // TODO protected?
    phases[phaseIndex].stateVariables.clearVariables();
    for (final name in phases[phaseIndex].dynamics.type.states) {
      variables(from: DecisionVariableType.state, phaseIndex: phaseIndex)
          .addVariable(DecisionVariable(
        name: name,
        bounds: Bounds(
          nbElements: 1,
          interpolation: Interpolation.constantWithFirstAndLastDifferent,
        ),
        initialGuess:
            InitialGuess(nbElements: 1, interpolation: Interpolation.constant),
      ));
    }

    phases[phaseIndex].controlVariables.clearVariables();
    for (final name in phases[phaseIndex].dynamics.type.controls) {
      variables(from: DecisionVariableType.control, phaseIndex: phaseIndex)
          .addVariable(DecisionVariable(
        name: name,
        bounds: Bounds(
          nbElements: 1,
          interpolation: Interpolation.constantWithFirstAndLastDifferent,
        ),
        initialGuess:
            InitialGuess(nbElements: 1, interpolation: Interpolation.constant),
      ));
    }

    _hasPendingChanges = true;
  }

  DecisionVariables variables(
      // TODO protected?
      {required DecisionVariableType from,
      required int phaseIndex}) {
    switch (from) {
      case DecisionVariableType.state:
        return phases[phaseIndex].stateVariables;
      case DecisionVariableType.control:
        return phases[phaseIndex].controlVariables;
    }
  }

  DecisionVariable variable(String name,
          {required DecisionVariableType from, required int phaseIndex}) =>
      variables(from: from, phaseIndex: phaseIndex)[name];

  final List<Objective> objectives = [];
  final List<Constraint> _constraints = [];

  ///
  /// Main interface

  void exportScript(String path) {
    _hasPendingChanges = false;

    // TODO Do a proper for loop
    const phaseIndex = 0;

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
        '    bio_model = ${phases[phaseIndex].bioModel.toPythonString()}'
        '(r"${phases[phaseIndex].modelPath}")\n'
        '    n_shooting = ${phases[phaseIndex].nbShootingPoints}\n'
        '    phase_time = ${phases[phaseIndex].duration}\n'
        '\n',
        mode: FileMode.append);

    // Write the dynamics section
    file.writeAsStringSync(
        '    # Declaration of the dynamics function used during integration\n'
        '    dynamics = Dynamics(${phases[phaseIndex].dynamics.type.toPythonString()}, '
        'expand=${phases[phaseIndex].dynamics.isExpanded ? 'True' : 'False'})\n'
        '\n',
        mode: FileMode.append);

    // Write the variable section
    file.writeAsStringSync(
        '    # Declaration of optimization variables bounds and initial guesses\n',
        mode: FileMode.append);

    for (final variableType in DecisionVariableType.values) {
      final allVariables =
          variables(from: variableType, phaseIndex: phaseIndex);
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
            '        phase=$phaseIndex,\n'
            '    )'
            '\n'
            '    ${basename}_initial_guesses.add(\n'
            '        "${variable.name}",\n'
            '        initial_guess=${variable.initialGuess.guess},\n'
            '        interpolation=${variable.initialGuess.interpolation.toPythonString()},\n'
            '        phase=$phaseIndex,\n'
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
    for (final objective in objectives) {
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
        '    return ${generic.ocpType.toPythonString()}(\n'
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
        '        use_sx=${generic.useSx ? 'True' : 'False'},\n'
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
        '    sol = ocp.solve(solver=${generic.solver.type.toPythonString()}())\n'
        '    sol.animate()\n'
        '\n'
        '\n'
        'if __name__ == "__main__":\n'
        '    main()\n',
        mode: FileMode.append);
  }
}
