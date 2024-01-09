import 'package:bioptim_gui/models/acrobatics_data.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/widgets/utils/custom_http_dropdown.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class AcrobaticPositionChooser extends StatelessWidget {
  const AcrobaticPositionChooser({
    super.key,
    required this.width,
    this.defaultValue = "Straight",
  });

  final double width;
  final String defaultValue;

  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, data, child) {
      return CustomHttpDropdown(
        title: "Jump position *",
        width: width,
        defaultValue: defaultValue,
        getEndpoint: "/acrobatics/position",
        putEndpoint: "/acrobatics/position",
        requestKey: "position",
        color: Colors.red,
        customOnSelected: (value) async {
          (data as AcrobaticsData).updateField("position", value.toLowerCase());
          return true;
        },
      );
    });
  }
}
