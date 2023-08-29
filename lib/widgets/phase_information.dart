import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class PhaseInformation extends StatelessWidget {
  const PhaseInformation({
    super.key,
    required this.columnWidth,
    required this.nbShootingPointController,
    required this.phaseTimeController,
  });

  final double columnWidth;
  final TextEditingController nbShootingPointController;
  final TextEditingController phaseTimeController;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        SizedBox(
          width: columnWidth / 2 - 6,
          child: TextField(
            controller: nbShootingPointController,
            decoration: const InputDecoration(
                labelText: 'Number of shooting points',
                border: OutlineInputBorder()),
            inputFormatters: [FilteringTextInputFormatter.digitsOnly],
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
