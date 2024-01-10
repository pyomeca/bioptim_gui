import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/models/penalty.dart';
import 'package:bioptim_gui/widgets/utils/custom_http_dropdown.dart';
import 'package:bioptim_gui/widgets/utils/extensions.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class PenaltyChooser extends StatelessWidget {
  const PenaltyChooser({
    super.key,
    required this.width,
    required this.title,
    required this.defaultValue,
    required this.endpointPrefix,
    required this.phaseIndex,
    required this.penaltyType,
    required this.penaltyIndex,
  });

  final String title;
  final double width;
  final String defaultValue;

  final String endpointPrefix;
  final int phaseIndex;
  final Type penaltyType;
  final int penaltyIndex;

  @override
  Widget build(BuildContext context) {
    final penaltyTypeString =
        penaltyType == Objective ? "objectives" : "constraints";

    return Consumer<OCPData>(builder: (context, data, child) {
      return CustomHttpDropdown(
        title: title,
        width: width,
        defaultValue:
            defaultValue.replaceAll("_", " ").toLowerCase().capitalize(),
        getEndpoint:
            '$endpointPrefix/$phaseIndex/$penaltyTypeString/$penaltyIndex',
        customOnSelected: (value) {
          data.updatePenaltyField(phaseIndex, penaltyIndex, penaltyType,
              "penalty_type", value.replaceAll(" ", "_").toUpperCase());
          return true;
        },
      );
    });
  }
}
