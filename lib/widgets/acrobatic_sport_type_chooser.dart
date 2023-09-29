import 'package:bioptim_gui/models/acrobatics_ocp_controllers.dart';
import 'package:bioptim_gui/models/acrobatics_sport_type.dart';
import 'package:bioptim_gui/widgets/custom_dropdown_button.dart';
import 'package:flutter/material.dart';

class AcrobaticSportTypeChooser extends StatelessWidget {
  const AcrobaticSportTypeChooser({
    super.key,
    required this.width,
  });

  final double width;

  @override
  Widget build(BuildContext context) {
    final controllers = AcrobaticsOCPControllers.instance;

    return SizedBox(
      width: width,
      child: CustomDropdownButton<AcrobaticsSportType>(
        value: controllers.sportType,
        items: AcrobaticsSportType.values,
        title: 'Sport type',
        onSelected: (value) => controllers.setSportType(value),
      ),
    );
  }
}
