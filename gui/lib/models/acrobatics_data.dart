import 'dart:convert';

import 'package:bioptim_gui/models/acrobatics_controllers.dart';
import 'package:bioptim_gui/models/acrobatics_request_maker.dart';
import 'package:bioptim_gui/models/ocp_data.dart';

class AcrobaticsData extends OCPData<SomersaultPhase> {
  int nbSomersaults;
  List<int> halfTwists = [];
  double finalTime;
  double finalTimeMargin;
  String position;
  String sportType;
  String preferredTwistSide;
  bool withVisualCriteria;
  bool collisionConstraint;
  bool withSpine;
  String dynamics;
  List<String> dofNames = [];

  AcrobaticsData.fromJson(Map<String, dynamic> data)
      : nbSomersaults = data["nb_somersaults"],
        halfTwists = List.from(data["nb_half_twists"]),
        finalTime = data["final_time"],
        finalTimeMargin = data["final_time_margin"],
        position = data["position"],
        sportType = data["sport_type"],
        preferredTwistSide = data["preferred_twist_side"],
        withVisualCriteria = data["with_visual_criteria"],
        collisionConstraint = data["collision_constraint"],
        withSpine = data["with_spine"],
        dynamics = data["dynamics"],
        dofNames = List.from(data["dof_names"]),
        super.fromJson(data, (json) => SomersaultPhase.fromJson(json),
            AcrobaticsRequestMaker());

  ///
  /// Update methods

  void updateHalfTwists(int index, int value) async {
    final response = await (requestMaker as AcrobaticsRequestMaker)
        .updateHalfTwists(index, value);

    final jsonData = json.decode(response.body);

    final newPhases = SomersaultPhase.convertDynamicList(jsonData);

    phasesInfo = newPhases;
    halfTwists[index] = value;
    notifyListeners();
  }

  Future<bool> updateFieldAndData(String field, String value) async {
    final response = await requestMaker.updateField(field, value);

    if (response.statusCode != 200) {
      return Future(() => false);
    }

    final newData = AcrobaticsData.fromJson(json.decode(response.body));

    updateData(newData);
    return Future(() => true);
  }

  @override
  void updateField(String name, dynamic value) async {
    final response = await requestMaker.updateField(name, value);

    if (response.statusCode != 200) throw Exception('Failed to update $name');

    final jsonData = json.decode(response.body);

    switch (name) {
      case "nb_somersaults":
      case "position":
        nbSomersaults = jsonData["nb_somersaults"];
        halfTwists = List.from(jsonData["nb_half_twists"]);
        position = jsonData["position"];
        dofNames = List.from(jsonData["dof_names"]);
        phasesInfo =
            SomersaultPhase.convertDynamicList(jsonData["phases_info"]);
        break;
      case "final_time":
        finalTime = jsonData["final_time"];
        for (var i = 0; i < phasesInfo.length; i++) {
          phasesInfo[i].duration = jsonData["new_phase_duration"];
        }
        break;
      case "final_time_margin":
        finalTimeMargin = jsonData["final_time_margin"];
        break;
      case "sport_type":
        sportType = jsonData["sport_type"];
        break;
      case "preferred_twist_side":
        preferredTwistSide = jsonData["preferred_twist_side"];
        break;
      case "with_visual_criteria":
        withVisualCriteria = jsonData["with_visual_criteria"];
        dofNames = List.from(jsonData["dof_names"]);
        phasesInfo =
            SomersaultPhase.convertDynamicList(jsonData["phases_info"]);
        break;
      case "collision_constraint":
        collisionConstraint = jsonData["collision_constraint"];
        phasesInfo =
            SomersaultPhase.convertDynamicList(jsonData["phases_info"]);
        break;
      case "with_spine":
        withSpine = jsonData["with_spine"];
        dynamics = jsonData["dynamics"];
        dofNames = List.from(jsonData["dof_names"]);
        phasesInfo =
            SomersaultPhase.convertDynamicList(jsonData["phases_info"]);
        break;
      case "dynamics":
        dynamics = jsonData["dynamics"];
        phasesInfo =
            SomersaultPhase.convertDynamicList(jsonData["phases_info"]);
        break;
      // model_path is not updated here because it is a special case, it has to
      // be send as a multipart file request
      // It is currently updated using requestMaker.updateBioModel
      case "model_path":
        break;
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
    final jsonData = json.decode(response.body);

    switch (fieldName) {
      case "duration":
        phasesInfo[phaseIndex].duration = jsonData["duration"];
        finalTime = jsonData["new_final_time"];
        break;
      case "nb_shooting_points":
        phasesInfo[phaseIndex].nbShootingPoints =
            jsonData["nb_shooting_points"];
        break;
      default:
        break;
    }
    notifyListeners();
  }

  void updateData(AcrobaticsData newData) {
    nbSomersaults = newData.nbSomersaults;
    halfTwists = List.from(newData.halfTwists);
    modelPath = newData.modelPath;
    finalTime = newData.finalTime;
    finalTimeMargin = newData.finalTimeMargin;
    position = newData.position;
    sportType = newData.sportType;
    preferredTwistSide = newData.preferredTwistSide;
    withVisualCriteria = newData.withVisualCriteria;
    collisionConstraint = newData.collisionConstraint;
    withSpine = newData.withSpine;
    dynamics = newData.dynamics;
    dofNames = List.from(newData.dofNames);
    phasesInfo = List.from(newData.phasesInfo);

    notifyListeners();
  }

  @override
  void notifyListeners() {
    AcrobaticsControllers.instance.notifyListeners();
    super.notifyListeners();
  }
}

class SomersaultPhase extends Phase {
  SomersaultPhase.fromJson(super.somersaultData) : super.fromJson();

  static List<SomersaultPhase> convertDynamicList(List<dynamic> list) {
    return list.map((item) => SomersaultPhase.fromJson(item)).toList();
  }
}
