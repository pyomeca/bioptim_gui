import 'package:bioptim_gui/models/bio_model.dart';

class AcrobaticsOptimalControlProgram {
  int nbSomersaults;
  BioModel bioModel;
  String modelPath;
  double finalTimeMargin;

  AcrobaticsOptimalControlProgram({
    this.nbSomersaults = 1,
    this.bioModel = BioModel.biorbd,
    this.modelPath = '',
    this.finalTimeMargin = 0.1,
  });
}
