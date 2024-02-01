import 'package:bioptim_gui/models/decision_variables_type.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/widgets/utils/custom_http_dropdown.dart';
import 'package:bioptim_gui/widgets/utils/extensions.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class InterpolationChooser extends StatelessWidget {
  const InterpolationChooser({
    super.key,
    required this.width,
    required this.requestKey,
    this.defaultValue = "Constant with first and last different",
    this.titlePrefix = "",
    required this.endpointPrefix,
    required this.phaseIndex,
    required this.decisionVariableType,
    required this.variableIndex,
    required this.fieldName,
  });

  final double width;
  final String defaultValue;
  final String requestKey;
  final String titlePrefix;

  final String endpointPrefix;
  final int phaseIndex;
  final DecisionVariableType decisionVariableType;
  final int variableIndex;
  final String fieldName;

  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, data, child) {
      return CustomHttpDropdown(
        title: '$titlePrefix interpolation type',
        width: width,
        defaultValue:
            defaultValue.toLowerCase().replaceAll("_", " ").capitalize(),
        items: data.availablesValue!.interpolationTypes,
        putEndpoint:
            '$endpointPrefix/$phaseIndex/${decisionVariableType.toPythonString()}/'
            '$variableIndex/$fieldName',
        requestKey: requestKey,
        customStringFormatting: (s) => s.replaceAll(" ", "_").toUpperCase(),
        customOnSelected: (value) {
          data.updateDecisionVariableField(
              phaseIndex,
              decisionVariableType,
              variableIndex,
              fieldName,
              value.replaceAll(" ", "_").toUpperCase());
          return true;
        },
      );
    });
  }
}
