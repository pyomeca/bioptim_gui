import 'package:bioptim_gui/models/ocp_request_maker.dart';
import 'package:bioptim_gui/models/penalty.dart';
import 'package:flutter/material.dart';

///
/// [OCPData] represents the most generic OCP data. It is used to be inherited
/// by "generic OCP" [GenericOcpData] and "acrobatics data" [AcrobaticsData].
/// It will be used in [Consumer] to provide the data to the widgets that
/// display the data that can be common to both OCPs. (penalties for now)
abstract class OCPData<T extends Phase> with ChangeNotifier {
  // Alexandre: TODO maybe gather the common data here like nbPhases and model_path

  ///
  /// Getter Setters

  OCPRequestMaker get requestMaker;
  List<T> get phaseInfo;
  int get nbPhases;
  String get modelPath;

  ///
  /// Update methods

  void updateField(String name, String value);
  void updatePhaseField(int phaseIndex, String fieldName, String newValue);
  void updatePhaseInfo(List<dynamic> newData);
  void updatePenalties(
      int phaseIndex, String penaltyType, List<Penalty> penalties);
  void updatePenalty(
      int phaseIndex, String penaltyType, int penaltyIndex, Penalty penalty);
  void updatePenaltyField(int phaseIndex, int penaltyIndex, String penaltyType,
      String fieldName, dynamic newValue,
      {bool? doUpdate});
  void updatePenaltyArgument(
      int phaseIndex,
      int penaltyIndex,
      String argumentName,
      String? newValue,
      String argumentType,
      int argumentIndex,
      String penaltyType);
}

///
/// [Phase] represents the most generic phase of an OCP with the least amount of
/// information. For now, It is used to be inherited by "phases" for
/// "generic OCP"'s [GenericPhase] and "acrobatics OCP" [Somersault] that
/// contains additional fields.
abstract class Phase {
  late int nbShootingPoints;
  late double duration;
  late List<Objective> objectives;
  late List<Constraint> constraints;

  Phase.fromJson(Map<String, dynamic> phaseData)
      : nbShootingPoints = phaseData["nb_shooting_points"],
        duration = phaseData["duration"],
        objectives =
            (phaseData["objectives"] as List<dynamic>).map((objective) {
          return Objective.fromJson(objective);
        }).toList(),
        constraints =
            (phaseData["constraints"] as List<dynamic>).map((constraint) {
          return Constraint.fromJson(constraint);
        }).toList();
}
