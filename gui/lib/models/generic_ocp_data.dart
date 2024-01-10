import 'dart:convert';

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
  void updateField(String name, dynamic value) async {
    final response = await requestMaker.updateField(name, value);
    if (response.statusCode != 200) {
      throw Exception("Failed to update field $name with value $value");
    }

    final jsonData = json.decode(response.body);

    switch (name) {
      case "nb_phases":
        nbPhases = jsonData["nb_phases"];
        break;
      // model_path is not updated here because it is a special case, it has to
      // be send as a multipart file request
      // It is currently updated using requestMaker.updateBioModel
      case "model_path":
      default:
        break;
    }
    notifyListeners();
  }

  @override
  void updatePhaseField(
      int phaseIndex, String fieldName, dynamic newValue) async {
    final response =
        await requestMaker.updatePhaseField(phaseIndex, fieldName, newValue);
    if (response.statusCode != 200) {
      throw Exception(
          "Failed to update field $fieldName of phase $phaseIndex with value $newValue");
    }

    final jsonData = json.decode(response.body);

    switch (fieldName) {
      case "dynamics":
        phasesInfo[phaseIndex].dynamics = jsonData["dynamics"];
        phasesInfo[phaseIndex] = GenericPhase.fromJson(jsonData["phase"]);
        break;
      case "nb_shooting_points":
        phasesInfo[phaseIndex].nbShootingPoints =
            jsonData["nb_shooting_points"];
        break;
      case "duration":
        phasesInfo[phaseIndex].duration = jsonData["duration"];
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

  static List<GenericPhase> convertDynamicList(List<dynamic> list) {
    return list.map((item) => GenericPhase.fromJson(item)).toList();
  }
}
