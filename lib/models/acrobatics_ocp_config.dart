import 'package:bioptim_gui/models/acrobatics_position.dart';
import 'package:bioptim_gui/models/acrobatics_sport_type.dart';
import 'package:bioptim_gui/models/bio_model.dart';

class AcrobaticsOptimalControlProgram {
  int nbSomersaults;
  BioModel bioModel;
  String modelPath;
  double finalTimeMargin;
  AcrobaticsPosition position;
  AcrobaticsSportType sportType;

  AcrobaticsOptimalControlProgram({
    this.nbSomersaults = 1,
    this.bioModel = BioModel.biorbd,
    this.modelPath = '',
    this.finalTimeMargin = 0.1,
    this.position = AcrobaticsPosition.straight,
    this.sportType = AcrobaticsSportType.trampoline,
  });
}