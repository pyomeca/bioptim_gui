import 'package:bioptim_gui/models/dynamics.dart';
import 'package:bioptim_gui/widgets/custom_dropdown_button.dart';
import 'package:flutter/material.dart';

class DynamicsChooser extends StatelessWidget {
  const DynamicsChooser({
    super.key,
    required this.dynamics,
    required this.onChanged,
    required this.width,
  });

  final Dynamics dynamics;
  final Function(Dynamics value) onChanged;
  final double width;

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Expanded(
          child: CustomDropdownButton<DynamicsType>(
              title: 'Dynamic equations',
              value: dynamics.type,
              items: DynamicsType.values,
              onSelected: (DynamicsType type) => onChanged(
                  Dynamics(type: type, isExpanded: dynamics.isExpanded))),
        ),
        const SizedBox(width: 12),
        InkWell(
          onTap: () {
            final value = !dynamics.isExpanded;
            onChanged(Dynamics(type: dynamics.type, isExpanded: value));
          },
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Checkbox(
                value: dynamics.isExpanded,
                onChanged: (value) => onChanged(
                    Dynamics(type: dynamics.type, isExpanded: value!)),
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
