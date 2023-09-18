import 'package:bioptim_gui/models/acrobatics_ocp_config.dart';
import 'package:bioptim_gui/models/dynamics.dart';
import 'package:bioptim_gui/models/decision_variables.dart';
import 'package:bioptim_gui/models/penalty.dart';

class _Somersault {
  int phaseIndex;
  int nbShootingPoints;
  int nbHalfTwists;
  double duration;
  Dynamics dynamics;

  final List<Objective> objectives = [];
  final List<Constraint> constraints = [];

  DecisionVariables stateVariables =
      DecisionVariables(DecisionVariableType.state);
  DecisionVariables controlVariables =
      DecisionVariables(DecisionVariableType.control);

  _Somersault({
    required this.phaseIndex,
    required this.nbShootingPoints,
    required this.nbHalfTwists,
    required this.duration,
    required this.dynamics,
  });
}

///
/// This is the main class holder for the model. Nevertheless, this class should
/// not be instantiated manually but only by the [AcrobaticsOCPController].
/// Similarly, it should not be directly access (except from the said calss).
class AcrobaticsOCPProgram {
  ///
  /// Constructor

  AcrobaticsOCPProgram() {
    updateSomersaults();
  }

  ///
  /// Setters and Getters

  bool _hasPendingChangesToBeExported = true;
  void notifyThatModelHasChanged() => _hasPendingChangesToBeExported = true;
  bool get mustExport => _hasPendingChangesToBeExported;

  AcrobaticsOptimalControlProgram generic = AcrobaticsOptimalControlProgram();

  final somersaults = <_Somersault>[];
  void updateSomersaults() {
    if (somersaults.length < generic.nbSomersaults) {
      for (int i = somersaults.length; i < generic.nbSomersaults; i++) {
        somersaults.add(_Somersault(
            phaseIndex: i,
            duration: 1.0,
            nbShootingPoints: 50,
            nbHalfTwists: 0,
            dynamics: const Dynamics(
                type: DynamicsType.torqueDriven, isExpanded: true)));
        resetVariables(somersaultIndex: i);
      }
    } else {
      // Do not change anything if we already have the right number of somersaults

      // Do not remove the somersaults if they are removed from the GUI, so it can
      // be reinstated prefilled with previous data
    }
    _hasPendingChangesToBeExported = true;
  }

