import 'package:bioptim_gui/models/optimal_control_program_controllers.dart';
import 'package:bioptim_gui/widgets/positive_integer_text_field.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class AcrobaticInformation extends StatelessWidget {
  const AcrobaticInformation({
    super.key,
    required this.width,
  });

  final double width;

  @override
  Widget build(BuildContext context) {
    // final controllers = OptimalControlProgramControllers.instance;

    return Row(
      children: [
        SizedBox(
          width: width / 2 - 6,
          child: TextField(
            decoration: const InputDecoration(
                labelText: 'Number of twists', border: OutlineInputBorder()),
            inputFormatters: [
              FilteringTextInputFormatter.allow(RegExp(r'[0-9\.]'))
            ],
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: TextField(
            // controller: controllers.phaseDurationControllers[phaseIndex],
            decoration: const InputDecoration(
                labelText: 'Number of somersaults',
                border: OutlineInputBorder()),
            inputFormatters: [
              FilteringTextInputFormatter.allow(RegExp(r'[0-9\.]'))
            ],
          ),
        ),
      ],
    );
  }
}
