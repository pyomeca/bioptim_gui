import 'package:bioptim_gui/models/optimal_control_program_type.dart';
import 'package:bioptim_gui/widgets/custom_dropdown_button.dart';
import 'package:flutter/material.dart';

class OptimalControlProgramTypeChooser extends StatelessWidget {
  const OptimalControlProgramTypeChooser(
      {super.key, required this.value, required this.onSelected});

  final Function(OptimalControlProgramType) onSelected;
  final OptimalControlProgramType value;

  @override
  Widget build(BuildContext context) {
    return CustomDropdownButton<OptimalControlProgramType>(
      value: value,
      items: OptimalControlProgramType.values,
      title: 'Optimal control type',
      onSelected: onSelected,
    );
  }
}
