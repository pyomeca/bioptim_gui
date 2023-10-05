import 'package:bioptim_gui/models/optimal_control_program_type.dart';
import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:bioptim_gui/widgets/utils/custom_dropdown_button.dart';
import 'package:flutter/material.dart';

class OptimalControlProgramTypeChooser extends StatelessWidget {
  const OptimalControlProgramTypeChooser({
    super.key,
    required this.width,
  });

  final double width;

  @override
  Widget build(BuildContext context) {
    final controllers = OptimalControlProgramControllers.instance;

    return SizedBox(
      width: width,
      child: CustomDropdownButton<OptimalControlProgramType>(
        value: controllers.ocpType,
        items: OptimalControlProgramType.values,
        title: 'Optimal control type',
        onSelected: (value) => controllers.setOcpType(value),
      ),
    );
  }
}
