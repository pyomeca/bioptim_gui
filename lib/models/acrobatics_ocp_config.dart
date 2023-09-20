import 'package:bioptim_gui/models/acrobatics_position.dart';
import 'package:bioptim_gui/models/acrobatics_sport_type.dart';
import 'package:bioptim_gui/models/acrobatics_twist_side.dart';
import 'package:bioptim_gui/models/bio_model.dart';

class AcrobaticsOptimalControlProgram {
  int nbSomersaults;
  BioModel bioModel;
  String modelPath;
  double finalTime;
  double finalTimeMargin;
  AcrobaticsPosition position;
  AcrobaticsSportType sportType;
  PreferredTwistSide preferredTwistSide;

  AcrobaticsOptimalControlProgram({
    this.nbSomersaults = 1,
    this.bioModel = BioModel.biorbd,
    this.modelPath = '',
    this.finalTime = 1.0,
    this.finalTimeMargin = 0.1,
    this.position = AcrobaticsPosition.straight,
    this.sportType = AcrobaticsSportType.trampoline,
    this.preferredTwistSide = PreferredTwistSide.left,
  });
}
