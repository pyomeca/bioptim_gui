import 'package:bioptim_gui/models/optimal_control_program_type.dart';

class GenericOptimalControlProgram {
  OptimalControlProgramType ocpType;

  GenericOptimalControlProgram({
    this.ocpType = OptimalControlProgramType.ocp,
  });
}
