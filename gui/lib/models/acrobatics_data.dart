import 'dart:convert';

import 'package:bioptim_gui/models/acrobatics_controllers.dart';
import 'package:bioptim_gui/models/acrobatics_request_maker.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/models/penalty.dart';
import 'package:flutter/foundation.dart';

class AcrobaticsData extends ChangeNotifier implements OCPData {
  int _nbSomersaults;
  String _modelPath;
  double finalTime;
  double finalTimeMargin;
  String position;
  String sportType;
  String preferredTwistSide;

  List<Somersault> somersaultInfo = [];

  AcrobaticsData.fromJson(Map<String, dynamic> data)
      : _nbSomersaults = data["nb_somersaults"],
        _modelPath = data["model_path"],
        finalTime = data["final_time"],
        finalTimeMargin = data["final_time_margin"],
        position = data["position"],
        sportType = data["sport_type"],
        preferredTwistSide = data["preferred_twist_side"],
        somersaultInfo =
            (data["somersaults_info"] as List<dynamic>).map((somersault) {
          return Somersault.fromJson(somersault);
        }).toList();

  ///
  /// Getters Setters

  @override
  AcrobaticsRequestMaker get requestMaker {
    return AcrobaticsRequestMaker();
  }

  @override
  List<Phase> get phaseInfo => somersaultInfo;

  @override
  String get modelPath => _modelPath;

  @override
  int get nbPhases => _nbSomersaults;

  int get nbSomersaults => _nbSomersaults;
  set nbSomersaults(int value) {
    _nbSomersaults = value;
    notifyListeners();
  }

  ///
  /// Update methods

  @override
  void updateField(String name, String value) {
    requestMaker.updateField(name, value);

    switch (name) {
      case "nb_somersaults":
        nbSomersaults = int.parse(value);
        break;
      case "model_path":
        _modelPath = value;
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
      default:
        break;
    }
    notifyListeners();
  }

  @override
  void updatePhaseField(int phaseIndex, String fieldName, String newValue) {
    requestMaker.updatePhaseField(phaseIndex, fieldName, newValue);

    switch (fieldName) {
      case "nb_half_twists":
        somersaultInfo[phaseIndex].nbHalfTwists = int.parse(newValue);
        break;
      case "duration":
        somersaultInfo[phaseIndex].duration = double.parse(newValue);
        break;
      case "nb_shooting_points":
        somersaultInfo[phaseIndex].nbShootingPoints = int.parse(newValue);
        break;
      default:
        break;
    }
    notifyListeners();
  }

  void updateData(AcrobaticsData newData) {
    nbSomersaults = newData.nbSomersaults;
    _modelPath = newData._modelPath;
    finalTime = newData.finalTime;
    finalTimeMargin = newData.finalTimeMargin;
    position = newData.position;
    sportType = newData.sportType;
    preferredTwistSide = newData.preferredTwistSide;
    somersaultInfo = List.from(newData.somersaultInfo);

    notifyListeners();
  }

  @override
  void updatePenalties(
      int somersaultIndex, String penaltyType, List<Penalty> penalties) {
    if (penaltyType == "objective") {
      somersaultInfo[somersaultIndex].objectives = penalties as List<Objective>;
    } else {
      somersaultInfo[somersaultIndex].constraints =
          penalties as List<Constraint>;
    }
    notifyListeners();
  }

  @override
  void updatePenalty(int somersaultIndex, String penaltyType, int penaltyIndex,
      Penalty penalty) {
    if (penaltyType == "objective") {
      somersaultInfo[somersaultIndex].objectives[penaltyIndex] =
          penalty as Objective;
    } else {
      somersaultInfo[somersaultIndex].constraints[penaltyIndex] =
          penalty as Constraint;
    }

    notifyListeners();
  }

  @override
  void updatePhaseInfo(List newData) {
    final newPhases = (newData).map((p) => Somersault.fromJson(p)).toList();
    somersaultInfo = newPhases;

    notifyListeners();
  }

  @override
  void notifyListeners() {
    AcrobaticsControllers.instance.notifyListeners();
    super.notifyListeners();
  }

  @override
  void updatePenaltyArgument(
      int phaseIndex,
      int objectiveIndex,
      String argumentName,
      String? newValue,
      String argumentType,
      int argumentIndex,
      String penaltyType) {
    requestMaker.updatePenaltyArgument(phaseIndex, objectiveIndex, argumentName,
        newValue, argumentType, penaltyType);

    somersaultInfo[phaseIndex]
        .objectives[objectiveIndex]
        .arguments[argumentIndex]
        .value = newValue;

    notifyListeners();
  }

  @override
  void updatePenaltyField(int phaseIndex, int penaltyIndex, String penaltyType,
      String fieldName, dynamic newValue,
      {bool? doUpdate}) async {
    final response = await requestMaker.updatePenaltyField(
        phaseIndex, penaltyType, penaltyIndex, fieldName, newValue);

    final isObjective = penaltyType == "objectives";

    switch (fieldName) {
      case "target":
        somersaultInfo[phaseIndex].objectives[penaltyIndex].target = newValue;
        break;
      case "integration_rule":
        somersaultInfo[phaseIndex].objectives[penaltyIndex].integrationRule =
            newValue!;
        break;
      case "weight":
        somersaultInfo[phaseIndex].objectives[penaltyIndex].weight =
            double.tryParse(newValue!) ?? 0.0;
        break;
      case "nodes":
        somersaultInfo[phaseIndex].constraints[penaltyIndex].nodes = newValue!;
        break;
      case "quadratic":
        somersaultInfo[phaseIndex].constraints[penaltyIndex].quadratic =
            newValue == "true";
        break;
      case "expand":
        somersaultInfo[phaseIndex].constraints[penaltyIndex].expand =
            newValue == "true";
        break;
      case "multi_thread":
        somersaultInfo[phaseIndex].constraints[penaltyIndex].multiThread =
            newValue == "true";
        break;
      case "derivative":
        somersaultInfo[phaseIndex].constraints[penaltyIndex].derivative =
            newValue == "true";
        break;
      default:
        break;
    }

    if (doUpdate != null && doUpdate) {
      final Penalty newPenalties = isObjective
          ? Objective.fromJson(
              json.decode(response.body) as Map<String, dynamic>)
          : Constraint.fromJson(
              json.decode(response.body) as Map<String, dynamic>);

      if (isObjective) {
        updatePenalty(phaseIndex, "objective", penaltyIndex, newPenalties);
      } else {
        updatePenalty(phaseIndex, "constraint", penaltyIndex, newPenalties);
      }
    } else {
      notifyListeners();
    }
  }
}

class Somersault extends Phase {
  int nbHalfTwists;

  Somersault.fromJson(Map<String, dynamic> somersaultData)
      : nbHalfTwists = somersaultData["nb_half_twists"],
        super.fromJson(somersaultData);
}
