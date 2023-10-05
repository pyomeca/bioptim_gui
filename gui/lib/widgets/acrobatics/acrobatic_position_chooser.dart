import 'package:bioptim_gui/widgets/utils/custom_http_dropdown.dart';
import 'package:flutter/material.dart';

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
    return CustomHttpDropdown(
      title: "Jump position *",
      width: width,
      defaultValue: defaultValue,
      getEndpoint: "/acrobatics/position",
      putEndpoint: "/acrobatics/position",
      requestKey: "position",
      color: Colors.red,
    );
  }
}
