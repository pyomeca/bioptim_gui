import 'dart:io';

import 'package:bioptim_gui/models/bio_model.dart';
import 'package:bioptim_gui/models/dynamics.dart';
import 'package:bioptim_gui/models/generic_ocp_config.dart';
import 'package:bioptim_gui/models/global.dart';
import 'package:bioptim_gui/models/decision_variables.dart';
import 'package:bioptim_gui/models/objective_type.dart';
import 'package:bioptim_gui/models/penalty.dart';
import 'package:bioptim_gui/models/quadrature_rules.dart';
import 'package:bioptim_gui/utils.dart';

class _Phase {
  int phaseIndex;
  BioModel bioModel;
  String modelPath;
  int nbShootingPoints;
  double duration;
  Dynamics dynamics;

  final List<Objective> objectives = [];
  final List<Constraint> constraints = [];

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

  bool _hasPendingChangesToBeExported = true;
  void notifyThatModelHasChanged() => _hasPendingChangesToBeExported = true;
  bool get mustExport => _hasPendingChangesToBeExported;

  GenericOptimalControlProgram generic = GenericOptimalControlProgram();

  final phases = <_Phase>[];
  void updatePhases() {
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
    _hasPendingChangesToBeExported = true;
  }

  void resetVariables({required int phaseIndex}) {
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

    _hasPendingChangesToBeExported = true;
  }

