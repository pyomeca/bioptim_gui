import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:bioptim_gui/widgets/positive_integer_text_field.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class PhaseInformation extends StatelessWidget {
  const PhaseInformation({
    super.key,
    required this.phaseIndex,
    required this.width,
  });

  final int phaseIndex;
  final double width;

  @override
  Widget build(BuildContext context) {
    final controllers = OptimalControlProgramControllers.instance;

    return Row(
      children: [
        SizedBox(
          width: width / 2 - 6,
          child: PositiveIntegerTextField(
            label: 'Number of shooting points',
            controller: controllers.nbShootingPointsControllers[phaseIndex],
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: TextField(
            controller: controllers.phaseDurationControllers[phaseIndex],
            decoration: const InputDecoration(
                labelText: 'Phase time (s)', border: OutlineInputBorder()),
            inputFormatters: [
              FilteringTextInputFormatter.allow(RegExp(r'[0-9\.]'))
            ],
          ),
        ),
      ],
    );
  }
}
