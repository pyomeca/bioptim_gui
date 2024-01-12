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
  bool expanded = false;
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

  Objective.fromJson(super.objectiveData)
      : objectiveType = objectiveData["objective_type"],
        weight = objectiveData["weight"],
        super.fromJson();

  @override
  String penaltyTypeToString() {
    return objectiveType.capitalize();
  }
}

class Constraint extends Penalty {
  Constraint.fromJson(super.constraintData) : super.fromJson();

  @override
  String penaltyTypeToString() {
    return "Constraint";
  }
}
