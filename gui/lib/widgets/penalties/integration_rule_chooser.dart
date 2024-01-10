import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/widgets/utils/custom_http_dropdown.dart';
import 'package:bioptim_gui/widgets/utils/extensions.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class IntegrationRuleChooser extends StatelessWidget {
  const IntegrationRuleChooser({
    super.key,
    required this.width,
    this.defaultValue = "Rectangle left",
    required this.endpointPrefix,
    required this.phaseIndex,
    required this.penaltyType,
    required this.penaltyIndex,
  });

  final double width;
  final String defaultValue;

  final String endpointPrefix;
  final int phaseIndex;
  final Type penaltyType;
  final int penaltyIndex;

  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, data, child) {
      return CustomHttpDropdown(
        title: "Integration rule",
        width: width,
        defaultValue:
            defaultValue.toLowerCase().capitalize().replaceAll("_", " "),
        items: data.availablesValue!.integrationRules,
        requestKey: "integration_rule",
        customStringFormatting: (s) => s.replaceAll(" ", "_").toLowerCase(),
        customOnSelected: (value) {
          data.updatePenaltyField(phaseIndex, penaltyIndex, penaltyType,
              "integration_rule", value.replaceAll(" ", "_").toLowerCase());
          return true;
        },
      );
    });
  }
}
