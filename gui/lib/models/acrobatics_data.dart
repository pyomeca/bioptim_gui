import 'dart:convert';

import 'package:bioptim_gui/models/acrobatics_controllers.dart';
import 'package:bioptim_gui/models/acrobatics_request_maker.dart';
import 'package:bioptim_gui/models/ocp_data.dart';

class AcrobaticsData extends OCPData<SomersaultPhase> {
  int _nbSomersaults;
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

  AcrobaticsData.fromJson(Map<String, dynamic> data)
      : _nbSomersaults = data["nb_somersaults"],
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
        super.fromJson(data, (json) => SomersaultPhase.fromJson(json),
            AcrobaticsRequestMaker());

  ///
  /// Getters Setters

  int get nbSomersaults => _nbSomersaults;
  set nbSomersaults(int value) {
    _nbSomersaults = value;
    notifyListeners();
  }

  ///
  /// Update methods

  void updateHalfTwists(int index, int value) async {
    final response = await requestMaker.updateHalfTwists(index, value);

    final newPhases = (json.decode(response.body) as List<dynamic>)
        .map((p) => SomersaultPhase.fromJson(p))
        .toList();

    phasesInfo = newPhases;

    halfTwists[index] = value;
    notifyListeners();
  }

  void updateDynamics(String value) async {
    final response = await requestMaker.updateField("dynamics", value);

    final newPhases = (json.decode(response.body) as List<dynamic>)
        .map((p) => SomersaultPhase.fromJson(p))
        .toList();

    phasesInfo = newPhases;
    dynamics = value;
    notifyListeners();
  }

  Future<bool> updatePosition(String value) async {
    final response = await requestMaker.updateField("position", value);

    if (response.statusCode != 200) {
      return Future(() => false);
    }

    final newData = AcrobaticsData.fromJson(json.decode(response.body));

    updateData(newData);
    return Future(() => true);
  }

  @override
  void updateField(String name, String value) {
    requestMaker.updateField(name, value);

    switch (name) {
      case "nb_somersaults":
        nbSomersaults = int.parse(value);
        break;
      case "final_time":
        finalTime = double.parse(value);
        break;
      case "final_time_margin":
        finalTimeMargin = double.parse(value);
        break;
      case "position":
        position = value;
        break;
      case "sport_type":
        sportType = value;
        break;
      case "preferred_twist_side":
        preferredTwistSide = value;
        break;
      case "with_visual_criteria":
        withVisualCriteria = value == "true";
        break;
      case "collision_constraint":
        collisionConstraint = value == "true";
        break;
      case "with_spine":
        withSpine = value == "true";
        break;
      case "dynamics":
        dynamics = value;
        break;
      default:
        break;
    }
    notifyListeners();
  }

  @override
  void updatePhaseField(int phaseIndex, String fieldName, String newValue) {
    requestMaker.updatePhaseField(phaseIndex, fieldName, newValue);

    switch (fieldName) {
      case "duration":
        phasesInfo[phaseIndex].duration = double.parse(newValue);
        break;
      case "nb_shooting_points":
        phasesInfo[phaseIndex].nbShootingPoints = int.parse(newValue);
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
}
