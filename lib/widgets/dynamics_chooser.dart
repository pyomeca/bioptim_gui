import 'package:bioptim_gui/models/dynamics.dart';
import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:bioptim_gui/widgets/custom_dropdown_button.dart';
import 'package:flutter/material.dart';

class DynamicsChooser extends StatelessWidget {
  const DynamicsChooser(
      {super.key, required this.phaseIndex, required this.width});

  final int phaseIndex;
  final double width;

  @override
  Widget build(BuildContext context) {
    final controllers = OptimalControlProgramControllers.instance;
    final dynamics = controllers.getDynamics(phaseIndex: phaseIndex);

    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Expanded(
          child: CustomDropdownButton<DynamicsType>(
              title: 'Dynamic equations',
              value: dynamics.type,
              items: DynamicsType.values,
              onSelected: (DynamicsType type) => controllers.setDynamics(
                  Dynamics(type: type, isExpanded: dynamics.isExpanded),
                  phaseIndex: phaseIndex)),
        ),
        const SizedBox(width: 12),
        InkWell(
          onTap: () {
            final value = !dynamics.isExpanded;
            controllers.setDynamics(
                Dynamics(type: dynamics.type, isExpanded: value),
                phaseIndex: phaseIndex);
          },
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Checkbox(
                value: dynamics.isExpanded,
                onChanged: (value) => controllers.setDynamics(
                    Dynamics(type: dynamics.type, isExpanded: value!),
                    phaseIndex: phaseIndex),
              ),
              const Text('Expand\ndynamics'),
              const SizedBox(width: 12),
            ],
          ),
        ),
      ],
    );
  }
}
