import 'package:bioptim_gui/models/acrobatics_ocp_controllers.dart';
import 'package:bioptim_gui/widgets/positive_integer_text_field.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class SomersaultInformation extends StatelessWidget {
  const SomersaultInformation({
    super.key,
    required this.somersaultIndex,
    required this.width,
  });

  final int somersaultIndex;
  final double width;

  @override
  Widget build(BuildContext context) {
    final controllers = AcrobaticsOCPControllers.instance;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SizedBox(
          width: width / 2 - 6,
          child: PositiveIntegerTextField(
            label: 'Number of half twists *',
            controller: controllers.nbHalfTwistsControllers[somersaultIndex],
            color: Colors.red,
          ),
        ),
        const SizedBox(height: 24),
        Row(
          children: [
            SizedBox(
              width: width / 2 - 6,
              child: PositiveIntegerTextField(
                label: 'Number of shooting points',
                controller:
                    controllers.nbShootingPointsControllers[somersaultIndex],
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: TextField(
                controller:
                    controllers.somersaultDurationControllers[somersaultIndex],
                decoration: const InputDecoration(
                    labelText: 'Phase time (s)', border: OutlineInputBorder()),
                inputFormatters: [
                  FilteringTextInputFormatter.allow(RegExp(r'[0-9\.]'))
                ],
              ),
            ),
          ],
        )
      ],
    );
  }
}