  void resetVariables({required int somersaultIndex}) {
    somersaults[somersaultIndex].stateVariables.clearVariables();
    for (final name in somersaults[somersaultIndex].dynamics.type.states) {
      variables(
              from: DecisionVariableType.state,
              somersaultIndex: somersaultIndex)
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

    somersaults[somersaultIndex].controlVariables.clearVariables();
    for (final name in somersaults[somersaultIndex].dynamics.type.controls) {
      variables(
              from: DecisionVariableType.control,
              somersaultIndex: somersaultIndex)
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
      {required DecisionVariableType from, required int somersaultIndex}) {
    switch (from) {
      case DecisionVariableType.state:
        return somersaults[somersaultIndex].stateVariables;
      case DecisionVariableType.control:
        return somersaults[somersaultIndex].controlVariables;
    }
  }

  DecisionVariable variable(String name,
          {required DecisionVariableType from, required int somersaultIndex}) =>
      variables(from: from, somersaultIndex: somersaultIndex)[name];

  ///
  /// Main interface

  void exportScript(String path) {}
  //   _hasPendingChangesToBeExported = false;
  //   final file = File(path);

  //   // Write the header
  //   file.writeAsStringSync('"""\n'
  //       'This file was automatically generated using BioptimGUI version $biotimGuiVersion\n'
  //       '"""\n'
  //       '\n'
  //       'from bioptim import *  # TODO Pariterre - Do not import "*"\n'
  //       '\n'
  //       '\n');

  //   // Write the docstring of the prepare_ocp section
  //   file.writeAsStringSync(
  //       'def prepare_ocp():\n'
  //       '    """\n'
  //       '    This function build an optimal control program and instantiate it.\n'
  //       '    It can be seen as a factory for the OptimalControlProgram class.\n'
  //       '\n'
  //       '    Parameters\n'
  //       '    ----------\n'
  //       '    # TODO fill this section\n'
  //       '\n'
  //       '    Returns\n'
  //       '    -------\n'
  //       '    The OptimalControlProgram ready to be solved\n'
  //       '    """\n'
  //       '\n',
  //       mode: FileMode.append);

  //   // Write the Generic section
  //   final bioModelAsString = generic.nbPhases == 1
  //       ? '${phases[0].bioModel.toPythonString()}(r"${phases[0].modelPath}")'
  //       : '${[
  //           for (int i = 0; i < generic.nbPhases; i++)
  //             '${phases[i].bioModel.toPythonString()}(r"${phases[i].modelPath}")'
  //         ]}';
  //   final nShootingAsString = generic.nbPhases == 1
  //       ? phases[0].nbShootingPoints.toString()
  //       : '${[
  //           for (int i = 0; i < generic.nbPhases; i++)
  //             phases[i].nbShootingPoints.toString()
  //         ]}';
  //   final durationAsString = generic.nbPhases == 1
  //       ? phases[0].duration.toString()
  //       : '${[
  //           for (int i = 0; i < generic.nbPhases; i++)
  //             phases[i].duration.toString()
  //         ]}';
  //   file.writeAsStringSync(
  //       '    # Declaration of generic elements\n'
  //       '    bio_model = $bioModelAsString\n'
  //       '    n_shooting = $nShootingAsString\n'
  //       '    phase_time = $durationAsString\n'
  //       '\n',
  //       mode: FileMode.append);

  //   file.writeAsStringSync(
  //       '    # Declaration of the dynamics function used during integration\n'
  //       '    dynamics = DynamicsList()\n\n',
  //       mode: FileMode.append);
  //   for (int phaseIndex = 0; phaseIndex < generic.nbPhases; phaseIndex++) {
  //     // Write the dynamics section
  //     file.writeAsStringSync(
  //         '    dynamics.add(\n'
  //         '        ${phases[phaseIndex].dynamics.type.toPythonString()},\n'
  //         '        expand=${phases[phaseIndex].dynamics.isExpanded ? 'True' : 'False'},\n'
  //         '${generic.nbPhases == 1 ? '' : '        phase=$phaseIndex,\n'}'
  //         '    )\n'
  //         '\n',
  //         mode: FileMode.append);
  //   }

  //   // Write the constraints and objectives functions
  //   file.writeAsStringSync(
  //       '    # Declaration of the constraints and objectives of the ocp\n'
  //       '    constraints = ConstraintList()\n'
  //       '    objective_functions = ObjectiveList()\n',
  //       mode: FileMode.append);
  //   for (int phaseIndex = 0; phaseIndex < generic.nbPhases; phaseIndex++) {
  //     for (final objective in phases[phaseIndex].objectives) {
  //       file.writeAsStringSync(
  //           '    objective_functions.add(\n'
  //           '        objective=${objective.fcn.toPythonString()},\n'
  //           '${objective.arguments.keys.isEmpty ? '' : '${objective.arguments.keys.map((key) => '        ${objective.argumentToPythonString(key)},').join('\n')}\n'}'
  //           '        node=${objective.nodes.toPythonString()},\n'
  //           '${generic.nbPhases == 1 ? '' : '        phase=$phaseIndex,\n'}'
  //           '        weight=${objective.weight},\n'
  //           '    )\n',
  //           mode: FileMode.append);
  //     }
  //     for (final constraint in phases[phaseIndex].constraints) {
  //       file.writeAsStringSync(
  //           '    constraints.add(\n'
  //           '        constraint=${constraint.fcn.toPythonString()},\n'
  //           '${constraint.arguments.keys.isEmpty ? '' : '${constraint.arguments.keys.map((key) => '        ${constraint.argumentToPythonString(key)},').join('\n')}\n'}'
  //           '        node=${constraint.nodes.toPythonString()},\n'
  //           '${generic.nbPhases == 1 ? '' : '        phase=$phaseIndex,\n'}'
  //           '    )\n',
  //           mode: FileMode.append);
  //     }
  //   }
  //   file.writeAsStringSync('\n', mode: FileMode.append);

  //   // Write the variable section
  //   file.writeAsStringSync(
  //       '    # Declaration of optimization variables bounds and initial guesses\n',
  //       mode: FileMode.append);
  //   for (final variableType in DecisionVariableType.values) {
  //     final basename = variableType.toPythonString();
  //     file.writeAsStringSync(
  //         '    ${basename}_bounds = BoundsList()\n'
  //         '    ${basename}_initial_guesses = InitialGuessList()\n'
  //         '\n',
  //         mode: FileMode.append);
  //   }

  //   for (int phaseIndex = 0; phaseIndex < generic.nbPhases; phaseIndex++) {
  //     for (final variableType in DecisionVariableType.values) {
  //       final basename = variableType.toPythonString();
  //       final allVariables =
  //           variables(from: variableType, phaseIndex: phaseIndex);

  //       for (final name in allVariables.names) {
  //         final variable = allVariables[name];
  //         file.writeAsStringSync(
  //             '    ${basename}_bounds.add(\n'
  //             '        "${variable.name}",\n'
  //             '        min_bound=${variable.bounds.min},\n'
  //             '        max_bound=${variable.bounds.max},\n'
  //             '        interpolation=${variable.bounds.interpolation.toPythonString()},\n'
  //             '${generic.nbPhases == 1 ? '' : '        phase=$phaseIndex,\n'}'
  //             '    )'
  //             '\n'
  //             '    ${basename}_initial_guesses.add(\n'
  //             '        "${variable.name}",\n'
  //             '        initial_guess=${variable.initialGuess.guess},\n'
  //             '        interpolation=${variable.initialGuess.interpolation.toPythonString()},\n'
  //             '${generic.nbPhases == 1 ? '' : '        phase=$phaseIndex,\n'}'
  //             '    )\n'
  //             '\n',
  //             mode: FileMode.append);
  //       }
  //     }
  //     file.writeAsStringSync('\n', mode: FileMode.append);
  //   }

  //   // Write the return section
  //   file.writeAsStringSync(
  //       '    # Construct and return the optimal control program (OCP)\n'
  //       '    return ${generic.ocpType.toPythonString()}(\n'
  //       '        bio_model=bio_model,\n'
  //       '        n_shooting=n_shooting,\n'
  //       '        phase_time=phase_time,\n'
  //       '        dynamics=dynamics,\n'
  //       '        x_bounds=x_bounds,\n'
  //       '        u_bounds=u_bounds,\n'
  //       '        x_init=x_initial_guesses,\n'
  //       '        u_init=u_initial_guesses,\n'
  //       '        constraints=constraints,\n'
  //       '        objective_functions=objective_functions,\n'
  //       '        use_sx=${generic.useSx ? 'True' : 'False'},\n'
  //       '    )\n'
  //       '\n'
  //       '\n',
  //       mode: FileMode.append);

  //   // Write run as a script section
  //   file.writeAsStringSync(
  //       'def main():\n'
  //       '    """\n'
  //       '    If this file is run, then it will perform the optimization\n'
  //       '    """\n'
  //       '\n'
  //       '    # --- Prepare the ocp --- #\n'
  //       '    ocp = prepare_ocp()\n'
  //       '\n'
  //       '    # --- Solve the ocp --- #\n'
  //       '    sol = ocp.solve(solver=${generic.solver.type.toPythonString()}())\n'
  //       '    sol.animate()\n'
  //       '\n'
  //       '\n'
  //       'if __name__ == "__main__":\n'
  //       '    main()\n',
  //       mode: FileMode.append);
  // }
}
