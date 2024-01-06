import 'package:bioptim_gui/models/generic_ocp_request_maker.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';

class GenericOcpData extends OCPData<GenericPhase> {
  GenericOcpData.fromJson(Map<String, dynamic> data)
      : super.fromJson(data, (json) => GenericPhase.fromJson(json),
            GenericOCPRequestMaker());

  ///
  /// update methods

  @override
  void updateField(String name, String value) {
    requestMaker.updateField(name, value);

    switch (name) {
      case "nb_phases":
        nbPhases = int.parse(value);
        break;
      case "model_path":
        modelPath = value;
        break;
    }
    notifyListeners();
  }

  @override
  void updatePhaseField(int phaseIndex, String fieldName, String newValue) {
    requestMaker.updatePhaseField(phaseIndex, fieldName, newValue);

    // TODO fix double calls to notifyListeners for nb_shooting_points and duration
    switch (fieldName) {
      case "dynamics":
        phasesInfo[phaseIndex].dynamics = newValue;
        break;
      case "nb_shooting_points":
        phasesInfo[phaseIndex].nbShootingPoints = int.parse(newValue);
        break;
      case "duration":
        phasesInfo[phaseIndex].duration = double.parse(newValue);
        break;
    }
    notifyListeners();
  }

  void updateData(GenericOcpData newData) {
    nbPhases = newData.nbPhases;
    modelPath = newData.modelPath;
    phasesInfo = List.from(newData.phasesInfo);

    notifyListeners();
  }

  void updateBioModelPath(String newModelPath) {
    modelPath = newModelPath;
    notifyListeners();
  }

  @override
  void notifyListeners() {
    OptimalControlProgramControllers.instance.notifyListeners();
    super.notifyListeners();
  }
}

class GenericPhase extends Phase {
  String dynamics;

  GenericPhase.fromJson(super.phaseData)
      : dynamics = phaseData["dynamics"],
        super.fromJson();
}
