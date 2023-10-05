import 'package:bioptim_gui/widgets/utils/custom_http_dropdown.dart';
import 'package:flutter/material.dart';

class AcrobaticSportTypeChooser extends StatelessWidget {
  const AcrobaticSportTypeChooser({
    super.key,
    required this.width,
    this.defaultValue = "Trampoline",
  });

  final double width;
  final String defaultValue;

  @override
  Widget build(BuildContext context) {
    return CustomHttpDropdown(
      title: "Sport type",
      width: width,
      defaultValue: defaultValue,
      getEndpoint: "/acrobatics/sport_type",
      putEndpoint: "/acrobatics/sport_type",
      requestKey: "sport_type",
    );
  }
}
