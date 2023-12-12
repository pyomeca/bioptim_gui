import 'dart:convert';

import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/widgets/utils/custom_http_dropdown.dart';
import 'package:bioptim_gui/widgets/utils/extensions.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class AcrobaticsDynamicChooser extends StatelessWidget {
  const AcrobaticsDynamicChooser({
    super.key,
    required this.width,
    this.defaultValue = "Torque driven",
  });

  final double width;
  final String defaultValue;

  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, data, child) {
      return CustomHttpDropdown(
        title: 'Dynamic equations',
        width: width,
        defaultValue:
            defaultValue.toLowerCase().replaceAll("_", " ").capitalize(),
        getEndpoint: "/acrobatics/dynamics",
        putEndpoint: '/acrobatics/dynamics',
        requestKey: "dynamics",
        customStringFormatting: (s) => s.replaceAll(" ", "_").toLowerCase(),
        customCallBack: (response) async {
          final newPhases = (json.decode(response.body) as List<dynamic>);
          data.updatePhaseInfo(newPhases);
        },
      );
    });
  }
}
