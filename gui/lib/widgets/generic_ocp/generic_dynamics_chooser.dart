import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/widgets/utils/custom_http_dropdown.dart';
import 'package:bioptim_gui/widgets/utils/extensions.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class GenericDynamicsChooser extends StatelessWidget {
  const GenericDynamicsChooser({
    super.key,
    required this.width,
    this.defaultValue = "Torque driven",
    required this.phaseIndex,
  });

  final double width;
  final String defaultValue;
  final int phaseIndex;

  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, data, child) {
      return CustomHttpDropdown(
        title: 'Dynamic equations',
        width: width,
        defaultValue:
            defaultValue.toLowerCase().replaceAll("_", " ").capitalize(),
        items: data.availablesValue!.dynamics,
        putEndpoint: '/generic_ocp/phases_info/$phaseIndex/dynamics',
        requestKey: "dynamics",
        customStringFormatting: (s) => s.replaceAll(" ", "_").toUpperCase(),
        customOnSelected: (value) async {
          data.updatePhaseField(
              phaseIndex, "dynamics", value.replaceAll(" ", "_").toUpperCase());
          return true;
        },
      );
    });
  }
}
