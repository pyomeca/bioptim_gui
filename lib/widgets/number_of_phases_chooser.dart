import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:bioptim_gui/widgets/positive_integer_text_field.dart';
import 'package:flutter/material.dart';

class NumberOfPhasesChooser extends StatelessWidget {
  const NumberOfPhasesChooser({
    super.key,
    required this.width,
  });

  final double width;

  @override
  Widget build(BuildContext context) {
    final controllers = OptimalControlProgramControllers.instance;
    return SizedBox(
      width: width * 1 / 2 - 6,
      child: PositiveIntegerTextField(
        label: 'Number of phases',
        controller: controllers.nbPhasesController,
        enabled: true,
      ),
    );
  }
}
