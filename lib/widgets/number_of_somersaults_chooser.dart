import 'package:bioptim_gui/models/acrobatics_ocp_controllers.dart';
import 'package:bioptim_gui/widgets/positive_integer_text_field.dart';
import 'package:flutter/material.dart';

class NumberOfSomersaultsChooser extends StatelessWidget {
  const NumberOfSomersaultsChooser({super.key, required this.width});

  final double width;

  @override
  Widget build(BuildContext context) {
    final controllers = AcrobaticsOCPControllers.instance;
    return SizedBox(
      width: width * 1 / 2 - 6,
      child: PositiveIntegerTextField(
        label: 'Number of somersaults',
        controller: controllers.nbSomersaultsController,
        enabled: true,
      ),
    );
  }
}
