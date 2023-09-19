import 'package:bioptim_gui/models/acrobatics_ocp_controllers.dart';
import 'package:bioptim_gui/widgets/positive_integer_text_field.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class AcrobaticInformation extends StatelessWidget {
  const AcrobaticInformation({super.key, required this.width});

  final double width;

  @override
  Widget build(BuildContext context) {
    final controllers = AcrobaticsOCPControllers.instance;

    return Row(
      children: [
        SizedBox(
          width: width / 2 - 6,
          child: PositiveIntegerTextField(
            label: 'Number of somersaults',
            controller: controllers.nbSomersaultsController,
            enabled: true,
          ),
        ),
        const SizedBox(width: 12),
        SizedBox(
          width: width / 2 - 6,
          child: TextField(
            controller: controllers.finalTimeMarginController,
            decoration: const InputDecoration(
                labelText: 'Final time margin(s)',
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
