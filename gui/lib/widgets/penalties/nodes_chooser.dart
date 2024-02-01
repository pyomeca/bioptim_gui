import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/models/penalty.dart';
import 'package:bioptim_gui/widgets/utils/custom_http_dropdown.dart';
import 'package:bioptim_gui/widgets/utils/extensions.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class NodesChooser extends StatelessWidget {
  const NodesChooser({
    super.key,
    required this.width,
    this.defaultValue = "All shooting",
    required this.endpointPrefix,
    required this.phaseIndex,
    required this.penaltyType,
    required this.penaltyIndex,
    required this.penalty,
  });

  final double width;
  final String defaultValue;

  final String endpointPrefix;
  final int phaseIndex;
  final Type penaltyType;
  final int penaltyIndex;
  final Penalty penalty;

  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, data, child) {
      return CustomHttpDropdown(
        title: "Nodes to apply",
        width: width,
        defaultValue:
            defaultValue.toLowerCase().replaceAll("_", " ").capitalize(),
        items: penaltyType == Objective &&
                (penalty as Objective).objectiveType == "lagrange"
            ? ["All shooting"]
            : data.availablesValue!.nodes,
        requestKey: "nodes",
        customStringFormatting: (s) => s.replaceAll(" ", "_").toLowerCase(),
        customOnSelected: (value) {
          data.updatePenaltyField(phaseIndex, penaltyIndex, penaltyType,
              "nodes", value.replaceAll(" ", "_").toLowerCase());
          return true;
        },
      );
    });
  }
}
