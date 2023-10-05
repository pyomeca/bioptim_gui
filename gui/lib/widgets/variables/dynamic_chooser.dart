import 'dart:convert';

import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/widgets/utils/custom_http_dropdown.dart';
import 'package:bioptim_gui/widgets/utils/extensions.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class DynamicChooser extends StatelessWidget {
  const DynamicChooser({
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
        getEndpoint: "/variables/dynamics",
        putEndpoint: '/generic_ocp/phases_info/$phaseIndex/dynamics',
        requestKey: "dynamics",
        customStringFormatting: (s) => s.replaceAll(" ", "_").toUpperCase(),
        customCallBack: (response) async {
          final newPhases = (json.decode(response.body) as List<dynamic>);
          data.updatePhaseInfo(newPhases);
        },
      );
    });
  }
}
