import 'package:bioptim_gui/models/bio_model.dart';

class AcrobaticsOptimalControlProgram {
  int nbSomersaults;
  BioModel bioModel;
  String modelPath;

  AcrobaticsOptimalControlProgram({
    this.nbSomersaults = 1,
    this.bioModel = BioModel.biorbd,
    this.modelPath = '',
  });
}
