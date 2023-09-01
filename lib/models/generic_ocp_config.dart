import 'package:bioptim_gui/models/optimal_control_program_type.dart';
import 'package:bioptim_gui/models/solver.dart';

class GenericOptimalControlProgram {
  OptimalControlProgramType ocpType;
  int nbPhases;
  bool useSx;
  Solver solver;

  GenericOptimalControlProgram({
    this.ocpType = OptimalControlProgramType.ocp,
    this.nbPhases = 1,
    this.solver = const Solver(type: SolverType.ipopt),
    this.useSx = true,
  });
}
