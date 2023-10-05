import 'package:bioptim_gui/widgets/utils/extensions.dart';

abstract class Penalty {
  String penaltyType;
  String nodes;
  bool quadratic;
  bool expand;
  bool multiThread;
  bool derivative;
  dynamic target;
  String integrationRule;
  List<Argument> arguments;

  Penalty.fromJson(Map<String, dynamic> penaltyData)
      : penaltyType = penaltyData["penalty_type"],
        nodes = penaltyData["nodes"],
        quadratic = penaltyData["quadratic"],
        expand = penaltyData["expand"],
        multiThread = penaltyData["multi_thread"],
        derivative = penaltyData["derivative"],
        target = penaltyData["target"],
        integrationRule = penaltyData["integration_rule"],
        arguments = (penaltyData["arguments"] as List<dynamic>).map((argument) {
          return Argument.fromJson(argument);
        }).toList();

  String penaltyTypeToString() {
    return "";
  }

  @override
  String toString() {
    return "";
  }
}

class Argument {
  String name;
  String type;
  String? value;

  Argument.fromJson(Map<String, dynamic> argumentData)
      : name = argumentData["name"],
        type = argumentData["type"],
        value = argumentData["value"].toString();
}

class Objective extends Penalty {
  String objectiveType;
  double weight;

  Objective.fromJson(Map<String, dynamic> objectiveData)
      : objectiveType = objectiveData["objective_type"],
        weight = objectiveData["weight"],
        super.fromJson(objectiveData);

  @override
  String penaltyTypeToString() {
    return objectiveType.capitalize();
  }

  @override
  String toString() {
    return "objective";
  }
}

class Constraint extends Penalty {
  Constraint.fromJson(Map<String, dynamic> constraintData)
      : super.fromJson(constraintData);

  @override
  String penaltyTypeToString() {
    return "Constraint";
  }

  @override
  String toString() {
    return "constraint";
  }
}
