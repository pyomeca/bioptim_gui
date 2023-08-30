import 'package:bioptim_gui/widgets/positive_integer_text_field.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class PhaseInformation extends StatelessWidget {
  const PhaseInformation({
    super.key,
    required this.width,
    required this.nbShootingPointController,
    required this.phaseTimeController,
  });

  final double width;
  final TextEditingController nbShootingPointController;
  final TextEditingController phaseTimeController;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        SizedBox(
          width: width / 2 - 6,
          child: PositiveIntegerTextField(
            label: 'Number of shooting points',
            controller: nbShootingPointController,
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: TextField(
            controller: phaseTimeController,
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
