import 'dart:convert';

import 'package:bioptim_gui/models/ocp_request_maker.dart';
import 'package:bioptim_gui/models/penalty.dart';
import 'package:bioptim_gui/models/variables.dart';
import 'package:flutter/material.dart';

///
/// [OCPData] represents the most generic OCP data. It is used to be inherited
/// by "generic OCP" [GenericOcpData] and "acrobatics data" [AcrobaticsData].
/// It will be used in [Consumer] to provide the data to the widgets that
/// display the data that can be common to both OCPs. (penalties for now)
abstract class OCPData<T extends Phase> with ChangeNotifier {
  int nbPhases;
  String modelPath;
  List<T> phasesInfo = [];
  T Function(Map<String, dynamic>) phaseFromJsonFunction;
  final OCPRequestMaker _requestMaker;
  OCPAvailableValues? availablesValue;

  OCPData.fromJson(
    Map<String, dynamic> data,
    this.phaseFromJsonFunction,
    this._requestMaker,
  )   : nbPhases = data["nb_phases"],
        modelPath = data["model_path"],
        phasesInfo = (data["phases_info"] as List<dynamic>).map((phase) {
          return phaseFromJsonFunction(phase);
        }).toList();

  OCPRequestMaker get requestMaker {
    notifyListeners();
    return _requestMaker;
  }

  ///
  /// Update methods

  void updateField(String name, String value);
  void updatePhaseField(int phaseIndex, String fieldName, String newValue);

  void updatePhaseInfo(List<dynamic> newData) {
    final newPhases = (newData).map((p) => phaseFromJsonFunction(p)).toList();

    phasesInfo = newPhases;

    notifyListeners();
  }

  void updatePenalties(
      int phaseIndex, String penaltyType, List<Penalty> penalties) {
    if (penaltyType == "objective") {
      phasesInfo[phaseIndex].objectives = penalties as List<Objective>;
    } else {
      phasesInfo[phaseIndex].constraints = penalties as List<Constraint>;
    }
    notifyListeners();
  }

  void updatePenalty(
      int phaseIndex, String penaltyType, int penaltyIndex, Penalty penalty) {
    final oldPenalty = penaltyType == "objective"
        ? phasesInfo[phaseIndex].objectives[penaltyIndex]
        : phasesInfo[phaseIndex].constraints[penaltyIndex];

    final newPenaltyType = penalty.penaltyType;
    final oldPenaltyType = oldPenalty.penaltyType;
    final penaltyTypeChanged = newPenaltyType != oldPenaltyType;

    final objectiveTypeChanged = penaltyType == "objective"
        ? (penalty as Objective).objectiveType !=
            (oldPenalty as Objective).objectiveType
        : false;

    final minMaxChanged = penaltyType == "objective"
        ? (penalty as Objective).weight * (oldPenalty as Objective).weight > 0
        : false;

    // keep expanded value
    penalty.expanded = penaltyType == "objective"
        ? phasesInfo[phaseIndex].objectives[penaltyIndex].expanded
        : phasesInfo[phaseIndex].constraints[penaltyIndex].expanded;

    if (penaltyType == "objective") {
      phasesInfo[phaseIndex].objectives[penaltyIndex] = penalty as Objective;
    } else {
      phasesInfo[phaseIndex].constraints[penaltyIndex] = penalty as Constraint;
    }

    // force redraw only if the penalty type or objective type if it's an objective
    // changes (to update arguments and other fields)
    if (penaltyTypeChanged || objectiveTypeChanged || minMaxChanged) {
      notifyListeners();
    }
  }

  Future<bool> updatePenaltyField(int phaseIndex, int penaltyIndex,
      String penaltyType, String fieldName, dynamic newValue,
      {bool? doUpdate}) async {
    final response = await requestMaker.updatePenaltyField(
        phaseIndex, penaltyType, penaltyIndex, fieldName, newValue);

    if (response.statusCode != 200) {
      return Future(() => false);
    }

    final isObjective = penaltyType == "objectives";

    switch (fieldName) {
      case "target":
        phasesInfo[phaseIndex].objectives[penaltyIndex].target = newValue;
        break;
      case "integration_rule":
        phasesInfo[phaseIndex].objectives[penaltyIndex].integrationRule =
            newValue!;
        break;
      case "weight":
        phasesInfo[phaseIndex].objectives[penaltyIndex].weight =
            double.tryParse(newValue!) ?? 0.0;
        break;
      case "nodes":
        phasesInfo[phaseIndex].constraints[penaltyIndex].nodes = newValue!;
        break;
      case "quadratic":
        phasesInfo[phaseIndex].constraints[penaltyIndex].quadratic =
            newValue == "true";
        break;
      case "expand":
        phasesInfo[phaseIndex].constraints[penaltyIndex].expand =
            newValue == "true";
        break;
      case "multi_thread":
        phasesInfo[phaseIndex].constraints[penaltyIndex].multiThread =
            newValue == "true";
        break;
      case "derivative":
        phasesInfo[phaseIndex].constraints[penaltyIndex].derivative =
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

      // keep expanded value
      newPenalties.expand = penaltyType == "objectives"
          ? phasesInfo[phaseIndex].objectives[penaltyIndex].expanded
          : phasesInfo[phaseIndex].constraints[penaltyIndex].expanded;

      if (isObjective) {
        updatePenalty(phaseIndex, "objective", penaltyIndex, newPenalties);
      } else {
        updatePenalty(phaseIndex, "constraint", penaltyIndex, newPenalties);
      }
    } else {
      notifyListeners();
    }

    return Future(() => true);
  }

  void updatePenaltyArgument(
      int phaseIndex,
      int penaltyIndex,
      String argumentName,
      String? newValue,
      String argumentType,
      int argumentIndex,
      String penaltyType) {
    requestMaker.updatePenaltyArgument(phaseIndex, penaltyIndex, argumentName,
        newValue, argumentType, penaltyType);

    phasesInfo[phaseIndex]
        .objectives[penaltyIndex]
        .arguments[argumentIndex]
        .value = newValue;

    notifyListeners();
  }
}

///
/// [Phase] represents the most generic phase of an OCP with the least amount of
/// information. For now, It is used to be inherited by "phases" for
/// "generic OCP"'s [GenericPhase] and "acrobatics OCP" [Somersault] that may
/// contain additional fields.
abstract class Phase {
  late String? phaseName;
  late int nbShootingPoints;
  late double duration;
  late List<Objective> objectives;
  late List<Constraint> constraints;
  List<Variable> stateVariables;
  List<Variable> controlVariables;

  Phase.fromJson(Map<String, dynamic> phaseData)
      : phaseName = phaseData["phase_name"],
        nbShootingPoints = phaseData["nb_shooting_points"],
        duration = phaseData["duration"],
        objectives =
            (phaseData["objectives"] as List<dynamic>).map((objective) {
          return Objective.fromJson(objective);
        }).toList(),
        constraints =
            (phaseData["constraints"] as List<dynamic>).map((constraint) {
          return Constraint.fromJson(constraint);
        }).toList(),
        stateVariables =
            (phaseData["state_variables"] as List<dynamic>).map((variable) {
          return Variable.fromJson(variable);
        }).toList(),
        controlVariables =
            (phaseData["control_variables"] as List<dynamic>).map((variable) {
          return Variable.fromJson(variable);
        }).toList();
}

///
/// [OCPAvailableValues] represents the available values for the dropdowns,
/// they can be used for performance reasons
class OCPAvailableValues {
  List<String> nodes = [];
  List<String> integrationRules = [];

  OCPAvailableValues(
    this.nodes,
    this.integrationRules,
  );
}