  DecisionVariables variables(
      {required DecisionVariableType from, required int phaseIndex}) {
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

  ///
  /// Main interface

  void exportScript(String path) {
    _hasPendingChangesToBeExported = false;
    final file = File(path);

    // Write the header
    file.writeAsStringSync('"""\n'
        'This file was automatically generated using BioptimGUI version $biotimGuiVersion\n'
        '"""\n'
        '\n'
        'from bioptim import *  # TODO Pariterre - Do not import "*"\n'
        'import numpy as np\n'
        'import pickle as pkl\n'
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
    final bioModelAsString = generic.nbPhases == 1
        ? '${phases[0].bioModel.toPythonString()}(r"${phases[0].modelPath}")'
        : '${[
            for (int i = 0; i < generic.nbPhases; i++)
              '${phases[i].bioModel.toPythonString()}(r"${phases[i].modelPath}")'
          ]}';
    final nShootingAsString = generic.nbPhases == 1
        ? phases[0].nbShootingPoints.toString()
        : '${[
            for (int i = 0; i < generic.nbPhases; i++)
              phases[i].nbShootingPoints.toString()
          ]}';
    final durationAsString = generic.nbPhases == 1
        ? phases[0].duration.toString()
        : '${[
            for (int i = 0; i < generic.nbPhases; i++)
              phases[i].duration.toString()
          ]}';
    file.writeAsStringSync(
        '    # Declaration of generic elements\n'
        '    bio_model = $bioModelAsString\n'
        '    n_shooting = $nShootingAsString\n'
        '    phase_time = $durationAsString\n'
        '\n',
        mode: FileMode.append);

    file.writeAsStringSync(
        '    # Declaration of the dynamics function used during integration\n'
        '    dynamics = DynamicsList()\n\n',
        mode: FileMode.append);
    for (int phaseIndex = 0; phaseIndex < generic.nbPhases; phaseIndex++) {
      // Write the dynamics section
      file.writeAsStringSync(
          '    dynamics.add(\n'
          '        ${phases[phaseIndex].dynamics.type.toPythonString()},\n'
          '        expand=${phases[phaseIndex].dynamics.isExpanded ? 'True' : 'False'},\n'
          '${generic.nbPhases == 1 ? '' : '        phase=$phaseIndex,\n'}'
          '    )\n'
          '\n',
          mode: FileMode.append);
    }

    // Write the constraints and objectives functions
    file.writeAsStringSync(
        '    # Declaration of the constraints and objectives of the ocp\n'
        '    constraints = ConstraintList()\n'
        '    objective_functions = ObjectiveList()\n',
        mode: FileMode.append);
    for (int phaseIndex = 0; phaseIndex < generic.nbPhases; phaseIndex++) {
      for (final objective in phases[phaseIndex].objectives) {
        file.writeAsStringSync(
            '    objective_functions.add(\n'
            '        objective=${objective.fcn.toPythonString()},\n'
            '${objective.arguments.keys.isEmpty ? '' : '${objective.arguments.keys.map((key) => '        ${objective.argumentToPythonString(key)},').join('\n')}\n'}'
            '        node=${objective.nodes.toPythonString()},\n'
            '${objective.quadratic == true ? '' : '        quadratic=${objective.quadratic.toPythonString()},\n'}'
            '${objective.expand == true ? '' : '        expand=${objective.expand.toPythonString()},\n'}'
            '${objective.target == 'None' ? '' : '        target=${objective.target == 'None' ? 'None' : 'np.array([${objective.target}])'},\n'}'
            '${objective.derivative == false ? '' : '        derivative=${objective.derivative.toPythonString()},\n'}'
            '${objective.objectiveType == ObjectiveType.mayer ? '' : objective.quadratureRules == QuadratureRules.rectangleLeft ? '' : '        integration_rule=${objective.quadratureRules.toPythonString()},\n'}'
            '${objective.multiThread == false ? '' : '        multi_thread=${objective.multiThread.toPythonString()},\n'}'
            '${generic.nbPhases == 1 ? '' : '        phase=$phaseIndex,\n'}'
            '        weight=${objective.minimizeOrMaximize.toPythonString()}${objective.weight},\n'
            '    )\n',
            mode: FileMode.append);
      }
      for (final constraint in phases[phaseIndex].constraints) {
        file.writeAsStringSync(
            '    constraints.add(\n'
            '        constraint=${constraint.fcn.toPythonString()},\n'
            '${constraint.arguments.keys.isEmpty ? '' : '${constraint.arguments.keys.map((key) => '        ${constraint.argumentToPythonString(key)},').join('\n')}\n'}'
            '        node=${constraint.nodes.toPythonString()},\n'
            '${constraint.quadratic == true ? '' : '        quadratic=${constraint.quadratic.toPythonString()},\n'}'
            '${constraint.expand == true ? '' : '        expand=${constraint.expand.toPythonString()},\n'}'
            '${constraint.target == 'None' ? '' : '        target=${constraint.target == 'None' ? 'None' : 'np.array([${constraint.target}])'},\n'}'
            '${constraint.derivative == false ? '' : '        derivative=${constraint.derivative.toPythonString()},\n'}'
            '${constraint.quadratureRules == QuadratureRules.rectangleLeft ? '' : '        integration_rule=${constraint.quadratureRules.toPythonString()},\n'}'
            '${constraint.multiThread == false ? '' : '        multi_thread=${constraint.multiThread.toPythonString()},\n'}'
            '${generic.nbPhases == 1 ? '' : '        phase=$phaseIndex,\n'}'
            '${generic.nbPhases == 1 ? '' : '        phase=$phaseIndex,\n'}'
            '    )\n',
            mode: FileMode.append);
      }
    }
    file.writeAsStringSync('\n', mode: FileMode.append);

    // Write the variable section
    file.writeAsStringSync(
        '    # Declaration of optimization variables bounds and initial guesses\n',
        mode: FileMode.append);
    for (final variableType in DecisionVariableType.values) {
      final basename = variableType.toPythonString();
      file.writeAsStringSync(
          '    ${basename}_bounds = BoundsList()\n'
          '    ${basename}_initial_guesses = InitialGuessList()\n'
          '\n',
          mode: FileMode.append);
    }

    for (int phaseIndex = 0; phaseIndex < generic.nbPhases; phaseIndex++) {
      for (final variableType in DecisionVariableType.values) {
        final basename = variableType.toPythonString();
        final allVariables =
            variables(from: variableType, phaseIndex: phaseIndex);

        for (final name in allVariables.names) {
          final variable = allVariables[name];
          file.writeAsStringSync(
              '    ${basename}_bounds.add(\n'
              '        "${variable.name}",\n'
              '        min_bound=${variable.bounds.min},\n'
              '        max_bound=${variable.bounds.max},\n'
              '        interpolation=${variable.bounds.interpolation.toPythonString()},\n'
              '${generic.nbPhases == 1 ? '' : '        phase=$phaseIndex,\n'}'
              '    )'
              '\n'
              '    ${basename}_initial_guesses.add(\n'
              '        "${variable.name}",\n'
              '        initial_guess=${variable.initialGuess.guess},\n'
              '        interpolation=${variable.initialGuess.interpolation.toPythonString()},\n'
              '${generic.nbPhases == 1 ? '' : '        phase=$phaseIndex,\n'}'
              '    )\n'
              '\n',
              mode: FileMode.append);
        }
      }
      file.writeAsStringSync('\n', mode: FileMode.append);
    }

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
        'if __name__ == "__main__":\n'
        '    """\n'
        '    If this file is run, then it will perform the optimization\n'
        '    """\n'
        '\n'
        '    # --- Prepare the ocp --- #\n'
        '    ocp = prepare_ocp()\n'
        '\n'
        '    solver = Solver.IPOPT()\n'
        '    # --- Solve the ocp --- #\n'
        '    sol = ocp.solve(solver=solver)\n'
        '\n'
        '    out = sol.integrate(merge_phases=True)\n'
        '    state, time_vector = out._states["unscaled"], out._time_vector\n'
        '\n'
        '    save = {\n'
        '        "solution": sol,\n'
        '        "unscaled_state": state,\n'
        '        "time_vector": time_vector,\n'
        '    }\n'
        '\n'
        '    del sol.ocp\n'
        '    with open(f"somersault.pkl", "wb") as f:\n'
        '        pkl.dump(save, f)\n'
        '\n',
        mode: FileMode.append);
  }
}
