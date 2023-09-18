import 'package:bioptim_gui/models/optimal_control_program_type.dart';
import 'package:bioptim_gui/models/solver.dart';
import 'package:bioptim_gui/models/bio_model.dart';

class AcrobaticsOptimalControlProgram {
  OptimalControlProgramType ocpType;
  int nbSomersaults;
  bool useSx;
  BioModel bioModel;
  String modelPath;
  Solver solver;

  AcrobaticsOptimalControlProgram({
    this.ocpType = OptimalControlProgramType.ocp,
    this.nbSomersaults = 1,
    this.solver = const Solver(type: SolverType.ipopt),
    this.useSx = true,
    this.bioModel = BioModel.biorbd,
    this.modelPath = '',
  });
}
