import 'dart:convert';
import 'dart:io';

import 'package:bioptim_gui/models/decision_variable_value_type.dart';
import 'package:bioptim_gui/models/decision_variables_type.dart';
import 'package:bioptim_gui/models/ocp_request_maker.dart';
import 'package:bioptim_gui/models/penalty.dart';
import 'package:bioptim_gui/models/variables.dart';
import 'package:flutter/material.dart';

///
/// [OCPData] represents the most generic OCP data. It is used to be inherited
/// by "generic OCP" [GenericOcpData] and "acrobatics data" [AcrobaticsData].
/// It will be used in [Consumer] to provide the data to the widgets that
/// display the data that can be common to both OCPs. (penalties for now)
/// requestMaker MUST NOT be access by other classes than [OCPData] and its
/// children.
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
    return _requestMaker;
  }

  ///
  /// Update methods

  void updateField(String name, String value);
  void updatePhaseField(int phaseIndex, String fieldName, dynamic newValue);

  void updatePhaseInfo(List<dynamic> newData) {
    final newPhases = (newData).map((p) => phaseFromJsonFunction(p)).toList();
    phasesInfo = newPhases;
  }

  void updateBioModel(List<File> files) {
    requestMaker.updateBioModel(files);
    notifyListeners();
  }

  void updatePenalties(
      int phaseIndex, Type penaltyType, List<Penalty> penalties) {
    if (penaltyType == Objective) {
      phasesInfo[phaseIndex].objectives = penalties as List<Objective>;
    } else {
      phasesInfo[phaseIndex].constraints = penalties as List<Constraint>;
    }
    notifyListeners();
  }

  void updatePenaltyField(
    int phaseIndex,
    int penaltyIndex,
    Type penaltyType,
    String fieldName,
    dynamic newValue,
  ) async {
    final response = await requestMaker.updatePenaltyField(
        phaseIndex, penaltyType, penaltyIndex, fieldName, newValue);

    if (response.statusCode != 200) {
      throw Exception("Failed to update penalty field $fieldName");
    }

    final jsonData = json.decode(response.body);
    final isObjective = penaltyType == Objective;
    final penalty = isObjective
        ? phasesInfo[phaseIndex].objectives[penaltyIndex]
        : phasesInfo[phaseIndex].constraints[penaltyIndex];

    switch (fieldName) {
      case "target":
        penalty.target = newValue;
        break;
      case "weight":
        (penalty as Objective).weight = jsonData["weight"];
        break;
      case "quadratic":
        penalty.quadratic = jsonData["quadratic"];
        break;
      case "expand":
        penalty.expand = jsonData["expand"];
        break;
      case "multi_thread":
        penalty.multiThread = jsonData["multi_thread"];
        break;
      case "derivative":
        penalty.derivative = jsonData["derivative"];
        break;
      case "integration_rule":
        penalty.integrationRule = jsonData["integration_rule"];
        break;
      case "objective_type" || "penalty_type":
        final Penalty newPenalty = isObjective
            ? Objective.fromJson(jsonData as Map<String, dynamic>)
            : Constraint.fromJson(jsonData as Map<String, dynamic>);
        // keep expanded value
        newPenalty.expanded = penalty.expanded;
        if (isObjective) {
          phasesInfo[phaseIndex].objectives[penaltyIndex] =
              newPenalty as Objective;
        } else {
          phasesInfo[phaseIndex].constraints[penaltyIndex] =
              newPenalty as Constraint;
        }
        break;
      default:
        break;
    }

    notifyListeners();
  }

  void updatePenaltyArgument(
      int phaseIndex,
      int penaltyIndex,
      String argumentName,
      dynamic newValue,
      String argumentType,
      int argumentIndex,
      Type penaltyType) async {
    final response = await requestMaker.updatePenaltyArgument(phaseIndex,
        penaltyIndex, argumentName, newValue, argumentType, penaltyType);

    if (response.statusCode != 200) {
      throw Exception("Failed to update penalty argument $argumentName");
    }

    final jsonData = json.decode(response.body);

    if (penaltyType == Objective) {
      phasesInfo[phaseIndex]
          .objectives[penaltyIndex]
          .arguments[argumentIndex]
          .value = jsonData["value"];
    } else {
      phasesInfo[phaseIndex]
          .constraints[penaltyIndex]
          .arguments[argumentIndex]
          .value = jsonData["value"];
    }

    notifyListeners();
  }

  void updateMaximizeMinimize(
      int phaseIndex, int penaltyIndex, String newValue) async {
    final response = await requestMaker.updateMaximizeMinimize(
        phaseIndex, penaltyIndex, newValue);

    if (response.statusCode != 200) {
      throw Exception("Failed to update maximize/minimize");
    }

    final jsonData = json.decode(response.body);

    final Objective newObjective =
        Objective.fromJson(jsonData as Map<String, dynamic>);

    // keep expanded value
    newObjective.expanded =
        phasesInfo[phaseIndex].objectives[penaltyIndex].expanded;

    phasesInfo[phaseIndex].objectives[penaltyIndex] = newObjective;

    notifyListeners();
  }

  void updateDecisionVariableField(
      int phaseIndex,
      DecisionVariableType decisionVariableType,
      int variableIndex,
      String fieldName,
      dynamic newValue) async {
    final response = await requestMaker.updateDecisionVariableField(
        phaseIndex, decisionVariableType, variableIndex, fieldName, newValue);

    if (response.statusCode != 200) {
      throw Exception("Failed to update $fieldName to value $newValue");
    }

    final jsonData = json.decode(response.body);

    switch (fieldName) {
      case "bounds_interpolation_type":
        updatePhaseInfo(jsonData as List<dynamic>);
        break;
      case "initial_guess_interpolation_type":
        updatePhaseInfo(jsonData as List<dynamic>);
        break;
      case "dimension":
        updatePhaseInfo(jsonData as List<dynamic>);
        break;
    }

    notifyListeners();
  }

  void updateDecisionVariableValue(
    int phaseIndex,
    DecisionVariableType decisionVariableType,
    DecisionVariableValueType decisionVariableValueType,
    int variableIndex,
    int dofIndex,
    int nodeIndex,
    double newValue,
  ) async {
    newValue = double.parse(newValue.toStringAsFixed(2));

    requestMaker.updateDecisionVariableValue(
        phaseIndex,
        decisionVariableType,
        decisionVariableValueType,
        variableIndex,
        dofIndex,
        nodeIndex,
        newValue);

    switch (decisionVariableType) {
      case DecisionVariableType.state:
        switch (decisionVariableValueType) {
          case DecisionVariableValueType.minBound:
            phasesInfo[phaseIndex]
                .stateVariables[variableIndex]
                .bounds
                .minBounds[dofIndex][nodeIndex] = newValue;
            break;
          case DecisionVariableValueType.maxBound:
            phasesInfo[phaseIndex]
                .stateVariables[variableIndex]
                .bounds
                .maxBounds[dofIndex][nodeIndex] = newValue;
            break;
          case DecisionVariableValueType.initGuess:
            phasesInfo[phaseIndex]
                .stateVariables[variableIndex]
                .initialGuess[dofIndex][nodeIndex] = newValue;
            break;
        }
        break;
      case DecisionVariableType.control:
        switch (decisionVariableValueType) {
          case DecisionVariableValueType.minBound:
            phasesInfo[phaseIndex]
                .controlVariables[variableIndex]
                .bounds
                .minBounds[dofIndex][nodeIndex] = newValue;
            break;
          case DecisionVariableValueType.maxBound:
            phasesInfo[phaseIndex]
                .controlVariables[variableIndex]
                .bounds
                .maxBounds[dofIndex][nodeIndex] = newValue;
            break;
          case DecisionVariableValueType.initGuess:
            phasesInfo[phaseIndex]
                .controlVariables[variableIndex]
                .initialGuess[dofIndex][nodeIndex] = newValue;
            break;
        }
        break;
    }

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
  List<String> objectivesMinimize = [];
  List<String> objectivesMaximize = [];
  List<String> constraints = [];
  List<String> interpolationTypes = [];
  List<String> dynamics = [];

  OCPAvailableValues(
    this.nodes,
    this.integrationRules,
    this.objectivesMinimize,
    this.objectivesMaximize,
    this.constraints,
    this.interpolationTypes,
    this.dynamics,
  );
}
