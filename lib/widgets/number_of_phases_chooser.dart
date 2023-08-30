import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class NumberOfPhasesChooser extends StatelessWidget {
  const NumberOfPhasesChooser({
    super.key,
    required this.phaseController,
    required this.onChanged,
  });

  final TextEditingController phaseController;
  final Function(int value) onChanged;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 100,
      child: Focus(
        onFocusChange: (hasFocus) {
          if (!hasFocus) {
            if (phaseController.text == '' ||
                int.tryParse(phaseController.text) == 0) {
              phaseController.text = '1';
            }
            onChanged(int.parse(phaseController.text));
          }
        },
        child: TextField(
          controller: phaseController,
          decoration: const InputDecoration(
              labelText: 'Number of phases', border: OutlineInputBorder()),
          inputFormatters: [FilteringTextInputFormatter.digitsOnly],
          enabled: true,
        ),
      ),
    );
  }
}
